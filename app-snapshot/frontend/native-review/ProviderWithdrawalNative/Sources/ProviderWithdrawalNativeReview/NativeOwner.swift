import Foundation

func ownerRequire(_ value: Bool) throws {
    if !value { throw WithdrawalNativeReviewError.held }
}
func ownerMatches(_ value: String, _ pattern: String) -> Bool {
    guard let range = value.range(of: pattern, options: .regularExpression) else { return false }
    return range.lowerBound == value.startIndex && range.upperBound == value.endIndex
}
public struct WithdrawalNativeOwnerPolicy: Sendable {
    let observersEnabled: Bool, credentialAccessEnabled: Bool
    let service: String, account: String, version: String, accessibility: String, changedNotification: String
    let vaultBytes: Int, bearerBytes: Int, SDKPresentationSeconds: TimeInterval
    public init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        let expected: [String: Any] = ["version":"1.0.1","scope":"isolated_local_review",
            "runtime_registered":false,"observer_registration_enabled":false,"operating_credential_access_authorized":false,
            "operating_member_transport_authorized":false,"actual_OS_member_attestation":false,
            "vault_service":"com.miraylab.poppy.session-vault","vault_account":"skinanalysis.app.session.v1",
            "vault_version":"1.0.0-app-draft","vault_accessibility":"when_unlocked_this_device_only",
            "maximum_vault_bytes":4096,"maximum_bearer_bytes":200,"maximum_sdk_presentation_seconds":300,"vault_writes":false,
            "native_session_changed_notification":"com.miraylab.poppy.session-vault.native-changed.v1",
            "identity":"original_server_bound_account_and_provider_never_vault_or_JS_claim",
            "lifetime":"original_reserved_SDK_inactive_only_active_return_before_callback_other_signals_terminal",
            "failure":"retire_original_owner_no_automatic_retry",
            "shared_authentication":"login_and_withdrawal_slot_retained_until_original_SDK_callback_drains"]
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
        observersEnabled = raw["observer_registration_enabled"] as! Bool
        credentialAccessEnabled = raw["operating_credential_access_authorized"] as! Bool
        service = raw["vault_service"] as! String; account = raw["vault_account"] as! String
        version = raw["vault_version"] as! String; accessibility = raw["vault_accessibility"] as! String
        changedNotification = raw["native_session_changed_notification"] as! String
        vaultBytes = (raw["maximum_vault_bytes"] as! NSNumber).intValue
        bearerBytes = (raw["maximum_bearer_bytes"] as! NSNumber).intValue
        SDKPresentationSeconds = (raw["maximum_sdk_presentation_seconds"] as! NSNumber).doubleValue
    }
}

public enum WithdrawalNativeOwnerSignal: Sendable {
    case inactive, background, protectedDataUnavailable, sessionChanged, sceneDisconnected, disposed
    case foreground, protectedDataAvailable, significantTimeChanged
}
struct WithdrawalNativeEpochSnapshot { let generation: UUID, now: Date }

