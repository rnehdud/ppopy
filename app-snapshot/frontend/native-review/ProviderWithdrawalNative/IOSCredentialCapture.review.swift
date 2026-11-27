// Unregistered callback adapter candidate; never starts SDK UI, signs out,
// touches Keychain, resolves a JS call, writes storage or calls a provider.
#if SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
import Foundation
import AuthenticationServices
import GoogleSignIn
import KakaoSDKAuth
import ProviderWithdrawalNativeReview

@MainActor public enum WithdrawalIOSCredentialCaptureReview {
    public static func apple(credential: ASAuthorizationAppleIDCredential,
        callbackController: ASAuthorizationController, expectedController: ASAuthorizationController,
        request: WithdrawalNativeCaptureRequest, policy: WithdrawalNativeReviewPolicy) throws -> WithdrawalNativeCredentials {
        try request.checkOriginalOperation()
        guard callbackController === expectedController, request.provider == .apple,
              let tokenData = credential.identityToken, let codeData = credential.authorizationCode,
              let token = String(data: tokenData, encoding: .utf8), let code = String(data: codeData, encoding: .utf8)
        else { throw WithdrawalNativeReviewError.unavailable }
        return try WithdrawalNativeCredentials(request: request, callbackOperationID: request.operationID,
            idToken: token, authorizationCode: code, capturedAt: Date(), policy: policy)
    }
    public static func google(result: GIDSignInResult, callbackOperationID: UUID,
        request: WithdrawalNativeCaptureRequest, policy: WithdrawalNativeReviewPolicy) throws -> WithdrawalNativeCredentials {
        try request.checkOriginalOperation()
        guard request.provider == .google else { throw WithdrawalNativeReviewError.unavailable }
        // Use this exact completed sign-in result. Refreshing another SDK user
        // would separate the ID token from its one-time server authorization code.
        return try WithdrawalNativeCredentials(request: request, callbackOperationID: callbackOperationID,
            idToken: result.user.idToken?.tokenString, authorizationCode: result.serverAuthCode,
            capturedAt: Date(), policy: policy)
    }
    public static func kakao(result: OAuthToken, callbackOperationID: UUID,
        request: WithdrawalNativeCaptureRequest, policy: WithdrawalNativeReviewPolicy) throws -> WithdrawalNativeCredentials {
        try request.checkOriginalOperation()
        guard request.provider == .kakao else { throw WithdrawalNativeReviewError.unavailable }
        // Capture only this completed callback. Do not read or refresh a
        // different SDK token owner or forward the credential to JavaScript.
        return try WithdrawalNativeCredentials(request:request,callbackOperationID:callbackOperationID,
            kakaoAccessToken:result.accessToken,capturedAt:Date(),policy:policy)
    }
}
#endif
