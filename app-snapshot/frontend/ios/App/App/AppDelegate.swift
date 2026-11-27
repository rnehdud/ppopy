import UIKit
import Capacitor
import Security
import Vision
import ImageIO
import GoogleSignIn
import GTMAppAuth
import CryptoKit
import AuthenticationServices
import KakaoSDKCommon
import KakaoSDKUser
import KakaoSDKAuth
import ProviderWithdrawalNativeReview
import PublicAppTransportReview

#if SKINANALYSIS_PUBLIC_RUNTIME_BUILD && (SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW || SKINANALYSIS_WITHDRAWAL_REVIEW_SDK)
#error("Public and TEST native registration flags must be separate")
#endif

private let sessionVaultKey = "skinanalysis.app.session.v1"
private let sessionVaultService = "com.miraylab.poppy.session-vault"
private let sessionVaultNativeChanged = Notification.Name("com.miraylab.poppy.session-vault.native-changed.v1")
private let photoAccessKey = "skinanalysis.app.product-photo-test.v1"
private let photoAccessService = "com.miraylab.poppy.product-photo-access"

@objc(SkinAnalysisBridgeViewController)
public class SkinAnalysisBridgeViewController: CAPBridgeViewController {
    private var backEdgePanGesture: UIScreenEdgePanGestureRecognizer?
    #if SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
    private var withdrawalRegistrationCandidate:WithdrawalIOSActualTESTRegistrationCandidate?
    private var withdrawalClosedProbeStarted=false
    #endif

    #if DEBUG && SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
    public override func viewDidLoad() {
        // Even a restored storyboard must never start the member web runtime
        // in the explicit native-only read-only diagnostic process.
        if WithdrawalNativeReadOnlyConsoleViewController.requested { return }
        WithdrawalNativeReadOnlyConsoleViewController.webBootstrapStarted=true
        super.viewDidLoad()
    }
    #endif

    #if DEBUG && SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
    public override func viewDidAppear(_ animated:Bool) {
        super.viewDidAppear(animated)
        guard !withdrawalClosedProbeStarted,let owner=withdrawalRegistrationCandidate,let web=bridge?.webView else {return}
        withdrawalClosedProbeStarted=true
        WithdrawalIOSClosedBridgeProbe.start(view:self,web:web,owner:owner)
    }
    #endif

    override public func capacitorDidLoad() {
        #if DEBUG && SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
        if WithdrawalNativeReadOnlyConsoleViewController.requested { return }
        #endif
        #if SKINANALYSIS_PUBLIC_RUNTIME_BUILD
        // A public build must provide the signed-bundle resource and Info pin.
        // Missing binding stays unavailable; do not register TEST vault/HTTP.
        if let plugin = try? IOSPublicRuntimePlugin.bundled() {
            bridge?.registerPluginInstance(plugin)
            bridge?.registerPluginInstance(IOSGoogleSignInPlugin())
            bridge?.registerPluginInstance(IOSAppleSignInPlugin())
            bridge?.registerPluginInstance(IOSKakaoSignInPlugin())
        }
        #else
        bridge?.registerPluginInstance(IOSSessionVaultPlugin())
        bridge?.registerPluginInstance(IOSProductPhotoAccessPlugin())
        bridge?.registerPluginInstance(IOSProductPhotoSearchPlugin())
        bridge?.registerPluginInstance(IOSProductTextRecognizerPlugin())
        bridge?.registerPluginInstance(IOSCatalogSearchPlugin())
        bridge?.registerPluginInstance(IOSGoogleSignInPlugin())
        bridge?.registerPluginInstance(IOSAppleSignInPlugin())
        bridge?.registerPluginInstance(IOSKakaoSignInPlugin())
        #if SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
        do {
            let original=try WithdrawalIOSActualTESTRegistrationCandidate(presenting:self)
            withdrawalRegistrationCandidate=original
            bridge?.registerPluginInstance(original.plugin)
        } catch {
            // Closed TEST candidate remains unavailable; no retry or logs.
        }
        #endif

        #endif // public versus existing TEST registrations

        let gesture = UIScreenEdgePanGestureRecognizer(target: self, action: #selector(handleBackEdgePan(_:)))
        gesture.edges = .left
        gesture.cancelsTouchesInView = false
        view.addGestureRecognizer(gesture)
        backEdgePanGesture = gesture
    }

    @objc private func handleBackEdgePan(_ gesture: UIScreenEdgePanGestureRecognizer) {
        guard gesture.state == .ended else { return }
        let translation = gesture.translation(in: view)
        let velocity = gesture.velocity(in: view)
        guard translation.x >= 60, velocity.x > 0 else { return }
        bridge?.webView?.evaluateJavaScript("window.dispatchEvent(new Event('skinanalysis:native-back'))")
    }
}

@objc(IOSKakaoSignInPlugin)
public class IOSKakaoSignInPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IOSKakaoSignInPlugin"
    public let jsName = "IOSKakaoSignIn"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "signIn", returnType: CAPPluginReturnPromise),
    ]

    private var pendingCall: CAPPluginCall?
    private var pendingLease: NativeAuthOperationLease?

    @objc public func signIn(_ call: CAPPluginCall) {
        guard let configuredKey = Bundle.main.object(forInfoDictionaryKey: "KakaoNativeAppKey") as? String,
              configuredKey == "00000000000000000000000000000000" else {
            call.reject("Kakao native app configuration is unavailable.", "kakao_not_configured")
            return
        }
        DispatchQueue.main.async {
            guard self.pendingCall == nil, self.bridge?.viewController?.view.window != nil else {
                call.reject("Kakao sign-in is unavailable or already in progress.", "kakao_sign_in_unavailable")
                return
            }
            let lease: NativeAuthOperationLease
            do { lease = try NativeAuthOperationGate.shared.begin(.login) }
            catch { call.reject("Authentication is already in progress.", "authentication_busy"); return }
            self.pendingCall = call
            self.pendingLease = lease
            if UserApi.isKakaoTalkLoginAvailable() {
                UserApi.shared.loginWithKakaoTalk(launchMethod: .CustomScheme) { token, error in
                    self.complete(token?.accessToken, error: error, lease: lease)
                }
            } else {
                UserApi.shared.loginWithKakaoAccount { token, error in
                    self.complete(token?.accessToken, error: error, lease: lease)
                }
            }
        }
    }

    private func complete(_ accessToken: String?, error: Error?, lease: NativeAuthOperationLease) {
        DispatchQueue.main.async {
            guard self.pendingLease == lease, let call = self.pendingCall else { return }
            self.pendingCall = nil
            self.pendingLease = nil
            defer { NativeAuthOperationGate.shared.finish(lease) }
            do { try NativeAuthOperationGate.shared.check(lease) }
            catch { call.reject("Authentication session changed.", "authentication_ended"); return }
            guard error == nil, let accessToken, !accessToken.isEmpty else {
                call.reject("Kakao sign-in was not completed.", "kakao_sign_in_failed")
                return
            }
            // Only the opaque access token crosses the bridge. The server
            // validates it with Kakao and checks the exact application ID.
            call.resolve(["accessToken": accessToken])
        }
    }
}

#if SKINANALYSIS_PUBLIC_RUNTIME_BUILD
/// One pending native authorization delivery, with no network or storage.
private final class AppleAuthorizationForegroundDelivery {
    private var readiness: PublicBootstrapReadiness?
    private var observers: [NSObjectProtocol] = []
    private var expiry: DispatchWorkItem?
    private var completion: ((Bool) -> Void)?
    init(completion: @escaping (Bool) -> Void) { self.completion = completion }
    func start() {
        readiness = try? PublicBootstrapReadiness(started: ProcessInfo.processInfo.systemUptime, timeoutMilliseconds: 5000)
        for name in [UIApplication.didBecomeActiveNotification, UIApplication.protectedDataDidBecomeAvailableNotification] {
            observers.append(NotificationCenter.default.addObserver(forName: name, object: nil, queue: .main) { [weak self] _ in self?.observe() })
        }
        observers.append(NotificationCenter.default.addObserver(forName: UIApplication.didEnterBackgroundNotification, object: nil, queue: .main) { [weak self] _ in self?.finish(false) })
        let timeout = DispatchWorkItem { [weak self] in self?.finish(false) }
        expiry = timeout
        DispatchQueue.main.asyncAfter(deadline: .now() + 5, execute: timeout)
        observe()
    }
    private func observe() {
        guard completion != nil, var state = readiness else { finish(false); return }
        let result = state.observe(now: ProcessInfo.processInfo.systemUptime, localOrigin: true,
            active: UIApplication.shared.applicationState == .active, protectedData: UIApplication.shared.isProtectedDataAvailable)
        readiness = state
        if result == .ready { finish(true) }
        else if result == .rejected { finish(false) }
    }
    private func finish(_ ready: Bool) {
        guard let callback = completion else { return }
        completion = nil
        expiry?.cancel(); expiry = nil
        observers.forEach(NotificationCenter.default.removeObserver); observers.removeAll()
        callback(ready)
    }
    deinit { expiry?.cancel(); observers.forEach(NotificationCenter.default.removeObserver) }
}
#endif

