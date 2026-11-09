import Foundation
import CoreFoundation
import CryptoKit

public enum PublicSessionError: Error, Equatable { case invalid }
private func requireSession(_ condition: Bool) throws { if !condition { throw PublicSessionError.invalid } }
private func sessionMatches(_ s: String, _ pattern: String) -> Bool {
    guard let r = s.range(of: pattern, options: .regularExpression) else { return false }; return r.lowerBound == s.startIndex && r.upperBound == s.endIndex
}
private func sessionHash(_ d: Data) -> String { SHA256.hash(data: d).map { String(format: "%02x", $0) }.joined() }
// Neutral bounded-flat parser: decode key spelling before Foundation discards
// duplicates. No TEST context, proof profile or capability is imported.
private func sessionObject(_ data: Data, max: Int) throws -> [String: Any] {
    try requireSession(!data.isEmpty && data.count <= max)
    let bytes = Array(data); var i = 0; var keys = Set<String>()
    func space() { while i < bytes.count && [9, 10, 13, 32].contains(bytes[i]) { i += 1 } }
    func take(_ b: UInt8) throws { space(); try requireSession(i < bytes.count && bytes[i] == b); i += 1 }
    func string() throws -> String {
        space(); let start = i; try take(34); var escaped = false
        while i < bytes.count {
            let b = bytes[i]; i += 1
            if !escaped && b == 34 {
                guard let s = try JSONSerialization.jsonObject(with: Data(bytes[start..<i]), options: .fragmentsAllowed) as? String else { throw PublicSessionError.invalid }; return s
            }; escaped = !escaped && b == 92
        }; throw PublicSessionError.invalid
    }
    try take(123)
    while true {
        let k = try string(); try requireSession(keys.insert(k).inserted); try take(58); space()
        if i < bytes.count && bytes[i] == 34 { _ = try string() }
        else {
            let start = i; while i < bytes.count && ![9, 10, 13, 32, 44, 125].contains(bytes[i]) { i += 1 }
            let s = String(decoding: bytes[start..<i], as: UTF8.self)
            try requireSession(s == "true" || s == "false" || sessionMatches(s, "^(0|[1-9][0-9]*)$"))
        }
        space(); if i < bytes.count && bytes[i] == 125 { i += 1; space(); try requireSession(i == bytes.count); break }; try take(44)
    }
    guard let d = try JSONSerialization.jsonObject(with: data) as? [String: Any] else { throw PublicSessionError.invalid }; return d
}
private func sessionInteger(_ v: Any?) throws -> Int64 {
    guard let n = v as? NSNumber, CFGetTypeID(n) != CFBooleanGetTypeID() else { throw PublicSessionError.invalid }
    let d = n.doubleValue; try requireSession(d.isFinite && d >= 0 && d <= 9007199254740991 && d.rounded(.down) == d); return n.int64Value
}
private func nowMillis(_ date: Date) throws -> Int64 {
    let n = date.timeIntervalSince1970 * 1000; try requireSession(n.isFinite && n >= 0 && n <= 9007199254740991); return Int64(n.rounded(.down))
}
private func expiryMillis(_ s: String) throws -> Int64 {
    try requireSession(sessionMatches(s, "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\\.[0-9]{1,6})?(Z|\\+00:00)$"))
    let base = String(s.prefix(19)), f = DateFormatter(); f.locale = Locale(identifier: "en_US_POSIX"); f.calendar = Calendar(identifier: .iso8601)
    f.timeZone = TimeZone(secondsFromGMT: 0); f.dateFormat = "yyyy-MM-dd'T'HH:mm:ss"; f.isLenient = false
    guard let date = f.date(from: base), f.string(from: date) == base else { throw PublicSessionError.invalid }
    let suffix = String(s.dropFirst(19)); let fraction = suffix.hasPrefix(".") ? String(suffix.dropFirst().prefix(while: { $0.isNumber })) : ""
    let millis = Int64(String((fraction + "000").prefix(3)))!
    let seconds = date.timeIntervalSince1970; try requireSession(seconds.isFinite && seconds >= 0)
    return Int64(seconds) * 1000 + millis
}
private func ownerDigest(_ parts: [String]) -> String {
    var value = Data(); for part in parts { let d = Data(part.utf8); var n = UInt32(d.count).bigEndian; Swift.withUnsafeBytes(of: &n) { value.append(contentsOf: $0) }; value.append(d) }; return sessionHash(value)
}
public enum PublicSessionProvider: String, Sendable { case google, kakao }

