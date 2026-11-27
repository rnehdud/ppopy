import Foundation
import CoreFoundation
import CryptoKit

struct WithdrawalClosureHTTPPolicy {
    let bounds: WithdrawalHTTPBounds
    let allowsKakao: Bool
    let accessTokenBytes: Int
    init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        var expected: [String: Any] = ["version":"1.0.0", "scope":"isolated_loopback_review",
            "runtime_registered":false,"native_plugin_registered":false,"operating_member_transport_authorized":false,
            "provider_live_calls_authorized":false,"actual_OS_member_attestation":false,"automatic_retry":false,"whole_erasure_receipt":false,
            "maximum_request_bytes":20480,"maximum_response_bytes":8192,"maximum_payload_bytes":4096,"maximum_response_chunks":64,
            "maximum_header_bytes":4096,"maximum_header_fields":20,"timeout_seconds":2,"maximum_proof_seconds":30,
            "methods":"withdrawal_challenge_or_withdrawal_close_only","url":"explicit_127.0.0.1_ephemeral_port_withdrawal_operation_only",
            "signature":"pinned_P256_SHA256_raw64_original_bearer_request_account_provider",
            "credential_storage":"invocation_memory_only_no_JS_logs_cookie_cache_or_vault_write",
            "failure":"retire_original_operation_unknown_ACK_never_resubmit",
            "result":"account_closure_and_provider_ACK_separate_whole_erasure_false"]
        allowsKakao = raw["methods"] as? String == "withdrawal_kakao_close_only"
        if allowsKakao {
            expected["methods"] = "withdrawal_kakao_close_only"
            expected["maximum_request_bytes"] = 4096
            expected["maximum_access_token_bytes"] = 2048
            expected["provider_contract"] = "original_server_kakao_binding_same_app_access_token_no_JWT_or_auth_code"
        }
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys) == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
        bounds = WithdrawalHTTPBounds(requestBytes: allowsKakao ? 4096 : 20480)
        accessTokenBytes = allowsKakao ? (raw["maximum_access_token_bytes"] as! NSNumber).intValue : 0
    }
}