@objc(IOSAppleSignInPlugin)
public class IOSAppleSignInPlugin: CAPPlugin, CAPBridgedPlugin,
    ASAuthorizationControllerDelegate, ASAuthorizationControllerPresentationContextProviding {
    public let identifier = "IOSAppleSignInPlugin"
    public let jsName = "IOSAppleSignIn"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "signIn", returnType: CAPPluginReturnPromise),
    ]

    private var pendingCall: CAPPluginCall?
    private var pendingController: ASAuthorizationController?
    #if SKINANALYSIS_PUBLIC_RUNTIME_BUILD
    private var foregroundDelivery: AppleAuthorizationForegroundDelivery?
    #endif
    private var pendingLease: NativeAuthOperationLease?

    @objc public func signIn(_ call: CAPPluginCall) {
        guard let nonce = call.getString("nonce"),
              nonce.range(of: #"^[A-Za-z0-9_-]{32,128}$"#, options: .regularExpression) != nil else {
            call.reject("A server-issued Apple nonce is required.", "invalid_apple_nonce")
            return
        }
        DispatchQueue.main.async {
            guard self.pendingCall == nil, self.bridge?.viewController?.view.window != nil else {
                call.reject("Apple sign-in is unavailable or already in progress.", "apple_sign_in_unavailable")
                return
            }
            let lease: NativeAuthOperationLease
            do { lease = try NativeAuthOperationGate.shared.begin(.login) }
            catch { call.reject("Authentication is already in progress.", "authentication_busy"); return }
            let request = ASAuthorizationAppleIDProvider().createRequest()
            request.nonce = nonce
            request.requestedScopes = []
            let controller = ASAuthorizationController(authorizationRequests: [request])
            controller.delegate = self
            controller.presentationContextProvider = self
            self.pendingCall = call
            self.pendingController = controller
            self.pendingLease = lease
            controller.performRequests()
        }
    }

    public func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor {
        return bridge?.viewController?.view.window ?? ASPresentationAnchor()
    }

    public func authorizationController(controller: ASAuthorizationController,
                                        didCompleteWithAuthorization authorization: ASAuthorization) {
        DispatchQueue.main.async { self.complete(controller, authorization: authorization) }
    }

    private func complete(_ controller: ASAuthorizationController, authorization: ASAuthorization) {
        guard controller === pendingController, let lease = pendingLease, let call = pendingCall else { return }
        pendingCall = nil
        pendingController = nil
        pendingLease = nil
        do { try NativeAuthOperationGate.shared.check(lease) }
        catch { NativeAuthOperationGate.shared.finish(lease); call.reject("Authentication session changed.", "authentication_ended"); return }
        guard let credential = authorization.credential as? ASAuthorizationAppleIDCredential,
              let data = credential.identityToken,
              let idToken = String(data: data, encoding: .utf8),
              !idToken.isEmpty else {
            NativeAuthOperationGate.shared.finish(lease)
            call.reject("Apple ID token is unavailable.", "apple_token_unavailable")
            return
        }
        // The opt-in original-login flow forwards a one-time code for server
        // validation/storage. It never persists a code or treats it as a session.
        if call.getBool("includeAuthorizationCode") == true {
            guard let rawCode = credential.authorizationCode,
                  let code = String(data: rawCode, encoding: .utf8),
                  (16...1024).contains(code.utf8.count),
                  code.range(of: #"\A[A-Za-z0-9._~+/=-]+\z"#, options: .regularExpression) != nil else {
                NativeAuthOperationGate.shared.finish(lease)
                call.reject("Apple authorization code is unavailable.", "apple_code_unavailable")
                return
            }
            deliverAuthorization(["idToken": idToken, "authorizationCode": code], call: call, lease: lease)
            return
        }
        // Existing TEST login retains its ID-token-only contract until the
        // matching server capture route is explicitly selected.
        deliverAuthorization(["idToken": idToken], call: call, lease: lease)
    }

    private func deliverAuthorization(_ payload: [String: String], call: CAPPluginCall, lease: NativeAuthOperationLease) {
        #if SKINANALYSIS_PUBLIC_RUNTIME_BUILD
        // The system authorization callback may precede didBecomeActive.
        // Keep this invocation/lease in memory until foreground admission;
        // never loosen the public HTTP guard or replay an HTTP request.
        let delivery = AppleAuthorizationForegroundDelivery { [weak self] ready in
            self?.foregroundDelivery = nil
            defer { NativeAuthOperationGate.shared.finish(lease) }
            guard ready else { call.reject("Apple authorization foreground was not confirmed.", "apple_foreground_unavailable"); return }
            do { try NativeAuthOperationGate.shared.check(lease) }
            catch { call.reject("Authentication session changed.", "authentication_ended"); return }
            call.resolve(payload)
        }
        foregroundDelivery = delivery
        delivery.start()
        #else
        defer { NativeAuthOperationGate.shared.finish(lease) }
        call.resolve(payload)
        #endif
    }

    public func authorizationController(controller: ASAuthorizationController,
                                        didCompleteWithError error: Error) {
        DispatchQueue.main.async { self.fail(controller) }
    }

    private func fail(_ controller: ASAuthorizationController) {
        guard controller === pendingController, let lease = pendingLease, let call = pendingCall else { return }
        pendingCall = nil
        pendingController = nil
        pendingLease = nil
        NativeAuthOperationGate.shared.finish(lease)
        call.reject("Apple sign-in was not completed.", "apple_sign_in_failed")
    }
}

@objc(IOSGoogleSignInPlugin)
public class IOSGoogleSignInPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IOSGoogleSignInPlugin"
    public let jsName = "IOSGoogleSignIn"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "signIn", returnType: CAPPluginReturnPromise),
    ]

    @objc public func signIn(_ call: CAPPluginCall) {
        guard let serverClientID = Bundle.main.object(forInfoDictionaryKey: "GIDServerClientID") as? String,
              !serverClientID.isEmpty,
              serverClientID.hasSuffix(".apps.googleusercontent.com"),
              let presenting = bridge?.viewController else {
            call.reject("Google server client configuration is unavailable.", "google_not_configured")
            return
        }
        DispatchQueue.main.async {
            let lease: NativeAuthOperationLease
            do { lease = try NativeAuthOperationGate.shared.begin(.login) }
            catch { call.reject("Authentication is already in progress.", "authentication_busy"); return }
            GIDSignIn.sharedInstance.signIn(withPresenting: presenting) { result, error in
                DispatchQueue.main.async {
                    do { try NativeAuthOperationGate.shared.check(lease) }
                    catch {
                        NativeAuthOperationGate.shared.finish(lease)
                        call.reject("Authentication session changed.", "authentication_ended"); return
                    }
                    guard error == nil, let result else {
                        NativeAuthOperationGate.shared.finish(lease)
                        call.reject("Google sign-in was not completed.", "google_sign_in_failed")
                        return
                    }
                    result.user.refreshTokensIfNeeded { user, refreshError in
                        DispatchQueue.main.async {
                            defer { NativeAuthOperationGate.shared.finish(lease) }
                            do { try NativeAuthOperationGate.shared.check(lease) }
                            catch { call.reject("Authentication session changed.", "authentication_ended"); return }
                            guard refreshError == nil,
                                  let user, user.userID != nil, user.userID == result.user.userID,
                                  let idToken = user.idToken?.tokenString,
                                  !idToken.isEmpty else {
                                call.reject("Google ID token is unavailable.", "google_token_unavailable")
                                return
                            }
                            if call.getBool("includeAuthorizationCode") == true {
                                guard GIDSignIn.sharedInstance.currentUser === result.user,
                                      let code = result.serverAuthCode,
                                      (16...1024).contains(code.utf8.count),
                                      code.range(of: #"\A[A-Za-z0-9._~+/=-]+\z"#, options: .regularExpression) != nil else {
                                    call.reject("Google authorization code is unavailable.", "google_code_unavailable")
                                    return
                                }
                                call.resolve(["idToken": idToken, "authorizationCode": code])
                                return
                            }
                            call.resolve(["idToken": idToken])
                        }
                    }
                }
            }
        }
    }
}

