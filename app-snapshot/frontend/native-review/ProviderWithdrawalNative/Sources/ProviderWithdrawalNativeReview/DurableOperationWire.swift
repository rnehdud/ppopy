import Foundation

// Separate exact OFF opt-in. Existing closure callers retain the legacy body;
// only the reviewed preparation composition can attach the new capability.
struct WithdrawalDurableWirePolicy {
    init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        let expected: [String: Any] = ["version":"1.0.0", "scope":"isolated_loopback_review",
            "runtime_registered":false, "native_plugin_registered":false, "operating_member_transport_authorized":false,
            "provider_live_calls_authorized":false, "actual_OS_member_attestation":false,
            "automatic_retry":false, "whole_erasure_receipt":false, "lookup_token_bytes":43, "maximum_grant_seconds":300,
            "wire":"original_verified_lookup_token_challenge_and_close_same_bearer_operation",
            "admission":"signed_original_grant_verified_and_checkpoint_readback_before_write_capability",
            "storage":"native_invocation_memory_only_no_JS_logs_or_mutable_token_setter",
            "restart":"signed_original_checkpoint_explicit_status_read_only_never_reauthorize_write",
            "expiry":"original_absolute_grant_deadline_caps_challenge_receipt_and_submission",
            "failure":"retire_original_owner_unknown_ACK_explicit_read_only_no_resubmit"]
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
    }
}
