import Foundation

final class WithdrawalNativeInvocationFence: @unchecked Sendable {
    private let lock = NSLock()
    private var live = true, originalAccessStarted = false
    func retire() { lock.withLock { live = false } }
    func isLive() -> Bool { lock.withLock { live } }
    func beginOriginalAccess() -> Bool {
        lock.withLock {
            guard live else { return false }
            originalAccessStarted = true; return true
        }
    }
    func retireIfOriginalAccessStarted() -> Bool {
        lock.withLock {
            guard originalAccessStarted, live else { return false }
            live = false; return true
        }
    }
}

// The native composition supplies both ports. JS supplies no account, token,
// provider, operation identifier, callback, key, or replacement factory.
// Review replies cannot become the application's operating closure acceptance.
public struct WithdrawalNativeInvocationReviewReply: Sendable {
    public let body: Data
    enum Publication:Sendable {case originalMutation,originalStatus(UUID)}
    let publication:Publication?
    private init(body:Data,publication:Publication){self.body=body;self.publication=publication}
    func requiringOriginalMutation()->Self {.init(body:body,publication:.originalMutation)}
    func attachingOriginalStatusGeneration(_ generation:UUID)->Self {.init(body:body,publication:.originalStatus(generation))}
    fileprivate init(_ fields: [String: Any]) throws {
        var value = fields
        value["version"] = "1.0.0"
        value["scope"] = "isolated_native_invocation_review"
        value["operationally_eligible"] = false
        value["whole_deletion_completed"] = false
        let bytes = try JSONSerialization.data(withJSONObject: value, options: .sortedKeys)
        try ownerRequire(bytes.count <= 2048)
        body = bytes;publication=nil
    }
}

@MainActor public protocol WithdrawalNativeInvocationPort:AnyObject,Sendable {
    func withdrawExplicit(options:Data) async throws -> WithdrawalNativeInvocationReviewReply
    func readOriginalStatusExplicit(options:Data) async throws -> WithdrawalNativeInvocationReviewReply
    func dispose()
    func mayPublishToOriginalPresentation()->Bool
    func mayPublishToOriginalPresentation(reply:WithdrawalNativeInvocationReviewReply)->Bool
    nonisolated func retireOriginalPresentation()
}
public extension WithdrawalNativeInvocationPort {
    func mayPublishToOriginalPresentation(reply:WithdrawalNativeInvocationReviewReply)->Bool {
        mayPublishToOriginalPresentation()
    }
}