@objc(IOSCatalogSearchPlugin)
public class IOSCatalogSearchPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IOSCatalogSearchPlugin"
    public let jsName = "IOSCatalogSearch"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "search", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "cancel", returnType: CAPPluginReturnPromise),
    ]

    private let allowedBaseURL = "https://unconfigured.invalid"

    private let lock = NSLock()
    private var requests: [String: ProductPhotoRequest] = [:]

    @objc public func search(_ call: CAPPluginCall) {
        guard let raw = call.getString("query") else {
            call.reject("A product-name query is required.", "invalid_query")
            return
        }
        let query = raw.precomposedStringWithCompatibilityMapping
            .components(separatedBy: .whitespacesAndNewlines)
            .filter { !$0.isEmpty }
            .joined(separator: " ")
        let hasPhoneNumber = query.range(
            of: #"(?:\+?82[- ]?)?0\d{1,2}[- ]?\d{3,4}[- ]?\d{4}"#,
            options: .regularExpression
        ) != nil
        guard !query.isEmpty, query.count <= 200, !query.contains("@"), !hasPhoneNumber,
              let configuredBase = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisTestAPIBaseURL") as? String,
              configuredBase == allowedBaseURL,
              var components = URLComponents(string: configuredBase) else {
            call.reject("Only a product-name query to the fixed AWS TEST catalog is allowed.", "invalid_query")
            return
        }
        components.path = "/api/v1/products"
        components.queryItems = [URLQueryItem(name: "query", value: query)]
        guard let url = components.url, url.scheme == "https", url.host == "synthetic00.execute-api.ap-northeast-2.amazonaws.com" else {
            call.reject("The AWS TEST catalog endpoint is not allowed.", "invalid_endpoint")
            return
        }
        var request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData, timeoutInterval: 12)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        let id = call.getString("requestId") ?? UUID().uuidString
        guard UUID(uuidString: id) != nil else {
            call.reject("Invalid catalog request identifier.", "invalid_request_id"); return
        }
        let operation = ProductPhotoRequest(call: call, maximumBytes: 1_000_000, timeout: 12, kind: "catalog") { [weak self] in
            guard let self else { return }
            self.lock.lock(); self.requests.removeValue(forKey: id); self.lock.unlock()
        }
        lock.lock()
        guard requests[id] == nil else { lock.unlock(); call.reject("Catalog request already active.", "catalog_lookup_busy"); return }
        requests[id] = operation; lock.unlock(); operation.start(request)
    }

    @objc public func cancel(_ call: CAPPluginCall) {
        guard let id = call.getString("requestId"), UUID(uuidString: id) != nil else {
            call.reject("Invalid catalog request identifier.", "invalid_request_id"); return
        }
        lock.lock(); let operation = requests[id]; lock.unlock()
        operation?.cancel()
        // A native transport ACK is not a server/provider cancellation receipt.
        call.resolve()
    }
}

@objc(IOSProductTextRecognizerPlugin)
public class IOSProductTextRecognizerPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IOSProductTextRecognizerPlugin"
    public let jsName = "IOSProductTextRecognizer"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "recognize", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "prepare", returnType: CAPPluginReturnPromise),
    ]

    @objc public func prepare(_ call: CAPPluginCall) {
        guard let maxEdge = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoMaxEdge") as? Int,
              let maxBytes = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoMaxImageBytes") as? Int,
              maxEdge > 0, maxBytes > 0, let encoded = call.getString("imageBase64"), encoded.count <= 21_000_000,
              let data = Data(base64Encoded: encoded), data.count <= 15 * 1024 * 1024,
              let source = CGImageSourceCreateWithData(data as CFData, nil) else {
            call.reject("The product photo could not be prepared.", "invalid_image")
            return
        }
        DispatchQueue.global(qos: .userInitiated).async {
            // Downsample before decode and apply orientation, including HEIC.
            // Fresh RGB encoding does not copy EXIF/GPS/XMP.
            let options: [CFString: Any] = [
                kCGImageSourceCreateThumbnailFromImageAlways: true,
                kCGImageSourceCreateThumbnailWithTransform: true,
                kCGImageSourceThumbnailMaxPixelSize: maxEdge,
                kCGImageSourceShouldCacheImmediately: true,
            ]
            guard let thumbnail = CGImageSourceCreateThumbnailAtIndex(source, 0, options as CFDictionary) else {
                call.reject("The product photo could not be prepared.", "invalid_image")
                return
            }
            let size = CGSize(width: thumbnail.width, height: thumbnail.height)
            let format = UIGraphicsImageRendererFormat()
            format.scale = 1
            format.opaque = true
            let normalized = UIGraphicsImageRenderer(size: size, format: format).image { context in
                UIColor.white.setFill()
                context.fill(CGRect(origin: .zero, size: size))
                UIImage(cgImage: thumbnail).draw(in: CGRect(origin: .zero, size: size))
            }
            guard let jpeg = normalized.jpegData(compressionQuality: 0.82), jpeg.count <= maxBytes else {
                call.reject("The product photo is too large.", "invalid_image")
                return
            }
            call.resolve(["imageBase64": jpeg.base64EncodedString(), "width": thumbnail.width, "height": thumbnail.height])
        }
    }

    @objc public func recognize(_ call: CAPPluginCall) {
        guard let encoded = call.getString("imageBase64"), encoded.count <= 21_000_000,
              let data = Data(base64Encoded: encoded), data.count <= 15 * 1024 * 1024,
              let source = CGImageSourceCreateWithData(data as CFData, nil),
              let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
            call.reject("The product photo is invalid or too large.", "invalid_image")
            return
        }
        let properties = CGImageSourceCopyPropertiesAtIndex(source, 0, nil) as? [CFString: Any]
        let rawOrientation = (properties?[kCGImagePropertyOrientation] as? NSNumber)?.uint32Value ?? 1
        let orientation = CGImagePropertyOrientation(rawValue: rawOrientation) ?? .up
        DispatchQueue.global(qos: .userInitiated).async {
            let request = VNRecognizeTextRequest()
            request.recognitionLevel = .accurate
            request.usesLanguageCorrection = true
            request.recognitionLanguages = ["ko-KR", "en-US"]
            do {
                try VNImageRequestHandler(cgImage: image, orientation: orientation, options: [:]).perform([request])
                let lines = (request.results ?? [])
                    .compactMap { $0.topCandidates(1).first?.string.trimmingCharacters(in: .whitespacesAndNewlines) }
                    .filter { !$0.isEmpty }
                    .prefix(100)
                    .map { String($0.prefix(120)) }
                call.resolve(["lines": Array(lines)])
            } catch {
                call.reject("Text could not be recognized from the product photo.", "recognition_failed")
            }
        }
    }
}

// Local retirement only: never restore, refresh or disconnect a Google grant.
// The exact pinned GoogleSignIn 9.2.0 store is GTMAppAuth 5.0.0's `auth` item.
@MainActor private enum IOSGoogleSDKRetirement {
    static func verifier() throws -> GoogleSDKOwnerProofReview {
        #if SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
        let context = try WithdrawalIOSActualTESTCompiledContract.loadContext()
        let profile = try WithdrawalProofProfileReview(
            configuration: WithdrawalIOSActualTESTCompiledInputs.data("app_withdrawal_proof_profile_local"),
            publicKeyX963: context.publicKeyX963, expectedKeySHA256: context.sourcePin,
            isolatedKeySHA256: context.isolatedPin, restoreKeySHA256: context.restorePin,
            deploymentContext: "actual_test_candidate", actualContext: context)
        guard let client = Bundle.main.object(forInfoDictionaryKey: "GIDServerClientID") as? String,
              let bundle = Bundle.main.bundleIdentifier else { throw WithdrawalNativeReviewError.held }
        return try GoogleSDKOwnerProofReview(
            configuration: WithdrawalIOSActualTESTCompiledInputs.data("app_google_sdk_owner_local"),
            publicKeyX963: context.publicKeyX963, expectedKeySHA256: context.sourcePin,
            clientID: client, bundleIdentifier: bundle, deploymentContext: "actual_test_candidate", proofProfile: profile)
        #else
        throw WithdrawalNativeReviewError.held
        #endif
    }

    static func observe(maximumArchiveBytes: Int) throws -> GoogleSDKLocalObservation {
        guard let client = Bundle.main.object(forInfoDictionaryKey: "GIDClientID") as? String,
              let serverClient = Bundle.main.object(forInfoDictionaryKey: "GIDServerClientID") as? String else {
            throw WithdrawalNativeReviewError.held
        }
        let sdk = GIDSignIn.sharedInstance
        guard sdk.configuration?.clientID == client, sdk.configuration?.serverClientID == serverClient else {
            throw WithdrawalNativeReviewError.held
        }
        let memory = sdk.currentUser
        if let memory {
            guard memory.configuration.clientID == client, memory.configuration.serverClientID == serverClient,
                  memory.userID != nil else { throw WithdrawalNativeReviewError.held }
        }
        let store = KeychainStore(itemName: "auth")
        let archived: Data?
        do { archived = try store.keychainHelper.passwordData(forService: "auth") }
        catch KeychainStore.Error.passwordNotFound(let name) where name == "auth" { archived = nil }
        // Every other OS/decoding/lock error propagates; it cannot mean absence.
        let subject: String
        var fingerprint = Data()
        if let archived {
            guard !archived.isEmpty, archived.count <= maximumArchiveBytes else { throw WithdrawalNativeReviewError.held }
            let stored = try store.retrieveAuthSession()
            guard stored.authState.lastAuthorizationResponse.request.clientID == client,
                  let storedSubject = stored.userID, memory == nil || memory?.userID == storedSubject,
                  try store.keychainHelper.passwordData(forService: "auth") == archived else {
                throw WithdrawalNativeReviewError.held
            }
            subject = storedSubject
            fingerprint.append(contentsOf: SHA256.hash(data: archived))
        } else if let memorySubject = memory?.userID {
            subject = memorySubject
            fingerprint.append(contentsOf: SHA256.hash(data: Data("absent-persistent-item".utf8)))
        } else {
            guard sdk.currentUser == nil else { throw WithdrawalNativeReviewError.held }
            return .absent
        }
        guard sdk.currentUser === memory else { throw WithdrawalNativeReviewError.held }
        fingerprint.append(contentsOf: Data((memory.map { "memory:" + String(describing: ObjectIdentifier($0)) } ?? "memory:nil").utf8))
        return .present(try GoogleSDKLocalSnapshot(subject: subject,
            recordFingerprint: SHA256.hash(data: fingerprint).map { String(format: "%02x", $0) }.joined()))
    }

