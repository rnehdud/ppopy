#if SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
import Foundation
import UIKit
import ProviderWithdrawalNativeReview

// Explicit native-only preparation, never called from app mount or JS options.
// This candidate is not registered in AppDelegate or a CAP bridge.
@MainActor public final class WithdrawalIOSActualTESTHostCandidate:WithdrawalNativeActualTESTPreparedHostPort {
    public let plugin:IOSWithdrawalInvocationReviewPlugin
    public var invocation:WithdrawalNativeInvocationReview {host.invocation}
    public var actualContext:WithdrawalNativeActualTESTContext {host.actualContext}
    private let host:WithdrawalNativeActualTESTHostCandidate
    private let osOwner:WithdrawalNativeActualTESTOSOwnerCandidate
    private init(host:WithdrawalNativeActualTESTHostCandidate,osOwner:WithdrawalNativeActualTESTOSOwnerCandidate) {
        self.host=host;self.osOwner=osOwner
        plugin=IOSWithdrawalInvocationReviewPlugin(originalHost:host.invocation)
    }
    public static func prepareCompiledExplicit(policies:WithdrawalHTTPSCompositionReviewPolicies,
        invocationConfiguration:Data,proofProfileConfiguration:Data,ownerConfiguration:Data,
        sdkUIConfiguration:Data,nativeConfiguration:Data,cleanupConfiguration:Data,restartConfiguration:Data,
        presenting:UIViewController,googleServerClientID:String) async throws -> WithdrawalIOSActualTESTHostCandidate {
        try await prepareExplicit(policies:policies,invocationConfiguration:invocationConfiguration,
            proofProfileConfiguration:proofProfileConfiguration,ownerConfiguration:ownerConfiguration,
            sdkUIConfiguration:sdkUIConfiguration,nativeConfiguration:nativeConfiguration,
            cleanupConfiguration:cleanupConfiguration,restartConfiguration:restartConfiguration,
            actualContext:WithdrawalIOSActualTESTCompiledContract.loadContext(),presenting:presenting,
            googleServerClientID:googleServerClientID)
    }
    public static func prepareExplicit(policies:WithdrawalHTTPSCompositionReviewPolicies,
        invocationConfiguration:Data,proofProfileConfiguration:Data,ownerConfiguration:Data,
        sdkUIConfiguration:Data,nativeConfiguration:Data,cleanupConfiguration:Data,restartConfiguration:Data,
        actualContext:WithdrawalNativeActualTESTContext,presenting:UIViewController,
        googleServerClientID:String,preparationObserver:@MainActor (WithdrawalNativePreparationStage)->Void = {_ in}) async throws -> WithdrawalIOSActualTESTHostCandidate {
        preparationObserver(.platformPrerequisites)
        let policy=try WithdrawalNativeOwnerPolicy(json:ownerConfiguration)
        let osOwner=try WithdrawalNativeActualTESTOSOwnerCandidate(policy:policy,actualContext:actualContext,presenting:presenting)
        do {
            preparationObserver(.SDKAdapter)
            let uiPolicy=try WithdrawalNativeSDKUIPolicy(json:sdkUIConfiguration)
            let driver=try WithdrawalIOSSDKUIReviewCandidate(UIpolicy:uiPolicy,
                credentialPolicy:WithdrawalNativeReviewPolicy(json:nativeConfiguration,kakaoConfiguration:policies.kakao),
                cleanupPolicy:WithdrawalNativeSDKCleanupPolicy(json:cleanupConfiguration),presenting:presenting,
                googleServerClientID:googleServerClientID,actualContext:actualContext)
            let callback=try WithdrawalNativeSDKCallbackReview(policy:uiPolicy,driver:driver,
                deploymentContext:"actual_test_candidate",actualContext:actualContext)
            preparationObserver(.checkpointAdapter)
            let store=try WithdrawalLookupKeychainCandidate(policy:WithdrawalLookupRestartPolicy(json:restartConfiguration),actualContext:actualContext)
            guard let window=presenting.view.window,let scene=window.windowScene else {throw WithdrawalNativeReviewError.held}
            let host=try await WithdrawalNativeActualTESTHostCandidate.prepareExplicit(policies:policies,
                invocationConfiguration:invocationConfiguration,proofProfileConfiguration:proofProfileConfiguration,
                actualContext:actualContext,epoch:osOwner.epoch,vault:osOwner.vault,sdk:callback,store:store,
                authenticationGate:NativeAuthOperationGate.shared,
                checkOriginalPresentation:{ [weak presenting] in
                    guard let presenting,presenting.isViewLoaded,presenting.view.window === window,
                        window.windowScene === scene,scene.activationState == .foregroundActive,
                        UIApplication.shared.applicationState == .active,UIApplication.shared.isProtectedDataAvailable
                    else {throw WithdrawalNativeReviewError.held}
                },activeLoginSessionPresent:{
                    // Conservative presence test; no bearer leaves this native closure.
                    let request=WithdrawalNativeVaultRequest(policy:policy)
                    switch try osOwner.vault.copy(request) {case .missing:return false;case .found:return true}
                },preparationObserver:preparationObserver)
            return WithdrawalIOSActualTESTHostCandidate(host:host,osOwner:osOwner)
        } catch {osOwner.dispose();throw WithdrawalNativeReviewError.held}
    }
    public func dispose(){host.dispose();osOwner.dispose()}
}
#endif
