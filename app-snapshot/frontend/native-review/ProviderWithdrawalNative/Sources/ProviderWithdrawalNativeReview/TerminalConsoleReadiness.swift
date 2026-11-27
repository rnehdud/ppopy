import Foundation

// Only waits for the explicitly launched terminal console. No stores or host
// are constructed until a fresh active/protected/root snapshot passes.
@MainActor public enum WithdrawalTerminalConsoleReadiness {
    public static func wait(configuration:Data,protected:()->Bool,ready:()->Bool,
        pause:(UInt64) async throws->Void = {try await Task.sleep(nanoseconds:$0)}) async -> Bool {
        guard let p=try? JSONSerialization.jsonObject(with:configuration) as? [String:Any],
            p["version"] as? String == "1.0.0",p["scope"] as? String == "explicit_terminal_console_activation_wait_only",
            p["production_enabled"] as? Bool == false,p["public_enabled"] as? Bool == false,
            let polls=p["maximum_readiness_polls"] as? Int,polls>0,polls<=10,
            let ms=p["readiness_poll_milliseconds"] as? Int,ms>0,ms<=500,
            let total=p["maximum_total_wait_milliseconds"] as? Int,total==polls*ms,total<=5000,
            ["store_reads_before_ready","store_writes_before_ready","network_calls"].allSatisfy({p[$0] as? Int == 0}) else {return false}
        for attempt in 0...polls {
            guard !Task.isCancelled,protected() else {return false}
            if ready() {return true}
            guard attempt<polls else {return false}
            do {try await pause(UInt64(ms)*1_000_000)} catch {return false}
        }
        return false
    }
}