/// Verification result only, not authority to mutate Keychain, provider SDK,
/// server accounts or provider connections. Native host must still compare its
/// exact current record and SDK snapshot at the actual mutation boundary.
public struct PublicSessionProof: Sendable, CustomStringConvertible, CustomDebugStringConvertible {
    private let record: String, bearer: String, provider: PublicSessionProvider?, client: String, app: Int64, nonce: String, digest: String
    public let expired: Bool
    public var SDKProvider: PublicSessionProvider? { provider }
    public var description: String { "<PublicSessionProof redacted>" }; public var debugDescription: String { description }
    fileprivate init(record: Data, token: String, provider: PublicSessionProvider?, client: String, app: Int64, nonce: String, digest: String, expired: Bool) {
        self.record = sessionHash(record); bearer = sessionHash(Data(token.utf8)); self.provider = provider; self.client = client
        self.app = app; self.nonce = nonce; self.digest = digest; self.expired = expired
    }
    public func matchesOriginalRecord(_ data: Data) -> Bool { data.count <= 4096 && sessionHash(data) == record }
    public func matchesBearer(_ token: String) -> Bool { sessionMatches(token, "^[A-Za-z0-9_-]{32,200}$") && sessionHash(Data(token.utf8)) == bearer }
    public func matchesGoogleSubject(_ subject: String) throws -> Bool {
        try requireSession(!subject.isEmpty && subject.utf8.count <= 512)
        return provider == .google && ownerDigest(["poppy-google-sdk-owner-v1", client, nonce, subject]) == digest
    }
    public func matchesKakaoAccessToken(_ token: String) throws -> Bool {
        try requireSession(sessionMatches(token, "^[A-Za-z0-9._~+/=-]{20,2048}$"))
        return provider == .kakao && ownerDigest(["poppy-kakao-sdk-owner-v1", String(app), nonce, sessionHash(Data(token.utf8))]) == digest
    }
}