    static func remove(_ original: GoogleSDKLocalSnapshot, maximumArchiveBytes: Int) throws {
        guard try observe(maximumArchiveBytes: maximumArchiveBytes) == .present(original) else {
            throw WithdrawalNativeReviewError.held
        }
        // signOut is one local mutation and discards its OS delete error.
        // The caller independently observes real memory + persistent absence.
        GIDSignIn.sharedInstance.signOut()
    }
}

// Local SDK retirement only. Server admin unlink is a separate acknowledged job.
@MainActor private enum IOSKakaoSDKRetirement {
    static func verifier() throws -> KakaoSDKOwnerProofReview {
        #if SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
        let context = try WithdrawalIOSActualTESTCompiledContract.loadContext()
        let profile = try WithdrawalProofProfileReview(
            configuration: WithdrawalIOSActualTESTCompiledInputs.data("app_withdrawal_proof_profile_local"),
            publicKeyX963: context.publicKeyX963, expectedKeySHA256: context.sourcePin,
            isolatedKeySHA256: context.isolatedPin, restoreKeySHA256: context.restorePin,
            deploymentContext: "actual_test_candidate", actualContext: context)
        guard let login = try JSONSerialization.jsonObject(with: WithdrawalIOSActualTESTCompiledInputs.data("app_login_plan")) as? [String: Any],
              let kakao = login["kakao_login"] as? [String: Any], let appID = kakao["expected_app_id"] as? Int64,
              let bundle = Bundle.main.bundleIdentifier else { throw WithdrawalNativeReviewError.held }
        return try KakaoSDKOwnerProofReview(
            configuration: WithdrawalIOSActualTESTCompiledInputs.data("app_kakao_sdk_owner_local"),
            publicKeyX963: context.publicKeyX963, expectedKeySHA256: context.sourcePin,
            appID: appID, bundleIdentifier: bundle, deploymentContext: "actual_test_candidate", proofProfile: profile)
        #else
        throw WithdrawalNativeReviewError.held
        #endif
    }

    // Disabled in the shared preview. The original uses a locally modified SDK.
    static func observe(maximumArchiveBytes: Int) throws -> KakaoSDKLocalObservation {
        throw WithdrawalNativeReviewError.held
    }

    static func remove(_ original: KakaoSDKLocalSnapshot, maximumArchiveBytes: Int) throws {
        throw WithdrawalNativeReviewError.held
    }
}

// Public owner verification remains in PublicNativeSessionSlot. These adapters
// project only SDK observations; they never invoke the TEST proof verifiers.
// The host must supply an actual HTTP/auth lease invalidation/drain boundary.
// Construction alone performs no SDK or Keychain operation; not yet registered.
@MainActor enum IOSPublicSessionSDKAdapter {
    static func runtime(binding: PublicHTTPBinding, verifier: PublicSessionVerifier,
                        maximumArchiveBytes: Int) throws -> PublicNativeRuntime {
        try PublicNativeRuntime(binding: binding, verifier: verifier, store: PublicDataProtectionKeychain()) { invalidate in
            try ports(maximumArchiveBytes: maximumArchiveBytes, invalidateAndDrain: invalidate)
        }
    }
    private static func google(_ snapshot: GoogleSDKLocalSnapshot) throws -> PublicSDKSnapshot {
        try PublicSDKSnapshot(provider: .google, identity: snapshot.subject, recordFingerprint: snapshot.recordFingerprint)
    }
    private static func kakao(_ snapshot: KakaoSDKLocalSnapshot) throws -> PublicSDKSnapshot {
        try PublicSDKSnapshot(provider: .kakao, identity: snapshot.accessToken, recordFingerprint: snapshot.recordFingerprint)
    }
    static func ports(maximumArchiveBytes: Int, invalidateAndDrain: @escaping @MainActor () throws -> Void) throws -> PublicSessionSDKPorts {
        guard maximumArchiveBytes > 0, maximumArchiveBytes <= 65536 else { throw PublicSessionSlotError.unavailable }
        return PublicSessionSDKPorts(observe: { provider in
            switch provider {
            case .google:
                switch try IOSGoogleSDKRetirement.observe(maximumArchiveBytes: maximumArchiveBytes) {
                case .absent: return .absent
                case .unavailable: return .unavailable
                case .present(let snapshot): return .present(try google(snapshot))
                }
            case .kakao:
                switch try IOSKakaoSDKRetirement.observe(maximumArchiveBytes: maximumArchiveBytes) {
                case .absent: return .absent
                case .unavailable: return .unavailable
                case .present(let snapshot): return .present(try kakao(snapshot))
                }
            }
        }, removeExact: { provider, expected in
            // Re-observe both SDK memory and persistent record. Convert this
            // fresh snapshot for comparison, then let the original remover
            // compare it again immediately before its one local mutation.
            switch provider {
            case .google:
                guard case .present(let current) = try IOSGoogleSDKRetirement.observe(maximumArchiveBytes: maximumArchiveBytes),
                      try google(current) == expected else { throw PublicSessionSlotError.unavailable }
                try IOSGoogleSDKRetirement.remove(current, maximumArchiveBytes: maximumArchiveBytes)
            case .kakao:
                guard case .present(let current) = try IOSKakaoSDKRetirement.observe(maximumArchiveBytes: maximumArchiveBytes),
                      try kakao(current) == expected else { throw PublicSessionSlotError.unavailable }
                try IOSKakaoSDKRetirement.remove(current, maximumArchiveBytes: maximumArchiveBytes)
            }
        }, invalidate: invalidateAndDrain)
    }
}

