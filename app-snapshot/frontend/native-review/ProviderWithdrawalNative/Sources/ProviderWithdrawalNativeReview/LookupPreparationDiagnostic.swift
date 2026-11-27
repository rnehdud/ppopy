import Foundation

// This explicit diagnostic can create one short-lived server lookup grant.
// Its checkpoint is memory only; it has no call to account closure or SDK.
@MainActor private final class PreparationMemoryCheckpoint: WithdrawalLookupStorePort {
    var bytes:Data?
    init(_ source:WithdrawalLookupStoreResult)throws {
        switch source {
        case .missing:break
        case let .found(data,service,account,accessibility,sync):
            try ownerRequire(service == "com.miraylab.poppy.withdrawal-status-review"
                && account == "skinanalysis.withdrawal.original-lookup.v1"
                && accessibility == "when_unlocked_this_device_only" && !sync && data.count<=16384)
            bytes=data
        }
    }
    func copy(_ r:WithdrawalLookupStoreRequest)throws->WithdrawalLookupStoreResult {
        guard let bytes else {return .missing}
        return .found(data:bytes,service:r.service,account:r.account,accessibility:r.accessibility,synchronizable:false)
    }
    func create(_ r:WithdrawalLookupStoreRequest,data:Data)throws {try ownerRequire(bytes==nil);bytes=data}
    func replace(_ r:WithdrawalLookupStoreRequest,expected:Data,replacement:Data)throws {try ownerRequire(bytes==expected);bytes=replacement}
    func remove(_ r:WithdrawalLookupStoreRequest,expected:Data)throws {try ownerRequire(bytes==expected);bytes=nil}
}

public enum WithdrawalPreparationDiagnostic {
    @MainActor public static func run(policies:WithdrawalHTTPSCompositionReviewPolicies,
        proofProfileConfiguration:Data,actualContext:WithdrawalNativeActualTESTContext,
        epoch:WithdrawalNativeOwnerEpoch,vault:any WithdrawalNativeVaultReadPort,
        originalStore:any WithdrawalLookupStorePort,
        sessionConfiguration:@escaping ()->URLSessionConfiguration = {.ephemeral},
        progress:@escaping (String)->Void = {_ in})async->[String:Any] {
        var stage="probe_context" {didSet {progress(stage)}}
        var binding=0,lookup=0,checkpointReads=0,completed=false
        progress(stage)
        do {
            try actualContext.requireWithdrawalReady()
            let transport=try WithdrawalHTTPSReviewTransport(configuration:policies.https)
            let profile=try WithdrawalProofProfileReview(configuration:proofProfileConfiguration,
                publicKeyX963:actualContext.publicKeyX963,expectedKeySHA256:actualContext.sourcePin,
                isolatedKeySHA256:actualContext.isolatedPin,restoreKeySHA256:actualContext.restorePin,
                deploymentContext:"actual_test_candidate",actualContext:actualContext)
            stage="checkpoint_seed";checkpointReads=1
            let memory=try PreparationMemoryCheckpoint(originalStore.copy(WithdrawalLookupStoreRequest(WithdrawalLookupRestartPolicy(json:policies.restart))))
            let bindingPort=try WithdrawalNativeBindingLoopbackReview(configuration:policies.bindingHTTP,
                url:transport.url(method:"withdrawal_binding"),deploymentContext:"actual_test_candidate",
                sessionConfiguration:sessionConfiguration,httpsReview:transport,actualContext:actualContext)
            stage="binding";binding=1
            let owner=try await WithdrawalNativeVerifiedBindingOwner.bootstrap(configuration:policies.binding,
                ownerPolicy:WithdrawalNativeOwnerPolicy(json:policies.owner),epoch:epoch,vault:vault,server:bindingPort,
                publicKeyX963:actualContext.publicKeyX963,expectedKeySHA256:actualContext.sourcePin,
                deploymentContext:"actual_test_candidate",authenticationGate:NativeAuthOperationGate(),
                kakaoConfiguration:policies.kakao,proofProfile:profile,preparationObserver:{next in
                    switch next {
                    case .readingVault:stage="vault_read"
                    case .fetchingBinding:stage="binding_http"
                    case .validatingBinding:stage="binding_validation"
                    case .bindingVerified:stage="binding_verified"
                    default:break
                    }
                })
            defer {owner.retire()}
            stage="status_adapter"
            let server=try WithdrawalNativeStatusLoopbackReview(configuration:policies.status,
                closureConfiguration:try owner.currentSession().provider == .kakao ? (policies.kakao ?? policies.closure) : policies.closure,
                url:transport.url(method:"withdrawal_lookup_prepare"),deploymentContext:"actual_test_candidate",owner:owner,
                publicKeyX963:actualContext.publicKeyX963,expectedKeySHA256:actualContext.sourcePin,
                sessionConfiguration:sessionConfiguration,readAdmission:{throw WithdrawalNativeReviewError.held},
                httpsReview:transport,durableConfiguration:policies.durable,proofProfile:profile)
            stage="restart_adapter"
            let restart=try WithdrawalLookupRestartReview(configuration:policies.restart,statusConfiguration:policies.status,
                url:transport.url(method:"withdrawal_status_read"),publicKeyX963:actualContext.publicKeyX963,
                expectedKeySHA256:actualContext.sourcePin,store:memory,deploymentContext:"actual_test_candidate",
                admission:{throw WithdrawalNativeReviewError.held},sessionConfiguration:sessionConfiguration,
                kakaoConfiguration:policies.kakao,httpsReview:transport,proofProfile:profile)
            stage="checkpoint_attachment"
            try restart.attachBeforePreparation(to:server,replacingExpiredSameSession:true,trace:{stage=$0})
            stage="lookup_start";lookup=1
            try await server.prepareStatusLookupDiagnosed(original:owner.currentSession(),requestID:UUID(),trace:{stage=$0})
            completed=true
        } catch {}
        return ["stage":stage,"prepared":completed,"binding_calls":binding,"lookup_calls":lookup,
            "checkpoint_reads":checkpointReads,"checkpoint_writes":0,"login_vault_writes":0,
            "closure_calls":0,"provider_authentication_calls":0]
    }
}
