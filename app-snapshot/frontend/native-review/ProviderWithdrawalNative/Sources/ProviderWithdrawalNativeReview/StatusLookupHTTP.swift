import Foundation
import CoreFoundation
import CryptoKit

struct WithdrawalStatusHTTPPolicy {
    let bounds = WithdrawalHTTPBounds(requestBytes: 512)
    init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        let expected: [String: Any] = ["version":"1.0.0","scope":"isolated_loopback_review",
            "runtime_registered":false,"native_plugin_registered":false,"operating_member_transport_authorized":false,
            "provider_live_calls_authorized":false,"native_secure_persistence_connected":false,
            "automatic_retry":false,"whole_erasure_receipt":false,
            "maximum_request_bytes":512,"maximum_response_bytes":8192,"maximum_payload_bytes":4096,
            "maximum_response_chunks":64,"maximum_header_bytes":4096,"maximum_header_fields":20,
            "timeout_seconds":2,"maximum_proof_seconds":30,"maximum_grant_seconds":300,
            "methods":"prepare_original_operation_or_read_committed_status_only",
            "url":"explicit_127.0.0.1_ephemeral_port_withdrawal_lookup_only",
            "signature":"pinned_P256_SHA256_raw64_original_operation_lookup_digest_and_expiry",
            "storage":"native_invocation_memory_only_no_JS_logs_cookie_cache_or_login_vault_write",
            "failure":"unknown_prepare_no_close_unknown_close_read_only_never_resubmit"]
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
    }
}

public struct WithdrawalNativeStatusReviewResult: Sendable {
    public let accountClosedInRecord: Bool, providerAcknowledgedInRecord: Bool, providerState: String
    public let SDKCleanupConfirmed = false, wholeDeletionCompleted = false, operationallyEligible = false
}

// Construction is confined to this file, after exact signed-grant validation
// and confirmed checkpoint readback. A restored read client never owns this
// capability, and no public/JS port accepts a raw token to authorize writes.
@MainActor final class WithdrawalDurableOperationCapability: CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    private let token: String, operation: UUID, deadline: Int64
    private let original: WithdrawalNativeSession, ownerID: ObjectIdentifier
    fileprivate init(token: String, operation: UUID, deadline: Int64,
        original: WithdrawalNativeSession, owner: WithdrawalNativeVerifiedBindingOwner) {
        self.token = token; self.operation = operation; self.deadline = deadline
        self.original = original; ownerID = ObjectIdentifier(owner)
    }
    nonisolated var description: String { "WithdrawalDurableOperationCapability(redacted)" }
    nonisolated var debugDescription: String { description }
    nonisolated var customMirror: Mirror { Mirror(self, children: [:]) }
    func fields(owner: WithdrawalNativeVerifiedBindingOwner, original: WithdrawalNativeSession,
        request: UUID) throws -> [String: String] {
        let current = try owner.currentSession()
        try ownerRequire(!Task.isCancelled && ObjectIdentifier(owner) == ownerID && request == operation
            && current.accountRef == self.original.accountRef && current.provider == self.original.provider
            && current.bearer == self.original.bearer && current.generation == self.original.generation
            && current.expiresAt == self.original.expiresAt && current.now >= self.original.now
            && original.accountRef == self.original.accountRef && original.provider == self.original.provider
            && original.bearer == self.original.bearer && original.generation == self.original.generation
            && original.expiresAt == self.original.expiresAt && current.now.timeIntervalSince1970.isFinite
            && current.now.timeIntervalSince1970 * 1000 < Double(deadline))
        return ["lookup_token":token]
    }
    func permits(_ expiry: Date) throws {
        try ownerRequire(expiry.timeIntervalSince1970.isFinite && expiry.timeIntervalSince1970 * 1000 <= Double(deadline))
    }
    func permits(milliseconds: Int64) throws { try ownerRequire(milliseconds <= deadline) }
}

