import Foundation

@MainActor public protocol WithdrawalNativeActualTESTPreparedHostPort:AnyObject,Sendable {
    var invocation:WithdrawalNativeInvocationReview {get}
    var actualContext:WithdrawalNativeActualTESTContext {get}
    func dispose()
}

// Native-only assembly API. The caller explicitly starts binding preparation;
// mounting the resulting CAP adapter does not start SDK or status reads.
@MainActor public final class WithdrawalNativeActualTESTHostCandidate:WithdrawalNativeActualTESTPreparedHostPort {
    public let invocation: WithdrawalNativeInvocationReview
    public let actualContext:WithdrawalNativeActualTESTContext
    private let owner: WithdrawalNativeVerifiedBindingOwner
    private init(invocation:WithdrawalNativeInvocationReview,owner:WithdrawalNativeVerifiedBindingOwner,
        actualContext:WithdrawalNativeActualTESTContext) {
        self.invocation=invocation;self.owner=owner;self.actualContext=actualContext
    }
    public static func prepareExplicit(policies:WithdrawalHTTPSCompositionReviewPolicies,
        invocationConfiguration:Data,proofProfileConfiguration:Data,
        actualContext:WithdrawalNativeActualTESTContext,epoch:WithdrawalNativeOwnerEpoch,
        vault:any WithdrawalNativeVaultReadPort,sdk:WithdrawalNativeSDKCallbackReview,
        store:any WithdrawalLookupStorePort,authenticationGate:NativeAuthOperationGate,
        checkOriginalPresentation:@escaping @MainActor () throws -> Void,
        activeLoginSessionPresent:@escaping @MainActor () throws -> Bool,
        preparationObserver:@MainActor (WithdrawalNativePreparationStage)->Void = {_ in}) async throws -> Self {
        try await prepare(policies:policies,invocationConfiguration:invocationConfiguration,
            proofProfileConfiguration:proofProfileConfiguration,actualContext:actualContext,epoch:epoch,
            vault:vault,sdk:sdk,store:store,authenticationGate:authenticationGate,
            checkOriginalPresentation:checkOriginalPresentation,activeLoginSessionPresent:activeLoginSessionPresent,
            sessionConfiguration:{.ephemeral},preparationObserver:preparationObserver)
    }
    static func prepare(policies:WithdrawalHTTPSCompositionReviewPolicies,
        invocationConfiguration:Data,proofProfileConfiguration:Data,
        actualContext:WithdrawalNativeActualTESTContext,epoch:WithdrawalNativeOwnerEpoch,
        vault:any WithdrawalNativeVaultReadPort,sdk:WithdrawalNativeSDKCallbackReview,
        store:any WithdrawalLookupStorePort,authenticationGate:NativeAuthOperationGate,
        checkOriginalPresentation:@escaping @MainActor () throws -> Void,
        activeLoginSessionPresent:@escaping @MainActor () throws -> Bool,
        sessionConfiguration:@escaping () -> URLSessionConfiguration,
        preparationObserver:@MainActor (WithdrawalNativePreparationStage)->Void = {_ in}) async throws -> Self {
        try ownerRequire(sdk.actualContext === actualContext)
        try WithdrawalNativeInvocationReview.requireConfiguration(invocationConfiguration)
        let generation=try epoch.snapshot().generation
        let check: @MainActor () throws -> Void = {
            try checkOriginalPresentation()
            try ownerRequire(try epoch.snapshot().generation == generation)
        }
        try check()
        let originalCredential = policies.originalSessionClosure
            ? try withdrawalReadVault(vault, policy: WithdrawalNativeOwnerPolicy(json: policies.owner)) : nil
        let readFence=WithdrawalActualTESTReadFence(gate:authenticationGate,activeLogin:{
            guard let originalCredential else { return try activeLoginSessionPresent() }
            let policy = try WithdrawalNativeOwnerPolicy(json: policies.owner)
            switch try vault.copy(WithdrawalNativeVaultRequest(policy: policy)) {
            case .missing: return false
            case .found:
                let value = try withdrawalReadVault(vault, policy: policy)
                return value.bearer != originalCredential.bearer || value.expiresAt != originalCredential.expiresAt
            }
        })
        let readCheck: @MainActor () throws -> Void = {
            try checkOriginalPresentation()
            if !policies.originalSessionClosure { try check() }
        }
        let profile=try WithdrawalProofProfileReview(configuration:proofProfileConfiguration,
            publicKeyX963:actualContext.publicKeyX963,expectedKeySHA256:actualContext.sourcePin,
            isolatedKeySHA256:actualContext.isolatedPin,restoreKeySHA256:actualContext.restorePin,
            deploymentContext:"actual_test_candidate",actualContext:actualContext)
        let composition=try await WithdrawalHTTPSOfflineReviewComposition.prepare(policies:policies,
            epoch:epoch,vault:vault,sdk:sdk,store:store,publicKeyX963:actualContext.publicKeyX963,
            expectedKeySHA256:actualContext.sourcePin,authenticationGate:authenticationGate,
            admission:{
                try readCheck()
                try readFence.check()
                return .init(now:try policies.originalSessionClosure ? epoch.originalReadbackTime() : epoch.snapshot().now,sceneActive:true,protectedDataAvailable:true,
                    authenticationInFlight:false,activeLoginSessionPresent:false)
            },sessionConfiguration:sessionConfiguration,proofProfile:profile,actualContext:actualContext,preparationObserver:preparationObserver)
        do {
            try check()
            let reader=WithdrawalActualTESTOriginalReader(restart:composition.restart,gate:authenticationGate,
                check:readCheck,readFence:readFence)
            let invocation=try WithdrawalNativeInvocationReview(configuration:invocationConfiguration,
                deploymentContext:"actual_test_candidate",originalFlow:composition.flow,originalReader:reader,
                checkOriginalPresentation:readCheck,retireOriginalReader:{reader.dispose()},actualContext:actualContext)
            return Self(invocation:invocation,owner:composition.owner,actualContext:actualContext)
        } catch {composition.owner.retire();composition.flow.retire();throw WithdrawalNativeReviewError.held}
    }
    public func dispose(){invocation.dispose();owner.retire()}
}

