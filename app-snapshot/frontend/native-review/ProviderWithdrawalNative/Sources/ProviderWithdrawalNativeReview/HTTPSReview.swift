import Foundation

// Every request is intercepted. A custom protocol that declines interception
// cannot silently fall through to URLSession's real HTTPS implementation.
class WithdrawalOfflineHTTPSProtocol: URLProtocol, @unchecked Sendable {
    final override class func canInit(with request: URLRequest) -> Bool { true }
    final override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }
    override func startLoading() { client?.urlProtocol(self, didFailWithError: URLError(.unsupportedURL)) }
    override func stopLoading() {}
}

// Synthetic callers require an intercepting offline URLProtocol. Only the
// separately sealed provider TEST context admits the native default HTTPS
// session. Original signed proofs and lifetime checks remain required.
struct WithdrawalHTTPSReviewTransport {
    private let origin: String
    private let routes: [String: String]
    private let sizes: [String: Int]
    private let seconds: TimeInterval
    init(configuration: Data) throws {
        let raw = try withdrawalFlatObject(configuration)
        let expected: [String: Any] = [
            "version":"1.0.0", "scope":"offline_exact_TEST_HTTPS_transport_review",
            "runtime_registered":false, "native_plugin_registered":false,
            "operating_member_transport_authorized":false, "provider_live_calls_authorized":false,
            "automatic_retry":false,
            "origin":"https://unconfigured.invalid",
            "route_withdrawal_binding":"/app/withdrawal/binding",
            "route_withdrawal_challenge":"/app/withdrawal/operation", "route_withdrawal_close":"/app/withdrawal/operation",
            "route_withdrawal_kakao_close":"/app/withdrawal/operation", "route_withdrawal_lookup_prepare":"/app/withdrawal/lookup",
            "route_withdrawal_status_read":"/app/withdrawal/lookup",
            "route_withdrawal_session_close":"/app/withdrawal/operation", "maximum_request_bytes_withdrawal_session_close":512,
            "maximum_request_bytes_withdrawal_binding":512, "maximum_request_bytes_withdrawal_challenge":20480,
            "maximum_request_bytes_withdrawal_close":20480, "maximum_request_bytes_withdrawal_kakao_close":4096,
            "maximum_request_bytes_withdrawal_lookup_prepare":4096, "maximum_request_bytes_withdrawal_status_read":4096,
            "timeout_seconds":20, "maximum_response_bytes":8192, "maximum_response_chunks":64,
            "maximum_header_bytes":4096, "maximum_header_fields":20, "minimum_TLS":"1.2",
            "trust":"platform_default_server_trust_only_exact_origin_no_custom_credentials",
            "response_proof":"existing_original_owner_pinned_P256_validator_still_required",
            "review_driver":"injected_URLProtocol_only_no_operating_network",
            "activation":"new_exact_route_permission_key_and_member_review_required"]
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
        origin = raw["origin"] as! String
        routes = Dictionary(uniqueKeysWithValues: raw.filter { $0.key.hasPrefix("route_") }
            .map { (String($0.key.dropFirst(6)), $0.value as! String) })
        sizes = Dictionary(uniqueKeysWithValues: raw.filter { $0.key.hasPrefix("maximum_request_bytes_") }
            .map { (String($0.key.dropFirst(22)), ($0.value as! NSNumber).intValue) })
        seconds = (raw["timeout_seconds"] as! NSNumber).doubleValue
    }
    func url(method: String) throws -> URL {
        guard let path = routes[method], let value = URL(string: origin + path) else { throw WithdrawalNativeReviewError.held }
        return value
    }
    func validateURL(method: String, url: URL) throws {
        guard let path = routes[method] else { throw WithdrawalNativeReviewError.held }
        // Compare the original URL spelling as well as parsed fields. No port,
        // alternate origin, escaping, userinfo, query, fragment or redirect.
        try ownerRequire(url.absoluteString == origin + path && url.scheme == "https"
            && url.port == nil && url.user == nil && url.password == nil && url.query == nil && url.fragment == nil)
    }
    func flight(method: String, url: URL, sessionConfiguration: URLSessionConfiguration,
        actualContext: WithdrawalNativeActualTESTContext? = nil) throws -> WithdrawalBindingHTTPFlight {
        try validateURL(method: method, url: url)
        guard let size = sizes[method] else { throw WithdrawalNativeReviewError.held }
        let configuration: URLSessionConfiguration
        if let protocols = sessionConfiguration.protocolClasses, protocols.count == 1,
            protocols[0] is WithdrawalOfflineHTTPSProtocol.Type {
            // Offline fixtures keep their mandatory interception, with or
            // without a synthetic sealed-context fixture. No network fallback.
            configuration = sessionConfiguration
        } else {
            guard let actualContext else { throw WithdrawalNativeReviewError.held }
            try actualContext.requireWithdrawalReady()
            try actualContext.requireURL(url)
            let native = URLSessionConfiguration.ephemeral
            // Accept only Foundation's native protocol set. Never carry a
            // caller's proxy, headers, cache, credential store or protocol into
            // the real TEST session. Flight.start supplies the fixed bounds.
            try ownerRequire((sessionConfiguration.protocolClasses ?? []).map {ObjectIdentifier($0)}
                == (native.protocolClasses ?? []).map {ObjectIdentifier($0)})
            configuration = native
        }
        return WithdrawalBindingHTTPFlight(url: url,
            policy: WithdrawalHTTPBounds(requestBytes: size, seconds: seconds),
            configuration: configuration, trustReview: .platformServerTrust)
    }
}

// A transport choice for the existing signed-proof ports. Public constructors
// still select loopback. The internal HTTPS choice is intercepted offline and
// retains the original synthetic proof scopes; it is not member attestation.
struct WithdrawalHTTPReviewEndpoint {
    let url: URL
    private let https: WithdrawalHTTPSReviewTransport?
    private let actualContext: WithdrawalNativeActualTESTContext?
    init(url: URL, path: String, method: String, deploymentContext: String,
        https: WithdrawalHTTPSReviewTransport? = nil, actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        try requireWithdrawalNativeContext(deploymentContext,actualContext)
        if let actualContext {try ownerRequire(https != nil);try actualContext.requireURL(url)}
        if let https { try https.validateURL(method: method, url: url) }
        else {
            try ownerRequire(url.scheme == "http" && url.host == "127.0.0.1"
                && url.port != nil && (1...65535).contains(url.port!)
                && url.absoluteString == "http://127.0.0.1:\(url.port!)/withdrawal/" + path
                && url.query == nil && url.fragment == nil && url.user == nil && url.password == nil)
        }
        self.url = url; self.https = https; self.actualContext = actualContext
    }
    func flight(method: String, bounds: WithdrawalHTTPBounds,
        configuration: URLSessionConfiguration) throws -> WithdrawalBindingHTTPFlight {
        if let https { return try https.flight(method: method, url: url, sessionConfiguration: configuration, actualContext: actualContext) }
        return WithdrawalBindingHTTPFlight(url: url, policy: bounds, configuration: configuration)
    }
}
