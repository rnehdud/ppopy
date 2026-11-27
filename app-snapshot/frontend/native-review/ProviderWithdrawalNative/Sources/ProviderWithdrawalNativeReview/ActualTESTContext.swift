import Foundation
import CryptoKit

// Immutable compiled input, never selected by JS or a server response. This
// candidate does not claim installation or successful provider/member erasure.
public final class WithdrawalNativeActualTESTContext: Sendable, Equatable {
    public static func == (lhs:WithdrawalNativeActualTESTContext,rhs:WithdrawalNativeActualTESTContext)->Bool {lhs === rhs}
    public let publicKeyX963: Data, sourcePin: String, isolatedPin: String, restorePin: String
    public let serverContractSHA256: String, serverCodeSHA256: String
    public let providerSettingsSealed: Bool
    public let providerSettingsBindingSHA256: String?
    public let bundleIdentifier: String
    let host: String
    public init(manifest: Data, expectedManifestSHA256: String, bundleIdentifier: String, teamIdentifier: String) throws {
        try ownerRequire(manifest.count > 0 && manifest.count <= 4096
            && ownerMatches(expectedManifestSHA256,"^[0-9a-f]{64}$")
            && SHA256.hash(data:manifest).map {String(format:"%02x",$0)}.joined() == expectedManifestSHA256)
        let raw = try withdrawalFlatObject(manifest)
        var fields: Set<String> = ["version","kind","bundle_identifier","team_identifier","host","namespace",
            "source_public_x963_b64","source_pin","isolated_pin","restore_pin","server_contract_sha256","server_code_sha256",
            "runtime_registered","provider_credentials_prepared","public_enabled","production_enabled"]
        let providerCandidate = raw["version"] as? String == "1.1.0"
        if providerCandidate {fields.insert("provider_settings_binding_sha256")}
        try ownerRequire(Set(raw.keys) == fields && bundleIdentifier == "com.miraylab.poppy" && teamIdentifier == "0000000000"
            && (providerCandidate ? raw["kind"] as? String == "SEALED_ACTUAL_TEST_NATIVE_PROVIDER_CONTEXT_CANDIDATE"
                : raw["version"] as? String == "1.0.0" && raw["kind"] as? String == "SEALED_ACTUAL_TEST_NATIVE_CONTEXT_CANDIDATE")
            && raw["bundle_identifier"] as? String == bundleIdentifier && raw["team_identifier"] as? String == teamIdentifier
            && raw["host"] as? String == "synthetic00.execute-api.ap-northeast-2.amazonaws.com"
            && raw["namespace"] as? String == "app_withdrawal_test_v1")
        for name in ["runtime_registered","public_enabled","production_enabled"] {
            try ownerRequire(try JSONSerialization.data(withJSONObject:[name:raw[name]!],options:.sortedKeys)
                == JSONSerialization.data(withJSONObject:[name:false],options:.sortedKeys))
        }
        try ownerRequire(try JSONSerialization.data(withJSONObject:["provider_credentials_prepared":raw["provider_credentials_prepared"]!],options:.sortedKeys)
            == JSONSerialization.data(withJSONObject:["provider_credentials_prepared":providerCandidate],options:.sortedKeys))
        let providerBinding = raw["provider_settings_binding_sha256"] as? String
        if providerCandidate {
            try ownerRequire(providerBinding.map {ownerMatches($0,"^[0-9a-f]{64}$")} == true)
        }
        guard let encoded=raw["source_public_x963_b64"] as? String, let key=Data(base64Encoded:encoded),
              let source=raw["source_pin"] as? String,let isolated=raw["isolated_pin"] as? String,
              let restore=raw["restore_pin"] as? String,let contract=raw["server_contract_sha256"] as? String,
              let code=raw["server_code_sha256"] as? String else {throw WithdrawalNativeReviewError.held}
        try ownerRequire(key.base64EncodedString() == encoded && key.count == 65 && Set([source,isolated,restore]).count == 3
            && [source,isolated,restore,contract,code].allSatisfy {ownerMatches($0,"^[0-9a-f]{64}$")}
            && SHA256.hash(data:key).map {String(format:"%02x",$0)}.joined() == source)
        try ownerRequire(P256.Signing.PublicKey(x963Representation:key).x963Representation == key)
        publicKeyX963=key;sourcePin=source;isolatedPin=isolated;restorePin=restore
        serverContractSHA256=contract;serverCodeSHA256=code;host=raw["host"] as! String
        providerSettingsSealed=providerCandidate;providerSettingsBindingSHA256=providerBinding
        self.bundleIdentifier=bundleIdentifier
    }
    func requireKey(_ key:Data,source:String,isolated:String,restore:String)throws {
        try ownerRequire(key == publicKeyX963 && source == sourcePin && isolated == isolatedPin && restore == restorePin)
    }
    func requireURL(_ url:URL)throws {
        try ownerRequire(url.scheme == "https" && url.host == host && url.port == nil
            && url.user == nil && url.password == nil && url.query == nil && url.fragment == nil
            && ["/app/withdrawal/binding","/app/withdrawal/lookup","/app/withdrawal/operation"].contains(url.path))
    }
    // The original v1 closed context stays held. A v1.1 compiled contract pins
    // the server code, request contract and separately sealed provider purpose.
    // Original session, signed lookup, lifecycle and SDK checks still follow.
    func requireWithdrawalReady() throws {
        try ownerRequire(providerSettingsSealed && providerSettingsBindingSHA256 != nil)
    }
    public func requireSDKAuthenticationReady() throws {
        try requireWithdrawalReady()
    }
}

func requireWithdrawalNativeContext(_ mode:String,_ actual:WithdrawalNativeActualTESTContext?)throws {
    if actual != nil {try ownerRequire(mode == "actual_test_candidate")}
    else {try ownerRequire(mode == "synthetic_test")}
}
