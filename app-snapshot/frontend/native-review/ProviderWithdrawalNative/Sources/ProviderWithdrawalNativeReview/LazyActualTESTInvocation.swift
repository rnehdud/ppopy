import Foundation

// Mounted native owner, with no vault/HTTP/SDK/checkpoint effects on creation.
// A missing provider/runtime prerequisite holds before evaluating the factory.
@MainActor public final class WithdrawalNativeLazyActualTESTInvocationCandidate:WithdrawalNativeInvocationPort {
    private let context:WithdrawalNativeActualTESTContext
    private let checkPresentation:@MainActor () throws -> Void
    private let prepare:@MainActor () async throws -> any WithdrawalNativeActualTESTPreparedHostPort
    private let fence=WithdrawalNativeInvocationFence()
    private let statusLifecycle:WithdrawalStatusReadLifecycleFence?
    private var host:(any WithdrawalNativeActualTESTPreparedHostPort)?,busy=false,retired=false,used=false
    public private(set) var preparationCount=0
    public init(configuration:Data,actualContext:WithdrawalNativeActualTESTContext,
        checkOriginalPresentation:@escaping @MainActor () throws -> Void,
        prepareOriginalHost:@escaping @MainActor () async throws -> any WithdrawalNativeActualTESTPreparedHostPort,
        statusLifecycleConfiguration:Data? = nil)throws {
        try WithdrawalNativeInvocationReview.requireConfiguration(configuration)
        if let statusLifecycleConfiguration {
            _ = try WithdrawalStatusReadLifecyclePolicy(statusLifecycleConfiguration)
            statusLifecycle=WithdrawalStatusReadLifecycleFence()
        } else {statusLifecycle=nil}
        context=actualContext;checkPresentation=checkOriginalPresentation;prepare=prepareOriginalHost
    }
    public nonisolated func suspendOriginalForBackground(){
        guard let statusLifecycle else {retireIfOriginalAccessStarted();return}
        statusLifecycle.suspend()
    }
    public nonisolated func retireOriginalPresentation(){
        fence.retire();Task { @MainActor [weak self] in self?.dispose() }
    }
    // Mount has no identity/checkpoint/HTTP ownership yet. A legitimate login
    // can change the vault before the first explicit request captures it.
    // After the first access begins, every such signal remains terminal.
    public nonisolated func retireIfOriginalAccessStarted(){
        if fence.retireIfOriginalAccessStarted() {
            Task { @MainActor [weak self] in self?.dispose() }
        }
    }
    public func dispose(){fence.retire();retired=true;host?.dispose()}
    public func mayPublishToOriginalPresentation()->Bool {
        guard fence.isLive(),!retired,!Task.isCancelled else {return false}
        do {try checkPresentation();return true} catch {
            // A transient inactive/locked scene cannot publish. It must not
            // destroy the separately bounded, original checkpoint reader.
            // Navigation/session/time/disposal still retire the outer fence.
            if statusLifecycle == nil {dispose()}
            return false
        }
    }
    public func mayPublishToOriginalPresentation(reply:WithdrawalNativeInvocationReviewReply)->Bool {
        guard mayPublishToOriginalPresentation() else {return false}
        guard let statusLifecycle else {return true}
        switch reply.publication {
        case .originalStatus(let generation):return statusLifecycle.isCurrent(generation)
        case .originalMutation:return statusLifecycle.mayMutate()
        case nil:return false
        }
    }
    private func admit(_ options:Data)throws {
        try ownerRequire(mayPublishToOriginalPresentation() && (2...64).contains(options.count))
        guard let fields=try JSONSerialization.jsonObject(with:options) as? [String:Any],fields.isEmpty else {throw WithdrawalNativeReviewError.held}
    }
    private func originalHost()async throws -> any WithdrawalNativeActualTESTPreparedHostPort {
        if let host {return host}
        try ownerRequire(fence.beginOriginalAccess())
        statusLifecycle?.beginOriginalAccess()
        preparationCount += 1
        let prepared=try await prepare()
        guard mayPublishToOriginalPresentation(),prepared.actualContext === context else {
            prepared.dispose();throw WithdrawalNativeReviewError.held
        }
        host=prepared;return prepared
    }
    // Native-only console preparation. It consumes this invocation so it
    // cannot be followed by a withdrawal. No coordinator/SDK/status call runs.
    public func prepareOriginalReadOnlyForConsole()async throws {
        try admit(Data("{}".utf8));try context.requireWithdrawalReady()
        if busy {throw WithdrawalNativeReviewError.busy}
        try ownerRequire(!used);used=true;busy=true;defer {busy=false}
        _ = try await originalHost()
        try ownerRequire(mayPublishToOriginalPresentation())
    }
    public func withdrawExplicit(options:Data)async throws -> WithdrawalNativeInvocationReviewReply {
        try admit(options);try context.requireWithdrawalReady()
        if busy {throw WithdrawalNativeReviewError.busy}
        try ownerRequire(!used && statusLifecycle?.mayMutate() != false);used=true;busy=true;defer {busy=false}
        let prepared=try await originalHost()
        try ownerRequire(statusLifecycle?.mayMutate() != false)
        let value=try await prepared.invocation.withdrawExplicit(options:options)
        try ownerRequire(statusLifecycle?.mayMutate() != false)
        try ownerRequire(mayPublishToOriginalPresentation())
        return statusLifecycle == nil ? value : value.requiringOriginalMutation()
    }
    public func readOriginalStatusExplicit(options:Data)async throws -> WithdrawalNativeInvocationReviewReply {
        try admit(options);try context.requireWithdrawalReady()
        if busy {throw WithdrawalNativeReviewError.busy}
        busy=true;defer {busy=false}
        let value:WithdrawalNativeInvocationReviewReply
        if let statusLifecycle {
            // No host factory, binding refresh, lookup preparation or SDK on
            // this path. The original reader enforces identity and expiry.
            guard let host else {throw WithdrawalNativeReviewError.held}
            let generation=statusLifecycle.snapshot()
            let observed=try await host.invocation.readOriginalStatusWithinOriginalGrantExplicit(options:options)
            try ownerRequire(statusLifecycle.isCurrent(generation))
            value=observed.attachingOriginalStatusGeneration(generation)
        } else {
            value=try await originalHost().invocation.readOriginalStatusExplicit(options:options)
        }
        try ownerRequire(mayPublishToOriginalPresentation());return value
    }
}
