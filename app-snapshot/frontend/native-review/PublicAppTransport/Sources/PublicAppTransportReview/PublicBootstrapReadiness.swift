import Foundation

/// One local startup admission, with a monotonic deadline. It grants no
/// session, SDK or HTTP operation and never changes the origin requirement.
public struct PublicBootstrapReadiness {
    public enum State: Equatable { case waiting, ready, rejected }
    public private(set) var state: State = .waiting
    private let started: TimeInterval, expires: TimeInterval
    public init(started: TimeInterval, timeoutMilliseconds: Int) throws {
        let end = started + Double(timeoutMilliseconds) / 1000
        guard started.isFinite, started >= 0, timeoutMilliseconds > 0,
              end.isFinite, end > started else { throw PublicHTTPError.binding }
        self.started = started; expires = end
    }
    public mutating func observe(now: TimeInterval, localOrigin: Bool, active: Bool, protectedData: Bool) -> State {
        guard state == .waiting else { return state }
        if !now.isFinite || now < started || now >= expires || !localOrigin { state = .rejected }
        else if active && protectedData { state = .ready }
        return state
    }
}
