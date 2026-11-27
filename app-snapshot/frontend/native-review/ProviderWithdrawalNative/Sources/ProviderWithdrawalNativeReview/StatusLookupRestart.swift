import Foundation
import CoreFoundation
import CryptoKit

public struct WithdrawalLookupRestartPolicy: Sendable {
    let service: String, account: String, maximumRecordBytes: Int
    let operatingAccess = false
    public init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        let expected: [String: Any] = ["version":"1.0.0","scope":"isolated_native_checkpoint_review",
            "runtime_registered":false,"native_plugin_registered":false,"operating_secure_store_access_authorized":false,
            "operating_member_transport_authorized":false,"provider_live_calls_authorized":false,
            "automatic_retry":false,"whole_erasure_receipt":false,
            "vault_service":"com.miraylab.poppy.withdrawal-status-review",
            "vault_account":"skinanalysis.withdrawal.original-lookup.v1",
            "vault_accessibility":"when_unlocked_this_device_only","vault_synchronizable":false,
            "maximum_record_bytes":16384,"maximum_grant_seconds":300,
            "storage":"original_signed_lookup_envelope_and_monotonic_wall_clock_floor_only",
            "namespace":"single_original_operation_no_JS_login_vault_cookie_cache_or_app_group",
            "restore":"explicit_read_only_original_deadline_no_active_login_no_refresh_or_close",
            "concurrency":"single_process_main_actor_compare_and_confirm_not_OS_CAS",
            "failure":"unknown_storage_no_SDK_or_close_no_automatic_retry"]
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
        service = raw["vault_service"] as! String; account = raw["vault_account"] as! String
        maximumRecordBytes = (raw["maximum_record_bytes"] as! NSNumber).intValue
    }
}

public struct WithdrawalLookupStoreRequest: Sendable, Equatable {
    public let service: String, account: String, maximumDataBytes: Int
    public let accessibility = "when_unlocked_this_device_only", synchronizable = false
    public let authenticationUIAllowed = false, appGroupAccess = false
    init(_ policy: WithdrawalLookupRestartPolicy) {
        service = policy.service; account = policy.account; maximumDataBytes = policy.maximumRecordBytes
    }
}
public enum WithdrawalLookupStoreResult {
    case missing
    case found(data: Data, service: String, account: String, accessibility: String, synchronizable: Bool)
}
// Trusted native boundary. No JavaScript bridge implements this port. Exact
// compare/readback is a single-process main-actor guard, not an OS-wide CAS.
@MainActor public protocol WithdrawalLookupStorePort: AnyObject {
    func copy(_ request: WithdrawalLookupStoreRequest) throws -> WithdrawalLookupStoreResult
    func create(_ request: WithdrawalLookupStoreRequest, data: Data) throws
    func replace(_ request: WithdrawalLookupStoreRequest, expected: Data, replacement: Data) throws
    func remove(_ request: WithdrawalLookupStoreRequest, expected: Data) throws
}
public struct WithdrawalLookupReadAdmission: Sendable {
    public let now: Date, sceneActive: Bool, protectedDataAvailable: Bool
    public let authenticationInFlight: Bool, activeLoginSessionPresent: Bool
    public init(now: Date, sceneActive: Bool, protectedDataAvailable: Bool,
        authenticationInFlight: Bool, activeLoginSessionPresent: Bool) {
        self.now = now; self.sceneActive = sceneActive; self.protectedDataAvailable = protectedDataAvailable
        self.authenticationInFlight = authenticationInFlight; self.activeLoginSessionPresent = activeLoginSessionPresent
    }
}
private func lookupInteger(_ value: Any?) throws -> Int64 {
    guard let n = value as? NSNumber else { throw WithdrawalNativeReviewError.held }
    try ownerRequire(CFGetTypeID(n) != CFBooleanGetTypeID() && n.doubleValue.isFinite
        && n.doubleValue >= 0 && n.doubleValue <= 9007199254740991 && n.doubleValue.rounded(.down) == n.doubleValue)
    return n.int64Value
}
private func lookupMilliseconds(_ now: Date) throws -> Int64 {
    let ms = now.timeIntervalSince1970 * 1000
    try ownerRequire(ms.isFinite && ms >= 0 && ms <= 9007199254740991)
    return Int64(ms.rounded(.down))
}