// Invocation-memory holder only. Secure OS persistence/restart/UI composition
// remains OFF. An explicit status read survives this original owner's disposal;
// it cannot capture credentials, close again, refresh a login or confirm erasure.
@MainActor public final class WithdrawalNativeStatusLoopbackReview: WithdrawalNativeServerReviewPort,
    WithdrawalNativeStatusPreparationPort, WithdrawalNativeSessionClosePort, CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    private struct Grant { let token: String, operation: UUID, expires: Int64 }
    private let owner: WithdrawalNativeVerifiedBindingOwner, closure: WithdrawalNativeClosureLoopbackReview
    private let key: P256.Signing.PublicKey, url: URL, policy: WithdrawalStatusHTTPPolicy
    private let endpoint: WithdrawalHTTPReviewEndpoint, httpsReview: WithdrawalHTTPSReviewTransport?
    private let configuration: () -> URLSessionConfiguration, readAdmission: () throws -> Date
    private var grant: Grant?, busy = false, prepareUsed = false, closeUsed = false
    private var reader: WithdrawalStatusReadClient?
    private var checkpoint: ((Data, Date) throws -> Void)?
    private var checkpointAttached = false
    private var checkpointReadAdmission: (() throws -> Date)?
    private let rawConfiguration: Data
    private let durablePolicy: WithdrawalDurableWirePolicy?
    private let proofProfile: WithdrawalProofProfileReview?
    func attachCheckpoint(keyPin: String, url: URL, save: @escaping (Data, Date) throws -> Void,
        readAdmission: @escaping () throws -> Date, proofProfile: WithdrawalProofProfileReview? = nil) throws {
        try ownerRequire(self.proofProfile == proofProfile)
        try ownerRequire(!busy && !prepareUsed && !checkpointAttached && self.url == url
            && SHA256.hash(data: key.x963Representation).map { String(format: "%02x", $0) }.joined() == keyPin)
        checkpointAttached = true; checkpoint = save; checkpointReadAdmission = readAdmission
    }
    public convenience init(configuration: Data, closureConfiguration: Data, url: URL,
        deploymentContext: String, owner: WithdrawalNativeVerifiedBindingOwner,
        publicKeyX963: Data, expectedKeySHA256: String, durableConfiguration: Data? = nil,
        proofProfile: WithdrawalProofProfileReview? = nil) throws {
        try self.init(configuration: configuration, closureConfiguration: closureConfiguration, url: url,
            deploymentContext: deploymentContext, owner: owner, publicKeyX963: publicKeyX963,
            expectedKeySHA256: expectedKeySHA256, sessionConfiguration: { .ephemeral }, readAdmission: { Date() },
            durableConfiguration: durableConfiguration, proofProfile: proofProfile)
    }
    init(configuration: Data, closureConfiguration: Data, url: URL, deploymentContext: String,
        owner: WithdrawalNativeVerifiedBindingOwner, publicKeyX963: Data, expectedKeySHA256: String,
        sessionConfiguration: @escaping () -> URLSessionConfiguration, readAdmission: @escaping () throws -> Date,
        httpsReview: WithdrawalHTTPSReviewTransport? = nil, durableConfiguration: Data? = nil,
        proofProfile: WithdrawalProofProfileReview? = nil) throws {
        try proofProfile?.requireKey(publicKeyX963)
        try owner.requireProofProfile(proofProfile,key:publicKeyX963)
        self.proofProfile = proofProfile
        durablePolicy = try durableConfiguration.map { try WithdrawalDurableWirePolicy(json: $0) }
        policy = try WithdrawalStatusHTTPPolicy(json: configuration)
        endpoint = try WithdrawalHTTPReviewEndpoint(url: url, path: "lookup", method: "withdrawal_lookup_prepare",
            deploymentContext: deploymentContext, https: httpsReview, actualContext: proofProfile?.actualContext)
        try ownerRequire(SHA256.hash(data: publicKeyX963).map { String(format: "%02x",$0) }.joined() == expectedKeySHA256)
        key = try P256.Signing.PublicKey(x963Representation: publicKeyX963)
        closure = try WithdrawalNativeClosureLoopbackReview(configuration: closureConfiguration,
            url: try httpsReview?.url(method: "withdrawal_close") ?? URL(string: "http://127.0.0.1:\(url.port!)/withdrawal/operation")!, deploymentContext: deploymentContext,
            owner: owner, publicKeyX963: publicKeyX963, expectedKeySHA256: expectedKeySHA256,
            sessionConfiguration: sessionConfiguration, httpsReview: httpsReview, durablePolicy: durablePolicy, proofProfile: proofProfile)
        self.owner = owner; self.url = url; self.configuration = sessionConfiguration; self.readAdmission = readAdmission; rawConfiguration = configuration
        self.httpsReview = httpsReview
    }
    public nonisolated var description: String { "WithdrawalNativeStatusLoopbackReview(redacted)" }
    public nonisolated var debugDescription: String { description }
    public nonisolated var customMirror: Mirror { Mirror(self, children: [:]) }
    private func integer(_ value: Any?) throws -> Int64 {
        guard let n = value as? NSNumber else { throw WithdrawalNativeReviewError.held }
        try ownerRequire(CFGetTypeID(n) != CFBooleanGetTypeID() && n.doubleValue >= 0 && n.doubleValue <= 9007199254740991
            && n.doubleValue.rounded(.down) == n.doubleValue)
        return n.int64Value
    }
    private func boolean(_ value: Any?) throws -> Bool {
        guard let n = value as? NSNumber, CFGetTypeID(n) == CFBooleanGetTypeID() else { throw WithdrawalNativeReviewError.held }
        return n.boolValue
    }
    private func decode(_ data: Data) throws -> [String: Any] {
        let outer = try withdrawalFlatObject(data)
        guard Set(outer.keys) == ["version","scope","payload","signature"], outer["version"] as? String == "1.0.0",
            outer["scope"] as? String == withdrawalOperationProofScope(proofProfile), let p = outer["payload"] as? String,
            let s = outer["signature"] as? String, let payload = Data(base64Encoded: p), let sig = Data(base64Encoded: s) else {
            throw WithdrawalNativeReviewError.held
        }
        try ownerRequire(payload.count <= 4096 && payload.base64EncodedString() == p && sig.count == 64
            && sig.base64EncodedString() == s && key.isValidSignature(try P256.Signing.ECDSASignature(rawRepresentation: sig), for: payload))
        return try withdrawalFlatObject(payload, maximumBytes: 4096)
    }
    private func proof(_ raw: [String: Any], request: UUID, kind: String, now: Date, deadline: Int64) throws {
        try ownerRequire(!Task.isCancelled && now.timeIntervalSince1970.isFinite
            && raw["version"] as? String == "1.0.0" && raw["scope"] as? String == withdrawalOperationProofScope(proofProfile)
            && raw["kind"] as? String == kind && raw["request_id"] as? String == request.uuidString.lowercased())
        let issued = try integer(raw["issued_ms"]), expires = try integer(raw["expires_ms"])
        let ms = now.timeIntervalSince1970 * 1000
        try ownerRequire(Double(issued) <= ms && ms < Double(expires) && issued < expires
            && expires - issued <= 30000 && expires <= deadline)
    }
    private func exchange(_ body: [String: String], bearer: String) async throws -> Data {
        let data = try JSONSerialization.data(withJSONObject: body, options: .sortedKeys)
        guard let method = body["method"] else { throw WithdrawalNativeReviewError.held }
        let flight = try endpoint.flight(method: method, bounds: policy.bounds, configuration: configuration())
        return try await withTaskCancellationHandler(operation: {
            try await withCheckedThrowingContinuation { flight.start(body: data, bearer: bearer, continuation: $0) }
        }, onCancel: { flight.cancel() })
    }
    private func current(_ original: WithdrawalNativeSession) throws -> WithdrawalNativeSession {
        let value = try owner.currentSession()
        try ownerRequire(!Task.isCancelled && value.accountRef == original.accountRef && value.provider == original.provider
            && value.bearer == original.bearer && value.generation == original.generation && value.expiresAt == original.expiresAt)
        return value
    }
    public func prepareStatusLookup(original: WithdrawalNativeSession, requestID: UUID) async throws {
        try await prepareStatusLookupDiagnosed(original:original,requestID:requestID)
    }
    func prepareStatusLookupDiagnosed(original: WithdrawalNativeSession, requestID: UUID,
        trace: (String)->Void = {_ in}) async throws {
        if busy { throw WithdrawalNativeReviewError.busy }
        try ownerRequire(!prepareUsed); prepareUsed = true; busy = true; defer { busy = false }
        do {
            if durablePolicy != nil { try ownerRequire(checkpointAttached && checkpoint != nil) }
            _ = try current(original)
            trace("lookup_response")
            let data = try await exchange(["method":"withdrawal_lookup_prepare","request_id":requestID.uuidString.lowercased()], bearer: original.bearer)
            trace("lookup_signature")
            let now = try current(original).now, raw = try decode(data)
            let fields: Set<String> = ["version","scope","kind","request_id","account_ref","provider","session_ref",
                "session_expires_at","issued_ms","expires_ms","lookup_token","grant_expires_ms"]
            guard let token = raw["lookup_token"] as? String, let expiry = raw["session_expires_at"] as? String else { throw WithdrawalNativeReviewError.held }
            let deadline = try integer(raw["grant_expires_ms"])
            trace("lookup_identity")
            try ownerRequire(Set(raw.keys) == fields && ownerMatches(token,"^[A-Za-z0-9_-]{43}$")
                && raw["account_ref"] as? String == original.accountRef && raw["provider"] as? String == original.provider.rawValue
                && raw["session_ref"] as? String == "sha256:" + SHA256.hash(data: Data(original.bearer.utf8)).map { String(format:"%02x",$0) }.joined()
                && withdrawalUTCDate(expiry) == original.expiresAt && Double(deadline) > now.timeIntervalSince1970 * 1000
                && Double(deadline) <= original.expiresAt.timeIntervalSince1970 * 1000
                && deadline - integer(raw["issued_ms"]) <= 300000)
            trace("lookup_lifetime")
            try proof(raw,request:requestID,kind:"withdrawal_lookup_grant",now:now,deadline:deadline)
            // Confirm local checkpoint bytes before publishing preparation or
            // permitting challenge/SDK/close. Ambiguous storage holds the flow.
            trace("checkpoint_admission")
            try checkpoint?(data, now)
            trace("lookup_owner")
            _ = try current(original)
            trace("reader_assembly")
            reader = try WithdrawalStatusReadClient(configuration: rawConfiguration, url: url, key: key,
                grant: .init(token: token, operation: requestID, expires: deadline),
                sessionConfiguration: self.configuration, readAdmission: checkpointReadAdmission ?? readAdmission,
                httpsReview: httpsReview, proofProfile: proofProfile)
            if durablePolicy != nil {
                trace("capability_attach")
                try closure.attachPreparedCapability(WithdrawalDurableOperationCapability(token:token,
                    operation:requestID,deadline:deadline,original:original,owner:owner), original:original, requestID:requestID)
            }
            grant = Grant(token:token,operation:requestID,expires:deadline)
            trace("preparation_complete")
        } catch { grant = nil; reader = nil; owner.retire(); throw WithdrawalNativeReviewError.held }
    }
    public func issueAppleChallenge(original: WithdrawalNativeSession, requestID: UUID) async throws -> WithdrawalNativeChallenge {
        if busy { throw WithdrawalNativeReviewError.busy }
        try ownerRequire(grant?.operation == requestID && !closeUsed)
        busy = true; defer { busy = false }
        return try await closure.issueAppleChallenge(original:original,requestID:requestID)
    }
    func closeOriginalSessionExplicit(original: WithdrawalNativeSession, requestID: UUID) async throws -> WithdrawalNativeLocalReceipt {
        if busy { throw WithdrawalNativeReviewError.busy }
        try ownerRequire(grant?.operation == requestID && !closeUsed && durablePolicy != nil); closeUsed = true
        busy = true; defer { busy = false }
        return try await closure.closeOriginalSessionExplicit(original: original, requestID: requestID)
    }
    public func closeAndRevokeExplicit(original: WithdrawalNativeSession, requestID: UUID,
        challenge: WithdrawalNativeChallenge?, credentials: WithdrawalNativeCredentials) async throws -> WithdrawalNativeLocalReceipt {
        if busy { throw WithdrawalNativeReviewError.busy }
        try ownerRequire(grant?.operation == requestID && !closeUsed); closeUsed = true
        busy = true; defer { busy = false }
        return try await closure.closeAndRevokeExplicit(original:original,requestID:requestID,challenge:challenge,credentials:credentials)
    }
    // Explicit read only. No active login owner, SDK capture or closure method is
    // called here; ambiguity/503 leaves the capability bounded and unchanged.
    public func readOriginalStatusExplicit() async throws -> WithdrawalNativeStatusReviewResult {
        if busy { throw WithdrawalNativeReviewError.busy }
        guard let reader else { throw WithdrawalNativeReviewError.held }
        busy = true; defer { busy = false }
        return try await reader.readExplicit()
    }
}

