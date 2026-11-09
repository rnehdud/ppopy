import Foundation

// Diagnostic process telemetry only. No account/session/token/capability data.
// A global-queue watchdog can claim completion even if the main actor stalls.
public final class WithdrawalDiagnosticProgress: @unchecked Sendable {
    public static let marker = "MIRAY_WITHDRAWAL_PREPARATION_STAGE_V1 "
    private static let stages: Set<String> = ["process_start","scene_connected","controller_visible",
        "probe_context","checkpoint_seed","binding","vault_read","binding_http","binding_validation","binding_verified",
        "status_adapter","restart_adapter","checkpoint_attachment",
        "lookup_start","lookup_response","lookup_signature","lookup_identity","lookup_lifetime",
        "checkpoint_admission","checkpoint_new_grant","checkpoint_previous","checkpoint_old_identity",
        "checkpoint_retire_memory","checkpoint_create_memory","lookup_owner","reader_assembly",
        "capability_attach","preparation_complete"]
    private let lock = NSLock(), nonce: String, emit: @Sendable (Data) -> Void
    private var stage = "process_start", sequence = 0, completed = false, deadlineArmed = false
    public init(nonce: String, emit: @escaping @Sendable (Data) -> Void) throws {
        guard let value = UUID(uuidString:nonce), nonce == value.uuidString.lowercased() else {
            throw WithdrawalNativeReviewError.held
        }
        self.nonce = nonce; self.emit = emit
    }
    public func record(_ value: String) {
        lock.withLock {
            guard !completed, Self.stages.contains(value), sequence < 63 else { return }
            stage = value; publish(terminal:false,outcome:"progress")
        }
    }
    // Only one of ordinary completion or deadline can publish the terminal
    // observation and exit. A deadline never asserts HTTP or storage outcomes.
    public func claimCompletion(deadline: Bool) -> Bool {
        lock.withLock {
            guard !completed else { return false }; completed = true
            publish(terminal:true,outcome:deadline ? "deadline" : "completed")
            return true
        }
    }
    @discardableResult public func armDeadline(after seconds: TimeInterval,
        onDeadline: @escaping @Sendable () -> Void) -> Bool {
        let armed=lock.withLock {
            guard seconds.isFinite,seconds>0,seconds<=45,!completed,!deadlineArmed else {return false}
            deadlineArmed=true;return true
        }
        guard armed else {return false}
        DispatchQueue.global(qos:.userInitiated).asyncAfter(deadline:.now()+seconds) {
            if self.claimCompletion(deadline:true) {onDeadline()}
        }
        return true
    }
    private func publish(terminal: Bool, outcome: String) {
        sequence += 1
        let fields: [String:Any] = ["version":"1.0.0","nonce":nonce,"sequence":sequence,
            "stage":stage,"terminal":terminal,"outcome":outcome]
        guard let data = try? JSONSerialization.data(withJSONObject:fields,options:.sortedKeys) else { return }
        // Trusted bounded stdout emitter only, serialized with state changes.
        emit(Data(Self.marker.utf8) + data + Data([10]))
    }
}
