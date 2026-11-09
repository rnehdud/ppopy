import Foundation
import CoreFoundation

public enum WithdrawalNativeReviewError: Error, Equatable { case unavailable, busy, held, invalidBinding }
private func require(_ value: Bool) throws {
    if !value { throw WithdrawalNativeReviewError.unavailable }
}
private func matches(_ value: String, _ pattern: String) -> Bool {
    guard let range = value.range(of: pattern, options: .regularExpression) else { return false }
    return range.lowerBound == value.startIndex && range.upperBound == value.endIndex
}

// Bounded flat configuration. Decode keys before Foundation can discard duplicates.
func withdrawalFlatObject(_ data: Data, maximumBytes: Int = 8192) throws -> [String: Any] {
    try require(!data.isEmpty && data.count <= maximumBytes)
    let bytes = Array(data); var i = 0; var keys = Set<String>()
    func space() { while i < bytes.count && [9,10,13,32].contains(bytes[i]) { i += 1 } }
    func take(_ byte: UInt8) throws { space(); try require(i < bytes.count && bytes[i] == byte); i += 1 }
    func string() throws -> String {
        space(); let start = i; try take(34); var escaped = false
        while i < bytes.count {
            let byte = bytes[i]; i += 1
            if !escaped && byte == 34 {
                guard let value = try JSONSerialization.jsonObject(with: Data(bytes[start..<i]), options: .fragmentsAllowed) as? String else { throw WithdrawalNativeReviewError.unavailable }
                return value
            }
            escaped = !escaped && byte == 92
        }
        throw WithdrawalNativeReviewError.unavailable
    }
    try take(123)
    while true {
        let key = try string(); try require(keys.insert(key).inserted); try take(58); space()
        if i < bytes.count && bytes[i] == 34 { _ = try string() }
        else {
            let start = i
            while i < bytes.count && ![9,10,13,32,44,125].contains(bytes[i]) { i += 1 }
            let value = String(decoding: bytes[start..<i], as: UTF8.self)
            try require(value == "true" || value == "false" || matches(value, "^(0|[1-9][0-9]*)$"))
        }
        space()
        if i < bytes.count && bytes[i] == 125 { i += 1; space(); try require(i == bytes.count); break }
        try take(44)
    }
    guard let object = try JSONSerialization.jsonObject(with: data) as? [String: Any] else { throw WithdrawalNativeReviewError.unavailable }
    return object
}

public struct WithdrawalNativeReviewPolicy: Sendable {
    let codeAge: TimeInterval, challengeAge: TimeInterval, codeBytes: Int, tokenBytes: Int, bearerBytes: Int
    let allowsKakao: Bool
    let kakaoTokenBytes: Int
    public init(json: Data, kakaoConfiguration: Data? = nil) throws {
        let raw = try withdrawalFlatObject(json)
        let expected: [String: Any] = ["version":"1.0.0", "scope":"isolated_local_review",
            "runtime_registered":false, "native_plugin_registered":false,
            "actual_provider_authentication_authorized":false, "operating_member_transport_authorized":false,
            "automatic_retry":false, "whole_erasure_receipt":false,
            "credential_storage":"memory_only_no_logs_JS_or_vault_write",
            "maximum_code_age_seconds":30, "maximum_apple_challenge_seconds":300,
            "maximum_code_bytes":1024, "maximum_id_token_bytes":16384, "maximum_bearer_bytes":200]
        try require(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys) == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
        codeAge = (raw["maximum_code_age_seconds"] as! NSNumber).doubleValue
        challengeAge = (raw["maximum_apple_challenge_seconds"] as! NSNumber).doubleValue
        codeBytes = (raw["maximum_code_bytes"] as! NSNumber).intValue
        tokenBytes = (raw["maximum_id_token_bytes"] as! NSNumber).intValue
        bearerBytes = (raw["maximum_bearer_bytes"] as! NSNumber).intValue
        if let kakaoConfiguration {
            let kakao = try WithdrawalClosureHTTPPolicy(json: kakaoConfiguration)
            try require(kakao.allowsKakao)
            allowsKakao = true
            kakaoTokenBytes = kakao.accessTokenBytes
        } else { allowsKakao = false; kakaoTokenBytes = 0 }
    }
}

