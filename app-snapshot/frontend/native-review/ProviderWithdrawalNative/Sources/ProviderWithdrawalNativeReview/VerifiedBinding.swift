import Foundation
import CoreFoundation
import CryptoKit

struct WithdrawalBindingPolicy {
    let proofSeconds: Int64 = 300, requestBytes = 512, responseBytes = 8192, payloadBytes = 4096
    init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        var expected: [String: Any] = ["version":"1.0.0", "scope":"isolated_local_review",
            "runtime_registered":false, "native_plugin_registered":false,
            "operating_credential_access_authorized":false, "operating_member_transport_authorized":false,
            "actual_OS_member_attestation":false, "persistent_writes":false, "automatic_retry":false,
            "whole_erasure_receipt":false, "method":"withdrawal_binding", "account_role":"miray_app_account_service",
            "maximum_proof_seconds":300, "maximum_request_bytes":512, "maximum_response_bytes":8192,
            "maximum_payload_bytes":4096,
            "identity":"original_bearer_single_active_server_provider_binding_no_client_claims",
            "notice_requirement":"none_for_leaving_service",
            "credential_storage":"native_invocation_memory_only_no_JS_logs_or_vault_write",
            "signature":"pinned_P256_SHA256_raw64",
            "owner":"original_native_epoch_and_vault_before_after_await_terminal_on_failure"]
        // The server's explicit provider inventory is compatible with the
        // original v1 policy. Kakao native composition still requires the
        // separate explicit OFF Kakao wire policy at bootstrap.
        if raw["provider_binding_contract"] != nil {
            expected["provider_binding_contract"] = "apple_google_kakao_server_only"
        }
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
    }
}
private func bindingMS(_ date: Date) throws -> Int64 {
    let ms = date.timeIntervalSince1970 * 1000
    try ownerRequire(ms.isFinite && ms >= 0 && ms <= 9007199254740991)
    return Int64(ms.rounded(.down))
}
private func bindingInteger(_ value: Any?) throws -> Int64 {
    guard let number = value as? NSNumber else { throw WithdrawalNativeReviewError.held }
    try ownerRequire(CFGetTypeID(number) != CFBooleanGetTypeID() && number.doubleValue >= 0
        && number.doubleValue <= 9007199254740991 && number.doubleValue.rounded(.down) == number.doubleValue)
    return number.int64Value
}

// Trusted local port only. This does not authorize or implement operating HTTP,
// expose an account/provider claim to JS, or authenticate a provider SDK user.
@MainActor public protocol WithdrawalNativeBindingReviewPort: AnyObject {
    func originalBinding(bearer: String, body: Data) async throws -> Data
}

