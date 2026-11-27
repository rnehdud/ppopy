#if canImport(UIKit)
import UIKit
import SwiftUI
import Foundation

private final class WithdrawalStatusHostNotifications: @unchecked Sendable {
    private let epoch:WithdrawalNativeOwnerEpoch,center:NotificationCenter,lock=NSLock()
    private var observers:[NSObjectProtocol]=[]
    init(epoch:WithdrawalNativeOwnerEpoch,scene:UIWindowScene,changedNotification:String) {
        self.epoch=epoch;center = .default
        let signals:[(Notification.Name,WithdrawalNativeOwnerSignal,AnyObject?)]=[
            (UIApplication.willResignActiveNotification,.inactive,nil),
            (UIApplication.didEnterBackgroundNotification,.background,nil),
            (UIApplication.protectedDataWillBecomeUnavailableNotification,.protectedDataUnavailable,nil),
            (UIApplication.significantTimeChangeNotification,.significantTimeChanged,nil),
            (UIScene.willDeactivateNotification,.inactive,scene),
            (UIScene.didEnterBackgroundNotification,.background,scene),
            (UIScene.didDisconnectNotification,.sceneDisconnected,scene),
            (Notification.Name(changedNotification),.sessionChanged,nil)]
        for(name,signal,object)in signals {
            observers.append(center.addObserver(forName:name,object:object,queue:nil){[epoch]_ in epoch.signal(signal)})
        }
    }
    func dispose() {
        epoch.signal(.disposed)
        let owned=lock.withLock {let result=observers;observers.removeAll();return result}
        for observer in owned {center.removeObserver(observer)}
    }
    deinit {dispose()}
}

// Explicit synthetic UIKit composition available in the App's existing local
// package. No CAP/JS plugin is registered and no OS credential port is created.
// The injected store/login state remain trusted synthetic ports, not real OS
// member attestation. Construction does not read the checkpoint or HTTP.
@MainActor public final class WithdrawalStatusUIKitReviewHost {
    private let host:WithdrawalStatusNativeHostReview,notifications:WithdrawalStatusHostNotifications
    private weak var presenting:UIViewController?
    private let window:UIWindow,scene:UIWindowScene
    private var screen:UIHostingController<WithdrawalLookupStatusScreenReview>?,presented=false,retired=false
    public init(configuration:Data,restartConfiguration:Data,statusConfiguration:Data,ownerConfiguration:Data,
        url:URL,publicKeyX963:Data,expectedKeySHA256:String,store:any WithdrawalLookupStorePort,
        deploymentContext:String,presenting:UIViewController,authenticationGate:NativeAuthOperationGate,
        activeLoginSessionPresent:@escaping ()throws->Bool) throws {
        _ = try WithdrawalStatusNativeHostPolicy(json:configuration)
        let ownerPolicy=try WithdrawalNativeOwnerPolicy(json:ownerConfiguration)
        try ownerRequire(deploymentContext == "synthetic_test")
        guard presenting.isViewLoaded,let window=presenting.view.window,let scene=window.windowScene,
            scene.activationState == .foregroundActive,UIApplication.shared.applicationState == .active,
            UIApplication.shared.isProtectedDataAvailable else {throw WithdrawalNativeReviewError.held}
        let epoch=try WithdrawalNativeOwnerEpoch(initiallyActive:true,protectedDataAvailable:true)
        host=try WithdrawalStatusNativeHostReview(configuration:configuration,restartConfiguration:restartConfiguration,
            statusConfiguration:statusConfiguration,url:url,publicKeyX963:publicKeyX963,expectedKeySHA256:expectedKeySHA256,
            store:store,deploymentContext:deploymentContext,lifetime:epoch,authenticationGate:authenticationGate,
            activeLoginSessionPresent:activeLoginSessionPresent)
        self.presenting=presenting;self.window=window;self.scene=scene
        notifications=WithdrawalStatusHostNotifications(epoch:epoch,scene:scene,changedNotification:ownerPolicy.changedNotification)
        if scene.activationState != .foregroundActive || UIApplication.shared.applicationState != .active
            || !UIApplication.shared.isProtectedDataAvailable {epoch.signal(.inactive)}
    }
    public func presentOriginalReviewExplicit() throws {
        guard !presented,!retired,let presenting,presenting.isViewLoaded,presenting.view.window === window,
            window.windowScene === scene,scene.activationState == .foregroundActive,
            UIApplication.shared.applicationState == .active,UIApplication.shared.isProtectedDataAvailable,
            presenting.presentedViewController == nil else {throw WithdrawalNativeReviewError.held}
        // A terminal original epoch cannot mount even after foreground/unlock.
        try host.checkOriginalPresentation()
        presented=true
        let state=WithdrawalLookupScreenState(reader:host,retireHost:{ [weak self] in self?.retireOriginalPresentation() })
        let screen=UIHostingController(rootView:WithdrawalLookupStatusScreenReview(state:state));self.screen=screen
        presenting.present(screen,animated:true)
    }
    private func retireOriginalPresentation() {
        guard !retired else {return}
        retired=true;host.dispose();notifications.dispose();screen=nil
    }
    public func dispose() {
        let originalScreen=screen
        retireOriginalPresentation()
        originalScreen?.dismiss(animated:false)
    }
}
#endif
