import Foundation
import Security
import LocalAuthentication

private func slotMatches(_ value: String, _ pattern: String) -> Bool { guard let r = value.range(of: pattern, options: .regularExpression) else { return false }; return r.lowerBound == value.startIndex && r.upperBound == value.endIndex }
public enum PublicSessionSlotError: Error, Equatable { case unavailable, unconfirmed, busy }
@MainActor public protocol PublicRawSessionStore: AnyObject {
    func read() throws -> Data?
    /// Must compare and mutate in the same native serialization boundary. This
    /// is not a claim of cross-process transactional SecItem compare-and-swap.
    func compareAndSwap(expected: Data?, replacement: Data?) throws -> Bool
}

/// Exclusive public namespace. Initializing/query construction does not read
/// Keychain. No access group, shared synchronization, TEST or generic-key API.
@MainActor public final class PublicDataProtectionKeychain: PublicRawSessionStore {
    public static let service = "com.miraylab.poppy.public-session-vault"
    public static let account = "poppy.public.session.v1"
    public init() {}
    static func query() -> [String: Any] {
        let context = LAContext(); context.interactionNotAllowed = true
        return [kSecClass as String: kSecClassGenericPassword, kSecAttrService as String: service, kSecAttrAccount as String: account,
         kSecAttrSynchronizable as String: false, kSecUseDataProtectionKeychain as String: true,
         kSecUseAuthenticationContext as String: context]
    }
    public func read() throws -> Data? {
        var q = Self.query(); q[kSecReturnData as String] = true; q[kSecReturnAttributes as String] = true; q[kSecMatchLimit as String] = kSecMatchLimitOne
        var result: CFTypeRef?; let status = SecItemCopyMatching(q as CFDictionary, &result)
        if status == errSecItemNotFound { return nil }
        guard status == errSecSuccess, let attrs = result as? [String: Any],
              attrs[kSecAttrAccessible as String] as? String == kSecAttrAccessibleWhenUnlockedThisDeviceOnly as String,
              let data = attrs[kSecValueData as String] as? Data, data.count <= 4096 else { throw PublicSessionSlotError.unavailable }
        return data
    }
    public func compareAndSwap(expected: Data?, replacement: Data?) throws -> Bool {
        guard expected == nil || expected!.count <= 4096, replacement == nil || replacement!.count <= 4096 else { throw PublicSessionSlotError.unavailable }
        guard try read() == expected else { return false }; if expected == replacement { return true }
        let status: OSStatus
        if let replacement {
            if expected != nil { status = SecItemUpdate(Self.query() as CFDictionary, [kSecValueData as String: replacement] as CFDictionary) }
            else {
                var add = Self.query(); add[kSecValueData as String] = replacement; add[kSecAttrAccessible as String] = kSecAttrAccessibleWhenUnlockedThisDeviceOnly
                status = SecItemAdd(add as CFDictionary, nil)
            }
        } else { status = SecItemDelete(Self.query() as CFDictionary) }
        guard status == errSecSuccess || replacement == nil && status == errSecItemNotFound else { throw PublicSessionSlotError.unconfirmed }
        return true
    }
}

public struct PublicSDKSnapshot: Equatable, Sendable, CustomStringConvertible, CustomDebugStringConvertible {
    fileprivate let provider: PublicSessionProvider, identity: String, fingerprint: String
    public init(provider: PublicSessionProvider, identity: String, recordFingerprint: String) throws {
        guard slotMatches(recordFingerprint, "^[a-f0-9]{64}$"),
              provider == .google ? !identity.isEmpty && identity.utf8.count <= 512
                : slotMatches(identity, "^[A-Za-z0-9._~+/=-]{20,2048}$") else { throw PublicSessionSlotError.unavailable }
        self.provider = provider; self.identity = identity; fingerprint = recordFingerprint
    }
    public var description: String { "<PublicSDKSnapshot redacted>" }; public var debugDescription: String { description }
}
/// .absent requires successful memory AND persistent-store absence. Unavailable
/// must not be represented as absent (e.g. hasPreviousSignIn false is not proof).
public enum PublicSDKObservation: Equatable, Sendable { case absent, present(PublicSDKSnapshot), unavailable }
@MainActor public struct PublicSessionSDKPorts {
    public let observe: (PublicSessionProvider) throws -> PublicSDKObservation
    public let removeExact: (PublicSessionProvider, PublicSDKSnapshot) throws -> Void
    /// Must invalidate/drain original native leases before a storage/SDK change;
    /// throwing holds the mutation. No default/noop production implementation.
    public let invalidate: () throws -> Void
    public init(observe: @escaping (PublicSessionProvider) throws -> PublicSDKObservation,
                removeExact: @escaping (PublicSessionProvider, PublicSDKSnapshot) throws -> Void,
                invalidate: @escaping () throws -> Void) {
        self.observe = observe; self.removeExact = removeExact; self.invalidate = invalidate
    }
}