// Invalidation is synchronous even for an off-main notification. Foreground
// and unlock never resurrect an old epoch. Real OS registration stays OFF.
public final class WithdrawalNativeOwnerEpoch: @unchecked Sendable {
    private let lock = NSLock(), clock: @Sendable () -> Date
    private var generation = UUID(), live = true, active = true, lastTime: Date
    private var SDKPresentation: (operation: UUID, expires: Date)?
    public init(initiallyActive: Bool, protectedDataAvailable: Bool, clock: @escaping @Sendable () -> Date = { Date() }) throws {
        let now = clock()
        try ownerRequire(initiallyActive && protectedDataAvailable && now.timeIntervalSince1970.isFinite)
        self.clock = clock; lastTime = now
    }
    private func snapshotLocked() throws -> WithdrawalNativeEpochSnapshot {
        try ownerRequire(live)
        let now = clock()
        guard now.timeIntervalSince1970.isFinite && now >= lastTime else {
            live = false; generation = UUID(); throw WithdrawalNativeReviewError.held
        }
        lastTime = now; return WithdrawalNativeEpochSnapshot(generation: generation, now: now)
    }
    func snapshot() throws -> WithdrawalNativeEpochSnapshot {
        try lock.withLock { let value = try snapshotLocked(); try ownerRequire(active); return value }
    }
    // Readback is separately bounded by the original signed lookup. Retiring a
    // closure owner must not disable that read-only clock. Scene/auth/vault
    // fences are checked by the readback owner before and after every await.
    func originalReadbackTime() throws -> Date {
        try lock.withLock {
            let now = clock()
            try ownerRequire(now.timeIntervalSince1970.isFinite && now >= lastTime)
            lastTime = now; return now
        }
    }
    func beginSDKPresentation(_ operation: UUID, maximumSeconds: TimeInterval) throws {
        try lock.withLock {
            let now = try snapshotLocked().now
            try ownerRequire(active && SDKPresentation == nil && maximumSeconds.isFinite && maximumSeconds > 0)
            SDKPresentation = (operation, now.addingTimeInterval(maximumSeconds))
        }
    }
    func endSDKPresentation(_ operation: UUID) {
        lock.withLock {
            guard let current = SDKPresentation, current.operation == operation else { return }
            SDKPresentation = nil
            guard let now = try? snapshotLocked().now, active, now < current.expires else {
                live = false; generation = UUID(); return
            }
        }
    }
    public func signal(_ signal: WithdrawalNativeOwnerSignal) {
        lock.withLock {
            switch signal {
            case .foreground:
                // Does not revive a terminal epoch. Only the same reserved,
                // bounded SDK call may return from transient inactivity.
                if live, let current = SDKPresentation,
                   let now = try? snapshotLocked().now, now < current.expires { active = true }
            case .protectedDataAvailable: break
            case .inactive:
                if live, let current = SDKPresentation,
                   let now = try? snapshotLocked().now, now < current.expires { active = false }
                else { live = false; generation = UUID() }
            case .significantTimeChanged: _ = try? snapshotLocked()
            default: live = false; generation = UUID()
            }
        }
    }
}
// Internal capability: a JS argument, arbitrary port or SDK driver cannot
// grant lifecycle tolerance. Only a verified original native owner supplies it.
@MainActor protocol WithdrawalNativeSDKPresentationOwnerPort: WithdrawalNativeSessionPort {
    func beginSDKPresentation(_ operation: UUID) throws
    func endSDKPresentation(_ operation: UUID)
}
public struct WithdrawalNativeVaultRequest: Sendable, Equatable {
    public let service: String, account: String, maximumDataBytes: Int
    public let returnData = true, returnAttributes = true, authenticationUIAllowed = false, matchOne = true
    public init(policy: WithdrawalNativeOwnerPolicy) { service = policy.service; account = policy.account; maximumDataBytes = policy.vaultBytes }
}
public enum WithdrawalNativeVaultResult {
    case missing
    case found(data: Data, service: String, account: String, accessibility: String, synchronizable: Bool)
}
@MainActor public protocol WithdrawalNativeVaultReadPort: AnyObject {
    func copy(_ request: WithdrawalNativeVaultRequest) throws -> WithdrawalNativeVaultResult
}

