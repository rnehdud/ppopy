import Foundation

public enum PublicHTTPError: Error, Equatable { case binding, request, busy, cancelled, timeout, response, size, network }
private func matches(_ value: String, _ pattern: String) -> Bool { guard let r = value.range(of: pattern, options: .regularExpression) else { return false }; return r.lowerBound == value.startIndex && r.upperBound == value.endIndex }
private func exactKeys(_ value: Any?, _ keys: [String]) -> Bool {
    guard let d = value as? [String: Any] else { return false }; return Set(d.keys) == Set(keys)
}

public struct PublicHTTPBinding {
    struct Identity: Decodable {
        let api_id: String; let api_stage: String; let origin: String; let auth_version_arn: String
        let server_source_manifest_sha256: String; let binding_receipt_sha256: String; let route_contract_version: String
    }
    struct Limits: Decodable {
        let request_deadline_milliseconds: Int; let maximum_response_headers: Int; let maximum_response_header_bytes: Int
        let state_read_accept: [String]; let state_write_accept: [String]
    }
    struct Route: Decodable { let method: String; let path: String; let maximum_request_bytes: Int; let maximum_response_bytes: Int }
    struct Wire: Decodable { let schema_version: String; let scope: String; let binding: Identity; let limits: Limits; let routes: [Route] }
    let wire: Wire
    public var origin: String { wire.binding.origin }
    public var requestDeadlineMilliseconds: Int { wire.limits.request_deadline_milliseconds }
    public init(review: Data) throws {
        guard review.count <= 32768, let root = try? JSONSerialization.jsonObject(with: review) as? [String: Any],
              exactKeys(root, ["schema_version", "scope", "binding", "limits", "routes"]),
              exactKeys(root["binding"], ["api_id", "api_stage", "origin", "auth_version_arn", "server_source_manifest_sha256", "binding_receipt_sha256", "route_contract_version"]),
              exactKeys(root["limits"], ["request_deadline_milliseconds", "maximum_response_headers", "maximum_response_header_bytes", "state_read_accept", "state_write_accept"]),
              let rawRoutes = root["routes"] as? [[String: Any]], rawRoutes.count == 26,
              rawRoutes.allSatisfy({ exactKeys($0, ["method", "path", "maximum_request_bytes", "maximum_response_bytes"]) }),
              let w = try? JSONDecoder().decode(Wire.self, from: review) else { throw PublicHTTPError.binding }
        let b = w.binding, l = w.limits
        guard w.schema_version == "1.0.0", w.scope == "public_native_original_http_not_registration",
              matches(b.api_id, "^[a-z0-9]{10}$"), b.api_id != "synthetic00", b.api_stage == "$default",
              b.origin == "https://\(b.api_id).execute-api.ap-northeast-2.amazonaws.com",
              matches(b.auth_version_arn, "^arn:aws:lambda:ap-northeast-2:000000000000:function:skinanalysis-public-[a-z0-9-]{1,44}:[1-9][0-9]*$"),
              matches(b.server_source_manifest_sha256, "^[a-f0-9]{64}$"), matches(b.binding_receipt_sha256, "^[a-f0-9]{64}$"),
              b.route_contract_version == "1.2.0-public-auth-route-contract-20261021",
              l.request_deadline_milliseconds > 0, l.request_deadline_milliseconds <= 35000,
              l.maximum_response_headers == 64, l.maximum_response_header_bytes == 8192,
              l.state_read_accept == ["application/vnd.poppy.loop-entry+json", "application/vnd.poppy.loop-entry+json; products=1", "application/vnd.poppy.loop-products+json", "application/vnd.poppy.loop-entry+json; products=2", "application/vnd.poppy.loop-products-v2+json"],
              l.state_write_accept == ["application/vnd.poppy.loop-products+json", "application/vnd.poppy.loop-products-v2+json"],
              Set(w.routes.map { $0.method + " " + $0.path }).count == 26 else { throw PublicHTTPError.binding }
        for r in w.routes {
            guard Self.routePairs.contains(r.method + " " + r.path), r.maximum_request_bytes > 0, r.maximum_request_bytes <= 65536,
                  r.maximum_response_bytes > 0, r.maximum_response_bytes <= 262144 else { throw PublicHTTPError.binding }
        }
        wire = w
    }
    // Defensive native allowlist. The build compiler checks exact equality to
    // the source route contract and bounds; a JS call cannot supply this review.
    static let routePairs: Set<String> = Set([
        "POST /api/v1/app/auth/protection-session", "POST /api/v1/app/auth/apple", "POST /api/v1/app/auth/apple/challenge",
        "POST /api/v1/app/auth/google", "POST /api/v1/app/auth/kakao", "GET /api/v1/app/auth/session", "DELETE /api/v1/app/auth/session",
        "GET /api/v1/app/portfolio", "PUT /api/v1/app/portfolio", "GET /api/v1/app/saved-candidates", "PUT /api/v1/app/saved-candidates",
        "POST /api/v1/app/skin-state", "GET /api/v1/app/history-consent", "POST /api/v1/app/history-consent", "GET /api/v1/app/quota-status",
        "DELETE /api/v1/app/account/withdrawal", "GET /api/v1/app/loop/state", "POST /api/v1/app/loop/state/registration",
        "POST /api/v1/app/loop/state/actual", "POST /api/v1/app/loop/state/followup", "GET /api/v1/app/loop/review",
        "POST /api/v1/app/loop/review", "GET /api/v1/app/loop/frequency", "POST /api/v1/app/loop/frequency", "POST /api/v1/app/products/search", "POST /api/v1/app/products/web-candidates"])
}