public enum WithdrawalNativeProvider: String, Sendable { case apple, google, kakao }

// Only a trusted native source may supply this snapshot; never a JS account/flag.
// This local-review port is not itself signed member attestation or OS verification.
public struct WithdrawalNativeSession: CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    let accountRef: String, bearer: String, provider: WithdrawalNativeProvider, generation: UUID
    let now: Date, expiresAt: Date, active: Bool, protectedDataAvailable: Bool
    public init(accountRef: String, bearer: String, provider: WithdrawalNativeProvider, generation: UUID,
                now: Date, expiresAt: Date, active: Bool, protectedDataAvailable: Bool) {
        self.accountRef = accountRef; self.bearer = bearer; self.provider = provider; self.generation = generation
        self.now = now; self.expiresAt = expiresAt; self.active = active; self.protectedDataAvailable = protectedDataAvailable
    }
    public var description: String { "WithdrawalNativeSession(redacted)" }
    public var debugDescription: String { description }
    public var customMirror: Mirror { Mirror(self, children: [:]) }
}
@MainActor public protocol WithdrawalNativeSessionPort: AnyObject {
    func currentSession() throws -> WithdrawalNativeSession
    func finishWithdrawal()
}
// Legacy synthetic snapshot ports have no OS/native owner to retire. Verified
// native owners override this terminal hook; operating ports remain OFF.
public extension WithdrawalNativeSessionPort { func finishWithdrawal() {} }

public struct WithdrawalNativeChallenge: CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    let accountRef: String, requestID: UUID, nonce: String, issuedAt: Date, expiresAt: Date
    public init(accountRef: String, requestID: UUID, nonce: String, issuedAt: Date, expiresAt: Date) {
        self.accountRef = accountRef; self.requestID = requestID; self.nonce = nonce
        self.issuedAt = issuedAt; self.expiresAt = expiresAt
    }
    public var description: String { "WithdrawalNativeChallenge(redacted)" }
    public var debugDescription: String { description }
    public var customMirror: Mirror { Mirror(self, children: [:]) }
}

// The coordinator creates the request; callback adapters must match this exact
// operation and, for Apple, the exact ASAuthorizationController identity too.
public struct WithdrawalNativeCaptureRequest: CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    public let provider: WithdrawalNativeProvider, operationID: UUID, nonce: String?
    private let originalOperation: @MainActor () throws -> Void
    fileprivate init(provider: WithdrawalNativeProvider, operationID: UUID, nonce: String?,
                     originalOperation: @escaping @MainActor () throws -> Void) {
        self.provider = provider; self.operationID = operationID; self.nonce = nonce; self.originalOperation = originalOperation
    }
    // The opaque request is minted inside the accepted coordinator. A callback
    // adapter can recheck its original owner/lease without learning identity.
    @MainActor public func checkOriginalOperation() throws { try originalOperation() }
    public var description: String { "WithdrawalNativeCaptureRequest(redacted)" }
    public var debugDescription: String { description }
    public var customMirror: Mirror { Mirror(self, children: [:]) }
}