struct WithdrawalVaultCredential {
    let bearer: String, expiresAt: Date
}
func withdrawalUTCDate(_ value: String) throws -> Date {
    try ownerRequire(ownerMatches(value, "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\\.[0-9]{1,6})?(?:Z|\\+00:00)$"))
    let formatter = ISO8601DateFormatter()
    formatter.formatOptions = value.contains(".") ? [.withInternetDateTime, .withFractionalSeconds] : [.withInternetDateTime]
    guard let result = formatter.date(from: value) else { throw WithdrawalNativeReviewError.held }
    return result
}
@MainActor func withdrawalReadVault(_ vault: any WithdrawalNativeVaultReadPort, policy: WithdrawalNativeOwnerPolicy) throws -> WithdrawalVaultCredential {
    let result = try vault.copy(WithdrawalNativeVaultRequest(policy: policy))
    guard case let .found(data, service, account, accessibility, synchronizable) = result else { throw WithdrawalNativeReviewError.held }
    try ownerRequire(service == policy.service && account == policy.account && accessibility == policy.accessibility && !synchronizable)
    let raw = try withdrawalFlatObject(data, maximumBytes: policy.vaultBytes)
    try ownerRequire(Set(raw.keys) == ["contract_version", "session_token", "expires_at"] && raw["contract_version"] as? String == policy.version)
    guard let bearer = raw["session_token"] as? String, let expiry = raw["expires_at"] as? String else { throw WithdrawalNativeReviewError.held }
    try ownerRequire(bearer.utf8.count <= policy.bearerBytes && ownerMatches(bearer, "^[A-Za-z0-9_-]{32,200}$"))
    return WithdrawalVaultCredential(bearer: bearer, expiresAt: try withdrawalUTCDate(expiry))
}

// Reads the real app's three-field JSON format, not an imagined raw bearer.
// Binding is still a synthetic trusted server input in this review. No public
// API/JS blob can establish an operating account/provider identity here.
@MainActor public final class WithdrawalNativeVaultSession: WithdrawalNativeSessionPort, WithdrawalNativeSDKPresentationOwnerPort {
    private let policy: WithdrawalNativeOwnerPolicy, epoch: WithdrawalNativeOwnerEpoch
    private let vault: any WithdrawalNativeVaultReadPort, binding: WithdrawalNativeSession
    private let generation: UUID
    public init(policy: WithdrawalNativeOwnerPolicy, epoch: WithdrawalNativeOwnerEpoch,
                vault: any WithdrawalNativeVaultReadPort, originalServerBinding: WithdrawalNativeSession,
                deploymentContext: String, actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        try requireWithdrawalNativeContext(deploymentContext,actualContext)
        let initial = try epoch.snapshot(); binding = originalServerBinding
        try ownerRequire(ownerMatches(binding.accountRef, "^sha256:[0-9a-f]{64}$")
            && binding.active && binding.protectedDataAvailable && binding.now.timeIntervalSince1970.isFinite
            && binding.expiresAt.timeIntervalSince1970.isFinite && binding.now <= initial.now && initial.now < binding.expiresAt)
        self.policy = policy; self.epoch = epoch; self.vault = vault; generation = initial.generation
        _ = try currentSession()
    }
    public func currentSession() throws -> WithdrawalNativeSession {
        do {
            try ownerRequire(!Task.isCancelled)
            let before = try epoch.snapshot(); try ownerRequire(before.generation == generation)
            let credential = try withdrawalReadVault(vault, policy: policy)
            let after = try epoch.snapshot()
            try ownerRequire(after.generation == generation && !Task.isCancelled)
            let bearer = credential.bearer, expiresAt = credential.expiresAt
            try ownerRequire(bearer == binding.bearer && expiresAt == binding.expiresAt && after.now < expiresAt)
            return WithdrawalNativeSession(accountRef: binding.accountRef, bearer: bearer, provider: binding.provider,
                generation: generation, now: after.now, expiresAt: expiresAt, active: true, protectedDataAvailable: true)
        } catch { epoch.signal(.disposed); throw WithdrawalNativeReviewError.held }
    }
    public func finishWithdrawal() { epoch.signal(.disposed) }
    func beginSDKPresentation(_ operation: UUID) throws {
        _ = try currentSession()
        try epoch.beginSDKPresentation(operation, maximumSeconds: policy.SDKPresentationSeconds)
    }
    func endSDKPresentation(_ operation: UUID) { epoch.endSDKPresentation(operation) }
}