// A single original verified owner, not a route registered for operating users.
@MainActor public final class WithdrawalNativeClosureLoopbackReview: WithdrawalNativeServerReviewPort, WithdrawalNativeSessionClosePort {
    private let owner: WithdrawalNativeVerifiedBindingOwner, key: P256.Signing.PublicKey, endpoint: WithdrawalHTTPReviewEndpoint, policy: WithdrawalClosureHTTPPolicy
    private let configuration: () -> URLSessionConfiguration
    private var requestID: UUID?, challengeUsed = false, closeUsed = false, busy = false, retired = false
    private let durablePolicy: WithdrawalDurableWirePolicy?
    private let proofProfile: WithdrawalProofProfileReview?
    private var durableCapability: WithdrawalDurableOperationCapability?
    public convenience init(configuration: Data, url: URL, deploymentContext: String,
        owner: WithdrawalNativeVerifiedBindingOwner, publicKeyX963: Data, expectedKeySHA256: String,
        proofProfile: WithdrawalProofProfileReview? = nil) throws {
        try self.init(configuration: configuration, url: url, deploymentContext: deploymentContext, owner: owner,
            publicKeyX963: publicKeyX963, expectedKeySHA256: expectedKeySHA256, sessionConfiguration: { .ephemeral }, proofProfile: proofProfile)
    }
    init(configuration: Data, url: URL, deploymentContext: String, owner: WithdrawalNativeVerifiedBindingOwner,
        publicKeyX963: Data, expectedKeySHA256: String, sessionConfiguration: @escaping () -> URLSessionConfiguration,
        httpsReview: WithdrawalHTTPSReviewTransport? = nil, durablePolicy: WithdrawalDurableWirePolicy? = nil,
        proofProfile: WithdrawalProofProfileReview? = nil) throws {
        try proofProfile?.requireKey(publicKeyX963)
        try owner.requireProofProfile(proofProfile,key:publicKeyX963)
        self.proofProfile = proofProfile
        self.durablePolicy = durablePolicy
        policy = try WithdrawalClosureHTTPPolicy(json: configuration)
        endpoint = try WithdrawalHTTPReviewEndpoint(url: url, path: "operation",
            method: policy.allowsKakao ? "withdrawal_kakao_close" : "withdrawal_close",
            deploymentContext: deploymentContext, https: httpsReview, actualContext: proofProfile?.actualContext)
        try ownerRequire(ownerMatches(expectedKeySHA256, "^[0-9a-f]{64}$")
            && SHA256.hash(data: publicKeyX963).map { String(format: "%02x", $0) }.joined() == expectedKeySHA256)
        key = try P256.Signing.PublicKey(x963Representation: publicKeyX963)
        self.owner = owner; self.configuration = sessionConfiguration
        let original = try owner.currentSession()
        try ownerRequire((original.provider == .kakao) == policy.allowsKakao)
    }
    func attachPreparedCapability(_ capability: WithdrawalDurableOperationCapability,
        original: WithdrawalNativeSession, requestID: UUID) throws {
        try ownerRequire(durablePolicy != nil && durableCapability == nil && self.requestID == nil
            && !busy && !retired && !challengeUsed && !closeUsed)
        _ = try capability.fields(owner:owner,original:original,request:requestID)
        durableCapability = capability
    }
    private func operationFields(original: WithdrawalNativeSession, requestID: UUID) throws -> [String: String] {
        guard durablePolicy != nil else { return [:] }
        guard let durableCapability else { throw WithdrawalNativeReviewError.held }
        return try durableCapability.fields(owner:owner,original:original,request:requestID)
    }
    private func current(_ original: WithdrawalNativeSession) throws -> WithdrawalNativeSession {
        try ownerRequire(!retired && !Task.isCancelled)
        let value = try owner.currentSession()
        try ownerRequire(value.accountRef == original.accountRef && value.provider == original.provider
            && value.bearer == original.bearer && value.generation == original.generation && value.expiresAt == original.expiresAt)
        return value
    }
    private func integer(_ value: Any?) throws -> Int64 {
        guard let n = value as? NSNumber else { throw WithdrawalNativeReviewError.held }
        try ownerRequire(CFGetTypeID(n) != CFBooleanGetTypeID() && n.doubleValue >= 0 && n.doubleValue <= 9007199254740991 && n.doubleValue.rounded(.down) == n.doubleValue)
        return n.int64Value
    }
    private func boolean(_ value: Any?) throws -> Bool {
        guard let n = value as? NSNumber, CFGetTypeID(n) == CFBooleanGetTypeID() else { throw WithdrawalNativeReviewError.held }
        return n.boolValue
    }
    private func signed(_ response: Data, original: WithdrawalNativeSession, request: UUID, kind: String, extra: Set<String>) throws -> [String: Any] {
        let outer = try withdrawalFlatObject(response)
        try ownerRequire(Set(outer.keys) == ["version","scope","payload","signature"] && outer["version"] as? String == "1.0.0" && outer["scope"] as? String == withdrawalOperationProofScope(proofProfile))
        guard let payloadString = outer["payload"] as? String, let sigString = outer["signature"] as? String,
            let payload = Data(base64Encoded: payloadString), let sig = Data(base64Encoded: sigString) else { throw WithdrawalNativeReviewError.held }
        try ownerRequire(payload.count <= 4096 && payload.base64EncodedString() == payloadString && sig.count == 64 && sig.base64EncodedString() == sigString
            && key.isValidSignature(try P256.Signing.ECDSASignature(rawRepresentation: sig), for: payload))
        let raw = try withdrawalFlatObject(payload, maximumBytes: 4096)
        let fields: Set<String> = ["version","scope","kind","request_id","account_ref","provider","session_ref","session_expires_at","issued_ms","expires_ms"]
        try ownerRequire(Set(raw.keys) == fields.union(extra) && raw["version"] as? String == "1.0.0" && raw["scope"] as? String == withdrawalOperationProofScope(proofProfile)
            && raw["kind"] as? String == kind && raw["request_id"] as? String == request.uuidString.lowercased()
            && raw["account_ref"] as? String == original.accountRef && raw["provider"] as? String == original.provider.rawValue
            && raw["session_ref"] as? String == "sha256:" + SHA256.hash(data: Data(original.bearer.utf8)).map { String(format: "%02x", $0) }.joined())
        guard let expiry = raw["session_expires_at"] as? String else { throw WithdrawalNativeReviewError.held }
        try ownerRequire(try withdrawalUTCDate(expiry) == original.expiresAt)
        let issued = try integer(raw["issued_ms"]), expires = try integer(raw["expires_ms"]), now = try current(original).now.timeIntervalSince1970 * 1000
        try ownerRequire(Double(issued) <= now && now < Double(expires) && issued < expires && expires - issued <= 30000
            && Double(expires) <= original.expiresAt.timeIntervalSince1970 * 1000)
        if durablePolicy != nil {
            _ = try operationFields(original:original,requestID:request)
            try durableCapability?.permits(milliseconds:expires)
        }
        return raw
    }
    private func exchange(_ body: Data, original: WithdrawalNativeSession) async throws -> Data {
        _ = try current(original)
        let raw = try withdrawalFlatObject(body, maximumBytes: policy.bounds.requestBytes)
        guard let method = raw["method"] as? String else { throw WithdrawalNativeReviewError.held }
        let flight = try endpoint.flight(method: method, bounds: policy.bounds, configuration: configuration())
        let response = try await withTaskCancellationHandler(operation: {
            try await withCheckedThrowingContinuation { flight.start(body: body, bearer: original.bearer, continuation: $0) }
        }, onCancel: { flight.cancel() })
        _ = try current(original); return response
    }
    public func issueAppleChallenge(original: WithdrawalNativeSession, requestID: UUID) async throws -> WithdrawalNativeChallenge {
        if busy { throw WithdrawalNativeReviewError.busy }
        do {
            _ = try current(original)
            try ownerRequire(original.provider == .apple && !challengeUsed && !closeUsed && self.requestID == nil)
            self.requestID = requestID; challengeUsed = true; busy = true; defer { busy = false }
            var fields = try operationFields(original:original,requestID:requestID)
            fields["method"] = "withdrawal_challenge"; fields["request_id"] = requestID.uuidString.lowercased()
            let body = try JSONSerialization.data(withJSONObject: fields, options: .sortedKeys)
            let raw = try signed(await exchange(body, original: original), original: original, request: requestID,
                kind: "withdrawal_challenge", extra: ["nonce","issued_at","expires_at"])
            guard let nonce = raw["nonce"] as? String, let issued = raw["issued_at"] as? String, let expires = raw["expires_at"] as? String else { throw WithdrawalNativeReviewError.held }
            try ownerRequire(ownerMatches(nonce, "^[A-Za-z0-9_-]{32,128}$"))
            let expiry = try withdrawalUTCDate(expires)
            try durableCapability?.permits(expiry)
            return WithdrawalNativeChallenge(accountRef: original.accountRef, requestID: requestID, nonce: nonce,
                issuedAt: try withdrawalUTCDate(issued), expiresAt: expiry)
        } catch { retired = true; durableCapability = nil; owner.retire(); throw WithdrawalNativeReviewError.held }
    }
    func closeOriginalSessionExplicit(original: WithdrawalNativeSession, requestID: UUID) async throws -> WithdrawalNativeLocalReceipt {
        if busy { throw WithdrawalNativeReviewError.busy }
        do {
            _ = try current(original)
            try ownerRequire(durablePolicy != nil && !closeUsed && !challengeUsed && self.requestID == nil)
            self.requestID = requestID; closeUsed = true; busy = true; defer { busy = false }
            var fields = try operationFields(original: original, requestID: requestID)
            fields["method"] = "withdrawal_session_close"; fields["request_id"] = requestID.uuidString.lowercased()
            let body = try JSONSerialization.data(withJSONObject: fields, options: .sortedKeys)
            try ownerRequire(body.count <= 512)
            let raw = try signed(await exchange(body, original: original), original: original, request: requestID,
                kind: "withdrawal_receipt", extra: ["account_closed","provider_acknowledged","whole_erasure"])
            try ownerRequire(try boolean(raw["account_closed"]) && !boolean(raw["provider_acknowledged"]) && !boolean(raw["whole_erasure"]))
            retired = true; durableCapability = nil
            return WithdrawalNativeLocalReceipt(accountRef: original.accountRef, requestID: requestID,
                accountClosed: true, providerAcknowledged: false, wholeErasure: false)
        } catch { retired = true; durableCapability = nil; owner.retire(); throw WithdrawalNativeReviewError.held }
    }
    public func closeAndRevokeExplicit(original: WithdrawalNativeSession, requestID: UUID,
        challenge: WithdrawalNativeChallenge?, credentials: WithdrawalNativeCredentials) async throws -> WithdrawalNativeLocalReceipt {
        if busy { throw WithdrawalNativeReviewError.busy }
        do {
            _ = try current(original)
            try ownerRequire(!closeUsed && credentials.request.operationID == requestID && credentials.request.provider == original.provider)
            if original.provider == .apple {
                try ownerRequire(challengeUsed && self.requestID == requestID && challenge?.requestID == requestID
                    && challenge?.accountRef == original.accountRef && credentials.request.nonce == challenge?.nonce)
            } else { try ownerRequire(!challengeUsed && self.requestID == nil && challenge == nil && credentials.request.nonce == nil); self.requestID = requestID }
            closeUsed = true; busy = true; defer { busy = false }
            let operation = try operationFields(original:original,requestID:requestID)
            let body: Data
            if original.provider == .kakao {
                try ownerRequire(policy.allowsKakao)
                body = try credentials.consumeKakaoInMemory { accessToken in
                    var raw = operation; raw["method"] = "withdrawal_kakao_close"
                    raw["request_id"] = requestID.uuidString.lowercased(); raw["access_token"] = accessToken
                    let body = try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
                    try ownerRequire(body.count <= policy.bounds.requestBytes); return body
                }
            } else {
                body = try credentials.consumeInMemory { token, code in
                    var raw = operation; raw["method"] = "withdrawal_close"
                    raw["request_id"] = requestID.uuidString.lowercased(); raw["id_token"] = token; raw["authorization_code"] = code
                    if let challenge { raw["nonce"] = challenge.nonce }
                    let body = try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
                    try ownerRequire(body.count <= policy.bounds.requestBytes); return body
                }
            }
            let raw = try signed(await exchange(body, original: original), original: original, request: requestID,
                kind: "withdrawal_receipt", extra: ["account_closed","provider_acknowledged","whole_erasure"])
            let closed = try boolean(raw["account_closed"]), acknowledged = try boolean(raw["provider_acknowledged"]), whole = try boolean(raw["whole_erasure"])
            try ownerRequire(closed && !whole)
            retired = true; durableCapability = nil
            return WithdrawalNativeLocalReceipt(accountRef: original.accountRef, requestID: requestID,
                accountClosed: closed, providerAcknowledged: acknowledged, wholeErasure: false)
        } catch { retired = true; durableCapability = nil; owner.retire(); throw WithdrawalNativeReviewError.held }
    }
}