// Registered only by an explicit future public build. No runtime JS URL/key
// selection, downloadable config or fallback to the existing TEST plugins.
@objc(IOSPublicRuntimePlugin)
final class IOSPublicRuntimePlugin: CAPPlugin, CAPBridgedPlugin {
    let identifier = "IOSPublicRuntimePlugin"
    let jsName = "PoppyPublicRuntime"
    let pluginMethods: [CAPPluginMethod] = ["bootstrap", "readSession", "compareAndSwapSession", "request", "cancel"].map {
        CAPPluginMethod(name: $0, returnType: CAPPluginReturnPromise)
    }
    private let runtime: PublicNativeRuntime, configuration: [String: Any]
    private let bootstrapTimeoutMilliseconds: Int
    private var bootstrapReadiness: PublicBootstrapReadiness?
    private var bootstrapCall: CAPPluginCall?
    private var bootstrapObservers: [NSObjectProtocol] = []
    private var bootstrapDeadline: DispatchWorkItem?
    private var activeRequest: String?
    @MainActor private init(runtime: PublicNativeRuntime, configuration: [String: Any], bootstrapTimeoutMilliseconds: Int) {
        self.runtime = runtime; self.configuration = configuration; self.bootstrapTimeoutMilliseconds = bootstrapTimeoutMilliseconds; super.init()
    }
    @MainActor static func bundled() throws -> IOSPublicRuntimePlugin {
        let bundle = Bundle.main
        guard let sha = bundle.object(forInfoDictionaryKey: "PoppyPublicRuntimeResourceSHA256") as? String,
              let client = bundle.object(forInfoDictionaryKey: "GIDServerClientID") as? String,
              let app = bundle.object(forInfoDictionaryKey: "PoppyPublicKakaoAppID") as? NSNumber,
              CFGetTypeID(app) != CFBooleanGetTypeID(), app.stringValue == String(app.int64Value),
              let identifier = bundle.bundleIdentifier,
              let url = bundle.url(forResource: "poppy-public-runtime", withExtension: "json"),
              let size = try url.resourceValues(forKeys: [.fileSizeKey]).fileSize, size <= 49152 else { throw PublicHTTPError.binding }
        let binding = try PublicNativeBundle(resource: Data(contentsOf: url), expectedSHA256: sha,
            bundleIdentifier: identifier, googleClientID: client, kakaoAppID: app.int64Value)
        let runtime = try IOSPublicSessionSDKAdapter.runtime(binding: binding.transport, verifier: binding.verifier, maximumArchiveBytes: binding.maximumArchiveBytes)
        return IOSPublicRuntimePlugin(runtime: runtime, configuration: binding.bootstrap,
            bootstrapTimeoutMilliseconds: binding.transport.requestDeadlineMilliseconds)
    }
    @MainActor private func accepts(_ call: CAPPluginCall, keys: Set<String>) -> Bool {
        guard Set(call.options.keys) == Set(keys.map { AnyHashable($0) }), UIApplication.shared.applicationState == .active,
              UIApplication.shared.isProtectedDataAvailable, let url = bridge?.webView?.url,
              url.scheme == "capacitor", url.host == "localhost", url.port == nil,
              url.user == nil, url.password == nil else { fail(call); return false }
        return true
    }
    private func fail(_ call: CAPPluginCall) { call.reject("The public operation result could not be confirmed.", "public_operation_unconfirmed") }
    @objc func bootstrap(_ call: CAPPluginCall) { DispatchQueue.main.async { self.bootstrapOnMain(call) } }
    @MainActor private func bootstrapOnMain(_ call: CAPPluginCall) {
        // WK can finish loading before the application's first activation.
        // Hold this one local bootstrap until active/unlocked; never replay it
        // or read session/SDK/HTTP while waiting. Other RPC admission is unchanged.
        guard call.options.isEmpty, bootstrapCall == nil, localBootstrapOrigin else { fail(call); return }
        do { bootstrapReadiness = try PublicBootstrapReadiness(started: ProcessInfo.processInfo.systemUptime,
            timeoutMilliseconds: bootstrapTimeoutMilliseconds) }
        catch { fail(call); return }
        bootstrapCall = call
        for name in [UIApplication.didBecomeActiveNotification, UIScene.didActivateNotification,
                     UIApplication.protectedDataDidBecomeAvailableNotification] {
            bootstrapObservers.append(NotificationCenter.default.addObserver(forName: name, object: nil, queue: .main) { [weak self] _ in
                DispatchQueue.main.async { self?.completeBootstrapIfReady() }
            })
        }
        bootstrapObservers.append(NotificationCenter.default.addObserver(forName: UIApplication.didEnterBackgroundNotification,
            object: nil, queue: .main) { [weak self] _ in DispatchQueue.main.async { self?.finishBootstrap(ready: false) } })
        let deadline = DispatchWorkItem { [weak self] in DispatchQueue.main.async { self?.finishBootstrap(ready: false) } }
        bootstrapDeadline = deadline
        DispatchQueue.main.asyncAfter(deadline: .now() + Double(bootstrapTimeoutMilliseconds) / 1000, execute: deadline)
        completeBootstrapIfReady()
    }
    @MainActor private var localBootstrapOrigin: Bool {
        guard let url = bridge?.webView?.url else { return false }
        return url.scheme == "capacitor" && url.host == "localhost" && url.port == nil && url.user == nil && url.password == nil
    }
    @MainActor private func completeBootstrapIfReady() {
        guard bootstrapCall != nil else { return }
        guard let state = bootstrapReadiness?.observe(now: ProcessInfo.processInfo.systemUptime,
            localOrigin: localBootstrapOrigin, active: UIApplication.shared.applicationState == .active,
            protectedData: UIApplication.shared.isProtectedDataAvailable) else { finishBootstrap(ready: false); return }
        switch state {
        case .ready: finishBootstrap(ready: true)
        case .rejected: finishBootstrap(ready: false)
        case .waiting: break
        }
    }
    @MainActor private func finishBootstrap(ready: Bool) {
        guard let call = bootstrapCall else { return }
        bootstrapCall = nil; bootstrapReadiness = nil; bootstrapDeadline?.cancel(); bootstrapDeadline = nil
        bootstrapObservers.forEach { NotificationCenter.default.removeObserver($0) }; bootstrapObservers.removeAll()
        if ready {
            guard accepts(call, keys: []) else { return }
            call.resolve(configuration)
        } else { call.reject("Public initialization readiness was not confirmed.", "public_bootstrap_unconfirmed") }
    }
    deinit {
        bootstrapDeadline?.cancel()
        bootstrapObservers.forEach { NotificationCenter.default.removeObserver($0) }
    }
    @objc func readSession(_ call: CAPPluginCall) { DispatchQueue.main.async { self.readOnMain(call) } }
    @MainActor private func readOnMain(_ call: CAPPluginCall) {
        guard accepts(call, keys: []) else { return }
        do {
            let value = try runtime.readSession()
            if let value { guard let text = String(data: value, encoding: .utf8) else { fail(call); return }; call.resolve(["value": text]) }
            else { call.resolve(["value": NSNull()]) }
        } catch { fail(call) }
    }
    @objc func compareAndSwapSession(_ call: CAPPluginCall) { DispatchQueue.main.async { self.swapOnMain(call) } }
    @MainActor private func swapOnMain(_ call: CAPPluginCall) {
        guard accepts(call, keys: ["expectedValue", "nextValue"]) else { return }
        func data(_ key: String) throws -> Data? {
            if call.options[key] is NSNull { return nil }
            guard let text = call.options[key] as? String, let bytes = text.data(using: .utf8), bytes.count <= 4096 else { throw PublicSessionSlotError.unavailable }
            return bytes
        }
        do { call.resolve(["changed": try runtime.compareAndSwapSession(expected: data("expectedValue"), replacement: data("nextValue"))]) }
        catch { fail(call) }
    }
    @objc func request(_ call: CAPPluginCall) { DispatchQueue.main.async { self.requestOnMain(call) } }
    @MainActor private func requestOnMain(_ call: CAPPluginCall) {
        guard accepts(call, keys: ["id", "url", "method", "headers", "body", "timeoutMilliseconds", "maximumResponseBytes"]) else { return }
        guard activeRequest == nil, let id = call.getString("id"), UUID(uuidString: id)?.uuidString.lowercased() == id,
              let url = call.getString("url"), let method = call.getString("method"), let headers = call.options["headers"] as? [String: String] else { fail(call); return }
        func integer(_ key: String) throws -> Int {
            guard let n = call.options[key] as? NSNumber, CFGetTypeID(n) != CFBooleanGetTypeID(), n.stringValue == String(n.intValue) else { throw PublicHTTPError.request }; return n.intValue
        }
        let body: String?
        if call.options["body"] is NSNull { body = nil }
        else if let text = call.options["body"] as? String { body = text }
        else { fail(call); return }
        do {
            let request = PublicHTTPRequest(url: url, method: method, headers: headers, body: body,
                timeoutMilliseconds: try integer("timeoutMilliseconds"), maximumResponseBytes: try integer("maximumResponseBytes"))
            activeRequest = id
            try runtime.send(request) { [weak self] result in
                guard let self else { call.reject("The public operation result could not be confirmed.", "public_operation_unconfirmed"); return }
                guard self.activeRequest == id else { return }; self.activeRequest = nil
                switch result {
                case .success(let response): call.resolve(["url": response.url, "status": response.status, "headers": response.headers, "body": response.body])
                case .failure: self.fail(call)
                }
            }
        } catch { activeRequest = nil; fail(call) }
    }
    @objc func cancel(_ call: CAPPluginCall) { DispatchQueue.main.async { self.cancelOnMain(call) } }
    @MainActor private func cancelOnMain(_ call: CAPPluginCall) {
        guard accepts(call, keys: ["id"]) else { return }
        guard let id = call.getString("id"), UUID(uuidString: id)?.uuidString.lowercased() == id else { fail(call); return }
        let matched = activeRequest == id
        if matched { runtime.cancelHTTP() }; call.resolve(["matched": matched])
    }
}

