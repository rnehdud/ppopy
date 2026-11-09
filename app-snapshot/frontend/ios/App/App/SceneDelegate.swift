import UIKit
import Capacitor
import GoogleSignIn
import KakaoSDKAuth
import ProviderWithdrawalNativeReview

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func sceneWillResignActive(_ scene: UIScene) { NativeAuthOperationGate.shared.withdrawalWillResignActive() }
    func sceneDidEnterBackground(_ scene: UIScene) { NativeAuthOperationGate.shared.invalidateWithdrawal() }
    func sceneDidDisconnect(_ scene: UIScene) { NativeAuthOperationGate.shared.invalidate() }

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }

        window = UIWindow(windowScene: windowScene)
        #if DEBUG && SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
        if WithdrawalNativeReadOnlyConsoleViewController.requested {
            WithdrawalNativeReadOnlyConsoleViewController.preparationStage("scene_connected")
            window?.rootViewController=WithdrawalNativeReadOnlyConsoleViewController()
            window?.makeKeyAndVisible()
            return
        }
        #endif
        // Use the subclass that registers the local OCR, Keychain, and bounded
        // AWS TEST catalog plugins. A plain CAPBridgeViewController silently
        // leaves those JavaScript bridges unimplemented.
        window?.rootViewController = SkinAnalysisBridgeViewController()
        window?.makeKeyAndVisible()

        SceneDelegateProxy.shared.scene(scene, willConnectTo: session, options: connectionOptions)
    }

    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        for context in URLContexts {
            if AuthApi.isKakaoTalkLoginUrl(context.url) {
                _ = AuthController.handleOpenUrl(url: context.url)
            } else {
                _ = GIDSignIn.sharedInstance.handle(context.url)
            }
        }
        SceneDelegateProxy.shared.scene(scene, openURLContexts: URLContexts)
    }

    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        SceneDelegateProxy.shared.scene(scene, continue: userActivity)
    }
}
