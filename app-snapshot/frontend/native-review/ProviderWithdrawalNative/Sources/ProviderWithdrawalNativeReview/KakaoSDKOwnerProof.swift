import Foundation
import CoreFoundation
import CryptoKit

public struct KakaoSDKRetirementOwner: Sendable {
    private let appID:Int64,nonce:String,digest:String
    fileprivate init(appID:Int64,nonce:String,digest:String){self.appID=appID;self.nonce=nonce;self.digest=digest}
    public func matchesKakaoAccessToken(_ token:String)throws->Bool {
        try ownerRequire(ownerMatches(token,"^[A-Za-z0-9._~+/=-]{20,2048}$"))
        return kakaoSDKOwnerDigest(appID:appID,nonce:nonce,accessDigest:kakaoSDKHash(Data(token.utf8)))==digest
    }
}

func kakaoSDKHash(_ data:Data)->String{SHA256.hash(data:data).map{String(format:"%02x",$0)}.joined()}
func kakaoSDKOwnerDigest(appID:Int64,nonce:String,accessDigest:String)->String {
    var input=Data()
    for part in ["poppy-kakao-sdk-owner-v1",String(appID),nonce,accessDigest] {
        let raw=Data(part.utf8);var length=UInt32(raw.count).bigEndian
        Swift.withUnsafeBytes(of:&length){input.append(contentsOf:$0)};input.append(raw)
    }
    return kakaoSDKHash(input)
}
private func kakaoSDKInteger(_ value:Any?)throws->Int64 {
    guard let n=value as? NSNumber,CFGetTypeID(n) != CFBooleanGetTypeID() else {throw WithdrawalNativeReviewError.held}
    let d=n.doubleValue
    try ownerRequire(d.isFinite && d>=0 && d<=9007199254740991 && d.rounded(.down)==d)
    return n.int64Value
}
private func kakaoSDKMilliseconds(_ date:Date)throws->Int64 {
    let n=date.timeIntervalSince1970*1000
    try ownerRequire(n.isFinite && n>=0 && n<=9007199254740991)
    return Int64(n.rounded(.down))
}

/// Only retires an unchanged local SDK/vault credential; never an HTTP/closure authority.
public struct KakaoSDKOwnerProofReview: Sendable {
    public let maximumSDKArchiveBytes:Int
    private let key:P256.Signing.PublicKey,scope:String,appID:Int64,bundleID:String
    public init(configuration:Data,publicKeyX963:Data,expectedKeySHA256:String,appID:Int64,
        bundleIdentifier:String,deploymentContext:String,proofProfile:WithdrawalProofProfileReview?=nil)throws {
        let raw=try withdrawalFlatObject(configuration)
        let expected:[String:Any]=["version":"1.0.0","scope":"local_kakao_sdk_owner_binding_review",
            "runtime_registered":false,"native_registered":false,"public_enabled":false,"whole_erasure_receipt":false,
            "kind":"kakao_sdk_owner_binding","isolated_proof_scope":"isolated_local_review_kakao_sdk_owner",
            "test_proof_scope":"app_withdrawal_test_v1_binding_kakao_sdk_owner","digest_domain":"poppy-kakao-sdk-owner-v1",
            "bundle_identifier":"com.miraylab.poppy","maximum_payload_bytes":1536,"maximum_envelope_bytes":2048,
            "maximum_identity_age_seconds":30,"maximum_token_bytes":2048,"nonce_bytes":32,"maximum_session_days":56,
            "expired_proof_use":"local_exact_session_credential_retirement_only","signature":"pinned_P256_SHA256_raw64",
            "session_vault_contract_version":"1.2.0-kakao-sdk-owner-review","maximum_vault_bytes":4096,"maximum_sdk_archive_bytes":65536]
        try ownerRequire(try JSONSerialization.data(withJSONObject:raw,options:.sortedKeys)
            == JSONSerialization.data(withJSONObject:expected,options:.sortedKeys))
        try requireWithdrawalNativeContext(deploymentContext,proofProfile?.actualContext)
        try proofProfile?.requireKey(publicKeyX963)
        try ownerRequire(ownerMatches(expectedKeySHA256,"^[0-9a-f]{64}$") && kakaoSDKHash(publicKeyX963)==expectedKeySHA256
            && appID>0 && appID<=9007199254740991 && bundleIdentifier=="com.miraylab.poppy")
        key=try P256.Signing.PublicKey(x963Representation:publicKeyX963)
        try ownerRequire(key.x963Representation==publicKeyX963)
        scope=withdrawalBindingProofScope(proofProfile)+"_kakao_sdk_owner"
        try ownerRequire(scope==expected["isolated_proof_scope"] as? String || scope==expected["test_proof_scope"] as? String)
        self.appID=appID;bundleID=bundleIdentifier;maximumSDKArchiveBytes=65536
    }

    public func verifyForRetirement(_ envelope:Data,bearer:String,sessionExpiresAt:Date,now:Date)throws->KakaoSDKRetirementOwner {
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
        try ownerRequire(Set(raw.keys)==["version","scope","kind","provider","bundle_identifier","app_id",
            "session_ref","owner_nonce","owner_digest","issued_ms","expires_ms"]
            && raw["version"] as? String=="1.0.0" && raw["scope"] as? String==scope
            && raw["kind"] as? String=="kakao_sdk_owner_binding" && raw["provider"] as? String=="kakao"
            && raw["bundle_identifier"] as? String==bundleID && kakaoSDKInteger(raw["app_id"])==appID
            && raw["session_ref"] as? String=="sha256:"+kakaoSDKHash(Data(bearer.utf8)))
        guard let nonce=raw["owner_nonce"] as? String,let digest=raw["owner_digest"] as? String else {throw WithdrawalNativeReviewError.held}
        let issued=try kakaoSDKInteger(raw["issued_ms"]),expires=try kakaoSDKInteger(raw["expires_ms"])
        try ownerRequire(ownerMatches(nonce,"^[A-Za-z0-9_-]{43}$") && ownerMatches(digest,"^[0-9a-f]{64}$")
            && issued<=kakaoSDKMilliseconds(now) && issued<expires && expires-issued<=56*86400000
            && expires==kakaoSDKMilliseconds(sessionExpiresAt))
        return KakaoSDKRetirementOwner(appID:appID,nonce:nonce,digest:digest)
    }

    public func verifyVaultForRetirement(_ data:Data,now:Date)throws->KakaoSDKRetirementOwner {
        let raw=try withdrawalFlatObject(data,maximumBytes:4096)
        try ownerRequire(Set(raw.keys)==["contract_version","session_token","expires_at","native_cleanup_proof"]
            && raw["contract_version"] as? String=="1.2.0-kakao-sdk-owner-review")
        guard let bearer=raw["session_token"] as? String,let expiry=raw["expires_at"] as? String,
            let envelope=raw["native_cleanup_proof"] as? String else {throw WithdrawalNativeReviewError.held}
        return try verifyForRetirement(Data(envelope.utf8),bearer:bearer,sessionExpiresAt:withdrawalUTCDate(expiry),now:now)
    }
}