@objc(IOSSessionVaultPlugin)
public class IOSSessionVaultPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IOSSessionVaultPlugin"
    public let jsName = "IOSSessionVault"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "get", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "set", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "remove", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "removeIfValueMatches", returnType: CAPPluginReturnPromise),
    ]

    private func accepts(_ call: CAPPluginCall) -> Bool {
        guard call.getString("key") == sessionVaultKey else {
            call.reject("Only the app session credential key is allowed.", "invalid_key")
            return false
        }
        return true
    }

    private func query(returnData: Bool = false) -> [String: Any] {
        var value: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: sessionVaultService,
            kSecAttrAccount as String: sessionVaultKey,
            kSecAttrSynchronizable as String: kCFBooleanFalse as Any,
        ]
        if returnData {
            value[kSecReturnData as String] = kCFBooleanTrue
            value[kSecMatchLimit as String] = kSecMatchLimitOne
        }
        return value
    }

    @objc public func get(_ call: CAPPluginCall) {
        guard accepts(call) else { return }
        var result: CFTypeRef?
        let status = SecItemCopyMatching(query(returnData: true) as CFDictionary, &result)
        if status == errSecItemNotFound {
            call.resolve(["value": NSNull()])
            return
        }
        guard status == errSecSuccess,
              let data = result as? Data,
              let value = String(data: data, encoding: .utf8) else {
            call.reject("The session credential could not be read.", "keychain_read_failed")
            return
        }
        call.resolve(["value": value])
    }

    @objc public func set(_ call: CAPPluginCall) {
        DispatchQueue.main.async { self.setOnMain(call) }
    }

    @MainActor private func setOnMain(_ call: CAPPluginCall) {
        guard accepts(call), let value = call.getString("value") else {
            if call.getString("key") == sessionVaultKey {
                call.reject("A session credential value is required.", "invalid_value")
            }
            return
        }
        guard let data = value.data(using: .utf8), data.count <= 4096 else {
            call.reject("The session credential value is invalid.", "invalid_value")
            return
        }
        do {
            if try requiresGoogleRetirement(data) {
                _ = try IOSGoogleSDKRetirement.verifier().verifyVaultForRetirement(data, now: Date())
            }
            if try requiresKakaoRetirement(data) {
                _ = try IOSKakaoSDKRetirement.verifier().verifyVaultForRetirement(data, now: Date())
            }
        } catch {
            call.reject("The signed session ownership could not be verified.", "invalid_session_owner"); return
        }
        // Retire native owners before even an uncertain mutation can occur.
        NativeAuthOperationGate.shared.invalidate()
        NotificationCenter.default.post(name: sessionVaultNativeChanged, object: nil)
        let updateStatus = SecItemUpdate(
            query() as CFDictionary,
            [kSecValueData as String: data] as CFDictionary
        )
        if updateStatus == errSecSuccess {
            call.resolve()
            return
        }
        guard updateStatus == errSecItemNotFound else {
            call.reject("The session credential could not be updated.", "keychain_write_failed")
            return
        }
        var insert = query()
        insert[kSecValueData as String] = data
        insert[kSecAttrAccessible as String] = kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        guard SecItemAdd(insert as CFDictionary, nil) == errSecSuccess else {
            call.reject("The session credential could not be stored.", "keychain_write_failed")
            return
        }
        call.resolve()
    }

    @objc public func remove(_ call: CAPPluginCall) {
        DispatchQueue.main.async { self.removeOnMain(call) }
    }

    @MainActor private func removeOnMain(_ call: CAPPluginCall) {
        guard accepts(call) else { return }
        do {
            guard try removeExpected(readVault()) else { throw WithdrawalNativeReviewError.held }
            call.resolve()
        } catch {
            call.reject("The original session removal could not be confirmed.", "keychain_delete_unconfirmed")
        }
    }

    private func readVault() throws -> Data? {
        var result: CFTypeRef?
        let status = SecItemCopyMatching(query(returnData: true) as CFDictionary, &result)
        if status == errSecItemNotFound { return nil }
        guard status == errSecSuccess, let data = result as? Data, data.count <= 4096 else {
            throw WithdrawalNativeReviewError.held
        }
        return data
    }

    private func deleteVault() throws {
        let status = SecItemDelete(query() as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else { throw WithdrawalNativeReviewError.held }
    }

    private func requiresGoogleRetirement(_ data: Data) throws -> Bool {
        guard let value = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return false }
        return value["contract_version"] as? String == "1.1.0-google-sdk-owner-review"
    }

    private func requiresKakaoRetirement(_ data: Data) throws -> Bool {
        guard let value = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return false }
        return value["contract_version"] as? String == "1.2.0-kakao-sdk-owner-review"
    }

    @MainActor private func removeExpected(_ expected: Data?) throws -> Bool {
        if let expected, try requiresKakaoRetirement(expected) {
            let verifier = try IOSKakaoSDKRetirement.verifier()
            let gate = NativeAuthOperationGate.shared
            var lease: NativeAuthOperationLease? = try gate.begin(.withdrawal)
            defer { if let current = lease { gate.finish(current) } }
            func check() throws {
                guard let current = lease else { throw WithdrawalNativeReviewError.held }; try gate.check(current)
            }
            return try KakaoSDKConditionalRetirement.retire(expectedVault: expected, verifier: verifier, now: Date(),
                readVault: { try check(); return try self.readVault() },
                observeSDK: { try check(); return try IOSKakaoSDKRetirement.observe(maximumArchiveBytes: verifier.maximumSDKArchiveBytes) },
                invalidate: {
                    guard let original = lease else { return }; gate.invalidate()
                    NotificationCenter.default.post(name: sessionVaultNativeChanged, object: nil)
                    gate.finish(original); lease = try? gate.begin(.withdrawal)
                }, removeSDK: { original in
                    try check(); try IOSKakaoSDKRetirement.remove(original, maximumArchiveBytes: verifier.maximumSDKArchiveBytes)
                }, removeVault: { try check(); try self.deleteVault() })
        }
        if let expected, try requiresGoogleRetirement(expected) {
            let verifier = try IOSGoogleSDKRetirement.verifier()
            let gate = NativeAuthOperationGate.shared
            var lease: NativeAuthOperationLease? = try gate.begin(.withdrawal)
            defer { if let current = lease { gate.finish(current) } }
            func check() throws {
                guard let current = lease else { throw WithdrawalNativeReviewError.held }
                try gate.check(current)
            }
            return try GoogleSDKConditionalRetirement.retire(expectedVault: expected, verifier: verifier, now: Date(),
                readVault: { try check(); return try self.readVault() },
                observeSDK: { try check(); return try IOSGoogleSDKRetirement.observe(maximumArchiveBytes: verifier.maximumSDKArchiveBytes) },
                invalidate: {
                    guard let original = lease else { return }
                    gate.invalidate()
                    NotificationCenter.default.post(name: sessionVaultNativeChanged, object: nil)
                    // Invalidation keeps the SDK slot occupied until its owner drains.
                    gate.finish(original)
                    lease = try? gate.begin(.withdrawal)
                },
                removeSDK: { original in
                    try check(); try IOSGoogleSDKRetirement.remove(original, maximumArchiveBytes: verifier.maximumSDKArchiveBytes)
                }, removeVault: { try check(); try self.deleteVault() })
        }
        return try SessionVaultConditionalRemoval.removeIfValueMatches(expected: expected, maximumDataBytes: 4096,
            read: { try self.readVault() }, invalidate: {
                NativeAuthOperationGate.shared.invalidate()
                NotificationCenter.default.post(name: sessionVaultNativeChanged, object: nil)
            }, delete: { try self.deleteVault() })
    }

    @objc public func removeIfValueMatches(_ call: CAPPluginCall) {
        DispatchQueue.main.async { self.removeIfValueMatchesOnMain(call) }
    }

    @MainActor private func removeIfValueMatchesOnMain(_ call: CAPPluginCall) {
        guard accepts(call) else { return }
        guard Set(call.options.keys) == Set(["key", "expectedValue"]) else {
            call.reject("The conditional session removal contract is invalid.", "invalid_value"); return
        }
        let expected: Data?
        if call.options["expectedValue"] is NSNull { expected = nil }
        else if let value = call.options["expectedValue"] as? String,
                let data = value.data(using: .utf8), data.count <= 4096 { expected = data }
        else { call.reject("The original session value is invalid.", "invalid_value"); return }
        do {
            let removed = try removeExpected(expected)
            call.resolve(["removed": removed])
        } catch {
            call.reject("The original session removal could not be confirmed.", "keychain_delete_unconfirmed")
        }
    }
}

@objc(IOSProductPhotoAccessPlugin)
public class IOSProductPhotoAccessPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IOSProductPhotoAccessPlugin"
    public let jsName = "IOSProductPhotoAccess"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "status", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "get", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "set", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "remove", returnType: CAPPluginReturnPromise),
    ]
    private func accepts(_ call: CAPPluginCall) -> Bool {
        guard call.getString("key") == photoAccessKey else {
            call.reject("Only the private photo TEST credential key is allowed.", "invalid_key")
            return false
        }
        return true
    }
    private func query() -> [String: Any] {
        return [kSecClass as String: kSecClassGenericPassword,
                kSecAttrService as String: photoAccessService,
                kSecAttrAccount as String: photoAccessKey,
                kSecAttrSynchronizable as String: kCFBooleanFalse as Any]
    }
    // Presence only: never return the credential or its attributes to the UI.
    @objc public func status(_ call: CAPPluginCall) {
        guard accepts(call) else { return }
        var search = query()
        search[kSecMatchLimit as String] = kSecMatchLimitOne
        let status = SecItemCopyMatching(search as CFDictionary, nil)
        if status == errSecItemNotFound { call.resolve(["stored": false]); return }
        guard status == errSecSuccess else {
            call.reject("The TEST credential presence could not be checked.", "keychain_status_failed"); return
        }
        call.resolve(["stored": true])
    }
    @objc public func get(_ call: CAPPluginCall) {
        guard accepts(call) else { return }
        var search = query()
        search[kSecReturnData as String] = kCFBooleanTrue
        search[kSecMatchLimit as String] = kSecMatchLimitOne
        var result: CFTypeRef?
        let status = SecItemCopyMatching(search as CFDictionary, &result)
        if status == errSecItemNotFound { call.resolve(["value": NSNull()]); return }
        guard status == errSecSuccess, let data = result as? Data,
              let value = String(data: data, encoding: .utf8) else {
            call.reject("The TEST credential could not be read.", "keychain_read_failed"); return
        }
        call.resolve(["value": value])
    }
    @objc public func set(_ call: CAPPluginCall) {
        guard accepts(call) else { return }
        guard let value = call.getString("value"), !value.hasPrefix("sk-"),
              value.range(of: #"^[A-Za-z0-9_-]{32,128}$"#, options: .regularExpression) != nil,
              let data = value.data(using: .utf8) else {
            call.reject("A separate TEST photo access code is required.", "invalid_value"); return
        }
        let status = SecItemUpdate(query() as CFDictionary, [kSecValueData as String: data] as CFDictionary)
        if status == errSecSuccess { call.resolve(); return }
        guard status == errSecItemNotFound else {
            call.reject("The TEST credential could not be stored.", "keychain_write_failed"); return
        }
        var insert = query()
        insert[kSecValueData as String] = data
        insert[kSecAttrAccessible as String] = kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        guard SecItemAdd(insert as CFDictionary, nil) == errSecSuccess else {
            call.reject("The TEST credential could not be stored.", "keychain_write_failed"); return
        }
        call.resolve()
    }
    @objc public func remove(_ call: CAPPluginCall) {
        guard accepts(call) else { return }
        let status = SecItemDelete(query() as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            call.reject("The TEST credential could not be removed.", "keychain_delete_failed"); return
        }
        call.resolve()
    }
}


