import Foundation
import CoreFoundation
import Security
import LocalAuthentication
#if canImport(UIKit)
import UIKit
#endif

struct WithdrawalLookupKeychainPolicy {
    let bundle: String
    init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        let expected: [String:Any] = ["version":"1.0.0","scope":"isolated_iOS_simulator_keychain_review",
            "runtime_registered":false,"native_plugin_registered":false,"operating_secure_store_access_authorized":false,
            "operating_member_transport_authorized":false,"provider_live_calls_authorized":false,
            "review_bundle_identifier":"com.miraylab.review.withdrawal-keychain-local","platform":"iOS_simulator_only",
            "namespace":"exact_original_lookup_restart_policy_no_login_vault",
            "access_group":"implicit_application_only_no_shared_group","authentication_UI":"fail_never_prompt",
            "admission":"foreground_protected_data_bundle_check_before_after_every_Security_call",
            "concurrency":"single_process_main_actor_compare_and_confirm_not_OS_CAS",
            "failure":"held_no_fallback_retry_or_cleanup","whole_erasure_receipt":false]
        try ownerRequire(try JSONSerialization.data(withJSONObject:raw,options:.sortedKeys)
            == JSONSerialization.data(withJSONObject:expected,options:.sortedKeys))
        bundle = raw["review_bundle_identifier"] as! String
    }
}

@MainActor protocol WithdrawalLookupKeychainAPI: AnyObject {
    func copy(_ query: [String:Any]) -> (OSStatus,Any?)
    func add(_ query: [String:Any]) -> OSStatus
    func update(_ query: [String:Any], attributes: [String:Any]) -> OSStatus
    func delete(_ query: [String:Any]) -> OSStatus
}
// Security.framework on iOS can return non-synchronizable metadata as an
// integer CFNumber(0). Normalize only this trusted native return value. Query
// flags and application/JSON metadata still require real CFBoolean values.
func withdrawalLookupSecurityAttributes(_ raw: Any?) -> Any? {
    guard var attributes = raw as? [String:Any],
        let sync = attributes[kSecAttrSynchronizable as String] as? NSNumber,
        CFGetTypeID(sync) == CFNumberGetTypeID(),
        ["c","s","i","l","q","C","S","I","L","Q"].contains(String(cString:sync.objCType)),
        sync.int64Value == 0 && sync.doubleValue == 0 else { return raw }
    attributes[kSecAttrSynchronizable as String] = kCFBooleanFalse
    return attributes
}
@MainActor private final class SystemLookupKeychainAPI: WithdrawalLookupKeychainAPI {
    func copy(_ query: [String:Any]) -> (OSStatus,Any?) {
        var value: CFTypeRef?
        let status = SecItemCopyMatching(query as CFDictionary,&value)
        return (status,withdrawalLookupSecurityAttributes(value))
    }
    func add(_ query: [String:Any]) -> OSStatus { SecItemAdd(query as CFDictionary,nil) }
    func update(_ query: [String:Any], attributes: [String:Any]) -> OSStatus {
        SecItemUpdate(query as CFDictionary,attributes as CFDictionary)
    }
    func delete(_ query: [String:Any]) -> OSStatus { SecItemDelete(query as CFDictionary) }
}

