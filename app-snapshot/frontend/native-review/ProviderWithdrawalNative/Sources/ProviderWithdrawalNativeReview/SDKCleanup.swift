import Foundation

public struct WithdrawalNativeSDKCleanupPolicy: Sendable {
    public let SDKCleanupEnabled: Bool
    public let kakaoTokenAdapterVersion: String?
    let grantAge: TimeInterval
    public init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        var expected: [String: Any] = ["version":"1.0.0","scope":"isolated_local_review",
            "runtime_registered":false,"native_plugin_registered":false,
            "operating_member_transport_authorized":false,"SDK_cleanup_enabled":false,
            "automatic_retry":false,"provider":"google","maximum_grant_age_seconds":5,
            "admission":"same_original_owner_consumed_credentials_verified_closure_and_durable_provider_ACK",
            "Google_action":"same_original_SDK_user_memory_signOut_after_server_ACK_no_disconnect_or_revoke_repeat",
            "confirmation":"memory_observation_only_SDK_storage_app_vault_and_whole_erasure_unconfirmed"]
        if raw["version"] as? String == "1.1.0" {
            expected["version"] = "1.1.0"
            expected.removeValue(forKey:"provider")
            expected["providers"] = "google|kakao"
            expected["Kakao_action"] = "same_original_manager_operation_full_token_and_writer_epoch_atomic_compare_delete_no_logout_unlink_or_repeat"
            expected["Kakao_SDK_version"] = "2.29.0"
            expected["Kakao_token_adapter_version"] = "1.0.0"
            kakaoTokenAdapterVersion = "1.0.0"
        } else { kakaoTokenAdapterVersion = nil }
        try ownerRequire(try JSONSerialization.data(withJSONObject:raw,options:.sortedKeys)
            == JSONSerialization.data(withJSONObject:expected,options:.sortedKeys))
        SDKCleanupEnabled = raw["SDK_cleanup_enabled"] as! Bool
        grantAge = (raw["maximum_grant_age_seconds"] as! NSNumber).doubleValue
    }
    func allows(_ provider: WithdrawalNativeProvider) -> Bool {
        provider == .google || (provider == .kakao && kakaoTokenAdapterVersion != nil)
    }
}

public enum WithdrawalNativeSDKMemoryCleanupObservation: Sendable { case memoryCleared, unavailable }
@MainActor public protocol WithdrawalNativeSDKMemoryCleanupPort: AnyObject {
    // No provider dispatch/refresh, app vault erase or whole-erasure receipt.
    // The driver must consume the same original one-use grant before effects.
    func clearOriginalAfterVerifiedACK(_ grant: WithdrawalNativeSDKCleanupGrant) throws -> WithdrawalNativeSDKMemoryCleanupObservation
}