// This composition is explicitly OFF for operating members. Synthetic native
// store fixtures can validate restart semantics; they are not OS persistence.
@MainActor public final class WithdrawalLookupRestartReview: CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    private struct Record {
        let envelope: Data, token: String, operation: UUID, deadline: Int64, floor: Int64
        let account: String, session: String, provider: String, sessionExpiry: String
    }
    private let policy: WithdrawalLookupRestartPolicy, statusConfiguration: Data, key: P256.Signing.PublicKey
    private let keyPin: String, url: URL, store: any WithdrawalLookupStorePort
    private let admission: () throws -> WithdrawalLookupReadAdmission, configuration: () -> URLSessionConfiguration
    private var attached = false, preparedRecord: Data?
    private let allowsKakao: Bool
    private let httpsReview: WithdrawalHTTPSReviewTransport?
    private let proofProfile: WithdrawalProofProfileReview?
    public convenience init(configuration: Data, statusConfiguration: Data, url: URL,
        publicKeyX963: Data, expectedKeySHA256: String, store: any WithdrawalLookupStorePort,
        deploymentContext: String, admission: @escaping () throws -> WithdrawalLookupReadAdmission,
        kakaoConfiguration: Data? = nil, proofProfile: WithdrawalProofProfileReview? = nil) throws {
        try self.init(configuration: configuration, statusConfiguration: statusConfiguration, url: url,
            publicKeyX963: publicKeyX963, expectedKeySHA256: expectedKeySHA256, store: store,
            deploymentContext: deploymentContext, admission: admission, sessionConfiguration: { .ephemeral }, kakaoConfiguration: kakaoConfiguration, proofProfile: proofProfile)
    }
    init(configuration: Data, statusConfiguration: Data, url: URL, publicKeyX963: Data,
        expectedKeySHA256: String, store: any WithdrawalLookupStorePort, deploymentContext: String,
        admission: @escaping () throws -> WithdrawalLookupReadAdmission,
        sessionConfiguration: @escaping () -> URLSessionConfiguration, kakaoConfiguration: Data? = nil,
        httpsReview: WithdrawalHTTPSReviewTransport? = nil, proofProfile: WithdrawalProofProfileReview? = nil) throws {
        try proofProfile?.requireKey(publicKeyX963)
        self.proofProfile = proofProfile
        policy = try WithdrawalLookupRestartPolicy(json: configuration)
        _ = try WithdrawalStatusHTTPPolicy(json: statusConfiguration)
        allowsKakao = try kakaoConfiguration.map { try WithdrawalClosureHTTPPolicy(json: $0).allowsKakao } ?? false
        if kakaoConfiguration != nil { try ownerRequire(allowsKakao) }
        _ = try WithdrawalHTTPReviewEndpoint(url: url, path: "lookup", method: "withdrawal_status_read",
            deploymentContext: deploymentContext, https: httpsReview, actualContext: proofProfile?.actualContext)
        try ownerRequire(SHA256.hash(data: publicKeyX963).map { String(format:"%02x",$0) }.joined() == expectedKeySHA256)
        key = try P256.Signing.PublicKey(x963Representation: publicKeyX963)
        self.keyPin = expectedKeySHA256; self.url = url; self.statusConfiguration = statusConfiguration
        self.store = store; self.admission = admission; self.configuration = sessionConfiguration
        self.httpsReview = httpsReview
    }
    public nonisolated var description: String { "WithdrawalLookupRestartReview(redacted)" }
    public nonisolated var debugDescription: String { description }
    public nonisolated var customMirror: Mirror { Mirror(self, children: [:]) }
    private func stored() throws -> Data? {
        switch try store.copy(WithdrawalLookupStoreRequest(policy)) {
        case .missing: return nil
        case let .found(data, service, account, accessibility, synchronizable):
            try ownerRequire(!data.isEmpty && data.count <= policy.maximumRecordBytes
                && service == policy.service && account == policy.account
                && accessibility == "when_unlocked_this_device_only" && !synchronizable)
            return data
        }
    }
    private func encode(_ envelope: Data, floor: Int64) throws -> Data {
        let data = try JSONSerialization.data(withJSONObject: ["version":"1.0.0",
            "signed_grant":envelope.base64EncodedString(),"last_admitted_ms":floor], options:.sortedKeys)
        try ownerRequire(data.count <= policy.maximumRecordBytes); return data
    }
    private func decode(_ bytes: Data, now: Date, allowExpired: Bool = false,
        trace: ((String) -> Void)? = nil) throws -> Record {
        trace?("checkpoint_record")
        let record = try withdrawalFlatObject(bytes, maximumBytes: policy.maximumRecordBytes)
        guard Set(record.keys) == ["version","signed_grant","last_admitted_ms"], record["version"] as? String == "1.0.0",
            let text = record["signed_grant"] as? String, let envelope = Data(base64Encoded: text) else { throw WithdrawalNativeReviewError.held }
        try ownerRequire(envelope.base64EncodedString() == text && envelope.count <= 8192)
        trace?("grant_envelope")
        let outer = try withdrawalFlatObject(envelope)
        guard Set(outer.keys) == ["version","scope","payload","signature"], outer["version"] as? String == "1.0.0",
            outer["scope"] as? String == withdrawalOperationProofScope(proofProfile), let p = outer["payload"] as? String,
            let s = outer["signature"] as? String, let payload = Data(base64Encoded: p), let sig = Data(base64Encoded: s) else { throw WithdrawalNativeReviewError.held }
        trace?("grant_signature")
        try ownerRequire(payload.count <= 4096 && payload.base64EncodedString() == p && sig.count == 64
            && sig.base64EncodedString() == s && key.isValidSignature(try P256.Signing.ECDSASignature(rawRepresentation:sig), for:payload))
        trace?("grant_fields")
        let raw = try withdrawalFlatObject(payload, maximumBytes:4096)
        let fields: Set<String> = ["version","scope","kind","request_id","account_ref","provider","session_ref",
            "session_expires_at","issued_ms","expires_ms","lookup_token","grant_expires_ms"]
        guard let token = raw["lookup_token"] as? String, let op = raw["request_id"] as? String, let operation = UUID(uuidString:op),
            let account = raw["account_ref"] as? String, let session = raw["session_ref"] as? String,
            let expiry = raw["session_expires_at"] as? String else { throw WithdrawalNativeReviewError.held }
        let issued = try lookupInteger(raw["issued_ms"]), proofExpires = try lookupInteger(raw["expires_ms"])
        let deadline = try lookupInteger(raw["grant_expires_ms"]), floor = try lookupInteger(record["last_admitted_ms"])
        let ms = try lookupMilliseconds(now)
        trace?("grant_lifetime")
        try ownerRequire(Set(raw.keys) == fields && raw["version"] as? String == "1.0.0"
            && raw["scope"] as? String == withdrawalOperationProofScope(proofProfile) && raw["kind"] as? String == "withdrawal_lookup_grant"
            && op == operation.uuidString.lowercased() && ownerMatches(account,"^sha256:[0-9a-f]{64}$")
            && ownerMatches(session,"^sha256:[0-9a-f]{64}$") && (allowsKakao ? ["apple","google","kakao"] : ["apple","google"]).contains(raw["provider"] as? String ?? "")
            && ownerMatches(token,"^[A-Za-z0-9_-]{43}$") && issued < proofExpires && proofExpires - issued <= 30000
            && proofExpires <= deadline && deadline - issued <= 300000 && deadline > issued
            && Double(deadline) <= withdrawalUTCDate(expiry).timeIntervalSince1970 * 1000
            && issued <= floor && floor <= ms && (allowExpired || ms < deadline))
        // The original 30-second issuance proof may be past after restart.
        // Its signed range is validated; only the original grant deadline is
        // live. This never makes preparation or account closure repeatable.
        return Record(envelope:envelope, token:token, operation:operation, deadline:deadline, floor:floor,
            account:account,session:session,provider:raw["provider"] as! String,sessionExpiry:expiry)
    }
    // OFF terminal cleanup stage, not a registered native/JS entry point.
    // The execution adapter must separately admit a frozen, same-owner purge
    // receipt and a fresh explicit cleanup operation. A signed lookup grant
    // binds the two local records; it is NOT evidence of account deletion.
    // All ports run synchronously on this main actor. This is not OS-wide CAS.
    func removeTerminalStoresForReview(expectedAccountFingerprint:String,expectedProvider:String,
        now:Date,vault:any WithdrawalNativeVaultReadPort,ownerPolicy:WithdrawalNativeOwnerPolicy,
        removeOriginalVault:(Data)throws->Bool)->[String:Any] {
        var result:[String:Any] = ["kind":"TERMINAL_LOCAL_STORE_STAGE_REVIEW",
            "stage":"original_records_unconfirmed","session_absent":false,"checkpoint_absent":false,
            "vault_delete_attempts":0,"checkpoint_delete_attempts":0,"network_calls":0,
            "provider_calls":0,"unknown_storage_action":false,"whole_erasure_verified":false]
        var writes=0
        func rawVault()throws->Data? {
            switch try vault.copy(WithdrawalNativeVaultRequest(policy:ownerPolicy)) {
            case .missing:return nil
            case let .found(data,service,account,accessibility,synchronizable):
                try ownerRequire(!data.isEmpty && data.count<=ownerPolicy.vaultBytes
                    && service==ownerPolicy.service && account==ownerPolicy.account
                    && accessibility==ownerPolicy.accessibility && !synchronizable)
                return data
            }
        }
        do {
            try ownerRequire(ownerMatches(expectedAccountFingerprint,"^[0-9a-f]{64}$")
                && ["apple","google","kakao"].contains(expectedProvider))
            let checkpoint=try stored(),login=try rawVault()
            if checkpoint==nil && login==nil {
                result["session_absent"]=true;result["checkpoint_absent"]=true
                result["stage"]="fixed_stores_already_absent";return result
            }
            guard let checkpoint else {throw WithdrawalNativeReviewError.held}
            let record=try decode(checkpoint,now:now,allowExpired:true)
            try ownerRequire(SHA256.hash(data:Data(record.account.utf8)).map{String(format:"%02x",$0)}.joined()==expectedAccountFingerprint
                && record.provider==expectedProvider && lookupMilliseconds(now)>=record.deadline)
            if login != nil {
                let credential=try withdrawalReadVault(vault,policy:ownerPolicy)
                try ownerRequire(record.session=="sha256:"+SHA256.hash(data:Data(credential.bearer.utf8)).map{String(format:"%02x",$0)}.joined()
                    && withdrawalUTCDate(record.sessionExpiry)==credential.expiresAt)
            }
            try ownerRequire(try stored()==checkpoint && rawVault()==login)
            if let login {
                result["vault_delete_attempts"]=1;writes+=1
                try ownerRequire(try removeOriginalVault(login))
                try ownerRequire(try rawVault()==nil)
            }
            result["session_absent"]=true
            // Never let a replacement checkpoint inherit the old operation.
            try ownerRequire(try stored()==checkpoint)
            result["checkpoint_delete_attempts"]=1;writes+=1
            try store.remove(WithdrawalLookupStoreRequest(policy),expected:checkpoint)
            try ownerRequire(try stored()==nil)
            result["checkpoint_absent"]=true;result["stage"]="two_fixed_stores_absent_not_whole_erasure"
        } catch {
            result["unknown_storage_action"]=writes>0
            result["stage"]=writes>0 ? "storage_action_unconfirmed_no_retry":"original_records_unconfirmed"
        }
        return result
    }
    // Explicit native diagnostic only. No network, identity lookup, writes,
    // expiry disposal or new preparation. Never return stored bytes or IDs.
    func inspectStoredForReview(now: Date, vault: (any WithdrawalNativeVaultReadPort)? = nil,
        ownerPolicy: WithdrawalNativeOwnerPolicy? = nil, observationWindow: ClosedRange<Int64>? = nil) -> [String: Any] {
        var stage="keychain_read",present=false,reads=0
        func read() throws -> Data? {reads += 1;return try stored()}
        do {
            guard let bytes=try read() else {
                return ["stage":"checkpoint_missing","present":false,"valid":false,"expired":false,"checkpoint_reads":reads]
            }
            present=true
            let record=try decode(bytes,now:now,allowExpired:true,trace:{stage=$0})
            stage="checkpoint_readback"
            try ownerRequire(try read() == bytes)
            var result: [String:Any] = ["stage":"checkpoint_valid","present":true,"valid":true,
                "expired":try lookupMilliseconds(now) >= record.deadline,"checkpoint_reads":reads]
            if let vault, let ownerPolicy, let observationWindow {
                result["login_vault_reads"]=1
                result["login_read_valid"]=false;result["same_session"]=false
                result["same_session_expiry"]=false;result["record_in_latest_attempt"]=false
                result["reader_assembly_valid"]=false
                result["expired_at_window_start"]=record.deadline<=observationWindow.lowerBound
                result["expired_at_window_end"]=record.deadline<=observationWindow.upperBound
                result["login_currently_unexpired"]=false
                let outer=try withdrawalFlatObject(record.envelope)
                guard let payload=outer["payload"] as? String, let raw=Data(base64Encoded:payload) else {throw WithdrawalNativeReviewError.held}
                result["record_in_latest_attempt"]=observationWindow.contains(try lookupInteger(withdrawalFlatObject(raw)["issued_ms"]))
                // Construction only. Never call readExplicit or admit this expired record.
                _ = try WithdrawalStatusReadClient(configuration:statusConfiguration,url:url,key:key,
                    grant:.init(token:record.token,operation:record.operation,expires:record.deadline),
                    sessionConfiguration:configuration,readAdmission:{throw WithdrawalNativeReviewError.held},
                    httpsReview:httpsReview,proofProfile:proofProfile)
                result["reader_assembly_valid"]=true
                do {
                    let credential=try withdrawalReadVault(vault,policy:ownerPolicy)
                    result["login_read_valid"]=true
                    result["login_currently_unexpired"]=now<credential.expiresAt
                    result["same_session"]=record.session == "sha256:" + SHA256.hash(data:Data(credential.bearer.utf8)).map {String(format:"%02x",$0)}.joined()
                    result["same_session_expiry"]=try withdrawalUTCDate(record.sessionExpiry) == credential.expiresAt
                } catch {result["stage"]="login_read"}
            }
            return result
        } catch {
            return ["stage":stage,"present":present,"valid":false,"expired":false,"checkpoint_reads":reads]
        }
    }
    public static func inspectActualTESTStoredForReview(configuration: Data,statusConfiguration: Data,
        httpsConfiguration: Data,proofProfileConfiguration: Data,
        actualContext:WithdrawalNativeActualTESTContext,store:any WithdrawalLookupStorePort,
        now:Date = Date(), vault: (any WithdrawalNativeVaultReadPort)? = nil,
        ownerConfiguration:Data? = nil, observationWindow:ClosedRange<Int64>? = nil) throws -> [String:Any] {
        try actualContext.requireWithdrawalReady()
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
        return inspector.inspectStoredForReview(now:now,vault:vault,
            ownerPolicy:try ownerConfiguration.map {try WithdrawalNativeOwnerPolicy(json:$0)},observationWindow:observationWindow)
    }
    private func admitted(originalEnvelope: Data) throws -> Date {
        let access = try admission()
        try ownerRequire(!Task.isCancelled && access.sceneActive && access.protectedDataAvailable
            && !access.authenticationInFlight && !access.activeLoginSessionPresent)
        guard let old = try stored() else { throw WithdrawalNativeReviewError.held }
        let record = try decode(old, now:access.now)
        try ownerRequire(record.envelope == originalEnvelope)
        let next = try encode(record.envelope, floor:lookupMilliseconds(access.now))
        if next != old {
            try store.replace(WithdrawalLookupStoreRequest(policy), expected:old, replacement:next)
        }
        try ownerRequire(try stored() == next && !Task.isCancelled)
        return access.now
    }
    private func savePrepared(_ envelope: Data, now: Date, replacingExpiredSameSession: Bool, trace:(String)->Void) throws {
        trace("checkpoint_new_grant")
        let bytes = try encode(envelope, floor:lookupMilliseconds(now))
        let next = try decode(bytes, now:now)
        try ownerRequire(!Task.isCancelled)
        trace("checkpoint_previous")
        if let previous = try stored() {
            // A separate explicit request may retire only an already expired,
            // verified record for the same authenticated session. Never renew
            // the old operation, replace a live/foreign record, or retry it.
            trace("checkpoint_old_identity")
            try ownerRequire(replacingExpiredSameSession)
            let old = try decode(previous, now:now, allowExpired:true)
            try ownerRequire(try lookupMilliseconds(now) >= old.deadline && old.operation != next.operation
                && old.account == next.account && old.session == next.session
                && old.provider == next.provider && old.sessionExpiry == next.sessionExpiry)
            trace("checkpoint_retire_memory")
            try store.remove(WithdrawalLookupStoreRequest(policy), expected:previous)
            try ownerRequire(try stored() == nil && !Task.isCancelled)
        }
        trace("checkpoint_create_memory")
        try store.create(WithdrawalLookupStoreRequest(policy), data:bytes)
        try ownerRequire(try stored() == bytes && !Task.isCancelled)
        preparedRecord = envelope
    }
    public func attachBeforePreparation(to original: WithdrawalNativeStatusLoopbackReview) throws {
        try attachBeforePreparation(to:original,replacingExpiredSameSession:false)
    }
    func attachBeforePreparation(to original: WithdrawalNativeStatusLoopbackReview,
        replacingExpiredSameSession: Bool, trace:@escaping (String)->Void = {_ in}) throws {
        try ownerRequire(!attached); attached = true
        try original.attachCheckpoint(keyPin:keyPin,url:url,save:{ [self] data, now in
            try savePrepared(data,now:now,replacingExpiredSameSession:replacingExpiredSameSession,trace:trace)
        },
            readAdmission:{ [self] in
                guard let envelope = preparedRecord else { throw WithdrawalNativeReviewError.held }
                return try admitted(originalEnvelope:envelope)
            }, proofProfile:proofProfile)
    }
    // Explicit expiry disposal, never a whole-deletion receipt. Invalid or
    // replaced records are not deleted. Original expiry is never extended.
    public func discardExpiredOriginalExplicit() throws -> Bool {
        let access = try admission()
        try ownerRequire(!Task.isCancelled && access.sceneActive && access.protectedDataAvailable
            && !access.authenticationInFlight && !access.activeLoginSessionPresent)
        guard let bytes = try stored() else { return false }
        let record = try decode(bytes, now:access.now, allowExpired:true)
        try ownerRequire(try lookupMilliseconds(access.now) >= record.deadline)
        try ownerRequire(try stored() == bytes)
        try store.remove(WithdrawalLookupStoreRequest(policy), expected:bytes)
        try ownerRequire(try stored() == nil && !Task.isCancelled)
        return true
    }
    public func restoreOriginalReadOnly() throws -> WithdrawalLookupReadOnlyReview {
        let access = try admission()
        try ownerRequire(!Task.isCancelled && access.sceneActive && access.protectedDataAvailable
            && !access.authenticationInFlight && !access.activeLoginSessionPresent)
        guard let bytes = try stored() else { throw WithdrawalNativeReviewError.held }
        let record = try decode(bytes, now:access.now)
        // This captures the original signed envelope, not a current login or
        // JavaScript operation identifier. A replaced record holds future reads.
        let client = try WithdrawalStatusReadClient(configuration:statusConfiguration, url:url, key:key,
            grant:.init(token:record.token,operation:record.operation,expires:record.deadline),
            sessionConfiguration:configuration,readAdmission:{ [self] in try admitted(originalEnvelope:record.envelope) },
            httpsReview: httpsReview, proofProfile: proofProfile)
        return WithdrawalLookupReadOnlyReview(client:client)
    }
}

@MainActor public protocol WithdrawalLookupReadOnlyPort: AnyObject {
    func readOriginalStatusExplicit() async throws -> WithdrawalNativeStatusReviewResult
}

// Deliberately has no preparation, challenge, credentials or close method.
@MainActor public final class WithdrawalLookupReadOnlyReview: WithdrawalLookupReadOnlyPort, CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    private let client: WithdrawalStatusReadClient
    init(client: WithdrawalStatusReadClient) { self.client = client }
    public func readOriginalStatusExplicit() async throws -> WithdrawalNativeStatusReviewResult { try await client.readExplicit() }
    public nonisolated var description: String { "WithdrawalLookupReadOnlyReview(redacted)" }
    public nonisolated var debugDescription: String { description }
    public nonisolated var customMirror: Mirror { Mirror(self, children: [:]) }
}