public struct PublicSessionVerifier: Sendable {
    private let googleKey: P256.Signing.PublicKey, kakaoKey: P256.Signing.PublicKey, clientID: String, appID: Int64
    public init(googlePublicX963: Data, googleSHA256: String, kakaoPublicX963: Data, kakaoSHA256: String, googleClientID: String, kakaoAppID: Int64) throws {
        try requireSession(googlePublicX963.count == 65 && kakaoPublicX963.count == 65 && googlePublicX963.first == 4 && kakaoPublicX963.first == 4
            && sessionMatches(googleSHA256, "^[a-f0-9]{64}$") && sessionMatches(kakaoSHA256, "^[a-f0-9]{64}$") && googleSHA256 != kakaoSHA256
            && sessionHash(googlePublicX963) == googleSHA256 && sessionHash(kakaoPublicX963) == kakaoSHA256
            && sessionMatches(googleClientID, "^[0-9]+-[a-z0-9]+\\.apps\\.googleusercontent\\.com$") && kakaoAppID > 0 && kakaoAppID <= 9007199254740991)
        do { googleKey = try P256.Signing.PublicKey(x963Representation: googlePublicX963); kakaoKey = try P256.Signing.PublicKey(x963Representation: kakaoPublicX963) }
        catch { throw PublicSessionError.invalid }; clientID = googleClientID; appID = kakaoAppID
    }
    public func verifyForStorage(_ record: Data, now: Date) throws -> PublicSessionProof { try verify(record, now: now, retirement: false) }
    public func verifyForRetirement(_ record: Data, now: Date) throws -> PublicSessionProof { try verify(record, now: now, retirement: true) }
    private func verify(_ record: Data, now: Date, retirement: Bool) throws -> PublicSessionProof {
        do { return try checked(record, now: now, retirement: retirement) } catch { throw PublicSessionError.invalid }
    }
    private func checked(_ record: Data, now: Date, retirement: Bool) throws -> PublicSessionProof {
        let r = try sessionObject(record, max: 4096), at = try nowMillis(now)
        guard let version = r["contract_version"] as? String, let token = r["session_token"] as? String, let expiry = r["expires_at"] as? String else { throw PublicSessionError.invalid }
        let provider: PublicSessionProvider? = version == "1.0.0-public-google-session" ? .google : version == "1.0.0-public-kakao-session" ? .kakao : nil
        let expected: Set<String> = Set(["contract_version", "environment", "purpose", "session_token", "expires_at"] + (provider != nil ? ["native_cleanup_proof"] : []))
        try requireSession(Set(r.keys) == expected && r["environment"] as? String == "production" && r["purpose"] as? String == "public_app_session"
            && (provider != nil || version == "1.0.0-public-session") && sessionMatches(token, "^[A-Za-z0-9_-]{32,200}$"))
        let expires = try expiryMillis(expiry), maximum: Int64 = 56 * 86400000
        try requireSession((retirement || expires > at) && expires <= at + maximum + 30000)
        var nonce = "", digest = ""
        if let provider {
            guard let text = r["native_cleanup_proof"] as? String else { throw PublicSessionError.invalid }
            let e = try sessionObject(Data(text.utf8), max: 2048), scope = "poppy_public_v1_binding_\(provider.rawValue)_sdk_owner"
            try requireSession(Set(e.keys) == ["version", "scope", "payload", "signature"] && e["version"] as? String == "1.0.0" && e["scope"] as? String == scope)
            guard let b64 = e["payload"] as? String, let sig64 = e["signature"] as? String, let payload = Data(base64Encoded: b64), let sig = Data(base64Encoded: sig64) else { throw PublicSessionError.invalid }
            try requireSession(payload.base64EncodedString() == b64 && sig.base64EncodedString() == sig64 && payload.count <= 1536 && sig.count == 64)
            let key = provider == .google ? googleKey : kakaoKey
            try requireSession(key.isValidSignature(try P256.Signing.ECDSASignature(rawRepresentation: sig), for: payload))
            let p = try sessionObject(payload, max: 1536), field = provider == .google ? "client_id" : "app_id"
            try requireSession(Set(p.keys) == ["version", "scope", "kind", "provider", "bundle_identifier", field, "session_ref", "owner_nonce", "owner_digest", "issued_ms", "expires_ms"]
                && p["version"] as? String == "1.0.0" && p["scope"] as? String == scope && p["provider"] as? String == provider.rawValue
                && p["kind"] as? String == "\(provider.rawValue)_sdk_owner_binding" && p["bundle_identifier"] as? String == "com.miraylab.poppy"
                && p["session_ref"] as? String == "sha256:" + sessionHash(Data(token.utf8)))
            if provider == .google { try requireSession(p["client_id"] as? String == clientID) } else { try requireSession(try sessionInteger(p["app_id"]) == appID) }
            guard let n = p["owner_nonce"] as? String, let d = p["owner_digest"] as? String else { throw PublicSessionError.invalid }
            let issued = try sessionInteger(p["issued_ms"]), end = try sessionInteger(p["expires_ms"])
            let nonce64 = n.replacingOccurrences(of: "-", with: "+").replacingOccurrences(of: "_", with: "/") + "="
            try requireSession(sessionMatches(n, "^[A-Za-z0-9_-]{43}$") && Data(base64Encoded: nonce64)?.count == 32 && Data(base64Encoded: nonce64)?.base64EncodedString() == nonce64
                && sessionMatches(d, "^[a-f0-9]{64}$") && issued > 0 && issued <= at + 30000 && issued < end && end - issued <= maximum && end == expires)
            nonce = n; digest = d
        }
        return PublicSessionProof(record: record, token: token, provider: provider, client: clientID, app: appID, nonce: nonce, digest: digest, expired: expires <= at)
    }
}
