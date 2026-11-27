// Compile the SDK derivative candidate only in an explicit local review build.
// The clean pinned SDK build remains valid without this compilation condition.
#if SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
// Its accepted policy rejects construction before UIApplication/SDK access.
// No JS bridge, operating transport or app vault mutation. Accepted policies
// disable SDK UI and post-ACK memory signOut before SDK access or effects.
// Google SDK-managed sign-in persistence/egress remains separately unverified.
import Foundation
import UIKit
import AuthenticationServices
import GoogleSignIn
import KakaoSDKAuth
import KakaoSDKUser
import ProviderWithdrawalNativeReview

@MainActor public final class WithdrawalIOSSDKUIReviewCandidate: NSObject,
    WithdrawalNativeSDKCallbackDriverPort, ASAuthorizationControllerDelegate,
    ASAuthorizationControllerPresentationContextProviding, ASWebAuthenticationPresentationContextProviding,
    WithdrawalNativeSDKMemoryCleanupPort {
    private weak var presenting: UIViewController?
    private let window: UIWindow, scene: UIWindowScene, policy: WithdrawalNativeReviewPolicy, googleServerClientID: String
    private var pending: (request: WithdrawalNativeCaptureRequest,
        completion: @MainActor (UUID, WithdrawalNativeSDKCallbackOutcome) -> Void)?
    private var appleController: ASAuthorizationController?, used = false
    private let cleanupPolicy: WithdrawalNativeSDKCleanupPolicy
    private let actualContext: WithdrawalNativeActualTESTContext?
    private var originalGoogleResult: (request:WithdrawalNativeCaptureRequest,user:GIDGoogleUser)?
    private var originalKakaoPresentationContext: Any?
    private var originalKakaoResult: (request:WithdrawalNativeCaptureRequest,manager:TokenManager,snapshot:WithdrawalTokenSnapshot)?

    public init(UIpolicy: WithdrawalNativeSDKUIPolicy, credentialPolicy: WithdrawalNativeReviewPolicy,
                cleanupPolicy: WithdrawalNativeSDKCleanupPolicy, presenting: UIViewController, googleServerClientID: String,
                actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        guard UIpolicy.SDKUIEnabled || actualContext != nil else { throw WithdrawalNativeReviewError.held }
        if let actualContext {guard Bundle.main.bundleIdentifier == actualContext.bundleIdentifier else {throw WithdrawalNativeReviewError.held}}
        self.actualContext=actualContext
        guard presenting.isViewLoaded, let window = presenting.view.window, let scene = window.windowScene,
              scene.activationState == .foregroundActive, UIApplication.shared.applicationState == .active,
              UIApplication.shared.isProtectedDataAvailable
        else { throw WithdrawalNativeReviewError.held }
        self.presenting = presenting; self.window = window; self.scene = scene
        policy = credentialPolicy; self.googleServerClientID = googleServerClientID
        self.cleanupPolicy = cleanupPolicy
        super.init()
    }
    private func originalPresentation(_ request: WithdrawalNativeCaptureRequest) throws -> UIViewController {
        try request.checkOriginalOperation()
        guard let presenting, presenting.isViewLoaded, presenting.view.window === window, window.windowScene === scene,
              scene.activationState == .foregroundActive, UIApplication.shared.applicationState == .active,
              UIApplication.shared.isProtectedDataAvailable else { throw WithdrawalNativeReviewError.held }
        return presenting
    }
    public func startExplicit(_ request: WithdrawalNativeCaptureRequest,
        completion: @escaping @MainActor (UUID, WithdrawalNativeSDKCallbackOutcome) -> Void) throws {
        try actualContext?.requireSDKAuthenticationReady()
        guard !used, pending == nil else { throw WithdrawalNativeReviewError.busy }
        let presenting = try originalPresentation(request)
        switch request.provider {
        case .apple:
            guard let nonce = request.nonce else { throw WithdrawalNativeReviewError.held }
            let apple = ASAuthorizationAppleIDProvider().createRequest()
            apple.nonce = nonce; apple.requestedScopes = []
            let controller = ASAuthorizationController(authorizationRequests: [apple])
            controller.delegate = self; controller.presentationContextProvider = self
            used = true; pending = (request,completion); appleController = controller
            controller.performRequests()
        case .kakao:
            guard request.nonce == nil,
                  cleanupPolicy.kakaoTokenAdapterVersion == TokenManager.withdrawalTokenAdapterVersion,
                  TokenManager.authResponseOwnershipVersion == "1.0.0",
                  let tokenManager = Auth.shared.tokenManager as? TokenManager
            else { throw WithdrawalNativeReviewError.held }
            used = true; pending = (request,completion)
            let callbackID = request.operationID
            originalKakaoPresentationContext = AuthController.shared.presentationContextProvider
            AuthController.shared.presentationContextProvider = self
            // Explicit account authentication only. No additional scopes,
            // login hint, silent refresh, Talk fallback, unlink or signOut.
            // The SDK persists its own token before the callback. That state
            // is not an app-owned capture and is not an erasure receipt.
            UserApi.shared.loginWithKakaoAccount(prompts:[.Login],loginHint:nil,nonce:nil) { [weak self] result, error in
                Task { @MainActor in
                    guard let self, let p = self.pending, p.request.operationID == callbackID else { return }
                    let ownsContext = (AuthController.shared.presentationContextProvider as? WithdrawalIOSSDKUIReviewCandidate) === self
                    // Restore only the context installed by this operation.
                    // A foreign SDK context is never overwritten on return.
                    if ownsContext {AuthController.shared.presentationContextProvider = self.originalKakaoPresentationContext}
                    self.originalKakaoPresentationContext = nil
                    self.pending = nil
                    do {
                        _ = try self.originalPresentation(p.request)
                        guard ownsContext, error == nil, let result,
                              let currentManager = Auth.shared.tokenManager as? TokenManager,
                              currentManager === tokenManager,
                              let snapshot = currentManager.captureOriginalWithdrawalToken(expected:result,operationID:callbackID)
                        else { throw WithdrawalNativeReviewError.held }
                        let value = try WithdrawalIOSCredentialCaptureReview.kakao(result:result,
                            callbackOperationID:callbackID,request:p.request,policy:self.policy)
                        self.originalKakaoResult = (p.request,currentManager,snapshot)
                        p.completion(callbackID,.captured(value))
                    } catch { p.completion(callbackID,.failed) }
                }
            }
        case .google:
            guard request.nonce == nil,
                  let configuredID = Bundle.main.object(forInfoDictionaryKey: "GIDServerClientID") as? String,
                  configuredID == googleServerClientID, configuredID.hasSuffix(".apps.googleusercontent.com"),
                  GIDSignIn.sharedInstance.configuration?.serverClientID == googleServerClientID
            else { throw WithdrawalNativeReviewError.held }
            used = true; pending = (request,completion)
            let callbackID = request.operationID
            // No additional scopes, SDK-user refresh, silent authentication or
            // fallback. Token and serverAuthCode come from this exact result.
            GIDSignIn.sharedInstance.signIn(withPresenting: presenting) { [weak self] result, error in
                Task { @MainActor in
                    guard let self, let p = self.pending, p.request.operationID == callbackID else { return }
                    self.pending = nil
                    do {
                        _ = try self.originalPresentation(p.request)
                        guard error == nil, let result else { throw WithdrawalNativeReviewError.held }
                        let value = try WithdrawalIOSCredentialCaptureReview.google(result: result,
                            callbackOperationID: p.request.operationID, request: p.request, policy: self.policy)
                        self.originalGoogleResult = (p.request,result.user)
                        p.completion(p.request.operationID,.captured(value))
                    } catch { p.completion(p.request.operationID,.failed) }
                }
            }
        }
    }
    public func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor {
        guard controller === appleController, let p = pending, (try? originalPresentation(p.request)) != nil else { return ASPresentationAnchor() }
        return window
    }
    public func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
        guard session === AuthController.shared.authenticationSession,
              (AuthController.shared.presentationContextProvider as? WithdrawalIOSSDKUIReviewCandidate) === self,
              let p = pending, p.request.provider == .kakao,
              (try? originalPresentation(p.request)) != nil else { return ASPresentationAnchor() }
        return window
    }
    public func authorizationController(controller: ASAuthorizationController, didCompleteWithAuthorization authorization: ASAuthorization) {
        guard controller === appleController, let p = pending else { return }
        pending = nil; appleController = nil
        do {
            _ = try originalPresentation(p.request)
            guard let credential = authorization.credential as? ASAuthorizationAppleIDCredential else { throw WithdrawalNativeReviewError.held }
            let value = try WithdrawalIOSCredentialCaptureReview.apple(credential:credential,
                callbackController:controller, expectedController:controller, request:p.request, policy:policy)
            p.completion(p.request.operationID,.captured(value))
        } catch { p.completion(p.request.operationID,.failed) }
    }
    public func authorizationController(controller: ASAuthorizationController, didCompleteWithError error: Error) {
        guard controller === appleController, let p = pending else { return }
        pending = nil; appleController = nil
        p.completion(p.request.operationID,.failed)
    }
    public func clearOriginalAfterVerifiedACK(_ grant:WithdrawalNativeSDKCleanupGrant) throws -> WithdrawalNativeSDKMemoryCleanupObservation {
        // Accepted policy is OFF. No SDK state access or effect occurs here.
        guard cleanupPolicy.SDKCleanupEnabled else {throw WithdrawalNativeReviewError.held}
        if grant.provider == .kakao {
            guard cleanupPolicy.kakaoTokenAdapterVersion == TokenManager.withdrawalTokenAdapterVersion,
                  let originalKakaoResult, originalKakaoResult.request.operationID == grant.operationID
            else { return .unavailable }
            // Retire this capture before validation/effects. An uncertain
            // cleanup is not a new reauthentication or retry permission.
            self.originalKakaoResult = nil
            try grant.consumeOriginal()
            _ = try originalPresentation(originalKakaoResult.request)
            guard let currentManager = Auth.shared.tokenManager as? TokenManager,
                  currentManager === originalKakaoResult.manager else {throw WithdrawalNativeReviewError.held}
            return currentManager.deleteOriginalWithdrawalToken(originalKakaoResult.snapshot,operationID:grant.operationID)
                ? .memoryCleared : .unavailable
        }
        guard grant.provider == .google, let originalGoogleResult,
              originalGoogleResult.request.operationID == grant.operationID else {return .unavailable}
        try grant.consumeOriginal()
        _ = try originalPresentation(originalGoogleResult.request)
        guard GIDSignIn.sharedInstance.currentUser === originalGoogleResult.user else {throw WithdrawalNativeReviewError.held}
        self.originalGoogleResult = nil
        // The server already acknowledged this original revoke. disconnect
        // would send another provider request. signOut returns no storage ACK;
        // currentUser nil proves only the SDK's present memory observation.
        GIDSignIn.sharedInstance.signOut()
        return GIDSignIn.sharedInstance.currentUser == nil ? .memoryCleared : .unavailable
    }
}
#endif