// The reusable reader has no original login owner, SDK or close port. A restart
// composition can only read a previously signed operation within its deadline.
@MainActor final class WithdrawalStatusReadClient {
    struct Grant { let token: String, operation: UUID, expires: Int64 }
    private let key: P256.Signing.PublicKey, url: URL, policy: WithdrawalStatusHTTPPolicy
    private let endpoint: WithdrawalHTTPReviewEndpoint
    private let configuration: () -> URLSessionConfiguration, readAdmission: () throws -> Date
    private let grant: Grant
    private let proofProfile: WithdrawalProofProfileReview?
    private var busy = false, lastRead: Date?
    init(configuration: Data, url: URL, key: P256.Signing.PublicKey, grant: Grant,
        sessionConfiguration: @escaping () -> URLSessionConfiguration, readAdmission: @escaping () throws -> Date,
        httpsReview: WithdrawalHTTPSReviewTransport? = nil, proofProfile: WithdrawalProofProfileReview? = nil) throws {
        try proofProfile?.requireKey(key.x963Representation)
        self.proofProfile = proofProfile
        self.policy = try WithdrawalStatusHTTPPolicy(json: configuration)
        endpoint = try WithdrawalHTTPReviewEndpoint(url: url, path: "lookup", method: "withdrawal_status_read",
            deploymentContext: proofProfile?.actualContext == nil ? "synthetic_test" : "actual_test_candidate",
            https: httpsReview, actualContext: proofProfile?.actualContext)
        self.key = key; self.url = url; self.grant = grant
        self.configuration = sessionConfiguration; self.readAdmission = readAdmission
    }
    func integer(_ value: Any?) throws -> Int64 {
        guard let n = value as? NSNumber else { throw WithdrawalNativeReviewError.held }
        try ownerRequire(CFGetTypeID(n) != CFBooleanGetTypeID() && n.doubleValue >= 0 && n.doubleValue <= 9007199254740991
            && n.doubleValue.rounded(.down) == n.doubleValue)
        return n.int64Value
    }
    func boolean(_ value: Any?) throws -> Bool {
        guard let n = value as? NSNumber, CFGetTypeID(n) == CFBooleanGetTypeID() else { throw WithdrawalNativeReviewError.held }
        return n.boolValue
    }
    func decode(_ data: Data) throws -> [String: Any] {
        let outer = try withdrawalFlatObject(data)
        guard Set(outer.keys) == ["version","scope","payload","signature"], outer["version"] as? String == "1.0.0",
            outer["scope"] as? String == withdrawalOperationProofScope(proofProfile), let p = outer["payload"] as? String,
            let s = outer["signature"] as? String, let payload = Data(base64Encoded: p), let sig = Data(base64Encoded: s) else {
            throw WithdrawalNativeReviewError.held
        }
        try ownerRequire(payload.count <= 4096 && payload.base64EncodedString() == p && sig.count == 64
            && sig.base64EncodedString() == s && key.isValidSignature(try P256.Signing.ECDSASignature(rawRepresentation: sig), for: payload))
        return try withdrawalFlatObject(payload, maximumBytes: 4096)
    }
    func proof(_ raw: [String: Any], request: UUID, kind: String, now: Date, deadline: Int64) throws {
        try ownerRequire(!Task.isCancelled && now.timeIntervalSince1970.isFinite
            && raw["version"] as? String == "1.0.0" && raw["scope"] as? String == withdrawalOperationProofScope(proofProfile)
            && raw["kind"] as? String == kind && raw["request_id"] as? String == request.uuidString.lowercased())
        let issued = try integer(raw["issued_ms"]), expires = try integer(raw["expires_ms"])
        let ms = now.timeIntervalSince1970 * 1000
        try ownerRequire(Double(issued) <= ms && ms < Double(expires) && issued < expires
            && expires - issued <= 30000 && expires <= deadline)
    }
    func exchange(_ body: [String: String], bearer: String) async throws -> Data {
        let data = try JSONSerialization.data(withJSONObject: body, options: .sortedKeys)
        guard let method = body["method"] else { throw WithdrawalNativeReviewError.held }
        let flight = try endpoint.flight(method: method, bounds: policy.bounds, configuration: configuration())
        return try await withTaskCancellationHandler(operation: {
            try await withCheckedThrowingContinuation { flight.start(body: data, bearer: bearer, continuation: $0) }
        }, onCancel: { flight.cancel() })
    }
    func readExplicit() async throws -> WithdrawalNativeStatusReviewResult {
        if busy { throw WithdrawalNativeReviewError.busy }
        busy = true; defer { busy = false }
        do {
            func admitted() throws -> Date {
                let now = try readAdmission()
                try ownerRequire(!Task.isCancelled && now.timeIntervalSince1970.isFinite
                    && now.timeIntervalSince1970 * 1000 < Double(grant.expires)
                    && (lastRead == nil || now >= lastRead!))
                lastRead = now; return now
            }
            _ = try admitted(); let request = UUID()
            let raw = try decode(await exchange(["method":"withdrawal_status_read","request_id":request.uuidString.lowercased(),
                "operation_ref":grant.operation.uuidString.lowercased()],bearer:grant.token))
            let now = try admitted()
            let fields: Set<String> = ["version","scope","kind","request_id","operation_ref","lookup_ref","grant_expires_ms",
                "issued_ms","expires_ms","account_closed","closure_state","provider_state","provider_acknowledged_in_record",
                "journal_record_present","read_at","SDK_cleanup_confirmed","whole_deletion_completed","automatic_retry","operationally_eligible"]
            try ownerRequire(Set(raw.keys) == fields && raw["operation_ref"] as? String == grant.operation.uuidString.lowercased()
                && raw["lookup_ref"] as? String == "sha256:" + SHA256.hash(data: Data(grant.token.utf8)).map { String(format:"%02x",$0) }.joined()
                && integer(raw["grant_expires_ms"]) == grant.expires)
            try proof(raw,request:request,kind:"withdrawal_status",now:now,deadline:grant.expires)
            let closed = try boolean(raw["account_closed"]), ack = try boolean(raw["provider_acknowledged_in_record"])
            let present = try boolean(raw["journal_record_present"])
            guard let state = raw["provider_state"] as? String, let readAt = raw["read_at"] as? String else { throw WithdrawalNativeReviewError.held }
            try ownerRequire(["NOT_RECORDED","CODE_EXCHANGE_RESERVED","REVOKE_RESERVED","UNCONFIRMED","ACKNOWLEDGED"].contains(state)
                && raw["closure_state"] as? String == (closed ? "CLOSED" : "NOT_RECORDED")
                && ack == (state == "ACKNOWLEDGED") && present == (state != "NOT_RECORDED")
                && (closed || state == "NOT_RECORDED") && withdrawalUTCDate(readAt) <= now)
            for flag in ["SDK_cleanup_confirmed","whole_deletion_completed","automatic_retry","operationally_eligible"] {
                try ownerRequire(try boolean(raw[flag]) == false)
            }
            return WithdrawalNativeStatusReviewResult(accountClosedInRecord:closed,providerAcknowledgedInRecord:ack,providerState:state)
        } catch { throw WithdrawalNativeReviewError.held }
    }
}