// Credentials are opaque, non-Codable and one-use. Reflection/description omit
// their contents. Swift String copies are not a secure-memory erasure guarantee.
@MainActor public final class WithdrawalNativeCredentials: CustomStringConvertible, CustomDebugStringConvertible, CustomReflectable {
    let request: WithdrawalNativeCaptureRequest
    let capturedAt: Date
    private(set) var wasConsumed = false
    private var token: String?, code: String?, kakaoAccessToken: String?
    private var admission: (() throws -> Void)?
    public init(request: WithdrawalNativeCaptureRequest, callbackOperationID: UUID,
                idToken: String?, authorizationCode: String?, capturedAt: Date,
                policy: WithdrawalNativeReviewPolicy) throws {
        try require(request.operationID == callbackOperationID && request.provider != .kakao)
        try require(capturedAt.timeIntervalSince1970.isFinite)
        guard let idToken, let authorizationCode else { throw WithdrawalNativeReviewError.unavailable }
        try require(idToken.utf8.count <= policy.tokenBytes && matches(idToken, "^[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+$"))
        try require(authorizationCode.utf8.count <= policy.codeBytes
            && matches(authorizationCode, "^[A-Za-z0-9._~+/=-]{16,}$"))
        try require(request.provider == .apple ? request.nonce.map { matches($0, "^[A-Za-z0-9_-]{32,128}$") } == true : request.nonce == nil)
        self.request = request; self.capturedAt = capturedAt; token = idToken; code = authorizationCode
    }
    public init(request: WithdrawalNativeCaptureRequest, callbackOperationID: UUID,
                kakaoAccessToken: String?, capturedAt: Date, policy: WithdrawalNativeReviewPolicy) throws {
        try require(policy.allowsKakao && request.provider == .kakao && request.nonce == nil
            && request.operationID == callbackOperationID && capturedAt.timeIntervalSince1970.isFinite)
        guard let kakaoAccessToken else { throw WithdrawalNativeReviewError.unavailable }
        try require(kakaoAccessToken.utf8.count <= policy.kakaoTokenBytes && matches(kakaoAccessToken,"^[A-Za-z0-9._~+/=-]{20,}$"))
        self.request = request; self.capturedAt = capturedAt; self.kakaoAccessToken = kakaoAccessToken
    }
    public func consumeInMemory<T>(_ body: (String, String) throws -> T) throws -> T {
        guard let token, let code, let admission else { throw WithdrawalNativeReviewError.held }
        try admission()
        wasConsumed = true
        self.token = nil; self.code = nil // Latch before a caller can throw or lose an ACK.
        self.admission = nil
        return try body(token, code)
    }
    public func consumeKakaoInMemory<T>(_ body: (String) throws -> T) throws -> T {
        guard request.provider == .kakao, let kakaoAccessToken, let admission else { throw WithdrawalNativeReviewError.held }
        try admission(); wasConsumed = true
        self.kakaoAccessToken = nil; self.admission = nil
        return try body(kakaoAccessToken)
    }
    fileprivate func bindConsumption(_ check: @escaping () throws -> Void) throws {
        try require(admission == nil && !wasConsumed && (request.provider == .kakao
            ? kakaoAccessToken != nil && token == nil && code == nil : token != nil && code != nil && kakaoAccessToken == nil))
        admission = check
    }
    func discard() { token = nil; code = nil; kakaoAccessToken = nil; admission = nil }
    public nonisolated var description: String { "WithdrawalNativeCredentials(redacted)" }
    public nonisolated var debugDescription: String { description }
    public nonisolated var customMirror: Mirror { Mirror(self, children: [:]) }
}
@MainActor public protocol WithdrawalNativeSDKCapturePort: AnyObject {
    func captureExplicit(_ request: WithdrawalNativeCaptureRequest) async throws -> WithdrawalNativeCredentials
}

// Synthetic trusted response only. A real composition requires verified server
// binding, close+nonce claim+durable journal and reviewed ephemeral transport.
public struct WithdrawalNativeLocalReceipt {
    let accountRef: String, requestID: UUID, accountClosed: Bool, providerAcknowledged: Bool, wholeErasure: Bool
    public init(accountRef: String, requestID: UUID, accountClosed: Bool, providerAcknowledged: Bool, wholeErasure: Bool) {
        self.accountRef = accountRef; self.requestID = requestID; self.accountClosed = accountClosed
        self.providerAcknowledged = providerAcknowledged; self.wholeErasure = wholeErasure
    }
}
@MainActor public protocol WithdrawalNativeServerReviewPort: AnyObject {
    func issueAppleChallenge(original: WithdrawalNativeSession, requestID: UUID) async throws -> WithdrawalNativeChallenge
    func closeAndRevokeExplicit(original: WithdrawalNativeSession, requestID: UUID,
        challenge: WithdrawalNativeChallenge?, credentials: WithdrawalNativeCredentials) async throws -> WithdrawalNativeLocalReceipt
}

