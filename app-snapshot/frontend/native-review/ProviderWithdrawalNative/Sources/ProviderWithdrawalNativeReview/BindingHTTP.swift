import Foundation

struct WithdrawalHTTPBounds {
    let requestBytes: Int
    let responseBytes = 8192, chunks = 64, headerBytes = 4096, headerFields = 20
    let seconds: TimeInterval
    init(requestBytes: Int, seconds: TimeInterval = 2) {
        self.requestBytes = requestBytes; self.seconds = seconds
    }
}

// Loopback callers retain their refusal of all authentication challenges.
// The separate, offline HTTPS candidate delegates certificate validation to
// Foundation; it never supplies credentials or overrides a trust failure.
enum WithdrawalHTTPTrustReview {
    case rejectChallenges
    case platformServerTrust
    func disposition(for space: URLProtectionSpace, url: URL) -> URLSession.AuthChallengeDisposition {
        guard case .platformServerTrust = self, url.scheme == "https", url.port == nil,
            space.authenticationMethod == NSURLAuthenticationMethodServerTrust,
            space.host == url.host, space.port == 443, space.protocol == "https", !space.isProxy() else {
            return .cancelAuthenticationChallenge
        }
        return .performDefaultHandling
    }
}

struct WithdrawalBindingHTTPPolicy {
    let requestBytes = 512, responseBytes = 8192, chunks = 64, headerBytes = 4096, headerFields = 20
    let seconds: TimeInterval = 2
    init(json: Data) throws {
        let raw = try withdrawalFlatObject(json)
        let expected: [String: Any] = ["version":"1.0.0", "scope":"isolated_loopback_review",
            "runtime_registered":false, "native_plugin_registered":false, "operating_member_transport_authorized":false,
            "actual_OS_member_attestation":false, "method":"withdrawal_binding", "maximum_request_bytes":512,
            "maximum_response_bytes":8192, "maximum_response_chunks":64, "maximum_header_bytes":4096,
            "maximum_header_fields":20, "timeout_seconds":2, "deadline":"monotonic_total_no_extension",
            "url":"explicit_127.0.0.1_ephemeral_port_withdrawal_binding_only",
            "response":"exact_URL_200_JSON_identity_no_cookie_no_store_complete_body",
            "storage":"ephemeral_no_cookie_cache_credential_storage", "retry":"no_application_retry",
            "failure":"fixed_held_no_response_or_credential_logs", "writes":"none_no_nonce_closure_code_exchange_or_revoke"]
        try ownerRequire(try JSONSerialization.data(withJSONObject: raw, options: .sortedKeys)
            == JSONSerialization.data(withJSONObject: expected, options: .sortedKeys))
    }
}

// A real URLSession adapter for the original-binding read only. Public creation
// accepts an exact isolated loopback endpoint, never a TEST/operating API URL.
// The verified native owner still checks the signed body and original lifetime.
@MainActor public final class WithdrawalNativeBindingLoopbackReview: WithdrawalNativeBindingReviewPort {
    private let endpoint: WithdrawalHTTPReviewEndpoint, policy: WithdrawalBindingHTTPPolicy, configuration: () -> URLSessionConfiguration
    private var busy = false, retired = false
    public convenience init(configuration: Data, url: URL, deploymentContext: String) throws {
        try self.init(configuration: configuration, url: url, deploymentContext: deploymentContext, sessionConfiguration: { .ephemeral })
    }
    init(configuration: Data, url: URL, deploymentContext: String, sessionConfiguration: @escaping () -> URLSessionConfiguration,
        httpsReview: WithdrawalHTTPSReviewTransport? = nil, actualContext: WithdrawalNativeActualTESTContext? = nil) throws {
        policy = try WithdrawalBindingHTTPPolicy(json: configuration)
        endpoint = try WithdrawalHTTPReviewEndpoint(url: url, path: "binding", method: "withdrawal_binding",
            deploymentContext: deploymentContext, https: httpsReview, actualContext: actualContext)
        self.configuration = sessionConfiguration
    }
    public func originalBinding(bearer: String, body: Data) async throws -> Data {
        if busy { throw WithdrawalNativeReviewError.busy }
        try ownerRequire(!retired && !Task.isCancelled && ownerMatches(bearer, "^[A-Za-z0-9_-]{32,200}$"))
        let raw = try withdrawalFlatObject(body, maximumBytes: policy.requestBytes)
        guard Set(raw.keys) == ["method", "request_id"], raw["method"] as? String == "withdrawal_binding",
            let id = raw["request_id"] as? String, let uuid = UUID(uuidString: id), uuid.uuidString.lowercased() == id else {
            throw WithdrawalNativeReviewError.held
        }
        busy = true; defer { busy = false }
        do {
            let flight = try endpoint.flight(method: "withdrawal_binding",
                bounds: WithdrawalHTTPBounds(requestBytes: policy.requestBytes), configuration: configuration())
            let response = try await withTaskCancellationHandler(operation: {
                try await withCheckedThrowingContinuation { flight.start(body: body, bearer: bearer, continuation: $0) }
            }, onCancel: { flight.cancel() })
            try ownerRequire(!Task.isCancelled)
            return response
        } catch { retired = true; throw WithdrawalNativeReviewError.held }
    }
}