@MainActor public final class WithdrawalNativeInvocationReview: WithdrawalNativeInvocationPort,CustomStringConvertible,
    CustomDebugStringConvertible, CustomReflectable {
    private let flow: WithdrawalNativeReviewCoordinator
    private let reader: any WithdrawalLookupReadOnlyPort
    private let checkPresentation: @MainActor () throws -> Void
    private let retireReader: @MainActor () -> Void
    private let fence = WithdrawalNativeInvocationFence()
    private var used = false, busy = false, retired = false
    private var task: Task<WithdrawalNativeInvocationReviewReply, Error>?

    public init(configuration: Data, deploymentContext: String,
        originalFlow: WithdrawalNativeReviewCoordinator, originalReader: any WithdrawalLookupReadOnlyPort,
        checkOriginalPresentation: @escaping @MainActor () throws -> Void,
        retireOriginalReader: @escaping @MainActor () -> Void,
        actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        try requireWithdrawalNativeContext(deploymentContext,actualContext)
        try ownerRequire(originalFlow.actualContext === actualContext)
        try Self.requireConfiguration(configuration)
        flow = originalFlow; reader = originalReader
        checkPresentation = checkOriginalPresentation; retireReader = retireOriginalReader
        // Construction/mount has no vault/checkpoint, SDK or HTTP effect.
    }
    static func requireConfiguration(_ configuration:Data)throws {
        let expected: [String: Any] = ["version":"1.0.0", "scope":"isolated_native_invocation_review",
            "runtime_registered":false, "native_plugin_registered":false,
            "operating_member_transport_authorized":false, "automatic_retry":false,
            "automatic_mount_read":false, "whole_erasure_receipt":false,
            "request":"empty_options_no_JS_identity_credential_provider_or_lookup_capability",
            "owner":"one_original_native_coordinator_and_checkpoint_reader_never_replace_after_dispatch",
            "lifetime":"native_presentation_admission_before_and_after_await_dispose_terminal_callback_drains",
            "response":"bounded_fixed_fixture_observations_no_operating_acceptance_or_identity"]
        let raw = try withdrawalFlatObject(configuration)
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
                == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
    }

    public nonisolated var description: String { "WithdrawalNativeInvocationReview(redacted)" }
    public nonisolated var debugDescription: String { description }
    public nonisolated var customMirror: Mirror { Mirror(self, children: [:]) }

    public func dispose() {
        guard !retired else { return }
        fence.retire(); retired = true; flow.retire(); retireReader(); task?.cancel()
        // Do not discard the running task or release the shared SDK lease.
        // The original coordinator retains it until its SDK callback drains.
    }
    // Navigation/destruction may arrive outside the actor. The synchronous
    // fence blocks admission/publication immediately; actor cleanup follows.
    public nonisolated func retireOriginalPresentation() {
        fence.retire()
        Task { @MainActor [weak self] in self?.dispose() }
    }
    private func admit(_ options: Data, retireOnPresentationLoss:Bool = true) throws {
        try ownerRequire(fence.isLive() && !retired && !Task.isCancelled)
        // The existing policy decoder intentionally requires at least one
        // configuration field. Invocation options instead accept only {}.
        // No duplicate/nonempty key set can normalize into an empty object.
        try ownerRequire((2...64).contains(options.count))
        guard let raw = try JSONSerialization.jsonObject(with: options) as? [String: Any], raw.isEmpty else {
            throw WithdrawalNativeReviewError.held
        }
        do { try checkPresentation() }
        catch { if retireOnPresentationLoss {dispose()}; throw WithdrawalNativeReviewError.held }
    }
    // CAP uses this for both success and failure callbacks. An error from an
    // old task must not resolve/reject a callback identifier on a reloaded page.
    // This checks presentation only; closure may already have retired identity.
    public func mayPublishToOriginalPresentation() -> Bool {
        presentationIsCurrent(retireOnLoss:true)
    }
    private func presentationIsCurrent(retireOnLoss:Bool) -> Bool {
        guard fence.isLive() && !retired && !Task.isCancelled else { return false }
        do { try checkPresentation() }
        catch { if retireOnLoss {dispose()}; return false }
        return true
    }
    private func publish(_ reply: WithdrawalNativeInvocationReviewReply,retireOnLoss:Bool = true) throws -> WithdrawalNativeInvocationReviewReply {
        try ownerRequire(presentationIsCurrent(retireOnLoss:retireOnLoss))
        return reply
    }

    public func withdrawExplicit(options: Data) async throws -> WithdrawalNativeInvocationReviewReply {
        try admit(options)
        if busy { throw WithdrawalNativeReviewError.busy }
        try ownerRequire(!used)
        used = true; busy = true
        let work = Task { @MainActor [flow] in
            let result = try await flow.withdrawExplicit()
            return try WithdrawalNativeInvocationReviewReply(["kind":"withdrawal_fixture_observation",
                "account_closed_in_fixture":result.accountClosedInFixture,
                "provider_acknowledged_in_fixture":result.providerAcknowledgedInFixture,
                "SDK_memory_cleared_in_fixture":result.SDKMemoryClearedInFixture,
                "SDK_storage_erasure_confirmed":false, "app_vault_erasure_confirmed":false])
        }
        task = work
        defer { busy = false; task = nil }
        do {
            let value = try await withTaskCancellationHandler(operation:{ try await work.value }, onCancel:{ work.cancel() })
            return try publish(value)
        } catch {
            // A competing authentication blocked the coordinator before it
            // accepted an operation. Only that specific path remains usable.
            if error as? WithdrawalNativeReviewError == .busy && !retired && !Task.isCancelled { used = false }
            throw WithdrawalNativeReviewError.held
        }
    }

    public func readOriginalStatusExplicit(options: Data) async throws -> WithdrawalNativeInvocationReviewReply {
        try await readOriginalStatus(options:options,retireOnPresentationLoss:true)
    }
    // Native-only entry for the separately reviewed background lifecycle. It
    // retains the original reader/capability and does not recreate any port.
    // The outer owner fences in-flight replies across background transitions.
    public func readOriginalStatusWithinOriginalGrantExplicit(options:Data) async throws -> WithdrawalNativeInvocationReviewReply {
        try await readOriginalStatus(options:options,retireOnPresentationLoss:false)
    }
    private func readOriginalStatus(options:Data,retireOnPresentationLoss:Bool) async throws -> WithdrawalNativeInvocationReviewReply {
        try admit(options,retireOnPresentationLoss:retireOnPresentationLoss)
        if busy { throw WithdrawalNativeReviewError.busy }
        busy = true
        let work = Task { @MainActor [reader] in
            let result = try await reader.readOriginalStatusExplicit()
            let text = WithdrawalLookupPresentation(result: result)
            return try WithdrawalNativeInvocationReviewReply(["kind":"withdrawal_record_observation",
                "title":text.title, "account":text.account, "connection":text.connection,
                "data_deletion":text.dataDeletion,
                "account_closed_in_record":result.accountClosedInRecord,
                "provider_acknowledged_in_record":result.providerAcknowledgedInRecord,
                "SDK_cleanup_confirmed":false])
        }
        task = work
        defer { busy = false; task = nil }
        let value = try await withTaskCancellationHandler(operation:{ try await work.value }, onCancel:{ work.cancel() })
        return try publish(value,retireOnLoss:retireOnPresentationLoss)
    }
}
