import Foundation
import CryptoKit

// Chosen by the trusted deployment composition before reading any response.
// This OFF TEST candidate neither registers a key nor admits operating users.
public struct WithdrawalProofProfileReview: Sendable, Equatable {
    let bindingScope: String, operationScope: String
    private let publicKey: Data, isolatedPin: String, restorePin: String
    let actualContext: WithdrawalNativeActualTESTContext?
    public init(configuration: Data, publicKeyX963: Data, expectedKeySHA256: String,
        isolatedKeySHA256: String, restoreKeySHA256: String, deploymentContext: String,
        actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        let raw = try withdrawalFlatObject(configuration)
        let expected: [String: Any] = ["version":"1.0.0", "scope":"withdrawal_test_candidate_profile_review",
            "namespace":"app_withdrawal_test_v1", "binding_scope":"app_withdrawal_test_v1_binding",
            "operation_scope":"app_withdrawal_test_v1_operation",
            "reserved_operating_namespace":"app_withdrawal_operating_v1_separate_exact_review_required",
            "runtime_registered":false, "native_plugin_registered":false, "operating_key_registered":false,
            "operating_member_transport_authorized":false, "whole_erasure_receipt":false,
            "key_rule":"explicit_P256_source_pin_distinct_from_isolated_and_restore_pins",
            "selection":"trusted_composition_only_never_request_or_response_selected",
            "activation":"exact_key_source_DB_API_server_native_review_required"]
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options:.sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options:.sortedKeys))
        let pins = [expectedKeySHA256, isolatedKeySHA256, restoreKeySHA256]
        try requireWithdrawalNativeContext(deploymentContext,actualContext)
        try actualContext?.requireKey(publicKeyX963,source:expectedKeySHA256,isolated:isolatedKeySHA256,restore:restoreKeySHA256)
        try ownerRequire(Set(pins).count == 3
            && pins.allSatisfy { ownerMatches($0,"^[0-9a-f]{64}$") }
            && SHA256.hash(data: publicKeyX963).map { String(format:"%02x",$0) }.joined() == expectedKeySHA256)
        let key = try P256.Signing.PublicKey(x963Representation: publicKeyX963)
        try ownerRequire(key.x963Representation == publicKeyX963)
        publicKey = publicKeyX963; isolatedPin = isolatedKeySHA256; restorePin = restoreKeySHA256
        self.actualContext = actualContext
        bindingScope = raw["binding_scope"] as! String; operationScope = raw["operation_scope"] as! String
    }
    func requireKey(_ publicKeyX963: Data) throws { try ownerRequire(publicKeyX963 == publicKey) }
}

func withdrawalBindingProofScope(_ profile: WithdrawalProofProfileReview?) -> String {
    profile?.bindingScope ?? "isolated_local_review"
}
func withdrawalOperationProofScope(_ profile: WithdrawalProofProfileReview?) -> String {
    profile?.operationScope ?? "isolated_loopback_review"
}