#if canImport(UIKit)
import UIKit
import Security
import LocalAuthentication
import CoreFoundation

private final class WithdrawalNativeOwnerNotifications: @unchecked Sendable {
    private let lock = NSLock(), center: NotificationCenter, epoch: WithdrawalNativeOwnerEpoch
    private var observers: [NSObjectProtocol] = []
    init(center: NotificationCenter, epoch: WithdrawalNativeOwnerEpoch,
         signals: [(Notification.Name, WithdrawalNativeOwnerSignal, AnyObject?)]) {
        self.center = center; self.epoch = epoch
        for (name, signal, object) in signals {
            observers.append(center.addObserver(forName: name, object: object, queue: nil) { [epoch] _ in epoch.signal(signal) })
        }
    }
    func dispose() {
        epoch.signal(.disposed)
        let owned = lock.withLock { let value = observers; observers.removeAll(); return value }
        for observer in owned { center.removeObserver(observer) }
    }
    deinit { dispose() }
}

// Source candidate compiles against the iOS SDK, but accepted policies reject
// construction before UIApplication access, observers, or any Keychain read.
@MainActor public final class WithdrawalNativeUIKitOwnerCandidate {
    public let epoch: WithdrawalNativeOwnerEpoch, session: WithdrawalNativeVaultSession
    private let notifications: WithdrawalNativeOwnerNotifications
    public init(policy: WithdrawalNativeOwnerPolicy, scene: UIWindowScene, originalServerBinding: WithdrawalNativeSession) throws {
        try ownerRequire(policy.observersEnabled && policy.credentialAccessEnabled)
        let app = UIApplication.shared
        let epoch = try WithdrawalNativeOwnerEpoch(initiallyActive: app.applicationState == .active && scene.activationState == .foregroundActive,
            protectedDataAvailable: app.isProtectedDataAvailable)
        self.epoch = epoch
        session = try WithdrawalNativeVaultSession(policy: policy, epoch: epoch,
            vault: WithdrawalNativeSystemVaultCandidate(policy: policy), originalServerBinding: originalServerBinding, deploymentContext: "synthetic_test")
        let signals: [(Notification.Name, WithdrawalNativeOwnerSignal, AnyObject?)] = [
            (UIApplication.willResignActiveNotification, .inactive, nil),
            (UIApplication.didBecomeActiveNotification, .foreground, nil),
            (UIApplication.didEnterBackgroundNotification, .background, nil),
            (UIApplication.protectedDataWillBecomeUnavailableNotification, .protectedDataUnavailable, nil),
            (UIApplication.significantTimeChangeNotification, .significantTimeChanged, nil),
            (UIScene.willDeactivateNotification, .inactive, scene),
            (UIScene.didActivateNotification, .foreground, scene),
            (UIScene.didEnterBackgroundNotification, .background, scene),
            (UIScene.didDisconnectNotification, .sceneDisconnected, scene),
            (Notification.Name(policy.changedNotification), .sessionChanged, nil)]
        notifications = WithdrawalNativeOwnerNotifications(center: .default, epoch: epoch, signals: signals)
        if app.applicationState != .active || scene.activationState != .foregroundActive || !app.isProtectedDataAvailable { epoch.signal(.inactive) }
    }
    public func dispose() {
        notifications.dispose()
    }
}
@MainActor private final class WithdrawalNativeSystemVaultCandidate: WithdrawalNativeVaultReadPort {
    private let policy: WithdrawalNativeOwnerPolicy
    private let actualContext: WithdrawalNativeActualTESTContext?
    init(policy: WithdrawalNativeOwnerPolicy, actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        try ownerRequire(policy.credentialAccessEnabled || actualContext != nil)
        if let actualContext {try ownerRequire(Bundle.main.bundleIdentifier == actualContext.bundleIdentifier)}
        self.policy = policy;self.actualContext=actualContext
    }
    func copy(_ request: WithdrawalNativeVaultRequest) throws -> WithdrawalNativeVaultResult {
        try ownerRequire((policy.credentialAccessEnabled || actualContext != nil) && request == WithdrawalNativeVaultRequest(policy: policy))
        if let actualContext {try ownerRequire(Bundle.main.bundleIdentifier == actualContext.bundleIdentifier
            && UIApplication.shared.applicationState == .active && UIApplication.shared.isProtectedDataAvailable)}
        let context = LAContext(); context.interactionNotAllowed = true
        let query: [String: Any] = [kSecClass as String:kSecClassGenericPassword,
            kSecAttrService as String:request.service, kSecAttrAccount as String:request.account,
            kSecAttrSynchronizable as String:kCFBooleanFalse as Any,
            kSecAttrAccessible as String:kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
            kSecReturnData as String:kCFBooleanTrue as Any, kSecReturnAttributes as String:kCFBooleanTrue as Any,
            kSecMatchLimit as String:kSecMatchLimitOne, kSecUseAuthenticationContext as String:context]
        var result: CFTypeRef?; let status = SecItemCopyMatching(query as CFDictionary, &result)
        if status == errSecItemNotFound { return .missing }
        try ownerRequire(status == errSecSuccess)
        return try withdrawalSystemVaultResult(result, request: request, accessibility: policy.accessibility)
    }
}