// Native construction selects this path. No JS option can select identity or
// turn a status read into closure; the original signed lookup is still required.
@MainActor protocol WithdrawalNativeSessionClosePort: AnyObject {
    func closeOriginalSessionExplicit(original: WithdrawalNativeSession, requestID: UUID) async throws -> WithdrawalNativeLocalReceipt
}

// Optional review composition prepares readback before any SDK capture/write.
// Its capability belongs to this exact operation, not a replacement login.
@MainActor public protocol WithdrawalNativeStatusPreparationPort: AnyObject {
    func prepareStatusLookup(original: WithdrawalNativeSession, requestID: UUID) async throws
}

public struct WithdrawalNativeLocalResult: Sendable {
    public let accountClosedInFixture: Bool, providerAcknowledgedInFixture: Bool
    public let SDKMemoryClearedInFixture: Bool
    public let SDKStorageErasureConfirmed = false, appVaultErasureConfirmed = false
    public let operationallyEligible = false, wholeErasure = false
}

@MainActor public final class WithdrawalNativeSDKCleanupGrant: CustomStringConvertible,
    CustomDebugStringConvertible, CustomReflectable {
    public let provider: WithdrawalNativeProvider, operationID: UUID
    private let issuedAt: Date, age: TimeInterval, originalOperation: @MainActor () throws -> Date
    private var used = false, validated = false
    fileprivate init(provider:WithdrawalNativeProvider,operationID:UUID,issuedAt:Date,age:TimeInterval,
                     originalOperation:@escaping @MainActor () throws -> Date) {
        self.provider=provider;self.operationID=operationID;self.issuedAt=issuedAt;self.age=age
        self.originalOperation=originalOperation
    }
    var wasVerified:Bool {validated}
    public func consumeOriginal() throws {
        try require(!used);used=true
        let now=try originalOperation()
        try require(now>=issuedAt && now.timeIntervalSince(issuedAt)<age)
        validated=true
    }
    public nonisolated var description:String {"WithdrawalNativeSDKCleanupGrant(redacted)"}
    public nonisolated var debugDescription:String {description}
    public nonisolated var customMirror:Mirror {Mirror(self,children:[:])}
}