// Dedicated product-photo TEST transport. No arbitrary URL, headers, session or API key.
@objc(IOSProductPhotoSearchPlugin)
public class IOSProductPhotoSearchPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IOSProductPhotoSearchPlugin"
    public let jsName = "IOSProductPhotoSearch"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "search", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "searchWeb", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "prepare", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "cancel", returnType: CAPPluginReturnPromise),
    ]
    private var requests: [String: ProductPhotoRequest] = [:]
    private let lock = NSLock()

    @objc public func search(_ call: CAPPluginCall) {
        guard Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoTestEnabled") as? Bool == true,
              let base = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisTestAPIBaseURL") as? String,
              base == "https://unconfigured.invalid",
              let route = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoTestRoute") as? String,
              route == "/api/v1/products/test-photo-identity",
              let maxBytes = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoMaxImageBytes") as? Int,
              let maxResponse = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoMaxResponseBytes") as? Int,
              let timeout = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoTimeoutMilliseconds") as? Int,
              maxBytes > 0, maxResponse > 0, timeout > 0,
              let id = call.getString("requestId"), UUID(uuidString: id) != nil,
              call.getBool("productAreaConfirmed") == true,
              let encoded = call.getString("imageBase64"), encoded.utf8.count <= 4 * ((maxBytes + 2) / 3),
              let image = Data(base64Encoded: encoded), image.count >= 4, image.count <= maxBytes,
              image.prefix(2) == Data([0xff, 0xd8]), image.suffix(2) == Data([0xff, 0xd9]),
              let url = URL(string: base + route) else {
            call.reject("The product photo TEST request is unavailable or invalid.", "photo_test_unavailable"); return
        }
        let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: photoAccessService, kSecAttrAccount as String: photoAccessKey,
            kSecAttrSynchronizable as String: kCFBooleanFalse as Any,
            kSecReturnData as String: kCFBooleanTrue as Any, kSecMatchLimit as String: kSecMatchLimitOne]
        var result: CFTypeRef?
        guard SecItemCopyMatching(query as CFDictionary, &result) == errSecSuccess,
              let tokenData = result as? Data, let token = String(data: tokenData, encoding: .utf8),
              !token.hasPrefix("sk-"), token.range(of: #"^[A-Za-z0-9_-]{32,128}$"#, options: .regularExpression) != nil,
              let body = try? JSONSerialization.data(withJSONObject: ["image_base64": encoded, "product_area_confirmed": true]) else {
            call.reject("A separate product photo TEST credential is required.", "photo_test_access_required"); return
        }
        var request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData,
                                 timeoutInterval: Double(timeout) / 1000)
        request.httpMethod = "POST"
        request.httpBody = body
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue("Bearer " + token, forHTTPHeaderField: "Authorization")
        let operation = ProductPhotoRequest(call: call, maximumBytes: maxResponse, timeout: Double(timeout) / 1000) { [weak self] in
            guard let self else { return }
            self.lock.lock(); self.requests.removeValue(forKey: id); self.lock.unlock()
        }
        lock.lock()
        guard requests.isEmpty else { lock.unlock(); call.reject("A photo TEST request is already running.", "photo_test_busy"); return }
        requests[id] = operation
        lock.unlock()
        operation.start(request)
    }

    @objc public func searchWeb(_ call: CAPPluginCall) {
        guard Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductWebTestEnabled") as? Bool == true,
              let text = call.getString("productQuery"), !text.contains("\n"), !text.contains("\r") else {
            call.reject("Product web TEST is unavailable.", "web_test_unavailable"); return
        }
        let query = text.precomposedStringWithCompatibilityMapping.split(whereSeparator: { $0.isWhitespace }).joined(separator: " ")
        guard (2...200).contains(query.count), !query.contains("@"),
              query.range(of: #"(?:\+?82[- ]?)?0\d{1,2}[- ]?\d{3,4}[- ]?\d{4}"#, options: .regularExpression) == nil else {
            call.reject("Use a product name without contact information.", "web_test_input_invalid"); return
        }
        let ingredientMode = call.getString("purpose") == "ingredients"
        startOwnerRequest(call, payload: [ingredientMode ? "product_ingredient_query" : "product_query": query], kind: ingredientMode ? "ingredients" : "web")
    }

    @objc public func prepare(_ call: CAPPluginCall) {
        startOwnerRequest(call, payload: ["prepare_product_search": true], kind: "ready")
    }

    private func startOwnerRequest(_ call: CAPPluginCall, payload: [String: Any], kind: String) {
        guard Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoTestEnabled") as? Bool == true,
              let base = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisTestAPIBaseURL") as? String,
              base == "https://unconfigured.invalid",
              let route = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoTestRoute") as? String,
              route == "/api/v1/products/test-photo-identity",
              let maxResponse = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoMaxResponseBytes") as? Int,
              let timeout = Bundle.main.object(forInfoDictionaryKey: "SkinAnalysisProductPhotoTimeoutMilliseconds") as? Int,
              maxResponse > 0, timeout > 0,
              let id = call.getString("requestId"), UUID(uuidString: id) != nil,
              let url = URL(string: base + route) else {
            call.reject("Owner product TEST is unavailable.", "web_test_unavailable"); return
        }
        let credential: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: photoAccessService, kSecAttrAccount as String: photoAccessKey,
            kSecAttrSynchronizable as String: kCFBooleanFalse as Any,
            kSecReturnData as String: kCFBooleanTrue as Any, kSecMatchLimit as String: kSecMatchLimitOne]
        var result: CFTypeRef?
        guard SecItemCopyMatching(credential as CFDictionary, &result) == errSecSuccess,
              let tokenData = result as? Data, let token = String(data: tokenData, encoding: .utf8),
              !token.hasPrefix("sk-"), token.range(of: #"^[A-Za-z0-9_-]{32,128}$"#, options: .regularExpression) != nil,
              let body = try? JSONSerialization.data(withJSONObject: payload) else {
            call.reject("Private TEST credential required.", "photo_test_access_required"); return
        }
        var request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData,
                                 timeoutInterval: Double(timeout) / 1000)
        request.httpMethod = "POST"; request.httpBody = body
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue("Bearer " + token, forHTTPHeaderField: "Authorization")
        let operation = ProductPhotoRequest(call: call, maximumBytes: maxResponse, timeout: Double(timeout) / 1000, kind: kind) { [weak self] in
            guard let self else { return }
            self.lock.lock(); self.requests.removeValue(forKey: id); self.lock.unlock()
        }
        lock.lock()
        guard requests.isEmpty else { lock.unlock(); call.reject("Owner TEST request busy.", "photo_test_busy"); return }
        requests[id] = operation; lock.unlock(); operation.start(request)
    }

    @objc public func cancel(_ call: CAPPluginCall) {
        guard let id = call.getString("requestId"), UUID(uuidString: id) != nil else {
            call.reject("Invalid photo TEST request identifier.", "invalid_request_id"); return
        }
        lock.lock(); let operation = requests[id]; lock.unlock()
        operation?.cancel()
        call.resolve()
    }
}

private final class ProductPhotoRequest: NSObject, URLSessionDataDelegate {
    private let call: CAPPluginCall
    private let maximumBytes: Int
    private let kind: String
    private let timeout: Double
    private let completed: () -> Void
    private var bytes = Data()
    private var session: URLSession?
    private let lock = NSLock()
    private var finished = false