// Owns real process/scene notifications and the fixed read-only app vault port.
// Creation does not read credentials, mount a plugin, or start an SDK call.
@MainActor public final class WithdrawalNativeActualTESTOSOwnerCandidate {
    public let epoch: WithdrawalNativeOwnerEpoch
    public let vault: any WithdrawalNativeVaultReadPort
    private let notifications: WithdrawalNativeOwnerNotifications
    public init(policy: WithdrawalNativeOwnerPolicy, actualContext: WithdrawalNativeActualTESTContext,
        presenting: UIViewController) throws {
        let app=UIApplication.shared
        guard Bundle.main.bundleIdentifier == actualContext.bundleIdentifier, presenting.isViewLoaded,
              let window=presenting.view.window,let scene=window.windowScene,scene.activationState == .foregroundActive,
              app.applicationState == .active,app.isProtectedDataAvailable else {throw WithdrawalNativeReviewError.held}
        let epoch=try WithdrawalNativeOwnerEpoch(initiallyActive:true,protectedDataAvailable:true)
        self.epoch=epoch
        vault=try WithdrawalNativeSystemVaultCandidate(policy:policy,actualContext:actualContext)
        let signals:[(Notification.Name,WithdrawalNativeOwnerSignal,AnyObject?)]=[
            (UIApplication.willResignActiveNotification,.inactive,nil),(UIApplication.didBecomeActiveNotification,.foreground,nil),
            (UIApplication.didEnterBackgroundNotification,.background,nil),(UIApplication.protectedDataWillBecomeUnavailableNotification,.protectedDataUnavailable,nil),
            (UIApplication.protectedDataDidBecomeAvailableNotification,.protectedDataAvailable,nil),
            (UIApplication.significantTimeChangeNotification,.significantTimeChanged,nil),
            (UIScene.willDeactivateNotification,.inactive,scene),
            (UIScene.didActivateNotification,.foreground,scene),
            (UIScene.didEnterBackgroundNotification,.background,scene),
            (UIScene.didDisconnectNotification,.sceneDisconnected,scene),
            (Notification.Name(policy.changedNotification),.sessionChanged,nil)]
        notifications=WithdrawalNativeOwnerNotifications(center:.default,epoch:epoch,signals:signals)
        if app.applicationState != .active || scene.activationState != .foregroundActive || !app.isProtectedDataAvailable {epoch.signal(.inactive)}
    }
    public func dispose(){notifications.dispose()}
}
#endif