public struct PublicHTTPRequest: Sendable {
    public let url: String; public let method: String; public let headers: [String: String]; public let body: String?
    public let timeoutMilliseconds: Int; public let maximumResponseBytes: Int
    public init(url: String, method: String, headers: [String: String], body: String?, timeoutMilliseconds: Int, maximumResponseBytes: Int) {
        self.url = url; self.method = method; self.headers = headers; self.body = body
        self.timeoutMilliseconds = timeoutMilliseconds; self.maximumResponseBytes = maximumResponseBytes
    }
    func checked(_ binding: PublicHTTPBinding) throws -> URLRequest {
        guard let u = URL(string: url), u.absoluteString == url, let c = URLComponents(url: u, resolvingAgainstBaseURL: false),
              c.user == nil, c.password == nil, c.query == nil, c.fragment == nil,
              url == binding.origin + c.path,
              let route = binding.wire.routes.first(where: { $0.method == method && $0.path == c.path }),
              timeoutMilliseconds > 0, timeoutMilliseconds <= binding.wire.limits.request_deadline_milliseconds,
              maximumResponseBytes == route.maximum_response_bytes, headers.count <= 3 else { throw PublicHTTPError.request }
        var normalized: [String: String] = [:]
        for (key, value) in headers {
            let k = key.lowercased()
            guard ["authorization", "accept", "content-type"].contains(k), normalized[k] == nil,
                  value.utf8.count <= 512, !value.contains("\r"), !value.contains("\n") else { throw PublicHTTPError.request }
            normalized[k] = value
        }
        if c.path == "/api/v1/app/auth/protection-session" {
            guard normalized["authorization"] == nil else { throw PublicHTTPError.request }
        } else {
            guard matches(normalized["authorization"] ?? "", "^Bearer [A-Za-z0-9_-]{32,200}$") else { throw PublicHTTPError.request }
        }
        if let accept = normalized["accept"], accept != "application/json" {
            let allowed = method == "GET" && c.path == "/api/v1/app/loop/state" ? binding.wire.limits.state_read_accept
                : method == "POST" && ["/api/v1/app/loop/state/registration", "/api/v1/app/loop/state/actual", "/api/v1/app/loop/state/followup"].contains(c.path) ? binding.wire.limits.state_write_accept : []
            guard allowed.contains(accept) else { throw PublicHTTPError.request }
        }
        var request = URLRequest(url: u, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData, timeoutInterval: Double(timeoutMilliseconds) / 1000)
        request.httpMethod = method; request.httpShouldHandleCookies = false
        if method == "GET" || method == "DELETE" {
            guard body == nil || body == "", normalized["content-type"] == nil else { throw PublicHTTPError.request }
        } else {
            guard let body, let data = body.data(using: .utf8), data.count <= route.maximum_request_bytes,
                  normalized["content-type"] == "application/json",
                  (try? JSONSerialization.jsonObject(with: data)) is [String: Any] else { throw PublicHTTPError.request }
            request.httpBody = data
        }
        for (k, v) in normalized { request.setValue(v, forHTTPHeaderField: k) }
        request.setValue("identity", forHTTPHeaderField: "Accept-Encoding")
        return request
    }
}
public struct PublicHTTPResponse: Sendable { public let url: String; public let status: Int; public let headers: [String: String]; public let body: String }