    init(call: CAPPluginCall, maximumBytes: Int, timeout: Double, kind: String = "photo", completed: @escaping () -> Void) {
        self.call = call; self.maximumBytes = maximumBytes; self.timeout = timeout; self.kind = kind; self.completed = completed
    }
    func start(_ request: URLRequest) {
        lock.lock()
        guard !finished else { lock.unlock(); return }
        let config = URLSessionConfiguration.ephemeral
        config.urlCache = nil; config.httpCookieStorage = nil; config.httpShouldSetCookies = false
        config.requestCachePolicy = .reloadIgnoringLocalAndRemoteCacheData
        config.timeoutIntervalForRequest = timeout; config.timeoutIntervalForResource = timeout
        config.waitsForConnectivity = false
        let value = URLSession(configuration: config, delegate: self, delegateQueue: nil)
        session = value
        let task = value.dataTask(with: request)
        lock.unlock()
        task.resume()
    }
    func cancel() { finish(nil, code: "photo_test_cancelled") }
    private func finish(_ payload: [String: Any]?, code: String) {
        lock.lock()
        guard !finished else { lock.unlock(); return }
        finished = true; let value = session; session = nil; bytes.removeAll(keepingCapacity: false)
        lock.unlock()
        value?.invalidateAndCancel(); completed()
        if let payload { call.resolve(payload) }
        else { call.reject("The product photo TEST request could not be completed.", code) }
    }
    func urlSession(_ session: URLSession, task: URLSessionTask,
                    willPerformHTTPRedirection response: HTTPURLResponse, newRequest request: URLRequest,
                    completionHandler: @escaping (URLRequest?) -> Void) {
        completionHandler(nil); finish(nil, code: "photo_test_redirect_denied")
    }
    func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive response: URLResponse,
                    completionHandler: @escaping (URLSession.ResponseDisposition) -> Void) {
        guard let http = response as? HTTPURLResponse else {
            completionHandler(.cancel); finish(nil, code: "photo_test_response_rejected"); return
        }
        if http.statusCode != 200 {
            let codes = [401: "photo_test_access_denied", 403: "photo_test_access_denied",
                         404: "photo_test_route_missing", 422: "photo_test_input_invalid",
                         429: "photo_test_limit", 502: "photo_test_provider_failure", 503: "photo_test_server_unavailable"]
            let diagnostic = http.value(forHTTPHeaderField: "X-SkinAnalysis-Photo-Code")
            let allowed = Set(["photo_test_database_warming", "photo_test_provider_configuration", "photo_test_provider_failure"])
            let code = http.statusCode == 503 && diagnostic.map({ allowed.contains($0) }) == true
                ? diagnostic! : (codes[http.statusCode] ?? "photo_test_response_rejected")
            completionHandler(.cancel); finish(nil, code: code); return
        }
        guard response.expectedContentLength <= Int64(maximumBytes) else {
            completionHandler(.cancel); finish(nil, code: "photo_test_response_too_large"); return
        }
        completionHandler(.allow)
    }
    func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive data: Data) {
        lock.lock()
        guard !finished else { lock.unlock(); return }
        guard bytes.count <= maximumBytes - data.count else {
            lock.unlock(); finish(nil, code: "photo_test_response_too_large"); return
        }
        bytes.append(data); lock.unlock()
    }
    func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
        lock.lock(); let data = bytes; let wasFinished = finished; lock.unlock()
        guard !wasFinished else { return }
        if let error {
            let code = (error as? URLError)?.code == .timedOut ? "photo_test_timeout" : "photo_test_network"
            finish(nil, code: code); return
        }
        guard let raw = try? JSONSerialization.jsonObject(with: data),
              let payload = raw as? [String: Any] else { finish(nil, code: "photo_test_identity_invalid"); return }
        if kind == "catalog" {
            guard payload["auto_confirmed"] as? Bool == false,
                  payload["candidates"] is [[String: Any]] else { finish(nil, code: "catalog_lookup_failed"); return }
            finish(payload, code: "")
        } else if kind == "ready" {
            guard Set(payload.keys) == Set(["ready"]), payload["ready"] as? Bool == true else { finish(nil, code: "photo_test_response_rejected"); return }
            finish(payload, code: "")
        } else if kind == "ingredients" {
            guard let drafts = checkedIngredientDrafts(payload) else { finish(nil, code: "web_test_response_invalid"); return }
            finish(drafts, code: "")
        } else if kind == "web" {
            guard let candidates = checkedProductWebCandidates(payload) else { finish(nil, code: "web_test_response_invalid"); return }
            finish(candidates, code: "")
        } else {
            guard let identity = checkedProductPhotoIdentity(payload) else { finish(nil, code: "photo_test_identity_invalid"); return }
            finish(identity, code: "")
        }
    }
}

// Unverified text only: never allow provider verification flags into the app.
private func checkedIngredientDrafts(_ payload: [String: Any]) -> [String: Any]? {
    guard Set(payload.keys) == Set(["provider", "auto_confirmed", "drafts"]),
          payload["provider"] as? String == "openai_responses", payload["auto_confirmed"] as? Bool == false,
          let drafts = payload["drafts"] as? [[String: Any]], drafts.count <= 2 else { return nil }
    let fields = Set(["product_name", "option", "source_url", "raw_ingredients", "version_note", "verification_status", "provenance_hash"])
    guard drafts.allSatisfy({ item in
        guard Set(item.keys) == fields, fields.allSatisfy({ item[$0] is String }),
              item["verification_status"] as? String == "review_required",
              let name = item["product_name"] as? String, !name.isEmpty, name.utf16.count <= 400,
              let option = item["option"] as? String, option.utf16.count <= 400,
              let note = item["version_note"] as? String, note.utf16.count <= 400,
              let raw = item["raw_ingredients"] as? String, !raw.isEmpty, raw.utf16.count <= 24000,
              let hash = item["provenance_hash"] as? String, hash.range(of: #"^[a-f0-9]{64}$"#, options: .regularExpression) != nil,
              let link = item["source_url"] as? String, link.utf16.count <= 4096,
              let url = URLComponents(string: link), url.scheme == "https", url.user == nil, url.password == nil,
              let host = url.host, !host.isEmpty else { return false }
        return true
    }) else { return nil }
    return payload
}

// Source-backed identity candidates only; never accept ingredient/automatic claims.
private func checkedProductWebCandidates(_ payload: [String: Any]) -> [String: Any]? {
    guard Set(payload.keys) == Set(["provider", "auto_confirmed", "candidates"]),
          payload["provider"] as? String == "openai_responses", payload["auto_confirmed"] as? Bool == false,
          let candidates = payload["candidates"] as? [[String: Any]], candidates.count <= 5 else { return nil }
    let fields = Set(["candidate_id", "title", "source_domain", "source_url", "snippet", "provenance_hash"])
    guard candidates.allSatisfy({ item in
        guard Set(item.keys) == fields, fields.allSatisfy({ item[$0] is String }),
              let title = item["title"] as? String, !title.isEmpty, title.utf16.count <= 360,
              let snippet = item["snippet"] as? String, snippet.utf16.count <= 480,
              let hash = item["provenance_hash"] as? String, hash.range(of: #"^[a-f0-9]{64}$"#, options: .regularExpression) != nil,
              let identifier = item["candidate_id"] as? String, identifier == String(hash.prefix(24)),
              let link = item["source_url"] as? String, link.utf16.count <= 4096,
              let url = URLComponents(string: link), url.scheme == "https", url.user == nil, url.password == nil,
              let host = url.host, !host.isEmpty, host.lowercased() == item["source_domain"] as? String else { return false }
        return true
    }) else { return nil }
    return payload
}

// Versioned server envelope -> identity-only app contract. Unknown fields stay rejected.
private func checkedProductPhotoIdentity(_ payload: [String: Any]) -> [String: Any]? {
    let fields = Set(["brand", "product_name", "variant", "volume", "needs_user_confirmation", "auto_confirmed"])
    let keys = Set(payload.keys)
    guard keys == fields || keys == fields.union(["schema_version"]) else { return nil }
    if keys.contains("schema_version") && payload["schema_version"] as? String != "2.0.0" { return nil }
    guard payload["needs_user_confirmation"] as? Bool == true,
          payload["auto_confirmed"] as? Bool == false,
          ["brand", "product_name", "variant", "volume"].allSatisfy({ key in
              payload[key] is NSNull || ((payload[key] as? String).map { $0.utf16.count <= 180 } ?? false)
          }) else { return nil }
    return payload.filter { fields.contains($0.key) }
}

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        #if DEBUG && SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
        WithdrawalIOSClosedBridgeProbe.installProviderDeadlineIfRequested()
        WithdrawalNativeReadOnlyConsoleViewController.installPreparationWatchdogIfRequested()
        // The separately admitted terminal store operation needs no provider
        // SDK startup. Ordinary launch and existing read-only probes retain
        // their current behavior.
        if ProcessInfo.processInfo.arguments.contains(WithdrawalNativeReadOnlyConsoleViewController.terminalCleanupArgument) {
            return true
        }
        #endif
        if let appKey = Bundle.main.object(forInfoDictionaryKey: "KakaoNativeAppKey") as? String,
           appKey == "00000000000000000000000000000000" {
            // Release compiler validation also checks SDK modules for DEBUG;
            // this flag alone does not suppress the SDK's Debug console path.
            KakaoSDK.initSDK(appKey: appKey, loggingEnable: false)
        }
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        NativeAuthOperationGate.shared.withdrawalWillResignActive()
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        NativeAuthOperationGate.shared.invalidateWithdrawal()
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        NativeAuthOperationGate.shared.invalidate()
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }

    func applicationProtectedDataWillBecomeUnavailable(_ application: UIApplication) {
        NativeAuthOperationGate.shared.invalidate()
    }

    func application(_ application: UIApplication,
                     configurationForConnecting connectingSceneSession: UISceneSession,
                     options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        let config = UISceneConfiguration(name: "Default Configuration",
                                          sessionRole: connectingSceneSession.role)
        config.delegateClass = SceneDelegate.self
        #if DEBUG && SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
        if WithdrawalNativeReadOnlyConsoleViewController.requested { config.storyboard=nil }
        #endif
        return config
    }
}
