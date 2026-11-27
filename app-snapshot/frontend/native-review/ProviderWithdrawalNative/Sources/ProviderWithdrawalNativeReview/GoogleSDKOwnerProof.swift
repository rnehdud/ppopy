import Foundation
import CoreFoundation
import CryptoKit

// A local credential-retirement capability only. It cannot authorize provider
// revocation, account closure, HTTP or a whole-erasure receipt. Session expiry
// does not prevent retiring its exact unchanged local credential/SDK owner.
public struct GoogleSDKRetirementOwner: Sendable {
    private let clientID: String, nonce: String, digest: String
    fileprivate init(clientID: String, nonce: String, digest: String) {
        self.clientID=clientID; self.nonce=nonce; self.digest=digest
    }
    public func matchesGoogleSubject(_ subject: String) throws -> Bool {
        try ownerRequire(!subject.isEmpty && subject.utf8.count<=512)
        return googleSDKOwnerDigest(clientID:clientID,nonce:nonce,subject:subject)==digest
    }
}

func googleSDKOwnerDigest(clientID:String,nonce:String,subject:String)->String {
    var value=Data()
    for part in ["poppy-google-sdk-owner-v1",clientID,nonce,subject] {
        let bytes=Data(part.utf8);var length=UInt32(bytes.count).bigEndian
        Swift.withUnsafeBytes(of:&length){value.append(contentsOf:$0)}
        value.append(bytes)
    }
    return SHA256.hash(data:value).map{String(format:"%02x",$0)}.joined()
}

private func googleSDKInteger(_ value:Any?)throws->Int64 {
    guard let number=value as? NSNumber,CFGetTypeID(number) != CFBooleanGetTypeID() else {throw WithdrawalNativeReviewError.held}
    let n=number.doubleValue
    try ownerRequire(n.isFinite && n>=0 && n<=9007199254740991 && n.rounded(.down)==n)
    return number.int64Value
}

private func googleSDKMilliseconds(_ date:Date)throws->Int64 {
    let n=date.timeIntervalSince1970*1000
    try ownerRequire(n.isFinite && n>=0 && n<=9007199254740991)
    return Int64(n.rounded(.down))
}

public struct GoogleSDKOwnerProofReview: Sendable {
    public let maximumSDKArchiveBytes:Int
    private let key:P256.Signing.PublicKey,scope:String,clientID:String,bundleID:String
    public init(configuration:Data,publicKeyX963:Data,expectedKeySHA256:String,clientID:String,
        bundleIdentifier:String,deploymentContext:String,proofProfile:WithdrawalProofProfileReview?=nil)throws {
        let raw=try withdrawalFlatObject(configuration)
        let expected:[String:Any]=["version":"1.0.0","scope":"local_google_sdk_owner_binding_review",
            "runtime_registered":false,"native_registered":false,"public_enabled":false,"whole_erasure_receipt":false,
            "kind":"google_sdk_owner_binding","isolated_proof_scope":"isolated_local_review_google_sdk_owner",
            "test_proof_scope":"app_withdrawal_test_v1_binding_google_sdk_owner","digest_domain":"poppy-google-sdk-owner-v1",
            "bundle_identifier":"com.miraylab.poppy","maximum_payload_bytes":1536,"maximum_envelope_bytes":2048,
            "maximum_identity_age_seconds":30,"maximum_subject_bytes":512,"nonce_bytes":32,"maximum_session_days":56,
            "expired_proof_use":"local_exact_session_credential_retirement_only","signature":"pinned_P256_SHA256_raw64"]
        var exact=expected
        exact["session_vault_contract_version"]="1.1.0-google-sdk-owner-review";exact["maximum_vault_bytes"]=4096;exact["maximum_sdk_archive_bytes"]=65536
        try ownerRequire(try JSONSerialization.data(withJSONObject:raw,options:.sortedKeys)
            == JSONSerialization.data(withJSONObject:exact,options:.sortedKeys))
        try requireWithdrawalNativeContext(deploymentContext,proofProfile?.actualContext)
        try proofProfile?.requireKey(publicKeyX963)
        try ownerRequire(ownerMatches(expectedKeySHA256,"^[0-9a-f]{64}$")
            && SHA256.hash(data:publicKeyX963).map{String(format:"%02x",$0)}.joined()==expectedKeySHA256
            && ownerMatches(clientID,"^[0-9]+-[a-z0-9]+\\.apps\\.googleusercontent\\.com$")
            && bundleIdentifier=="com.miraylab.poppy")
        key=try P256.Signing.PublicKey(x963Representation:publicKeyX963)
        try ownerRequire(key.x963Representation==publicKeyX963)
        scope=withdrawalBindingProofScope(proofProfile)+"_google_sdk_owner"
        try ownerRequire(scope==expected["isolated_proof_scope"] as? String || scope==expected["test_proof_scope"] as? String)
        self.clientID=clientID;bundleID=bundleIdentifier;maximumSDKArchiveBytes=65536
    }

    public func verifyForRetirement(_ envelope:Data,bearer:String,sessionExpiresAt:Date,now:Date)throws->GoogleSDKRetirementOwner {
        try ownerRequire(ownerMatches(bearer,"^[A-Za-z0-9_-]{32,200}$"))
        let outer=try withdrawalFlatObject(envelope,maximumBytes:2048)
        try ownerRequire(Set(outer.keys)==["version","scope","payload","signature"]
            && outer["version"] as? String=="1.0.0" && outer["scope"] as? String==scope)
        guard let p=outer["payload"] as? String,let s=outer["signature"] as? String,
            let payload=Data(base64Encoded:p),let signature=Data(base64Encoded:s) else {throw WithdrawalNativeReviewError.held}
        try ownerRequire(payload.base64EncodedString()==p && signature.base64EncodedString()==s
            && !payload.isEmpty && payload.count<=1536 && signature.count==64
            && key.isValidSignature(try P256.Signing.ECDSASignature(rawRepresentation:signature),for:payload))
        let raw=try withdrawalFlatObject(payload,maximumBytes:1536)
        try ownerRequire(Set(raw.keys)==["version","scope","kind","provider","bundle_identifier","client_id",
            "session_ref","owner_nonce","owner_digest","issued_ms","expires_ms"]
            && raw["version"] as? String=="1.0.0" && raw["scope"] as? String==scope
            && raw["kind"] as? String=="google_sdk_owner_binding" && raw["provider"] as? String=="google"
            && raw["bundle_identifier"] as? String==bundleID && raw["client_id"] as? String==clientID
            && raw["session_ref"] as? String=="sha256:"+SHA256.hash(data:Data(bearer.utf8)).map{String(format:"%02x",$0)}.joined())
        guard let nonce=raw["owner_nonce"] as? String,let digest=raw["owner_digest"] as? String else {throw WithdrawalNativeReviewError.held}
        let issued=try googleSDKInteger(raw["issued_ms"]),expires=try googleSDKInteger(raw["expires_ms"])
        try ownerRequire(ownerMatches(nonce,"^[A-Za-z0-9_-]{43}$") && ownerMatches(digest,"^[0-9a-f]{64}$")
            && issued<=googleSDKMilliseconds(now) && issued<expires && expires-issued<=56*86400000
            && expires==googleSDKMilliseconds(sessionExpiresAt))
        return GoogleSDKRetirementOwner(clientID:clientID,nonce:nonce,digest:digest)
    }
}