public final class PublicNativeHTTPClient: @unchecked Sendable {
    private let binding: PublicHTTPBinding; private let protocols: [AnyClass]?
    private let lock = NSLock(); private var active: (UUID, PublicHTTPExchange)?
    public convenience init(binding: PublicHTTPBinding) { self.init(binding: binding, testingProtocols: nil) }
    init(binding: PublicHTTPBinding, testingProtocols: [AnyClass]?) { self.binding = binding; protocols = testingProtocols }
    @discardableResult public func send(_ request: PublicHTTPRequest, completion: @escaping @Sendable (Result<PublicHTTPResponse, PublicHTTPError>) -> Void) throws -> PublicHTTPExchange {
        let checked = try request.checked(binding), id = UUID()
        lock.lock(); guard active == nil else { lock.unlock(); throw PublicHTTPError.busy }
        let exchange = PublicHTTPExchange(request: checked, limits: binding.wire.limits, maximum: request.maximumResponseBytes,
            timeout: Double(request.timeoutMilliseconds) / 1000, protocols: protocols) { [weak self] result in
                if let self { self.lock.lock(); if self.active?.0 == id { self.active = nil }; self.lock.unlock() }
                completion(result)
            }
        active = (id, exchange); lock.unlock(); exchange.start(); return exchange
    }
    public func cancel() { lock.lock(); let value = active?.1; lock.unlock(); value?.cancel() }
}

