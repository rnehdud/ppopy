#if canImport(UIKit)
import Foundation
import UIKit
import Security
import LocalAuthentication

// Source-only iOS adapter. Accepted OFF policy rejects construction before OS
// access. No plugin registration or real app Keychain write is enabled here.
@MainActor public final class WithdrawalLookupKeychainCandidate: WithdrawalLookupStorePort {
    private let request: WithdrawalLookupStoreRequest
    private let actualContext:WithdrawalNativeActualTESTContext?
    public init(policy: WithdrawalLookupRestartPolicy,actualContext:WithdrawalNativeActualTESTContext? = nil) throws {
        try ownerRequire(policy.operatingAccess || actualContext != nil)
        self.actualContext=actualContext
        if let actualContext {try ownerRequire(Bundle.main.bundleIdentifier == actualContext.bundleIdentifier)}
        request = WithdrawalLookupStoreRequest(policy)
    }
    private func query(_ requested: WithdrawalLookupStoreRequest) throws -> [String: Any] {
        try actualContext?.requireWithdrawalReady()
        try ownerRequire(requested == request && UIApplication.shared.isProtectedDataAvailable)
        let context = LAContext(); context.interactionNotAllowed = true
        return [kSecClass as String:kSecClassGenericPassword,
            kSecAttrService as String:request.service,kSecAttrAccount as String:request.account,
            kSecAttrSynchronizable as String:false,kSecUseAuthenticationContext as String:context]
    }
    public func copy(_ requested: WithdrawalLookupStoreRequest) throws -> WithdrawalLookupStoreResult {
        var q = try query(requested); q[kSecReturnData as String] = true; q[kSecReturnAttributes as String] = true
        q[kSecMatchLimit as String] = kSecMatchLimitOne
        var result: CFTypeRef?; let code = SecItemCopyMatching(q as CFDictionary,&result)
        if code == errSecItemNotFound { return .missing }
        guard code == errSecSuccess, let raw = result as? [String:Any], let data = raw[kSecValueData as String] as? Data,
            raw[kSecAttrService as String] as? String == request.service,
            raw[kSecAttrAccount as String] as? String == request.account,
            raw[kSecAttrAccessible as String] as? String == kSecAttrAccessibleWhenUnlockedThisDeviceOnly as String,
            let sync = raw[kSecAttrSynchronizable as String] as? NSNumber, !sync.boolValue,
            !data.isEmpty, data.count <= request.maximumDataBytes else { throw WithdrawalNativeReviewError.held }
        return .found(data:data,service:request.service,account:request.account,
            accessibility:request.accessibility,synchronizable:false)
    }
    private func matches(_ requested: WithdrawalLookupStoreRequest, _ expected: Data) throws {
        guard case let .found(data,_,_,_,_) = try copy(requested), data == expected else { throw WithdrawalNativeReviewError.held }
    }
    public func create(_ requested: WithdrawalLookupStoreRequest, data: Data) throws {
        try actualContext?.requireWithdrawalReady()
        try ownerRequire(!data.isEmpty && data.count <= request.maximumDataBytes)
        guard case .missing = try copy(requested) else { throw WithdrawalNativeReviewError.held }
        var q = try query(requested); q[kSecValueData as String] = data
        q[kSecAttrAccessible as String] = kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        try ownerRequire(SecItemAdd(q as CFDictionary,nil) == errSecSuccess)
        try matches(requested,data)
    }
    public func replace(_ requested: WithdrawalLookupStoreRequest, expected: Data, replacement: Data) throws {
        try actualContext?.requireWithdrawalReady()
        try ownerRequire(!replacement.isEmpty && replacement.count <= request.maximumDataBytes)
        try matches(requested,expected)
        let q = try query(requested)
        try ownerRequire(SecItemUpdate(q as CFDictionary,[kSecValueData as String:replacement] as CFDictionary) == errSecSuccess)
        try matches(requested,replacement)
    }
    public func remove(_ requested: WithdrawalLookupStoreRequest, expected: Data) throws {
        try actualContext?.requireWithdrawalReady()
        try matches(requested,expected)
        try ownerRequire(SecItemDelete(try query(requested) as CFDictionary) == errSecSuccess)
        guard case .missing = try copy(requested) else { throw WithdrawalNativeReviewError.held }
    }
}
#endif
