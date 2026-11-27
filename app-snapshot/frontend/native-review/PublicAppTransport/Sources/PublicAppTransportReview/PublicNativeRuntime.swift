import Foundation
import ProviderWithdrawalNativeReview

/// Actual HTTP/session serialization, sharing the existing SDK sign-in gate.
/// No plugin registration, TEST session access or automatic retry. Construction
/// alone performs no SDK, Keychain or HTTP operation.
@MainActor public final class PublicNativeRuntime {
    private let binding: PublicHTTPBinding, client: PublicNativeHTTPClient, gate: NativeAuthOperationGate
    private var slot: PublicNativeSessionSlot!
    private var http: (UUID, NativeAuthOperationLease)?
    private var mutation: NativeAuthOperationLease?
    public convenience init(binding: PublicHTTPBinding, verifier: PublicSessionVerifier, store: PublicRawSessionStore,
        gate: NativeAuthOperationGate = .shared,
        makeSDKPorts: (@escaping @MainActor () throws -> Void) throws -> PublicSessionSDKPorts) throws {
        try self.init(binding: binding, client: PublicNativeHTTPClient(binding: binding), verifier: verifier, store: store,
                      gate: gate, now: Date.init, makeSDKPorts: makeSDKPorts)
    }
    init(binding: PublicHTTPBinding, client: PublicNativeHTTPClient, verifier: PublicSessionVerifier, store: PublicRawSessionStore,
         gate: NativeAuthOperationGate, now: @escaping () -> Date,
         makeSDKPorts: (@escaping @MainActor () throws -> Void) throws -> PublicSessionSDKPorts) throws {
        self.binding = binding; self.client = client; self.gate = gate
        let ports = try makeSDKPorts { [weak self] in
            guard let self, let lease = self.mutation, self.http == nil else { throw PublicSessionSlotError.busy }
            try self.gate.check(lease)
        }
        slot = PublicNativeSessionSlot(store: store, verifier: verifier, sdk: ports, now: now)
    }
    public func readSession() throws -> Data? {
        let lease = try gate.begin(.publicSessionMutation); defer { gate.finish(lease) }
        try gate.check(lease); return try slot.read()
    }
    public func compareAndSwapSession(expected: Data?, replacement: Data?) throws -> Bool {
        let lease = try gate.begin(.publicSessionMutation); mutation = lease
        defer { mutation = nil; gate.finish(lease) }
        try gate.check(lease); return try slot.compareAndSwap(expected: expected, replacement: replacement)
    }
    public func send(_ request: PublicHTTPRequest,
        completion: @escaping @MainActor (Result<PublicHTTPResponse, PublicHTTPError>) -> Void) throws {
        let checked = try request.checked(binding)
        let path = checked.url!.path
        // Only the five fixed new-login routes use a protection credential
        // rather than the current member's signed native session.
        let login = ["/api/v1/app/auth/protection-session", "/api/v1/app/auth/google", "/api/v1/app/auth/apple",
                     "/api/v1/app/auth/kakao", "/api/v1/app/auth/apple/challenge"].contains(path)
        let bearer: String?
        if login { bearer = nil }
        else {
            guard let header = checked.value(forHTTPHeaderField: "Authorization"), header.hasPrefix("Bearer ") else { throw PublicHTTPError.request }
            bearer = String(header.dropFirst(7))
        }
        let lease = try gate.begin(.publicHTTP), id = UUID()
        do {
            try gate.check(lease)
            if let bearer { try slot.assertCurrentBearer(bearer) }
            try gate.check(lease)
            http = (id, lease)
            let callbackGate = gate
            try client.send(request) { [weak self] result in
                Task { @MainActor in
                    guard let self else { callbackGate.finish(lease); completion(.failure(.cancelled)); return }
                    guard self.http?.0 == id else { return }
                    var delivered = result
                    do {
                        try self.gate.check(lease)
                        if let bearer { try self.slot.assertCurrentBearer(bearer) }
                    } catch { delivered = .failure(.cancelled) }
                    // URLSession has actually invalidated before this callback.
                    // Cancel/timeouts cannot release SDK/login slots early.
                    self.http = nil; self.gate.finish(lease); completion(delivered)
                }
            }
        } catch {
            http = nil; gate.finish(lease); throw PublicHTTPError.request
        }
    }
    public func cancelHTTP() {
        guard let (_, lease) = http else { return }
        gate.invalidate(lease); client.cancel()
        // Keep both leases until the actual URLSession invalidation callback.
        // A write may already have committed; cancellation is not a rollback.
    }
}