public final class PublicHTTPExchange: NSObject, URLSessionDataDelegate, @unchecked Sendable {
    private let lock = NSLock(); private let request: URLRequest; private let limits: PublicHTTPBinding.Limits
    private let maximum: Int; private let timeout: TimeInterval; private let protocols: [AnyClass]?
    private let completion: @Sendable (Result<PublicHTTPResponse, PublicHTTPError>) -> Void
    private var finished = false; private var started = false; private var session: URLSession?; private var bytes = Data()
    private var response: HTTPURLResponse?; private var checkedHeaders: [String: String] = [:]; private var declaredLength: Int?
    private var deadline: DispatchWorkItem?
    private var pendingResult: Result<PublicHTTPResponse, PublicHTTPError>?; private var delivered = false
    init(request: URLRequest, limits: PublicHTTPBinding.Limits, maximum: Int, timeout: TimeInterval, protocols: [AnyClass]?,
         completion: @escaping @Sendable (Result<PublicHTTPResponse, PublicHTTPError>) -> Void) {
        self.request = request; self.limits = limits; self.maximum = maximum; self.timeout = timeout; self.protocols = protocols; self.completion = completion
    }
    static func configuration(timeout: TimeInterval) -> URLSessionConfiguration {
        let c = URLSessionConfiguration.ephemeral; c.urlCache = nil; c.httpCookieStorage = nil; c.urlCredentialStorage = nil
        c.httpShouldSetCookies = false; c.httpCookieAcceptPolicy = .never; c.requestCachePolicy = .reloadIgnoringLocalAndRemoteCacheData
        c.timeoutIntervalForRequest = timeout; c.timeoutIntervalForResource = timeout; c.waitsForConnectivity = false
        c.tlsMinimumSupportedProtocolVersion = .TLSv12
        return c
    }
    func start() {
        lock.lock(); guard !started, !finished else { lock.unlock(); return }; started = true
        let c = Self.configuration(timeout: timeout); if let protocols { c.protocolClasses = protocols }
        let queue = OperationQueue(); queue.maxConcurrentOperationCount = 1
        let s = URLSession(configuration: c, delegate: self, delegateQueue: queue); session = s
        let task = s.dataTask(with: request)
        let item = DispatchWorkItem { [weak self] in self?.finish(.failure(.timeout)) }; deadline = item
        lock.unlock(); DispatchQueue.global().asyncAfter(deadline: .now() + timeout, execute: item); task.resume()
    }
    public func cancel() { finish(.failure(.cancelled)) }
    private func finish(_ result: Result<PublicHTTPResponse, PublicHTTPError>) {
        lock.lock(); guard !finished else { lock.unlock(); return }; finished = true
        let s = session; session = nil; deadline?.cancel(); deadline = nil; bytes.removeAll(keepingCapacity: false)
        response = nil; checkedHeaders.removeAll(); pendingResult = result; lock.unlock()
        if let s { s.invalidateAndCancel() } else { deliver() }
    }
    private func deliver() {
        lock.lock(); guard !delivered, let result = pendingResult else { lock.unlock(); return }
        delivered = true; pendingResult = nil; lock.unlock(); completion(result)
    }
    public func urlSession(_ session: URLSession, didBecomeInvalidWithError error: Error?) {
        lock.lock(); let pending = pendingResult != nil; lock.unlock()
        if !pending { finish(.failure(.network)) }; deliver()
    }
    public func urlSession(_ session: URLSession, task: URLSessionTask, willPerformHTTPRedirection response: HTTPURLResponse,
                           newRequest request: URLRequest, completionHandler: @escaping (URLRequest?) -> Void) {
        completionHandler(nil); finish(.failure(.response))
    }
    public func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge,
                           completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        completionHandler(challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust ? .performDefaultHandling : .cancelAuthenticationChallenge, nil)
    }
    public func urlSession(_ session: URLSession, task: URLSessionTask, needNewBodyStream completionHandler: @escaping (InputStream?) -> Void) { completionHandler(nil) }
    public func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive response: URLResponse,
                           completionHandler: @escaping (URLSession.ResponseDisposition) -> Void) {
        guard let h = response as? HTTPURLResponse, h.url == request.url, (200...599).contains(h.statusCode), !(300...399).contains(h.statusCode),
              h.expectedContentLength <= Int64(maximum), h.allHeaderFields.count <= limits.maximum_response_headers else {
            completionHandler(.cancel); finish(.failure(.response)); return
        }
        var headers: [String: String] = [:]; var size = 0
        for (key, value) in h.allHeaderFields {
            guard let k = key as? String, let v = value as? String else { completionHandler(.cancel); finish(.failure(.response)); return }
            let normalized = k.lowercased(); size += k.utf8.count + v.utf8.count
            guard headers[normalized] == nil, normalized != "set-cookie", size <= limits.maximum_response_header_bytes else {
                completionHandler(.cancel); finish(.failure(.response)); return
            }; headers[normalized] = v
        }
        guard headers["content-type"]?.split(separator: ";").first == "application/json",
              headers["cache-control"]?.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() == "no-store",
              headers["content-encoding"] == nil || headers["content-encoding"] == "identity" else {
            completionHandler(.cancel); finish(.failure(.response)); return
        }
        var declared: Int?
        if let value = headers["content-length"] {
            guard matches(value, "^[0-9]+$"), let count = Int(value), count <= maximum else { completionHandler(.cancel); finish(.failure(.size)); return }; declared = count
        }
        lock.lock(); guard !finished else { lock.unlock(); completionHandler(.cancel); return }
        self.response = h; checkedHeaders = headers; declaredLength = declared; lock.unlock(); completionHandler(.allow)
    }
    public func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive data: Data) {
        lock.lock(); guard !finished else { lock.unlock(); return }
        guard data.count <= maximum - bytes.count else { lock.unlock(); finish(.failure(.size)); return }
        bytes.append(data); lock.unlock()
    }
    public func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
        lock.lock(); let done = finished, data = bytes, h = response, headers = checkedHeaders, length = declaredLength; lock.unlock()
        guard !done else { return }
        if let error { finish(.failure((error as? URLError)?.code == .timedOut ? .timeout : .network)); return }
        guard let h, let body = String(data: data, encoding: .utf8), length == nil || length == data.count,
              ![204, 205].contains(h.statusCode) || body.isEmpty else { finish(.failure(.response)); return }
        finish(.success(PublicHTTPResponse(url: request.url!.absoluteString, status: h.statusCode, headers: headers, body: body)))
    }
}
