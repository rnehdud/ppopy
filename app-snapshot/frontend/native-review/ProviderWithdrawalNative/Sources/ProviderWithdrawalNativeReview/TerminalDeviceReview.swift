import Foundation
import CryptoKit

// Immutable build inputs describe required evidence. The frozen controller
// verifies actual receipts before launch; arbitrary JSON is not authority.
struct WithdrawalTerminalDevicePolicy {
    let fingerprint:String,provider:String,chainSHA256:String
    init(_ data:Data,sourcePin:String)throws {
        let raw=try withdrawalFlatObject(data,maximumBytes:8192)
        let sourceOnly=(raw["scope"] as? String)=="frozen_actual_TEST_source_remainder_store_review"
        let chainKey=sourceOnly ? "required_completion_contract_sha256":"completed_ACK_chain_sha256"
        for name in ["subject_fingerprint","source_event","source_pin",chainKey] {
            guard let s=raw[name] as? String else {throw WithdrawalNativeReviewError.held}
            try ownerRequire(ownerMatches(s,"^[0-9a-f]{64}$"))
        }
        fingerprint=raw["subject_fingerprint"] as! String
        provider="apple";chainSHA256=raw[chainKey] as! String
        var expected:[String:Any] = ["version":"1.0.0","scope":"frozen_actual_TEST_terminal_store_review",
            "runtime_registered":false,"native_JS_entrypoint":false,"production_enabled":false,
            "public_enabled":false,"automatic_retry":false,"network_calls":0,"provider_calls":0,
            "closure_calls":0,"web_bootstrap":false,"maximum_store_delete_calls":2,
            "bundle_identifier":"com.miraylab.poppy","team_identifier":"0000000000",
            "subject_fingerprint":fingerprint,"provider":provider,"source_event":raw["source_event"]!,
            "source_pin":sourcePin,"completed_service_COMMIT_ACKs":9,"completed_ACK_chain_sha256":chainSHA256,
            "admission":"frozen_source_restore_completed_ACK_chain_and_original_signed_checkpoint_bound_same_owner_session",
            "authority":"signed_lookup_grant_is_binding_only_not_account_closure_authority",
            "confirmation":"only_two_fixed_local_stores_not_SDK_OS_provider_backup_or_whole_erasure"]
        if sourceOnly {
            guard let plan=raw["required_terminal_plan_sha256"] as? String else {throw WithdrawalNativeReviewError.held}
            try ownerRequire(ownerMatches(plan,"^[0-9a-f]{64}$"))
            expected.removeValue(forKey:"completed_service_COMMIT_ACKs")
            expected.removeValue(forKey:"completed_ACK_chain_sha256")
            expected["version"]="2.0.0"
            expected["scope"]="frozen_actual_TEST_source_remainder_store_review"
            expected["required_source_COMMIT_ACKs"]=3
            expected["required_provider_ACK"]=true
            expected["required_terminal_plan_sha256"]=plan
            expected["required_completion_contract_sha256"]=chainSHA256
            expected["admission"]="frozen_source_remainder_actual_ACKs_and_provider_ACK_before_same_owner_session_cleanup"
        }
        try ownerRequire(try JSONSerialization.data(withJSONObject:raw,options:.sortedKeys)
            == JSONSerialization.data(withJSONObject:expected,options:.sortedKeys))
    }
}

extension WithdrawalLookupRestartReview {
    // No registered JS or ordinary-app call site. The explicit native command
    // is admitted only by the frozen signed build and same-owner controller.
    // No HTTP/SDK object is dispatched here; transport construction only checks
    // the pinned existing TEST endpoint and original verification namespace.
    public static func removeActualTESTStoresForTerminalReview(terminalConfiguration:Data,
        configuration:Data,statusConfiguration:Data,httpsConfiguration:Data,
        proofProfileConfiguration:Data,actualContext:WithdrawalNativeActualTESTContext,
        store:any WithdrawalLookupStorePort,vault:any WithdrawalNativeVaultReadPort,
        ownerConfiguration:Data,now:Date = Date(),invalidateOriginalOwner:@MainActor ()->Void,
        deleteOriginalVault:@MainActor ()throws->Void)throws->[String:Any] {
        try actualContext.requireWithdrawalReady()
        let terminal=try WithdrawalTerminalDevicePolicy(terminalConfiguration,sourcePin:actualContext.sourcePin)
        let profile=try WithdrawalProofProfileReview(configuration:proofProfileConfiguration,
            publicKeyX963:actualContext.publicKeyX963,expectedKeySHA256:actualContext.sourcePin,
            isolatedKeySHA256:actualContext.isolatedPin,restoreKeySHA256:actualContext.restorePin,
            deploymentContext:"actual_test_candidate",actualContext:actualContext)
        let transport=try WithdrawalHTTPSReviewTransport(configuration:httpsConfiguration)
        let inspector=try Self(configuration:configuration,statusConfiguration:statusConfiguration,
            url:transport.url(method:"withdrawal_status_read"),publicKeyX963:actualContext.publicKeyX963,
            expectedKeySHA256:actualContext.sourcePin,store:store,deploymentContext:"actual_test_candidate",
            admission:{throw WithdrawalNativeReviewError.held},sessionConfiguration:{.ephemeral},
            httpsReview:transport,proofProfile:profile)
        let owner=try WithdrawalNativeOwnerPolicy(json:ownerConfiguration)
        return inspector.removeTerminalStoresForReview(expectedAccountFingerprint:terminal.fingerprint,
            expectedProvider:terminal.provider,now:now,vault:vault,
            ownerPolicy:owner,removeOriginalVault:{expected in
                try SessionVaultConditionalRemoval.removeIfValueMatches(expected:expected,maximumDataBytes:owner.vaultBytes,
                    read:{
                        switch try vault.copy(WithdrawalNativeVaultRequest(policy:owner)) {
                        case .missing:return nil
                        case let .found(data,service,account,accessibility,synchronizable):
                            try ownerRequire(service==owner.service && account==owner.account
                                && accessibility==owner.accessibility && !synchronizable)
                            return data
                        }
                    },invalidate:invalidateOriginalOwner,delete:deleteOriginalVault)
            })
    }
}