// The account/provider can enter this owner only through a pinned signed proof
// tied to the original native bearer and this native UUID. Its proof has its
// own short expiry; it cannot extend the original protection-session lifetime.
@MainActor public final class WithdrawalNativeVerifiedBindingOwner: WithdrawalNativeSessionPort, WithdrawalNativeSDKPresentationOwnerPort,
    CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    private let session: WithdrawalNativeVaultSession, epoch: WithdrawalNativeOwnerEpoch
    private let issued: Int64, expires: Int64
    private let proofProfile: WithdrawalProofProfileReview?, proofKey: Data
    var actualContext: WithdrawalNativeActualTESTContext? {proofProfile?.actualContext}
    func requireProofProfile(_ profile: WithdrawalProofProfileReview?, key: Data) throws {
        try ownerRequire(proofProfile == profile)
        if profile != nil { try ownerRequire(proofKey == key); try profile?.requireKey(key) }
    }
    private init(session: WithdrawalNativeVaultSession, epoch: WithdrawalNativeOwnerEpoch, issued: Int64, expires: Int64,
        proofProfile: WithdrawalProofProfileReview?, proofKey: Data) {
        self.proofProfile = proofProfile; self.proofKey = proofKey
        self.session = session; self.epoch = epoch; self.issued = issued; self.expires = expires
    }
    public func currentSession() throws -> WithdrawalNativeSession {
        do {
            let value = try session.currentSession(), now = try bindingMS(value.now)
            try ownerRequire(issued <= now && now < expires)
            return value
        } catch { epoch.signal(.disposed); throw WithdrawalNativeReviewError.held }
    }
    public func retire() { epoch.signal(.disposed) }
    public func finishWithdrawal() { retire() }
    func beginSDKPresentation(_ operation: UUID) throws {
        _ = try currentSession(); try session.beginSDKPresentation(operation)
    }
    func endSDKPresentation(_ operation: UUID) { session.endSDKPresentation(operation) }
    public nonisolated var description: String { "WithdrawalNativeVerifiedBindingOwner(redacted)" }
    public nonisolated var debugDescription: String { description }
    public nonisolated var customMirror: Mirror { Mirror(self, children: [:]) }

    public static func bootstrap(configuration: Data, ownerPolicy: WithdrawalNativeOwnerPolicy,
        epoch: WithdrawalNativeOwnerEpoch, vault: any WithdrawalNativeVaultReadPort,
        server: any WithdrawalNativeBindingReviewPort, publicKeyX963: Data, expectedKeySHA256: String,
        deploymentContext: String, authenticationGate: NativeAuthOperationGate,
        kakaoConfiguration: Data? = nil, proofProfile: WithdrawalProofProfileReview? = nil,
        preparationObserver:@MainActor (WithdrawalNativePreparationStage)->Void = {_ in}) async throws -> WithdrawalNativeVerifiedBindingOwner {
        try await bootstrapOriginal(configuration: configuration, ownerPolicy: ownerPolicy, epoch: epoch, vault: vault,
            server: server, publicKeyX963: publicKeyX963, expectedKeySHA256: expectedKeySHA256,
            deploymentContext: deploymentContext, authenticationGate: authenticationGate, requestID: UUID(), kakaoConfiguration: kakaoConfiguration, proofProfile: proofProfile, preparationObserver:preparationObserver)
    }
    // Internal seam fixes only the native UUID for cross-language synthetic proof
    // verification. The public entry point always generates its own UUID.
    static func bootstrapOriginal(configuration: Data, ownerPolicy: WithdrawalNativeOwnerPolicy,
        epoch: WithdrawalNativeOwnerEpoch, vault: any WithdrawalNativeVaultReadPort,
        server: any WithdrawalNativeBindingReviewPort, publicKeyX963: Data, expectedKeySHA256: String,
        deploymentContext: String, authenticationGate: NativeAuthOperationGate, requestID: UUID,
        kakaoConfiguration: Data? = nil, proofProfile: WithdrawalProofProfileReview? = nil,
        preparationObserver:@MainActor (WithdrawalNativePreparationStage)->Void = {_ in}) async throws -> WithdrawalNativeVerifiedBindingOwner {
        // A competing authentication cannot retire an unstarted owner's epoch.
        let lease: NativeAuthOperationLease
        do { lease = try authenticationGate.begin(.withdrawal) }
        catch { throw WithdrawalNativeReviewError.busy }
        defer { authenticationGate.finish(lease) }
        do {
            let policy = try WithdrawalBindingPolicy(json: configuration)
            let allowsKakao = try kakaoConfiguration.map { try WithdrawalClosureHTTPPolicy(json: $0).allowsKakao } ?? false
            if kakaoConfiguration != nil { try ownerRequire(allowsKakao) }
            try requireWithdrawalNativeContext(deploymentContext,proofProfile?.actualContext)
            try ownerRequire(ownerMatches(expectedKeySHA256, "^[0-9a-f]{64}$")
                && SHA256.hash(data: publicKeyX963).map { String(format: "%02x", $0) }.joined() == expectedKeySHA256)
            try proofProfile?.requireKey(publicKeyX963)
            let key = try P256.Signing.PublicKey(x963Representation: publicKeyX963)
            let original = try epoch.snapshot()
            func current() throws -> WithdrawalNativeEpochSnapshot {
                try ownerRequire(!Task.isCancelled); try authenticationGate.check(lease)
                let now = try epoch.snapshot(); try ownerRequire(now.generation == original.generation)
                _ = try bindingMS(now.now); return now
            }
            _ = try current()
            preparationObserver(.readingVault)
            let credential = try withdrawalReadVault(vault, policy: ownerPolicy)
            try ownerRequire(try current().now < credential.expiresAt)
            let body = try JSONSerialization.data(withJSONObject: ["method":"withdrawal_binding",
                "request_id":requestID.uuidString.lowercased()], options: .sortedKeys)
            try ownerRequire(body.count <= policy.requestBytes)
            preparationObserver(.fetchingBinding)
            let response = try await server.originalBinding(bearer: credential.bearer, body: body)
            _ = try current()
            let final = try withdrawalReadVault(vault, policy: ownerPolicy)
            let now = try current()
            try ownerRequire(final.bearer == credential.bearer && final.expiresAt == credential.expiresAt && now.now < final.expiresAt)
            preparationObserver(.validatingBinding)
            let outer = try withdrawalFlatObject(response, maximumBytes: policy.responseBytes)
            try ownerRequire(Set(outer.keys) == ["version", "scope", "payload", "signature"]
                && outer["version"] as? String == "1.0.0" && outer["scope"] as? String == withdrawalBindingProofScope(proofProfile))
            guard let payloadString = outer["payload"] as? String, let signatureString = outer["signature"] as? String,
                let payload = Data(base64Encoded: payloadString), let signature = Data(base64Encoded: signatureString) else { throw WithdrawalNativeReviewError.held }
            try ownerRequire(payload.base64EncodedString() == payloadString && signature.base64EncodedString() == signatureString
                && !payload.isEmpty && payload.count <= policy.payloadBytes && signature.count == 64)
            try ownerRequire(key.isValidSignature(try P256.Signing.ECDSASignature(rawRepresentation: signature), for: payload))
            let raw = try withdrawalFlatObject(payload, maximumBytes: policy.payloadBytes)
            try ownerRequire(Set(raw.keys) == ["version", "scope", "kind", "request_id", "account_ref", "provider",
                "session_ref", "session_expires_at", "issued_ms", "expires_ms"]
                && raw["version"] as? String == "1.0.0" && raw["scope"] as? String == withdrawalBindingProofScope(proofProfile)
                && raw["kind"] as? String == "withdrawal_binding" && raw["request_id"] as? String == requestID.uuidString.lowercased())
            guard let account = raw["account_ref"] as? String, let providerString = raw["provider"] as? String,
                let provider = WithdrawalNativeProvider(rawValue: providerString), let expiry = raw["session_expires_at"] as? String else { throw WithdrawalNativeReviewError.held }
            try ownerRequire(provider != .kakao || allowsKakao)
            try ownerRequire(ownerMatches(account, "^sha256:[0-9a-f]{64}$")
                && raw["session_ref"] as? String == "sha256:" + SHA256.hash(data: Data(credential.bearer.utf8)).map { String(format: "%02x", $0) }.joined()
                && (try withdrawalUTCDate(expiry)) == credential.expiresAt)
            let issued = try bindingInteger(raw["issued_ms"]), expires = try bindingInteger(raw["expires_ms"])
            let finalTime = try bindingMS(current().now)
            try ownerRequire(issued <= finalTime && finalTime < expires && expires > issued
                && expires - issued <= policy.proofSeconds * 1000 && expires <= bindingMS(credential.expiresAt))
            let binding = WithdrawalNativeSession(accountRef: account, bearer: credential.bearer, provider: provider,
                generation: original.generation, now: now.now, expiresAt: credential.expiresAt, active: true, protectedDataAvailable: true)
            let owner = WithdrawalNativeVerifiedBindingOwner(session: try WithdrawalNativeVaultSession(policy: ownerPolicy,
                epoch: epoch, vault: vault, originalServerBinding: binding, deploymentContext: deploymentContext,
                actualContext: proofProfile?.actualContext),
                epoch: epoch, issued: issued, expires: expires, proofProfile: proofProfile, proofKey: publicKeyX963)
            _ = try owner.currentSession(); preparationObserver(.bindingVerified); return owner
        } catch { epoch.signal(.disposed); throw WithdrawalNativeReviewError.held }
    }
}
