#if canImport(Security)
import Foundation
import Security
import CoreFoundation

// Decode the attributes returned by Security, before the app JSON contract.
// The OS may return kSecAttrSynchronizable as CFNumber(0), not CFBoolean.
func withdrawalSystemVaultResult(_ result: CFTypeRef?, request: WithdrawalNativeVaultRequest,
                                accessibility: String) throws -> WithdrawalNativeVaultResult {
    guard let attrs = result as? [String: Any], let data = attrs[kSecValueData as String] as? Data,
        data.count <= request.maximumDataBytes,
        attrs[kSecAttrService as String] as? String == request.service,
        attrs[kSecAttrAccount as String] as? String == request.account,
        attrs[kSecAttrAccessible as String] as? String == kSecAttrAccessibleWhenUnlockedThisDeviceOnly as String,
        let sync = attrs[kSecAttrSynchronizable as String] as? NSNumber,
        (CFGetTypeID(sync) == CFBooleanGetTypeID() || CFGetTypeID(sync) == CFNumberGetTypeID()),
        sync.compare(NSNumber(value: 0)) == .orderedSame else { throw WithdrawalNativeReviewError.held }
    return .found(data: data, service: request.service, account: request.account,
                  accessibility: accessibility, synchronizable: false)
}
#endif
