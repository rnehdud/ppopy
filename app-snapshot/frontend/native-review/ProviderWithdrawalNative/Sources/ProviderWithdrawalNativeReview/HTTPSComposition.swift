import Foundation

// Byte-exact OFF policies are decoded by their existing validators. This
// assembly can carry an explicit OFF TEST proof profile; it does not register
// an operating key or grant route authorization.
public struct WithdrawalHTTPSCompositionReviewPolicies {
    let https: Data, binding: Data, bindingHTTP: Data, owner: Data, native: Data
    let closure: Data, status: Data, restart: Data
    public let kakao: Data?
    let durable: Data?
    let originalSessionClosure: Bool
    public init(https: Data, binding: Data, bindingHTTP: Data, owner: Data, native: Data,
        closure: Data, status: Data, restart: Data, kakao: Data?, durable: Data? = nil, originalSessionClosure: Bool = false) {
        self.https = https; self.binding = binding; self.bindingHTTP = bindingHTTP; self.owner = owner; self.native = native
        self.closure = closure; self.status = status; self.restart = restart; self.kakao = kakao; self.durable = durable; self.originalSessionClosure = originalSessionClosure
    }
}

@MainActor struct WithdrawalHTTPSOfflineReviewComposition {
    let owner: WithdrawalNativeVerifiedBindingOwner
    let flow: WithdrawalNativeReviewCoordinator
    let restart: WithdrawalLookupRestartReview

    static func prepare(policies: WithdrawalHTTPSCompositionReviewPolicies,
        epoch: WithdrawalNativeOwnerEpoch, vault: any WithdrawalNativeVaultReadPort,
        sdk: any WithdrawalNativeSDKCapturePort, store: any WithdrawalLookupStorePort,
        publicKeyX963: Data, expectedKeySHA256: String, authenticationGate: NativeAuthOperationGate,
        admission: @escaping () throws -> WithdrawalLookupReadAdmission,
        sessionConfiguration: @escaping () -> URLSessionConfiguration,
        proofProfile: WithdrawalProofProfileReview? = nil,
        actualContext: WithdrawalNativeActualTESTContext? = nil,
        preparationObserver:@MainActor (WithdrawalNativePreparationStage)->Void = {_ in}) async throws -> Self {
        let mode = actualContext == nil ? "synthetic_test" : "actual_test_candidate"
        try ownerRequire(proofProfile?.actualContext === actualContext)
        if let actualContext {
            try ownerRequire((sdk as? WithdrawalNativeSDKCallbackReview)?.actualContext === actualContext)
        }
        try proofProfile?.requireKey(publicKeyX963)
        preparationObserver(.validatingPolicies)
        // Reject every policy before the first vault/binding request.
        _ = try WithdrawalBindingPolicy(json:policies.binding)
        _ = try WithdrawalBindingHTTPPolicy(json:policies.bindingHTTP)
        _ = try WithdrawalNativeOwnerPolicy(json:policies.owner)
        _ = try WithdrawalNativeReviewPolicy(json:policies.native,kakaoConfiguration:policies.kakao)
        _ = try WithdrawalClosureHTTPPolicy(json:policies.closure)
        _ = try WithdrawalStatusHTTPPolicy(json:policies.status)
        _ = try WithdrawalLookupRestartPolicy(json:policies.restart)
        if let durable=policies.durable {_ = try WithdrawalDurableWirePolicy(json:durable)}
        let transport = try WithdrawalHTTPSReviewTransport(configuration: policies.https)
        let binding = try WithdrawalNativeBindingLoopbackReview(configuration: policies.bindingHTTP,
            url: transport.url(method: "withdrawal_binding"), deploymentContext: mode,
            sessionConfiguration: sessionConfiguration, httpsReview: transport, actualContext: actualContext)
        let owner = try await WithdrawalNativeVerifiedBindingOwner.bootstrap(configuration: policies.binding,
            ownerPolicy: WithdrawalNativeOwnerPolicy(json: policies.owner), epoch: epoch, vault: vault, server: binding,
            publicKeyX963: publicKeyX963, expectedKeySHA256: expectedKeySHA256,
            deploymentContext: mode, authenticationGate: authenticationGate, kakaoConfiguration: policies.kakao, proofProfile: proofProfile, preparationObserver:preparationObserver)
        do {
            preparationObserver(.providerAdapter)
            // Select only from the verified server binding; JS and a guessed
            // login provider never choose the provider-specific close adapter.
            let originalProvider = try owner.currentSession().provider
            let closureConfiguration = originalProvider == .kakao ? (policies.kakao ?? policies.closure) : policies.closure
            let server = try WithdrawalNativeStatusLoopbackReview(configuration: policies.status,
                closureConfiguration: closureConfiguration, url: transport.url(method: "withdrawal_lookup_prepare"),
                deploymentContext: mode, owner: owner, publicKeyX963: publicKeyX963,
                expectedKeySHA256: expectedKeySHA256, sessionConfiguration: sessionConfiguration,
                readAdmission: { try admission().now }, httpsReview: transport, durableConfiguration: policies.durable, proofProfile: proofProfile)
            let restart = try WithdrawalLookupRestartReview(configuration: policies.restart,
                statusConfiguration: policies.status, url: transport.url(method: "withdrawal_status_read"),
                publicKeyX963: publicKeyX963, expectedKeySHA256: expectedKeySHA256, store: store,
                deploymentContext: mode, admission: admission, sessionConfiguration: sessionConfiguration,
                kakaoConfiguration: policies.kakao, httpsReview: transport, proofProfile: proofProfile)
            // The exact signed grant is stored/read back before any challenge,
            // SDK capture or close can run. Restoration exposes reads only.
            try restart.attachBeforePreparation(to: server,
                replacingExpiredSameSession:actualContext != nil && policies.durable != nil)
            let policy = try WithdrawalNativeReviewPolicy(json: policies.native, kakaoConfiguration: policies.kakao)
            let flow = try WithdrawalNativeReviewCoordinator(policy: policy, session: owner, sdk: sdk, server: server,
                deploymentContext: mode, authenticationGate: authenticationGate, originalSessionClosure: policies.originalSessionClosure, actualContext: actualContext)
            return Self(owner: owner, flow: flow, restart: restart)
        } catch { owner.retire(); throw WithdrawalNativeReviewError.held }
    }
}
