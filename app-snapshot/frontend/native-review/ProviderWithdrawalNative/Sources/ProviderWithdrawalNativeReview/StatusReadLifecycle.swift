import Foundation

struct WithdrawalStatusReadLifecyclePolicy {
    init(_ data:Data)throws {
        let expected:[String:Any] = ["version":"1.0.0",
            "scope":"closed_TEST_original_status_after_background_review",
            "runtime_registered":false,"operating_member_transport_authorized":false,
            "automatic_retry":false,"automatic_mount_read":false,"maximum_original_grant_seconds":300,
            "withdrawal":"one_original_dispatch_background_never_reauthorizes_mutation",
            "status":"explicit_existing_native_reader_only_no_host_recreation_or_lookup_preparation",
            "background":"invalidate_pending_reply_allow_new_explicit_read_after_foreground_unlock",
            "terminal":"session_change_clock_change_document_navigation_scene_disconnect_disposal",
            "admission":"same_original_native_identity_shared_auth_gate_signed_checkpoint_original_deadline",
            "response":"no_identity_or_capability_no_whole_deletion_claim"]
        try ownerRequire(try JSONSerialization.data(withJSONObject:withdrawalFlatObject(data),options:.sortedKeys)
            == JSONSerialization.data(withJSONObject:expected,options:.sortedKeys))
    }
}

// A background event never restores mutation authority. It only invalidates
// pending replies. A later explicit read still uses the original prepared
// reader, signed checkpoint/deadline, vault identity and shared auth gate.
final class WithdrawalStatusReadLifecycleFence:@unchecked Sendable {
    private let lock=NSLock()
    private var started=false,mutationAllowed=true,readGeneration=UUID()
    func beginOriginalAccess(){lock.withLock {started=true}}
    func suspend(){lock.withLock {
        guard started else {return}
        mutationAllowed=false;readGeneration=UUID()
    }}
    func mayMutate()->Bool {lock.withLock {mutationAllowed}}
    func snapshot()->UUID {lock.withLock {readGeneration}}
    func isCurrent(_ generation:UUID)->Bool {lock.withLock {generation == readGeneration}}
}