// Real Security calls are available only in a distinct synthetic simulator app.
// This is not registered in the operating App, and never queries its login slot.
// Comparison/readback is synchronous on the main actor, not cross-process CAS.
@MainActor public final class WithdrawalLookupKeychainSimulatorReview: WithdrawalLookupStorePort,
    CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    private let request: WithdrawalLookupStoreRequest
    private let api: any WithdrawalLookupKeychainAPI
    private let admission: @MainActor () throws -> Void
    private var busy = false
    public convenience init(configuration: Data, restartConfiguration: Data, deploymentContext: String) throws {
        let policy = try WithdrawalLookupKeychainPolicy(json:configuration)
        _ = try WithdrawalLookupRestartPolicy(json:restartConfiguration)
        try ownerRequire(deploymentContext == "synthetic_test")
        #if canImport(UIKit) && targetEnvironment(simulator)
        try self.init(configuration:configuration,restartConfiguration:restartConfiguration,
            deploymentContext:deploymentContext,api:SystemLookupKeychainAPI(),admission:{
                try ownerRequire(Bundle.main.bundleIdentifier == policy.bundle
                    && UIApplication.shared.applicationState == .active
                    && UIApplication.shared.isProtectedDataAvailable)
            })
        #else
        _ = policy
        throw WithdrawalNativeReviewError.held
        #endif
    }
    init(configuration: Data, restartConfiguration: Data, deploymentContext: String,
        api: any WithdrawalLookupKeychainAPI, admission: @escaping @MainActor () throws -> Void) throws {
        _ = try WithdrawalLookupKeychainPolicy(json:configuration)
        let restart = try WithdrawalLookupRestartPolicy(json:restartConfiguration)
        try ownerRequire(deploymentContext == "synthetic_test")
        try admission()
        request = WithdrawalLookupStoreRequest(restart); self.api = api; self.admission = admission
    }
    public nonisolated var description: String { "WithdrawalLookupKeychainSimulatorReview(redacted)" }
    public nonisolated var debugDescription: String { description }
    public nonisolated var customMirror: Mirror { Mirror(self,children:[:]) }
    private func accepts(_ value: WithdrawalLookupStoreRequest) throws {
        try ownerRequire(value == request); try admission()
    }
    private func bounded(_ data: Data) throws {
        try ownerRequire(!data.isEmpty && data.count <= request.maximumDataBytes)
    }
    private func query() -> [String:Any] {
        let context = LAContext(); context.interactionNotAllowed = true
        return [kSecClass as String:kSecClassGenericPassword,
         kSecAttrService as String:request.service,kSecAttrAccount as String:request.account,
         kSecAttrSynchronizable as String:kCFBooleanFalse as Any,
         kSecUseAuthenticationContext as String:context]
    }
    private func bytes(_ result: WithdrawalLookupStoreResult) throws -> Data? {
        switch result {
        case .missing:return nil
        case let .found(data,_,_,_,_):return data
        }
    }
    private func perform<T>(_ body: () throws -> T) throws -> T {
        try ownerRequire(!busy)
        busy = true; defer { busy = false }
        return try body()
    }
    public func copy(_ value: WithdrawalLookupStoreRequest) throws -> WithdrawalLookupStoreResult {
        try perform { try read(value) }
    }
    private func read(_ value: WithdrawalLookupStoreRequest) throws -> WithdrawalLookupStoreResult {
        try accepts(value)
        var q = query();q[kSecMatchLimit as String] = kSecMatchLimitOne
        q[kSecReturnAttributes as String] = kCFBooleanTrue;q[kSecReturnData as String] = kCFBooleanTrue
        let (status,raw) = api.copy(q);try admission()
        if status == errSecItemNotFound { return .missing }
        guard status == errSecSuccess,let attributes = raw as? [String:Any],
            let data = attributes[kSecValueData as String] as? Data,
            let sync = attributes[kSecAttrSynchronizable as String] as? NSNumber else {
            throw WithdrawalNativeReviewError.held
        }
        try bounded(data)
        try ownerRequire(attributes[kSecAttrService as String] as? String == request.service
            && attributes[kSecAttrAccount as String] as? String == request.account
            && attributes[kSecAttrAccessible as String] as? String == kSecAttrAccessibleWhenUnlockedThisDeviceOnly as String
            && CFGetTypeID(sync) == CFBooleanGetTypeID() && !sync.boolValue)
        return .found(data:data,service:request.service,account:request.account,
            accessibility:request.accessibility,synchronizable:false)
    }
    public func create(_ value: WithdrawalLookupStoreRequest, data: Data) throws {
        try perform {
        try accepts(value);try bounded(data)
        try ownerRequire(try bytes(read(value)) == nil)
        try admission()
        var q = query();q[kSecValueData as String] = data
        q[kSecAttrAccessible as String] = kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        let status = api.add(q);try admission();try ownerRequire(status == errSecSuccess)
        try ownerRequire(try bytes(read(value)) == data)
        }
    }
    public func replace(_ value: WithdrawalLookupStoreRequest, expected: Data, replacement: Data) throws {
        try perform {
        try accepts(value);try bounded(expected);try bounded(replacement)
        try ownerRequire(try bytes(read(value)) == expected);try admission()
        let status = api.update(query(),attributes:[kSecValueData as String:replacement])
        try admission();try ownerRequire(status == errSecSuccess)
        try ownerRequire(try bytes(read(value)) == replacement)
        }
    }
    public func remove(_ value: WithdrawalLookupStoreRequest, expected: Data) throws {
        try perform {
        try accepts(value);try bounded(expected)
        try ownerRequire(try bytes(read(value)) == expected);try admission()
        let status = api.delete(query());try admission();try ownerRequire(status == errSecSuccess)
        try ownerRequire(try bytes(read(value)) == nil)
        }
    }
}
