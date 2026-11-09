import Foundation

// Shared by the existing app sign-in plugins and the held withdrawal candidate.
// Cancellation retires an operation but keeps its SDK slot until its callback
// drains. A late callback can neither disclose credentials nor release a newer
// operation. This is an in-process guard, never server identity verification.
public enum NativeAuthOperationPurpose: Sendable { case login, withdrawal, withdrawalStatusRead, publicHTTP, publicSessionMutation }
public enum NativeAuthOperationGateError: Error, Equatable { case busy, held }
public struct NativeAuthOperationLease: Sendable, Equatable, CustomStringConvertible, CustomReflectable {
    fileprivate let gateID: UUID, operationID: UUID, generation: UUID
    public var description: String { "NativeAuthOperationLease(redacted)" }
    public var customMirror: Mirror { Mirror(self, children: [:]) }
}
public final class NativeAuthOperationGate: @unchecked Sendable {
    public static let shared = NativeAuthOperationGate()
    private let lock = NSLock(), id = UUID()
    private var generation = UUID()
    private var operation: (lease: NativeAuthOperationLease, purpose: NativeAuthOperationPurpose)?
    private var SDKPresentation: NativeAuthOperationLease?
    public init() {}
    public func begin(_ purpose: NativeAuthOperationPurpose) throws -> NativeAuthOperationLease {
        try lock.withLock {
            guard operation == nil else { throw NativeAuthOperationGateError.busy }
            let lease = NativeAuthOperationLease(gateID: id, operationID: UUID(), generation: generation)
            operation = (lease, purpose); return lease
        }
    }
    public func check(_ lease: NativeAuthOperationLease) throws {
        try lock.withLock {
            guard lease.gateID == id, lease.generation == generation,
                  operation?.lease.operationID == lease.operationID else { throw NativeAuthOperationGateError.held }
        }
    }
    // Does not require a live generation: a cancelled original SDK must drain.
    public func finish(_ lease: NativeAuthOperationLease) {
        lock.withLock {
            if lease.gateID == id && operation?.lease.operationID == lease.operationID { operation = nil; SDKPresentation = nil }
        }
    }
    public func invalidate() { lock.withLock { generation = UUID() } }
    public func invalidate(_ lease: NativeAuthOperationLease) {
        lock.withLock {
            if lease.gateID == id && operation?.lease.operationID == lease.operationID { generation = UUID() }
        }
    }
    // Normal login can leave the app for a provider's approved authentication
    // UI. Unreserved withdrawal inactivity remains terminal; SDK-only
    // tolerance is minted internally for one verified original owner below.
    public func invalidateWithdrawal() {
        lock.withLock { if operation?.purpose == .withdrawal || operation?.purpose == .withdrawalStatusRead { generation = UUID() } }
    }
    // Only the coordinator can reserve its current withdrawal's SDK call.
    // Background/lock/disconnect still use unconditional invalidation above.
    func beginSDKPresentation(_ lease: NativeAuthOperationLease) throws {
        try lock.withLock {
            guard operation?.purpose == .withdrawal, SDKPresentation == nil,
                  lease.gateID == id, lease.generation == generation,
                  operation?.lease == lease else { throw NativeAuthOperationGateError.held }
            SDKPresentation = lease
        }
    }
    func endSDKPresentation(_ lease: NativeAuthOperationLease) {
        lock.withLock { if SDKPresentation == lease { SDKPresentation = nil } }
    }
    public func withdrawalWillResignActive() {
        lock.withLock {
            guard operation?.purpose == .withdrawal || operation?.purpose == .withdrawalStatusRead else { return }
            if operation?.purpose == .withdrawal, let SDKPresentation,
               SDKPresentation == operation?.lease, SDKPresentation.generation == generation { return }
            generation = UUID()
        }
    }
}