// One explicit operation per original owner. Optional synthetic SDK memory
// cleanup follows a verified, durable provider ACK; no startup or retry.
// New accounts and a fresh native owner never inherit an old operation's result.
@MainActor public final class WithdrawalNativeReviewCoordinator {
    private let policy: WithdrawalNativeReviewPolicy
    private let session: any WithdrawalNativeSessionPort, sdk: any WithdrawalNativeSDKCapturePort
    private let server: any WithdrawalNativeServerReviewPort, original: WithdrawalNativeSession
    private let authenticationGate: NativeAuthOperationGate
    private let SDKCleanupPolicy: WithdrawalNativeSDKCleanupPolicy?
    private let originalSessionClosure: Bool
    let actualContext: WithdrawalNativeActualTESTContext?
    private var authenticationLease: NativeAuthOperationLease?
    private var lastTime: Date, busy = false, used = false, retired = false
    public init(policy: WithdrawalNativeReviewPolicy, session: any WithdrawalNativeSessionPort,
                sdk: any WithdrawalNativeSDKCapturePort, server: any WithdrawalNativeServerReviewPort,
                deploymentContext: String, authenticationGate: NativeAuthOperationGate = NativeAuthOperationGate(),
                SDKCleanupPolicy: WithdrawalNativeSDKCleanupPolicy? = nil, originalSessionClosure: Bool = false,
                actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        try requireWithdrawalNativeContext(deploymentContext,actualContext)
        if let actualContext {try require((session as? WithdrawalNativeVerifiedBindingOwner)?.actualContext === actualContext)}
        self.actualContext = actualContext
        let original = try session.currentSession()
        try require(original.provider != .kakao || policy.allowsKakao)
        try require(matches(original.accountRef, "^sha256:[0-9a-f]{64}$")
            && original.bearer.utf8.count <= policy.bearerBytes && matches(original.bearer, "^[A-Za-z0-9_-]{32,200}$")
            && original.now.timeIntervalSince1970.isFinite && original.expiresAt.timeIntervalSince1970.isFinite
            && original.now < original.expiresAt && original.active && original.protectedDataAvailable)
        self.policy = policy; self.session = session; self.sdk = sdk; self.server = server
        self.authenticationGate = authenticationGate
        self.SDKCleanupPolicy = SDKCleanupPolicy
        try require(!originalSessionClosure || server is any WithdrawalNativeSessionClosePort)
        self.originalSessionClosure = originalSessionClosure
        self.original = original; lastTime = original.now
    }
    public func retire() {
        retired = true
        if let authenticationLease { authenticationGate.invalidate(authenticationLease) }
    }
    private func current() throws -> Date {
        do {
            try require(!retired && !Task.isCancelled)
            if let authenticationLease { try authenticationGate.check(authenticationLease) }
            let value = try session.currentSession()
            try require(value.accountRef == original.accountRef && value.bearer == original.bearer
                && value.provider == original.provider && value.generation == original.generation
                && value.active && value.protectedDataAvailable && value.now.timeIntervalSince1970.isFinite
                && value.now >= lastTime && value.now < original.expiresAt
                && value.expiresAt == original.expiresAt)
            lastTime = value.now; return value.now
        } catch { retired = true; throw WithdrawalNativeReviewError.held }
    }
    public func withdrawExplicit() async throws -> WithdrawalNativeLocalResult {
        try actualContext?.requireWithdrawalReady()
        if busy { throw WithdrawalNativeReviewError.busy }
        if used || retired { throw WithdrawalNativeReviewError.held }
        _ = try current()
        // A competing login/withdrawal keeps the unstarted owner usable. An
        // accepted operation remains one-use even after an uncertain response.
        let lease: NativeAuthOperationLease
        do { lease = try authenticationGate.begin(.withdrawal) }
        catch { throw WithdrawalNativeReviewError.busy }
        authenticationLease = lease; used = true; busy = true
        defer { authenticationGate.finish(lease); authenticationLease = nil; busy = false }
        let requestID = UUID(); var captured: WithdrawalNativeCredentials?
        defer { captured?.discard() }
        do {
            if let readback = server as? any WithdrawalNativeStatusPreparationPort {
                try await readback.prepareStatusLookup(original: original, requestID: requestID)
                _ = try current()
            }
            if originalSessionClosure {
                guard let closer = server as? any WithdrawalNativeSessionClosePort,
                      server is any WithdrawalNativeStatusPreparationPort else { throw WithdrawalNativeReviewError.held }
                let receipt = try await closer.closeOriginalSessionExplicit(original: original, requestID: requestID)
                _ = try current()
                try require(receipt.accountRef == original.accountRef && receipt.requestID == requestID
                    && receipt.accountClosed && !receipt.providerAcknowledged && !receipt.wholeErasure)
                session.finishWithdrawal()
                return WithdrawalNativeLocalResult(accountClosedInFixture: true,
                    providerAcknowledgedInFixture: false, SDKMemoryClearedInFixture: false)
            }
            var challenge: WithdrawalNativeChallenge?
            if original.provider == .apple {
                let issued = try await server.issueAppleChallenge(original: original, requestID: requestID)
                let now = try current()
                try require(issued.accountRef == original.accountRef && issued.requestID == requestID
                    && matches(issued.nonce, "^[A-Za-z0-9_-]{32,128}$")
                    && issued.issuedAt.timeIntervalSince1970.isFinite && issued.expiresAt.timeIntervalSince1970.isFinite
                    && issued.issuedAt >= original.now && issued.issuedAt <= now && issued.expiresAt > now
                    && issued.expiresAt <= original.expiresAt
                    && issued.expiresAt.timeIntervalSince(issued.issuedAt) <= policy.challengeAge)
                challenge = issued
            }
            let authStartedAt = try current()
            let request = WithdrawalNativeCaptureRequest(provider: original.provider, operationID: requestID, nonce: challenge?.nonce,
                originalOperation: { [weak self] in
                    guard let self else { throw WithdrawalNativeReviewError.held }
                    _ = try self.current()
                })
            let value: WithdrawalNativeCredentials
            if let owner = session as? any WithdrawalNativeSDKPresentationOwnerPort {
                // Covers only this SDK capture, after nonce/readback and before
                // close HTTP. No vault read or closure is admitted inactive.
                try owner.beginSDKPresentation(requestID)
                defer { owner.endSDKPresentation(requestID) }
                try authenticationGate.beginSDKPresentation(lease)
                defer { authenticationGate.endSDKPresentation(lease) }
                value = try await sdk.captureExplicit(request)
            } else { value = try await sdk.captureExplicit(request) }
            captured = value
            let capturedAt = try current()
            try require(value.request.operationID == requestID && value.request.provider == original.provider
                && value.request.nonce == challenge?.nonce
                && value.capturedAt >= authStartedAt && value.capturedAt <= capturedAt)
            if let challenge { try require(capturedAt < challenge.expiresAt) }
            let beforeSubmit = try current()
            try require(beforeSubmit.timeIntervalSince(value.capturedAt) < policy.codeAge)
            let credentialCapturedAt = value.capturedAt
            try value.bindConsumption { [weak self] in
                guard let self else { throw WithdrawalNativeReviewError.held }
                let now = try self.current()
                try require(now.timeIntervalSince(credentialCapturedAt) < self.policy.codeAge)
                if let challenge { try require(now < challenge.expiresAt) }
            }
            // This single local port receives the original pre-closure context.
            // It must not look up a newly rotated bearer or retry an uncertain write.
            let receipt = try await server.closeAndRevokeExplicit(original: original, requestID: requestID,
                challenge: challenge, credentials: value)
            _ = try current()
            try require(value.wasConsumed && receipt.accountRef == original.accountRef && receipt.requestID == requestID
                && receipt.accountClosed && !receipt.wholeErasure)
            var memoryCleared = false
            if receipt.providerAcknowledged, let cleanupPolicy = SDKCleanupPolicy, cleanupPolicy.allows(original.provider),
               let cleanup = sdk as? any WithdrawalNativeSDKMemoryCleanupPort {
                let grant = WithdrawalNativeSDKCleanupGrant(provider:original.provider,operationID:requestID,
                    issuedAt:try current(),age:cleanupPolicy.grantAge,originalOperation:{[weak self] in
                        guard let self else {throw WithdrawalNativeReviewError.held}
                        return try self.current()
                    })
                // A cleanup failure never changes a verified closure into a
                // replayable withdrawal. Recheck owner before returning it.
                do {memoryCleared = try cleanup.clearOriginalAfterVerifiedACK(grant) == .memoryCleared && grant.wasVerified}
                catch {memoryCleared=false}
                _ = try current()
            }
            session.finishWithdrawal()
            return WithdrawalNativeLocalResult(accountClosedInFixture: true,
                providerAcknowledgedInFixture: receipt.providerAcknowledged,SDKMemoryClearedInFixture:memoryCleared)
        } catch {
            retired = true
            // This operation already acquired the authentication slot. SDK
            // cancellation/mismatched capture must retire its original native
            // owner even when no close HTTP request was dispatched. The busy
            // path above remains outside this accepted-operation failure hook.
            session.finishWithdrawal()
            throw WithdrawalNativeReviewError.held
        }
    }
}
