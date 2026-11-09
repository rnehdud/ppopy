import Foundation

public struct WithdrawalNativeSDKUIPolicy: Sendable {
    public let SDKUIEnabled: Bool
    public init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        let expected: [String: Any] = ["version":"1.0.1","scope":"isolated_local_review",
            "runtime_registered":false,"native_plugin_registered":false,
            "actual_provider_authentication_authorized":false,"operating_member_transport_authorized":false,
            "SDK_UI_enabled":false,"automatic_retry":false,
            "credential_storage":"app_handoff_memory_only_no_JS_logs_app_vault_or_app_disk_SDK_storage_unverified",
            "driver":"explicit_synthetic_callback_driver_only",
            "admission":"opaque_coordinator_request_original_owner_and_authentication_lease_before_start_after_callback",
            "cancellation":"hold_original_authentication_slot_until_same_SDK_callback_drains",
            "callback":"same_native_operation_and_controller_one_use_foreign_and_duplicate_ignored",
            "inactive_policy":"original_coordinator_reserved_inactive_only_active_return_other_signals_terminal",
            "result":"capture_only_not_account_closure_provider_ACK_or_whole_erasure"]
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
        SDKUIEnabled = raw["SDK_UI_enabled"] as! Bool
    }
}

@MainActor public enum WithdrawalNativeSDKCallbackOutcome {
    case captured(WithdrawalNativeCredentials)
    case failed
}
@MainActor public protocol WithdrawalNativeSDKCallbackDriverPort: AnyObject {
    // A thrown start means no SDK invocation began. An accepted start must
    // deliver its original completion even after the caller cancels. No SDK
    // signOut, credential refresh, app storage or provider revocation belongs
    // here. Actual SDK-managed persistence remains separately unverified.
    func startExplicit(_ request: WithdrawalNativeCaptureRequest,
        completion: @escaping @MainActor (UUID, WithdrawalNativeSDKCallbackOutcome) -> Void) throws
}

// A cancellation never fabricates an SDK completion. The waiting coordinator
// keeps its original authentication lease until the driver callback drains.
@MainActor public final class WithdrawalNativeSDKCallbackReview: WithdrawalNativeSDKCapturePort,
    WithdrawalNativeSDKMemoryCleanupPort, CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    private let driver: any WithdrawalNativeSDKCallbackDriverPort
    let actualContext: WithdrawalNativeActualTESTContext?
    private var pending: (request: WithdrawalNativeCaptureRequest,
        continuation: CheckedContinuation<WithdrawalNativeCredentials, Error>, cancelled: Bool)?
    private var used = false
    private var capturedOperation: (id:UUID,provider:WithdrawalNativeProvider)?
    public init(policy: WithdrawalNativeSDKUIPolicy, driver: any WithdrawalNativeSDKCallbackDriverPort, deploymentContext: String,
        actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        try requireWithdrawalNativeContext(deploymentContext,actualContext)
        try ownerRequire(!policy.SDKUIEnabled)
        self.actualContext=actualContext
        self.driver = driver
    }
    public func captureExplicit(_ request: WithdrawalNativeCaptureRequest) async throws -> WithdrawalNativeCredentials {
        try actualContext?.requireWithdrawalReady()
        if pending != nil { throw WithdrawalNativeReviewError.busy }
        try ownerRequire(!used); try request.checkOriginalOperation()
        used = true
        return try await withTaskCancellationHandler {
            try await withCheckedThrowingContinuation { continuation in
                if Task.isCancelled { continuation.resume(throwing: WithdrawalNativeReviewError.held); return }
                pending = (request, continuation, false)
                do {
                    try request.checkOriginalOperation()
                    try driver.startExplicit(request) { [weak self] id, result in self?.complete(id, result: result) }
                } catch {
                    // start threw before an invocation began; no callback exists
                    // to drain. If a synchronous callback already completed, do
                    // not resume a continuation twice.
                    if let p = pending, p.request.operationID == request.operationID {
                        pending = nil; p.continuation.resume(throwing: WithdrawalNativeReviewError.held)
                    }
                }
            }
        } onCancel: { [id = request.operationID] in
            Task { @MainActor [weak self] in self?.cancel(id) }
        }
    }
    private func cancel(_ id: UUID) {
        guard var p = pending, p.request.operationID == id else { return }
        p.cancelled = true; pending = p
        // Keep the continuation and authentication slot until this callback.
    }
    private func complete(_ id: UUID, result: WithdrawalNativeSDKCallbackOutcome) {
        guard let p = pending, p.request.operationID == id else {
            if case let .captured(value) = result { value.discard() }
            return
        }
        pending = nil
        do {
            try ownerRequire(!p.cancelled); try p.request.checkOriginalOperation()
            guard case let .captured(value) = result else { throw WithdrawalNativeReviewError.held }
            try ownerRequire(value.request.operationID == id && value.request.provider == p.request.provider
                && value.request.nonce == p.request.nonce)
            capturedOperation = (id,p.request.provider)
            p.continuation.resume(returning: value)
        } catch {
            if case let .captured(value) = result { value.discard() }
            p.continuation.resume(throwing: WithdrawalNativeReviewError.held)
        }
    }
    public func clearOriginalAfterVerifiedACK(_ grant: WithdrawalNativeSDKCleanupGrant) throws -> WithdrawalNativeSDKMemoryCleanupObservation {
        guard let capturedOperation, capturedOperation.id == grant.operationID,
              capturedOperation.provider == grant.provider else {throw WithdrawalNativeReviewError.held}
        self.capturedOperation = nil
        guard let cleanup = driver as? any WithdrawalNativeSDKMemoryCleanupPort else {return .unavailable}
        return try cleanup.clearOriginalAfterVerifiedACK(grant)
    }
    public nonisolated var description: String { "WithdrawalNativeSDKCallbackReview(redacted)" }
    public nonisolated var debugDescription: String { description }
    public nonisolated var customMirror: Mirror { Mirror(self, children: [:]) }
}
