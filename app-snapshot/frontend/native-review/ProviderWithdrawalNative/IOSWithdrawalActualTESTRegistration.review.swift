#if SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
import Foundation
import UIKit
import ProviderWithdrawalNativeReview

private final class WithdrawalRegistrationNotifications:@unchecked Sendable {
    private let center=NotificationCenter.default,lock=NSLock()
    private var tokens:[NSObjectProtocol]=[]
    init(original:WithdrawalNativeLazyActualTESTInvocationCandidate,sessionChanged:String) {
        for name in [UIApplication.didEnterBackgroundNotification,UIApplication.protectedDataWillBecomeUnavailableNotification] {
            tokens.append(center.addObserver(forName:name,object:nil,queue:nil) {_ in original.suspendOriginalForBackground()})
        }
        for name in [UIApplication.significantTimeChangeNotification,Notification.Name(sessionChanged)] {
            tokens.append(center.addObserver(forName:name,object:nil,queue:nil) {_ in original.retireIfOriginalAccessStarted()})
        }
        // A disconnected scene/document is always a different presentation,
        // including before the first credential access.
        tokens.append(center.addObserver(forName:UIScene.didDisconnectNotification,object:nil,queue:nil) {_ in original.retireOriginalPresentation()})
    }
    func dispose(){let owned=lock.withLock {let copy=tokens;tokens=[];return copy};owned.forEach {center.removeObserver($0)}}
    deinit {dispose()}
}

// Closed TEST build registration owner. No eager vault, HTTP, SDK or status read.
@MainActor public final class WithdrawalIOSActualTESTRegistrationCandidate {
    public let plugin:IOSWithdrawalInvocationReviewPlugin
    private let invocation:WithdrawalNativeLazyActualTESTInvocationCandidate
    private let notifications:WithdrawalRegistrationNotifications
    private let preparationTrace:WithdrawalNativePreparationTrace
    public init(presenting:UIViewController)throws {
        let trace=WithdrawalNativePreparationTrace();preparationTrace=trace
        let context=try WithdrawalIOSActualTESTCompiledContract.loadContext()
        guard Bundle.main.bundleIdentifier==context.bundleIdentifier else {throw WithdrawalNativeReviewError.held}
        let data=WithdrawalIOSActualTESTCompiledInputs.data
        let policies=try WithdrawalHTTPSCompositionReviewPolicies(https:data("app_provider_withdrawal_https_review"),
            binding:data("app_provider_withdrawal_binding_local"),bindingHTTP:data("app_provider_withdrawal_binding_http_local"),
            owner:data("app_provider_withdrawal_native_owner_local"),native:data("app_provider_withdrawal_native_local"),
            closure:data("app_provider_withdrawal_http_local"),status:data("app_withdrawal_status_http_local"),
            restart:data("app_withdrawal_lookup_restart_local"),kakao:data("app_kakao_withdrawal_http_local"),
            durable:data("app_withdrawal_durable_native_wire_local"),originalSessionClosure:true)
        let original=try WithdrawalNativeLazyActualTESTInvocationCandidate(configuration:data("app_withdrawal_native_invocation_review"),
            actualContext:context,checkOriginalPresentation:{ [weak presenting] in
                guard let presenting,presenting.isViewLoaded,let scene=presenting.view.window?.windowScene,
                    scene.activationState == .foregroundActive,UIApplication.shared.applicationState == .active,
                    UIApplication.shared.isProtectedDataAvailable else {throw WithdrawalNativeReviewError.held}
            },prepareOriginalHost:{ [weak presenting] in
                guard let presenting,let client=Bundle.main.object(forInfoDictionaryKey:"GIDServerClientID") as? String else {throw WithdrawalNativeReviewError.held}
                return try await WithdrawalIOSActualTESTHostCandidate.prepareExplicit(policies:policies,
                    invocationConfiguration:data("app_withdrawal_native_invocation_review"),proofProfileConfiguration:data("app_withdrawal_proof_profile_local"),
                    ownerConfiguration:data("app_provider_withdrawal_native_owner_local"),sdkUIConfiguration:data("app_provider_withdrawal_sdk_ui_local"),
                    nativeConfiguration:data("app_provider_withdrawal_native_local"),cleanupConfiguration:data("app_provider_withdrawal_sdk_cleanup_local"),
                    restartConfiguration:data("app_withdrawal_lookup_restart_local"),actualContext:context,presenting:presenting,googleServerClientID:client,preparationObserver:{trace.mark($0)})
            },statusLifecycleConfiguration:data("app_withdrawal_status_lifecycle_local"))
        invocation=original;plugin=try IOSWithdrawalInvocationReviewPlugin(originalHost:original,
            originalDocumentFence:WithdrawalNativeOriginalDocumentFence(configuration:data("app_withdrawal_bridge_document_review")))
        let ownerData=try data("app_provider_withdrawal_native_owner_local")
        _ = try WithdrawalNativeOwnerPolicy(json:ownerData)
        guard let owner=try JSONSerialization.jsonObject(with:ownerData) as? [String:Any],
            let changed=owner["native_session_changed_notification"] as? String else {throw WithdrawalNativeReviewError.held}
        notifications=WithdrawalRegistrationNotifications(original:original,sessionChanged:changed)
    }
    // Invoked only by the explicit native process argument, never CAP/JS.
    public func prepareReadOnlyForConsole()async -> [String:Any] {
        var prepared=false
        do {try await invocation.prepareOriginalReadOnlyForConsole();prepared=true;preparationTrace.mark(.ready)} catch {}
        return ["prepared":prepared,"stage":preparationTrace.stage.rawValue,
            "host_preparation_count":invocation.preparationCount,"binding_read_attempts":preparationTrace.bindingReadAttempts,
            "original_presentation_live":invocation.mayPublishToOriginalPresentation()]
    }
    public func dispose(){invocation.dispose();notifications.dispose()}
    public var closedHostPreparationCount:Int {invocation.preparationCount}
    deinit {invocation.retireOriginalPresentation();notifications.dispose()}
}
#endif