/// Same-process main-actor serialization plus exact raw compare, independent
/// public signature verification and snapshot checks around each callback.
@MainActor public final class PublicNativeSessionSlot {
    private let store: PublicRawSessionStore, verifier: PublicSessionVerifier, sdk: PublicSessionSDKPorts, now: () -> Date
    private var busy = false, quarantined = false
    public init(store: PublicRawSessionStore, verifier: PublicSessionVerifier, sdk: PublicSessionSDKPorts, now: @escaping () -> Date = Date.init) {
        self.store = store; self.verifier = verifier; self.sdk = sdk; self.now = now
    }
    private func live() throws { guard !quarantined else { throw PublicSessionSlotError.unconfirmed }; guard !busy else { throw PublicSessionSlotError.busy } }
    public func read() throws -> Data? {
        try live(); do { guard let d = try store.read() else { return nil }; _ = try verifier.verifyForRetirement(d, now: now()); return d }
        catch { throw PublicSessionSlotError.unavailable }
    }
    public func assertCurrentBearer(_ bearer: String) throws {
        try live(); do { guard let d = try store.read(), try verifier.verifyForStorage(d, now: now()).matchesBearer(bearer) else { throw PublicSessionSlotError.unavailable } }
        catch { throw PublicSessionSlotError.unavailable }
    }
    private func snapshot(_ provider: PublicSessionProvider, proof: PublicSessionProof, requirePresent: Bool) throws -> PublicSDKObservation {
        let observation = try sdk.observe(provider)
        switch observation {
        case .unavailable: throw PublicSessionSlotError.unavailable
        case .absent: if requirePresent { throw PublicSessionSlotError.unavailable }
        case .present(let s):
            guard s.provider == provider else { throw PublicSessionSlotError.unavailable }
            let same = provider == .google ? try proof.matchesGoogleSubject(s.identity) : try proof.matchesKakaoAccessToken(s.identity)
            guard same else { throw PublicSessionSlotError.unavailable }
        }; return observation
    }
    public func compareAndSwap(expected: Data?, replacement: Data?) throws -> Bool {
        try live(); busy = true; defer { busy = false }; var mutating = false
        do {
            guard try store.read() == expected else { return false }
            let old = try expected.map { try verifier.verifyForRetirement($0, now: now()) }
            let new = try replacement.map { try verifier.verifyForStorage($0, now: now()) }
            let newObservation: PublicSDKObservation? = try new?.SDKProvider.map { try snapshot($0, proof: new!, requirePresent: true) }
            let retiring = old?.SDKProvider != new?.SDKProvider ? old?.SDKProvider : replacement == nil ? old?.SDKProvider : nil
            let oldObservation = try retiring.map { try snapshot($0, proof: old!, requirePresent: false) }
            guard try store.read() == expected else { return false }
            if expected == replacement { return true }
            try sdk.invalidate()
            guard try store.read() == expected else { return false }
            if let provider = new?.SDKProvider, try sdk.observe(provider) != newObservation { throw PublicSessionSlotError.unavailable }
            if let provider = retiring {
                guard try sdk.observe(provider) == oldObservation else { throw PublicSessionSlotError.unavailable }
                if case .present(let s) = oldObservation {
                    mutating = true; try sdk.removeExact(provider, s)
                    guard try sdk.observe(provider) == .absent else { throw PublicSessionSlotError.unconfirmed }
                }
            }
            // Callbacks may have changed the other provider or app record.
            if let provider = new?.SDKProvider, try sdk.observe(provider) != newObservation { throw PublicSessionSlotError.unconfirmed }
            guard try store.read() == expected else { return false }
            if let replacement { _ = try verifier.verifyForStorage(replacement, now: now()) }
            mutating = true
            guard try store.compareAndSwap(expected: expected, replacement: replacement) else { return false }
            guard try store.read() == replacement else { throw PublicSessionSlotError.unconfirmed }
            return true
        } catch {
            if mutating { quarantined = true; throw PublicSessionSlotError.unconfirmed }
            throw PublicSessionSlotError.unavailable
        }
    }
}
