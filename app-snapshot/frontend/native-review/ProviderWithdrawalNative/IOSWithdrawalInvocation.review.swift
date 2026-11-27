// Candidate CAP adapter, compiled in App but not registered with its bridge.
// Source/key/OS/SDK composition remains pending. No default host or JS factory.
import Foundation
import Capacitor
import WebKit
import ProviderWithdrawalNativeReview

@objc(IOSWithdrawalInvocationReviewPlugin)
public final class IOSWithdrawalInvocationReviewPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IOSWithdrawalInvocationReviewPlugin"
    public let jsName = "IOSWithdrawalInvocationReview"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "withdrawExplicit", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "readOriginalStatusExplicit", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "dispose", returnType: CAPPluginReturnPromise)
    ]
    private let original: (any WithdrawalNativeInvocationPort)?
    private let documentFence:WithdrawalNativeOriginalDocumentFence?
    public override init() { original = nil;documentFence=nil; super.init() }
    @MainActor public init(originalHost: any WithdrawalNativeInvocationPort,originalDocumentFence:WithdrawalNativeOriginalDocumentFence? = nil) {
        original = originalHost;documentFence=originalDocumentFence; super.init()
    }
    deinit { original?.retireOriginalPresentation() }
    public override func shouldOverrideLoad(_ navigationAction: WKNavigationAction) -> NSNumber? {
        // Capacitor's ObjC override has no actor annotation. Read WebKit's
        // frame only on its main executor; an off-main callback is held.
        if Thread.isMainThread {
            let navigation = MainActor.assumeIsolated {(navigationAction.targetFrame?.isMainFrame == true,navigationAction.request.url)}
            if navigation.0 && (documentFence?.navigationIsTerminal(navigation.1) ?? true) { original?.retireOriginalPresentation() }
        } else { original?.retireOriginalPresentation() }
        // Keep Capacitor's original navigation policy; this only retires the
        // old invocation. A reload never reconstructs a withdrawal owner.
        return nil
    }
    private func accepts(_ call: CAPPluginCall) -> Bool {
        guard call.options.isEmpty else {
            call.reject("Native withdrawal options are unavailable.", "withdrawal_request_invalid"); return false
        }
        return true
    }
    private func run(_ call: CAPPluginCall, read: Bool) {
        guard accepts(call) else { return }
        Task { @MainActor [original] in
            guard let original else {
                call.reject("Native withdrawal is not ready.", "withdrawal_not_ready"); return
            }
            do {
                let result = try await read ? original.readOriginalStatusExplicit(options: Data("{}".utf8))
                    : original.withdrawExplicit(options: Data("{}".utf8))
                guard let value = try JSONSerialization.jsonObject(with: result.body) as? [String: Any] else {
                    throw WithdrawalNativeReviewError.held
                }
                guard original.mayPublishToOriginalPresentation(reply:result) else { return }
                call.resolve(value)
            } catch {
                // SDK/server errors and credentials never enter JS or logs.
                guard original.mayPublishToOriginalPresentation() else { return }
                call.reject("Native withdrawal result is unconfirmed.", "withdrawal_unconfirmed")
            }
        }
    }
    @objc public func withdrawExplicit(_ call: CAPPluginCall) { run(call, read: false) }
    @objc public func readOriginalStatusExplicit(_ call: CAPPluginCall) { run(call, read: true) }
    @objc public func dispose(_ call: CAPPluginCall) {
        guard accepts(call) else { return }
        Task { @MainActor [original] in original?.dispose(); call.resolve() }
    }
}
