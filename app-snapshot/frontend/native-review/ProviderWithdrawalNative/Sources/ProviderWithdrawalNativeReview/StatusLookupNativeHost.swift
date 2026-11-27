import Foundation

struct WithdrawalStatusNativeHostPolicy {
    init(json: Data) throws {
        let expected:[String:Any] = ["version":"1.0.0","scope":"isolated_native_host_review",
            "runtime_registered":false,"native_plugin_registered":false,"operating_native_host_authorized":false,
            "operating_member_transport_authorized":false,"provider_live_calls_authorized":false,"operating_OS_attestation":false,
            "automatic_retry":false,"automatic_mount_read":false,"whole_erasure_receipt":false,
            "authentication_gate":"same_native_login_and_withdrawal_gate_read_slot_until_original_read_drains",
            "lifetime":"terminal_original_scene_epoch_no_foreground_unlock_reactivation",
            "storage":"trusted_native_original_checkpoint_only_no_JS_claims",
            "transport":"existing_pinned_explicit_loopback_review_only",
            "actions":"explicit_original_status_read_only_no_login_SDK_close_or_prepare"]
        let raw = try withdrawalFlatObject(json)
        try ownerRequire(try JSONSerialization.data(withJSONObject:raw,options:.sortedKeys)
            == JSONSerialization.data(withJSONObject:expected,options:.sortedKeys))
    }
}

// Trusted native state, independent of React/JS claims. The original epoch is
// terminal after background/lock/session change. Explicit recreation creates a
// new scene epoch, never extends the signed original operation's deadline.
@MainActor public final class WithdrawalStatusNativeHostReview: WithdrawalLookupReadOnlyPort,
    CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    private let lifetime: WithdrawalNativeOwnerEpoch, generation: UUID, gate: NativeAuthOperationGate
    private let activeLoginSessionPresent: () throws -> Bool
    private var lease: NativeAuthOperationLease?, task: Task<WithdrawalNativeStatusReviewResult, Error>?
    private var holder: WithdrawalLookupRestartReview!
    public convenience init(configuration:Data, restartConfiguration:Data, statusConfiguration:Data, url:URL,
        publicKeyX963:Data, expectedKeySHA256:String, store:any WithdrawalLookupStorePort,
        deploymentContext:String, lifetime:WithdrawalNativeOwnerEpoch, authenticationGate:NativeAuthOperationGate,
        activeLoginSessionPresent:@escaping () throws -> Bool) throws {
        try self.init(configuration:configuration,restartConfiguration:restartConfiguration,statusConfiguration:statusConfiguration,
            url:url,publicKeyX963:publicKeyX963,expectedKeySHA256:expectedKeySHA256,store:store,deploymentContext:deploymentContext,
            lifetime:lifetime,authenticationGate:authenticationGate,activeLoginSessionPresent:activeLoginSessionPresent,
            sessionConfiguration:{.ephemeral})
    }
    init(configuration:Data,restartConfiguration:Data,statusConfiguration:Data,url:URL,publicKeyX963:Data,
        expectedKeySHA256:String,store:any WithdrawalLookupStorePort,deploymentContext:String,lifetime:WithdrawalNativeOwnerEpoch,
        authenticationGate:NativeAuthOperationGate,activeLoginSessionPresent:@escaping () throws -> Bool,
        sessionConfiguration:@escaping () -> URLSessionConfiguration) throws {
        _ = try WithdrawalStatusNativeHostPolicy(json:configuration)
        try ownerRequire(deploymentContext == "synthetic_test")
        let initial = try lifetime.snapshot()
        self.lifetime = lifetime;generation = initial.generation;gate = authenticationGate
        self.activeLoginSessionPresent = activeLoginSessionPresent
        // Construction/mount has no store read, SDK, login or HTTP effect.
        holder = try WithdrawalLookupRestartReview(configuration:restartConfiguration,statusConfiguration:statusConfiguration,
            url:url,publicKeyX963:publicKeyX963,expectedKeySHA256:expectedKeySHA256,store:store,deploymentContext:deploymentContext,
            admission:{ [weak self] in
                guard let self else { throw WithdrawalNativeReviewError.held }
                return try self.admit()
            },sessionConfiguration:sessionConfiguration)
    }
    public nonisolated var description:String { "WithdrawalStatusNativeHostReview(redacted)" }
    public nonisolated var debugDescription:String { description }
    public nonisolated var customMirror:Mirror { Mirror(self,children:[:]) }
    private func admit() throws -> WithdrawalLookupReadAdmission {
        guard let lease else { throw WithdrawalNativeReviewError.held }
        try ownerRequire(!Task.isCancelled);try gate.check(lease)
        let first = try lifetime.snapshot();try ownerRequire(first.generation == generation)
        do {
            if try activeLoginSessionPresent() { lifetime.signal(.sessionChanged);throw WithdrawalNativeReviewError.held }
        } catch { lifetime.signal(.sessionChanged);throw WithdrawalNativeReviewError.held }
        let final = try lifetime.snapshot();try ownerRequire(final.generation == generation && !Task.isCancelled)
        try gate.check(lease)
        return .init(now:final.now,sceneActive:true,protectedDataAvailable:true,authenticationInFlight:false,activeLoginSessionPresent:false)
    }
    func checkOriginalPresentation() throws {
        let now = try lifetime.snapshot();try ownerRequire(now.generation == generation)
        do {try ownerRequire(try !activeLoginSessionPresent())}
        catch {lifetime.signal(.sessionChanged);throw WithdrawalNativeReviewError.held}
        let final = try lifetime.snapshot();try ownerRequire(final.generation == generation)
    }
    // Can be called synchronously by the existing app/scene/vault event paths.
    // A foreground/unlock signal cannot resurrect this original host.
    public nonisolated func signal(_ signal:WithdrawalNativeOwnerSignal) { lifetime.signal(signal) }
    public func dispose() { lifetime.signal(.disposed);task?.cancel() }
    public func readOriginalStatusExplicit() async throws -> WithdrawalNativeStatusReviewResult {
        try ownerRequire(!Task.isCancelled)
        if lease != nil { throw WithdrawalNativeReviewError.busy }
        let acquired:NativeAuthOperationLease
        do { acquired = try gate.begin(.withdrawalStatusRead) }
        catch { throw WithdrawalNativeReviewError.busy }
        lease = acquired
        defer { task = nil;lease = nil;gate.finish(acquired) }
        _ = try admit()
        let reader = try holder.restoreOriginalReadOnly()
        let work = Task { @MainActor in try await reader.readOriginalStatusExplicit() }
        task = work
        let result = try await withTaskCancellationHandler(operation:{try await work.value},onCancel:{work.cancel()})
        _ = try admit()
        return result
    }
}