final class WithdrawalBindingHTTPFlight: NSObject, URLSessionDataDelegate, @unchecked Sendable {
    private let lock = NSLock(), url: URL, policy: WithdrawalHTTPBounds, configuration: URLSessionConfiguration
    private let trustReview: WithdrawalHTTPTrustReview
    private let deadline: DispatchTime
    private var continuation: CheckedContinuation<Data, Error>?, session: URLSession?, task: URLSessionDataTask?
    private var terminal = false, admitted = false, expected: Int?, body = Data(), chunks = 0
    init(url: URL, policy: WithdrawalHTTPBounds, configuration: URLSessionConfiguration,
        trustReview: WithdrawalHTTPTrustReview = .rejectChallenges) {
        self.url = url; self.policy = policy; self.configuration = configuration
        self.trustReview = trustReview
        deadline = DispatchTime.now() + policy.seconds
    }
    private func timely() -> Bool { DispatchTime.now().uptimeNanoseconds < deadline.uptimeNanoseconds }
    func start(body: Data, bearer: String, continuation: CheckedContinuation<Data, Error>) {
        guard !body.isEmpty && body.count <= policy.requestBytes else {
            finish(false); continuation.resume(throwing: WithdrawalNativeReviewError.held); return
        }
        configuration.urlCache = nil; configuration.httpCookieStorage = nil; configuration.urlCredentialStorage = nil
        configuration.httpShouldSetCookies = false; configuration.httpAdditionalHeaders = [:]
        configuration.requestCachePolicy = .reloadIgnoringLocalCacheData
        configuration.timeoutIntervalForRequest = policy.seconds; configuration.timeoutIntervalForResource = policy.seconds
        configuration.waitsForConnectivity = false
        configuration.tlsMinimumSupportedProtocolVersion = .TLSv12
        let queue = OperationQueue(); queue.maxConcurrentOperationCount = 1
        let session = URLSession(configuration: configuration, delegate: self, delegateQueue: queue)
        var request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: policy.seconds)
        request.httpMethod = "POST"; request.httpBody = body; request.httpShouldHandleCookies = false
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue("identity", forHTTPHeaderField: "Accept-Encoding")
        request.setValue("Bearer " + bearer, forHTTPHeaderField: "Authorization")
        let task = session.dataTask(with: request)
        let ready = lock.withLock { () -> Bool in
            guard !terminal && timely() else { return false }
            self.continuation = continuation; self.session = session; self.task = task; return true
        }
        if ready {
            DispatchQueue.global().asyncAfter(deadline: deadline) { [weak self] in self?.finish(false) }
            task.resume()
        } else { session.invalidateAndCancel(); continuation.resume(throwing: WithdrawalNativeReviewError.held) }
    }
    func cancel() { finish(false) }
    private func finish(_ success: Bool) {
        let old = lock.withLock { () -> (CheckedContinuation<Data, Error>?, URLSession?, URLSessionDataTask?, Data, Bool) in
            guard !terminal else { return (nil, nil, nil, Data(), false) }
            terminal = true
            let value = (continuation, session, task, body, success && timely())
            continuation = nil; session = nil; task = nil; body = Data(); return value
        }
        if old.4 { old.1?.finishTasksAndInvalidate(); old.0?.resume(returning: old.3) }
        else { old.2?.cancel(); old.1?.invalidateAndCancel(); old.0?.resume(throwing: WithdrawalNativeReviewError.held) }
    }
    func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive response: URLResponse,
        completionHandler: @escaping @Sendable (URLSession.ResponseDisposition) -> Void) {
        do {
            guard let http = response as? HTTPURLResponse, http.url == url, http.statusCode == 200,
                http.allHeaderFields.count <= policy.headerFields else { throw WithdrawalNativeReviewError.held }
            var headers: [String: String] = [:], size = 0
            for (key, value) in http.allHeaderFields {
                guard let key = key as? String, let value = value as? String, headers[key.lowercased()] == nil else { throw WithdrawalNativeReviewError.held }
                size += key.utf8.count + value.utf8.count + 4; try ownerRequire(size <= policy.headerBytes)
                headers[key.lowercased()] = value
            }
            try ownerRequire(headers["content-type"]?.lowercased() == "application/json"
                && headers["cache-control"]?.lowercased() == "no-store" && headers["set-cookie"] == nil
                && (headers["content-encoding"] == nil || headers["content-encoding"]?.lowercased() == "identity")
                && !(headers["content-length"] != nil && headers["transfer-encoding"] != nil)
                && (headers["transfer-encoding"] == nil || headers["transfer-encoding"]?.lowercased() == "chunked"))
            var length: Int?
            if let raw = headers["content-length"] {
                try ownerRequire(!raw.isEmpty && raw.utf8.allSatisfy { (48...57).contains($0) })
                guard let n = Int(raw), n > 0, n <= policy.responseBytes else { throw WithdrawalNativeReviewError.held }
                length = n
            }
            let ready = lock.withLock { () -> Bool in
                guard !terminal && !admitted && timely() else { return false }
                admitted = true; expected = length; return true
            }
            completionHandler(ready ? .allow : .cancel); if !ready { finish(false) }
        } catch { completionHandler(.cancel); finish(false) }
    }
    func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive data: Data) {
        let ready = lock.withLock { () -> Bool in
            guard !terminal && admitted && timely() && !data.isEmpty && chunks < policy.chunks
                && data.count <= policy.responseBytes - body.count
                && (expected == nil || data.count <= expected! - body.count) else { return false }
            body.append(data); chunks += 1; return true
        }; if !ready { finish(false) }
    }
    func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
        let ready = lock.withLock { !terminal && admitted && timely() && !body.isEmpty && (expected == nil || body.count == expected!) }
        finish(error == nil && ready)
    }
    func urlSession(_ session: URLSession, task: URLSessionTask, willPerformHTTPRedirection response: HTTPURLResponse,
        newRequest request: URLRequest, completionHandler: @escaping @Sendable (URLRequest?) -> Void) {
        completionHandler(nil); finish(false)
    }
    func urlSession(_ session: URLSession, task: URLSessionTask, didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping @Sendable (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        let disposition = task.originalRequest?.url == url
            ? trustReview.disposition(for: challenge.protectionSpace, url: url) : .cancelAuthenticationChallenge
        completionHandler(disposition, nil)
        if disposition == .cancelAuthenticationChallenge { finish(false) }
    }
    func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping @Sendable (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        let disposition = trustReview.disposition(for: challenge.protectionSpace, url: url)
        completionHandler(disposition, nil)
        if disposition == .cancelAuthenticationChallenge { finish(false) }
    }
}