@MainActor private final class WithdrawalActualTESTReadFence {
    let gate:NativeAuthOperationGate,activeLogin:@MainActor () throws -> Bool
    var lease:NativeAuthOperationLease?,retired=false
    init(gate:NativeAuthOperationGate,activeLogin:@escaping @MainActor () throws -> Bool) {
        self.gate=gate;self.activeLogin=activeLogin
    }
    func check()throws {
        try ownerRequire(!retired)
        if let lease {
            do {try gate.check(lease);try ownerRequire(try !activeLogin())}
            catch {retired=true;throw WithdrawalNativeReviewError.held}
        }
    }
}

@MainActor private final class WithdrawalActualTESTOriginalReader:WithdrawalLookupReadOnlyPort {
    let restart:WithdrawalLookupRestartReview,gate:NativeAuthOperationGate
    let check:@MainActor () throws -> Void,readFence:WithdrawalActualTESTReadFence
    var retired=false
    init(restart:WithdrawalLookupRestartReview,gate:NativeAuthOperationGate,
        check:@escaping @MainActor () throws -> Void,readFence:WithdrawalActualTESTReadFence) {
        self.restart=restart;self.gate=gate;self.check=check;self.readFence=readFence
    }
    func dispose(){retired=true;readFence.retired=true}
    func admit(_ lease:NativeAuthOperationLease)throws {
        try ownerRequire(!retired && !Task.isCancelled);try gate.check(lease);try check()
        try readFence.check();try gate.check(lease);try check()
    }
    func readOriginalStatusExplicit() async throws -> WithdrawalNativeStatusReviewResult {
        let lease=try gate.begin(.withdrawalStatusRead);readFence.lease=lease
        defer {readFence.lease=nil;gate.finish(lease)}
        try admit(lease)
        let result=try await restart.restoreOriginalReadOnly().readOriginalStatusExplicit()
        try admit(lease);return result
    }
}
