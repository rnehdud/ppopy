#if DEBUG && SKINANALYSIS_WITHDRAWAL_REGISTRATION_REVIEW && SKINANALYSIS_WITHDRAWAL_REVIEW_SDK
import Foundation
import ProviderWithdrawalNativeReview
import UIKit
import WebKit
import Darwin
import Security
import LocalAuthentication

// Explicit process argument enables a bounded probe of this closed candidate.
// Receipt contains booleans/counters only, never app account or credentials.
@MainActor enum WithdrawalIOSClosedBridgeProbe {
    private static var providerProgress:WithdrawalDiagnosticProgress?
    static func installProviderDeadlineIfRequested() {
        let args=ProcessInfo.processInfo.arguments
        guard providerProgress == nil,
            args.filter({$0 == "--miray-withdrawal-provider-negative-probe-v1"}).count == 1,
            args.filter({$0 == "--miray-withdrawal-probe-nonce"}).count == 1,
            let index=args.firstIndex(of:"--miray-withdrawal-probe-nonce"),index+1<args.count,
            let progress=try? WithdrawalDiagnosticProgress(nonce:args[index+1],emit:{FileHandle.standardOutput.write($0)}) else {return}
        providerProgress=progress;progress.record("process_start")
        // Arm before the web/controller registration. Early returns and a
        // stalled main actor must not leave --console attached indefinitely.
        // This reports diagnostic non-completion, never a successful bridge.
        progress.armDeadline(after:20) {Darwin.exit(EXIT_SUCCESS)}
    }
    static func start(view:UIViewController,web:WKWebView,owner:WithdrawalIOSActualTESTRegistrationCandidate) {
        if ProcessInfo.processInfo.arguments.contains("--miray-withdrawal-provider-negative-probe-v1") {
            providerProgress?.record("controller_visible")
            startProviderNegative(view:view,web:web,owner:owner);return
        }
        // The old empty-options probe would become a valid member operation
        // in a provider-enabled candidate. Never run it in that candidate.
        guard let context=try? WithdrawalIOSActualTESTCompiledContract.loadContext(),
            !context.providerSettingsSealed else {return}
        guard let data=try? WithdrawalIOSActualTESTCompiledInputs.data("app_withdrawal_native_console_probe_review"),
            let policy=try? JSONSerialization.jsonObject(with:data) as? [String:Any],
            let argument=policy["launch_argument"] as? String,ProcessInfo.processInfo.arguments.contains(argument),
            let marker=policy["receipt_marker"] as? String,marker=="MIRAY_WITHDRAWAL_CLOSED_BRIDGE_V1 ",
            policy["probe_process_exit_after_receipt"] as? Bool == true,
            policy["private_container_reads"] as? Bool == false,
            let polls=policy["maximum_readiness_polls"] as? Int,let interval=policy["readiness_poll_seconds"] as? Int,
            let timeout=policy["javascript_call_timeout_ms"] as? Int,let maximum=policy["maximum_receipt_bytes"] as? Int else {return}
        // This explicit review process emits only its own public observation.
        // It never exports a private app container or arbitrary console logs.
        let args=ProcessInfo.processInfo.arguments
        guard let index=args.firstIndex(of:"--miray-withdrawal-probe-nonce"),index+1<args.count,
            let nonce=UUID(uuidString:args[index+1]) else {return}
        Task { @MainActor in
            for _ in 0..<polls {
                guard UIApplication.shared.applicationState == .active,UIApplication.shared.isProtectedDataAvailable,
                    view.isViewLoaded,view.view.window != nil else {return}
                if web.isLoading {try? await Task.sleep(nanoseconds:UInt64(interval)*1_000_000_000);continue}
                let script="""
                const cap=window.Capacitor;
                const available=!!cap && cap.isPluginAvailable('IOSWithdrawalInvocationReview');
                if(!available)return {plugin_available:false};
                const plugin=cap.registerPlugin('IOSWithdrawalInvocationReview');
                const call=async(method,options)=>{
                  try {
                    await Promise.race([plugin[method](options),new Promise((_,reject)=>setTimeout(()=>reject({code:'PROBE_TIMEOUT'}),timeout))]);
                    return 'UNEXPECTED_SUCCESS';
                  } catch(error) {return typeof error?.code==='string'?error.code:'UNCONFIRMED';}
                };
                return {plugin_available:true,
                  empty_options_withdraw_rejected:(await call('withdrawExplicit',{}))==='withdrawal_unconfirmed',
                  empty_options_status_rejected:(await call('readOriginalStatusExplicit',{}))==='withdrawal_unconfirmed',
                  nonempty_options_rejected:(await call('withdrawExplicit',{probe:'synthetic'}))==='withdrawal_request_invalid'};
                """
                let result:Any?
                do {result=try await web.callAsyncJavaScript(script,arguments:["timeout":timeout],in:nil,contentWorld:.page)}
                catch {result=nil}
                let observed=result as? [String:Any] ?? [:]
                if observed["plugin_available"] as? Bool != true {
                    try? await Task.sleep(nanoseconds:UInt64(interval)*1_000_000_000);continue
                }
                let fields:[String:Any]=["version":"1.0.0","kind":"CLOSED_TEST_NATIVE_BRIDGE_OBSERVATION",
                    "nonce":nonce.uuidString.lowercased(),"plugin_available":observed["plugin_available"] as? Bool ?? false,
                    "empty_options_withdraw_rejected":observed["empty_options_withdraw_rejected"] as? Bool ?? false,
                    "empty_options_status_rejected":observed["empty_options_status_rejected"] as? Bool ?? false,
                    "nonempty_options_rejected":observed["nonempty_options_rejected"] as? Bool ?? false,
                    "host_preparation_count":owner.closedHostPreparationCount,
                    "new_host_transport_or_credential_or_SDK_started":owner.closedHostPreparationCount != 0]
                guard let raw=try? JSONSerialization.data(withJSONObject:fields,options:.sortedKeys),raw.count<=maximum else {return}
                FileHandle.standardOutput.write(Data(marker.utf8)+raw+Data([10]))
                // --console waits for process exit. Only this explicit review
                // argument and both compile flags reach this branch.
                Darwin.exit(EXIT_SUCCESS)
            }
        }
    }

    private static func startProviderNegative(view:UIViewController,web:WKWebView,owner:WithdrawalIOSActualTESTRegistrationCandidate) {
        guard let context=try? WithdrawalIOSActualTESTCompiledContract.loadContext(),context.providerSettingsSealed,
            let data=try? WithdrawalIOSActualTESTCompiledInputs.data("app_withdrawal_native_provider_probe_review"),
            let p=try? JSONSerialization.jsonObject(with:data) as? [String:Any],
            p["scope"] as? String == "explicit_provider_sealed_TEST_bridge_negative_probe",
            p["launch_argument"] as? String == "--miray-withdrawal-provider-negative-probe-v1",
            p["valid_member_calls"] as? Int == 0,p["probe_options"] as? String == "nonempty_synthetic_options_only",
            p["member_identity_or_credentials"] as? Bool == false,p["provider_authentication"] as? Bool == false,
            p["private_container_reads"] as? Bool == false,p["probe_process_exit_after_receipt"] as? Bool == true,
            let marker=p["receipt_marker"] as? String,marker=="MIRAY_WITHDRAWAL_PROVIDER_NEGATIVE_BRIDGE_V1 ",
            let polls=p["maximum_readiness_polls"] as? Int,polls==10,
            let interval=p["readiness_poll_seconds"] as? Int,interval==1,
            let timeout=p["javascript_call_timeout_ms"] as? Int,timeout==1500,
            let maximum=p["maximum_receipt_bytes"] as? Int,maximum==4096 else {return}
        let args=ProcessInfo.processInfo.arguments
        guard let index=args.firstIndex(of:"--miray-withdrawal-probe-nonce"),index+1<args.count,
            let nonce=UUID(uuidString:args[index+1]) else {return}
        providerProgress?.record("probe_context")
        Task { @MainActor in
            for _ in 0..<polls {
                guard UIApplication.shared.isProtectedDataAvailable else {return}
                if UIApplication.shared.applicationState != .active || !view.isViewLoaded || view.view.window == nil {
                    try? await Task.sleep(nanoseconds:UInt64(interval)*1_000_000_000);continue
                }
                if web.isLoading {try? await Task.sleep(nanoseconds:UInt64(interval)*1_000_000_000);continue}
                let script="""
                const cap=window.Capacitor;
                const available=!!cap && cap.isPluginAvailable('IOSWithdrawalInvocationReview');
                if(!available)return {plugin_available:false};
                const plugin=cap.registerPlugin('IOSWithdrawalInvocationReview');
                const invalid=async(method)=>{
                  try {
                    await Promise.race([plugin[method]({probe:'synthetic'}),new Promise((_,reject)=>setTimeout(()=>reject({code:'PROBE_TIMEOUT'}),timeout))]);
                    return false;
                  } catch(error) {return error?.code==='withdrawal_request_invalid';}
                };
                return {plugin_available:true,nonempty_withdraw_rejected:await invalid('withdrawExplicit'),
                  nonempty_status_rejected:await invalid('readOriginalStatusExplicit')};
                """
                let result:Any?
                do {result=try await web.callAsyncJavaScript(script,arguments:["timeout":timeout],in:nil,contentWorld:.page)}
                catch {result=nil}
                let observed=result as? [String:Any] ?? [:]
                if observed["plugin_available"] as? Bool != true {
                    try? await Task.sleep(nanoseconds:UInt64(interval)*1_000_000_000);continue
                }
                let fields:[String:Any]=["version":"1.0.0","kind":"TEST_PROVIDER_BRIDGE_NEGATIVE_OBSERVATION",
                    "nonce":nonce.uuidString.lowercased(),"plugin_available":true,"provider_settings_sealed":context.providerSettingsSealed,
                    "nonempty_withdraw_rejected":observed["nonempty_withdraw_rejected"] as? Bool ?? false,
                    "nonempty_status_rejected":observed["nonempty_status_rejected"] as? Bool ?? false,
                    "valid_member_calls":0,"host_preparation_count":owner.closedHostPreparationCount,
                    "new_host_transport_or_credential_or_SDK_started":owner.closedHostPreparationCount != 0]
                guard let raw=try? JSONSerialization.data(withJSONObject:fields,options:.sortedKeys),raw.count<=maximum else {return}
                guard providerProgress?.claimCompletion(deadline:false) == true else {return}
                FileHandle.standardOutput.write(Data(marker.utf8)+raw+Data([10]))
                Darwin.exit(EXIT_SUCCESS)
            }
        }
    }
}
// A plain native controller, selected before the CAP/member web root.
// No JS bootstrap or automatic cleanup. The terminal cleanup command below is
// a separately admitted, explicit frozen TEST operation, never normal startup.
@MainActor final class WithdrawalNativeReadOnlyConsoleViewController:UIViewController {
    static let argument="--miray-withdrawal-preauth-readonly-probe-v1"
    static let checkpointArgument="--miray-withdrawal-checkpoint-readonly-probe-v1"
    static let sessionCheckpointArgument="--miray-withdrawal-checkpoint-session-readonly-probe-v1"
    static let preparationArgument="--miray-withdrawal-preparation-memory-probe-v1"
    static let presenceArgument="--miray-withdrawal-store-presence-probe-v1"
    static let terminalCleanupArgument="--miray-withdrawal-terminal-stores-cleanup-v1"
    static var requested:Bool {ProcessInfo.processInfo.arguments.contains(argument)
        || ProcessInfo.processInfo.arguments.contains(checkpointArgument)
        || ProcessInfo.processInfo.arguments.contains(sessionCheckpointArgument)
        || ProcessInfo.processInfo.arguments.contains(preparationArgument)
        || ProcessInfo.processInfo.arguments.contains(presenceArgument)
        || ProcessInfo.processInfo.arguments.contains(terminalCleanupArgument)}
    static var webBootstrapStarted=false
    private static var preparationProgress:WithdrawalDiagnosticProgress?
    static func installPreparationWatchdogIfRequested() {
        let args=ProcessInfo.processInfo.arguments
        guard preparationProgress == nil,args.contains(preparationArgument),
            args.filter({$0 == "--miray-withdrawal-probe-nonce"}).count == 1,
            let index=args.firstIndex(of:"--miray-withdrawal-probe-nonce"),index+1<args.count,
            let progress=try? WithdrawalDiagnosticProgress(nonce:args[index+1],emit:{FileHandle.standardOutput.write($0)}) else {return}
        preparationProgress=progress;progress.record("process_start")
        // Monotonic, fixed deadline: stage updates never extend it. The OS
        // can still suspend a manually backgrounded/locked diagnostic process.
        progress.armDeadline(after:45) {Darwin.exit(EXIT_SUCCESS)}
    }
    static func preparationStage(_ stage:String) {preparationProgress?.record(stage)}
    private var started=false
    override func loadView(){let root=UIView();root.backgroundColor = .systemBackground;view=root}
    private func runTerminalCleanup(args:[String],nonce:UUID,activationReady:Bool) {
            var fields:[String:Any]=["version":"1.0.0","kind":"TEST_NATIVE_TERMINAL_STORE_CLEANUP_OBSERVATION",
                "nonce":nonce.uuidString.lowercased(),"stage":"platform_prerequisites",
                "session_absent":false,"checkpoint_absent":false,"vault_delete_attempts":0,
                "checkpoint_delete_attempts":0,"unknown_storage_action":false,
                "credential_values_exported":0,"network_calls":0,"provider_calls":0,"closure_calls":0,
                "web_bootstrap_started":Self.webBootstrapStarted,"whole_erasure_verified":false]
            let modes=[Self.argument,Self.checkpointArgument,Self.sessionCheckpointArgument,Self.preparationArgument,Self.presenceArgument,Self.terminalCleanupArgument]
            if activationReady,!Self.webBootstrapStarted,args.filter({modes.contains($0)}).count==1,
                args.filter({$0=="--miray-withdrawal-probe-nonce"}).count==1,
                UIApplication.shared.applicationState == .active,UIApplication.shared.isProtectedDataAvailable,
                self.view.window?.rootViewController === self,Bundle.main.bundleIdentifier=="com.miraylab.poppy" {
                do {
                    let context=try WithdrawalIOSActualTESTCompiledContract.loadContext()
                    let data=WithdrawalIOSActualTESTCompiledInputs.data
                    let ownerData=try data("app_provider_withdrawal_native_owner_local")
                    let ownerPolicy=try WithdrawalNativeOwnerPolicy(json:ownerData)
                    let owner=try JSONSerialization.jsonObject(with:ownerData) as? [String:Any]
                    guard let service=owner?["vault_service"] as? String,
                        let account=owner?["vault_account"] as? String else {throw WithdrawalNativeReviewError.held}
                    let osOwner=try WithdrawalNativeActualTESTOSOwnerCandidate(policy:ownerPolicy,actualContext:context,presenting:self)
                    defer {osOwner.dispose()}
                    let restartPolicy=try WithdrawalLookupRestartPolicy(json:data("app_withdrawal_lookup_restart_local"))
                    let store=try WithdrawalLookupKeychainCandidate(policy:restartPolicy,actualContext:context)
                    let result=try WithdrawalLookupRestartReview.removeActualTESTStoresForTerminalReview(
                        terminalConfiguration:data("app_withdrawal_terminal_device_review"),
                        configuration:data("app_withdrawal_lookup_restart_local"),statusConfiguration:data("app_withdrawal_status_http_local"),
                        httpsConfiguration:data("app_provider_withdrawal_https_review"),proofProfileConfiguration:data("app_withdrawal_proof_profile_local"),
                        actualContext:context,store:store,vault:osOwner.vault,ownerConfiguration:ownerData,
                        invalidateOriginalOwner:{osOwner.dispose()},deleteOriginalVault:{
                            let authentication=LAContext();authentication.interactionNotAllowed=true
                            let query:[String:Any]=[kSecClass as String:kSecClassGenericPassword,
                                kSecAttrService as String:service,kSecAttrAccount as String:account,
                                kSecAttrSynchronizable as String:false,kSecUseAuthenticationContext as String:authentication]
                            guard SecItemDelete(query as CFDictionary)==errSecSuccess else {throw WithdrawalNativeReviewError.held}
                        })
                    for (key,value) in result where key != "kind" {fields[key]=value}
                } catch {fields["stage"]="terminal_context_unconfirmed"}
            }
            if let raw=try? JSONSerialization.data(withJSONObject:fields,options:.sortedKeys),raw.count<=4096 {
                FileHandle.standardOutput.write(Data("MIRAY_WITHDRAWAL_TERMINAL_STORES_V1 ".utf8)+raw+Data([10]))
            }
            Darwin.exit(EXIT_SUCCESS)
    }
    override func viewDidAppear(_ animated:Bool) {
        super.viewDidAppear(animated)
        guard !started else {return};started=true
        let args=ProcessInfo.processInfo.arguments
        guard Self.requested,let index=args.firstIndex(of:"--miray-withdrawal-probe-nonce"),index+1<args.count,
            let nonce=UUID(uuidString:args[index+1]) else {return}
        if args.contains(Self.presenceArgument) {
            // Presence only: never request Keychain data/attributes, construct
            // a member host, start the web view, or normalize/delete a record.
            var fields:[String:Any]=["version":"1.0.0","kind":"TEST_NATIVE_STORE_PRESENCE_OBSERVATION",
                "nonce":nonce.uuidString.lowercased(),"stage":"platform_prerequisites",
                "session_present":false,"checkpoint_present":false,"observation_complete":false,
                "presence_queries":0,"credential_value_reads":0,"store_writes":0,
                "network_calls":0,"provider_calls":0,"closure_calls":0,
                "web_bootstrap_started":Self.webBootstrapStarted]
            let modes=[Self.argument,Self.checkpointArgument,Self.sessionCheckpointArgument,Self.preparationArgument,Self.presenceArgument,Self.terminalCleanupArgument]
            if !Self.webBootstrapStarted,args.filter({modes.contains($0)}).count == 1,
                args.filter({$0 == "--miray-withdrawal-probe-nonce"}).count == 1,
                UIApplication.shared.isProtectedDataAvailable,Bundle.main.bundleIdentifier == "com.miraylab.poppy" {
                do {
                    let data=WithdrawalIOSActualTESTCompiledInputs.data
                    let owner=try JSONSerialization.jsonObject(with:data("app_provider_withdrawal_native_owner_local")) as? [String:Any]
                    let restart=try JSONSerialization.jsonObject(with:data("app_withdrawal_lookup_restart_local")) as? [String:Any]
                    guard let sessionService=owner?["vault_service"] as? String,
                        let sessionAccount=owner?["vault_account"] as? String,
                        let checkpointService=restart?["vault_service"] as? String,
                        let checkpointAccount=restart?["vault_account"] as? String else {throw WithdrawalNativeReviewError.held}
                    for (key,service,account) in [("session_present",sessionService,sessionAccount),
                        ("checkpoint_present",checkpointService,checkpointAccount)] {
                        let context=LAContext();context.interactionNotAllowed=true
                        let query:[String:Any]=[kSecClass as String:kSecClassGenericPassword,
                            kSecAttrService as String:service,kSecAttrAccount as String:account,
                            kSecAttrSynchronizable as String:false,kSecUseAuthenticationContext as String:context,
                            kSecMatchLimit as String:kSecMatchLimitOne]
                        fields["presence_queries"]=(fields["presence_queries"] as? Int ?? 0)+1
                        let status=SecItemCopyMatching(query as CFDictionary,nil)
                        guard status == errSecSuccess || status == errSecItemNotFound else {throw WithdrawalNativeReviewError.held}
                        fields[key]=status == errSecSuccess
                    }
                    fields["stage"]="presence_observed";fields["observation_complete"]=true
                } catch {fields["stage"]="presence_unconfirmed"}
            }
            if let raw=try? JSONSerialization.data(withJSONObject:fields,options:.sortedKeys),raw.count<=4096 {
                FileHandle.standardOutput.write(Data("MIRAY_WITHDRAWAL_STORE_PRESENCE_V1 ".utf8)+raw+Data([10]))
            }
            Darwin.exit(EXIT_SUCCESS)
        }
        if args.contains(Self.terminalCleanupArgument) {
            Task { @MainActor in
                let configuration=(try? WithdrawalIOSActualTESTCompiledInputs.data("app_withdrawal_terminal_console_readiness_local")) ?? Data()
                let ready=await WithdrawalTerminalConsoleReadiness.wait(configuration:configuration,
                    protected:{UIApplication.shared.isProtectedDataAvailable},
                    ready:{UIApplication.shared.applicationState == .active && self.view.window?.rootViewController === self})
                self.runTerminalCleanup(args:args,nonce:nonce,activationReady:ready)
            }
            return
        }
        Self.installPreparationWatchdogIfRequested()
        Task { @MainActor in
            var observation:[String:Any]=["prepared":false,"stage":"platform_prerequisites",
                "host_preparation_count":0,"binding_read_attempts":0,"original_presentation_live":false]
            for _ in 0..<10 {
                if UIApplication.shared.applicationState == .active,UIApplication.shared.isProtectedDataAvailable,
                    let scene=self.view.window?.windowScene,scene.activationState == .foregroundActive {break}
                try? await Task.sleep(nanoseconds:1_000_000_000)
            }
            if args.contains(Self.preparationArgument) {
                Self.preparationStage("controller_visible")
                let previousIdleTimer=UIApplication.shared.isIdleTimerDisabled
                // Only the explicit short diagnostic; ordinary app/OS lock
                // settings are untouched. Process exit releases this override.
                UIApplication.shared.isIdleTimerDisabled=true
                var fields:[String:Any]=["version":"1.0.0","kind":"TEST_NATIVE_PREPARATION_MEMORY_OBSERVATION",
                    "nonce":nonce.uuidString.lowercased(),"stage":"platform_prerequisites","prepared":false,
                    "binding_calls":0,"lookup_calls":0,"checkpoint_reads":0,"checkpoint_writes":0,
                    "login_vault_writes":0,"closure_calls":0,"provider_authentication_calls":0,
                    "web_bootstrap_started":Self.webBootstrapStarted]
                if !Self.webBootstrapStarted,UIApplication.shared.applicationState == .active,
                    UIApplication.shared.isProtectedDataAvailable,self.view.window?.rootViewController === self {
                    do {
                        let context=try WithdrawalIOSActualTESTCompiledContract.loadContext()
                        let data=WithdrawalIOSActualTESTCompiledInputs.data
                        let policies=try WithdrawalHTTPSCompositionReviewPolicies(https:data("app_provider_withdrawal_https_review"),
                            binding:data("app_provider_withdrawal_binding_local"),bindingHTTP:data("app_provider_withdrawal_binding_http_local"),
                            owner:data("app_provider_withdrawal_native_owner_local"),native:data("app_provider_withdrawal_native_local"),
                            closure:data("app_provider_withdrawal_http_local"),status:data("app_withdrawal_status_http_local"),
                            restart:data("app_withdrawal_lookup_restart_local"),kakao:data("app_kakao_withdrawal_http_local"),
                            durable:data("app_withdrawal_durable_native_wire_local"),originalSessionClosure:true)
                        let osOwner=try WithdrawalNativeActualTESTOSOwnerCandidate(policy:WithdrawalNativeOwnerPolicy(json:data("app_provider_withdrawal_native_owner_local")),actualContext:context,presenting:self)
                        defer {osOwner.dispose()}
                        let store=try WithdrawalLookupKeychainCandidate(policy:WithdrawalLookupRestartPolicy(json:data("app_withdrawal_lookup_restart_local")),actualContext:context)
                        fields.merge(await WithdrawalPreparationDiagnostic.run(policies:policies,
                            proofProfileConfiguration:try data("app_withdrawal_proof_profile_local"),actualContext:context,
                            epoch:osOwner.epoch,vault:osOwner.vault,originalStore:store,
                            progress:{Self.preparationStage($0)})) {_,new in new}
                    } catch {fields["stage"]="probe_context"}
                }
                UIApplication.shared.isIdleTimerDisabled=previousIdleTimer
                guard Self.preparationProgress?.claimCompletion(deadline:false) == true else {return}
                if let raw=try? JSONSerialization.data(withJSONObject:fields,options:.sortedKeys),raw.count<=4096 {
                    FileHandle.standardOutput.write(Data("MIRAY_WITHDRAWAL_PREPARATION_MEMORY_V1 ".utf8)+raw+Data([10]))
                }
                Darwin.exit(EXIT_SUCCESS)
            }
            if args.contains(Self.checkpointArgument) || args.contains(Self.sessionCheckpointArgument) {
                var fields:[String:Any]=["version":"1.0.0","kind":"TEST_NATIVE_CHECKPOINT_READONLY_OBSERVATION",
                    "nonce":nonce.uuidString.lowercased(),"stage":"platform_prerequisites",
                    "present":false,"valid":false,"expired":false,"checkpoint_reads":0,
                    "checkpoint_writes":0,"login_vault_reads":0,"network_calls":0,
                    "provider_authentication_calls":0,"closure_calls":0,"web_bootstrap_started":Self.webBootstrapStarted]
                if !Self.webBootstrapStarted,UIApplication.shared.applicationState == .active,
                    UIApplication.shared.isProtectedDataAvailable,self.view.window?.rootViewController === self {
                    do {
                        let context=try WithdrawalIOSActualTESTCompiledContract.loadContext()
                        let data=WithdrawalIOSActualTESTCompiledInputs.data
                        let policy=try WithdrawalLookupRestartPolicy(json:data("app_withdrawal_lookup_restart_local"))
                        let store=try WithdrawalLookupKeychainCandidate(policy:policy,actualContext:context)
                        let sessionInspection=args.contains(Self.sessionCheckpointArgument)
                        let osOwner = try sessionInspection ? WithdrawalNativeActualTESTOSOwnerCandidate(
                            policy:WithdrawalNativeOwnerPolicy(json:data("app_provider_withdrawal_native_owner_local")),actualContext:context,presenting:self) : nil
                        defer {osOwner?.dispose()}
                        if sessionInspection {
                            fields["kind"]="TEST_NATIVE_CHECKPOINT_SESSION_READONLY_OBSERVATION"
                            for key in ["login_read_valid","same_session","same_session_expiry","record_in_latest_attempt","reader_assembly_valid","expired_at_window_start","expired_at_window_end","login_currently_unexpired"] {fields[key]=false}
                        }
                        fields.merge(try WithdrawalLookupRestartReview.inspectActualTESTStoredForReview(
                            configuration:data("app_withdrawal_lookup_restart_local"),
                            statusConfiguration:data("app_withdrawal_status_http_local"),
                            httpsConfiguration:data("app_provider_withdrawal_https_review"),
                            proofProfileConfiguration:data("app_withdrawal_proof_profile_local"),
                            actualContext:context,store:store,vault:osOwner?.vault,
                            ownerConfiguration:try sessionInspection ? data("app_provider_withdrawal_native_owner_local") : nil,
                            observationWindow:sessionInspection ? 1792131359509...1792131371106 : nil)) {_,new in new}
                    } catch {fields["stage"]="checkpoint_context"}
                }
                if let raw=try? JSONSerialization.data(withJSONObject:fields,options:.sortedKeys),raw.count<=4096 {
                    let marker=args.contains(Self.sessionCheckpointArgument) ? "MIRAY_WITHDRAWAL_CHECKPOINT_SESSION_READONLY_V1 " : "MIRAY_WITHDRAWAL_CHECKPOINT_READONLY_V1 "
                    FileHandle.standardOutput.write(Data(marker.utf8)+raw+Data([10]))
                }
                Darwin.exit(EXIT_SUCCESS)
            }
            if !Self.webBootstrapStarted,UIApplication.shared.applicationState == .active,
                UIApplication.shared.isProtectedDataAvailable,self.view.window?.rootViewController === self {
                #if targetEnvironment(simulator)
                let canary=Self.beginOwnedInvalidSessionCanary(args:args)
                #endif
                #if targetEnvironment(simulator)
                let mayPrepare = !args.contains("--miray-owned-empty-simulator-invalid-session-canary") || canary != nil
                #else
                let mayPrepare=true
                #endif
                if mayPrepare,let owner=try? WithdrawalIOSActualTESTRegistrationCandidate(presenting:self) {
                    observation=await owner.prepareReadOnlyForConsole()
                }
                #if targetEnvironment(simulator)
                Self.finishOwnedInvalidSessionCanary(canary,nonce:nonce)
                #endif
            }
            observation["version"]="1.0.0";observation["kind"]="TEST_NATIVE_PREAUTH_READONLY_OBSERVATION"
            observation["nonce"]=nonce.uuidString.lowercased()
            observation["provider_authentication_calls"]=0;observation["lookup_prepare_calls"]=0
            observation["closure_calls"]=0;observation["app_vault_writes"]=0;observation["checkpoint_writes"]=0
            guard let raw=try? JSONSerialization.data(withJSONObject:observation,options:.sortedKeys),raw.count<=4096 else {return}
            FileHandle.standardOutput.write(Data("MIRAY_WITHDRAWAL_PREAUTH_READONLY_V1 ".utf8)+raw+Data([10]))
            Darwin.exit(EXIT_SUCCESS)
        }
    }
}

#if targetEnvironment(simulator)
import Security
extension WithdrawalNativeReadOnlyConsoleViewController {
    private static var canaryQuery:[String:Any] {[
        kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:"com.miraylab.poppy.session-vault",
        kSecAttrAccount as String:"skinanalysis.app.session.v1",kSecAttrSynchronizable as String:kCFBooleanFalse as Any]}
    private static func beginOwnedInvalidSessionCanary(args:[String])->Data? {
        guard args.contains("--miray-owned-empty-simulator-invalid-session-canary") else {return nil}
        let query=canaryQuery
        guard SecItemCopyMatching(query as CFDictionary,nil)==errSecItemNotFound else {return nil}
        let raw=Data("owned-simulator-invalid-session-canary-never-authenticate".utf8)
        var insert=query;insert[kSecValueData as String]=raw;insert[kSecAttrAccessible as String]=kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        guard SecItemAdd(insert as CFDictionary,nil)==errSecSuccess else {return nil};return raw
    }
    private static func finishOwnedInvalidSessionCanary(_ raw:Data?,nonce:UUID) {
        var preserved=false,cleaned=false
        if let raw {
            var read=canaryQuery;read[kSecReturnData as String]=kCFBooleanTrue;read[kSecMatchLimit as String]=kSecMatchLimitOne
            var found:CFTypeRef?
            preserved=SecItemCopyMatching(read as CFDictionary,&found)==errSecSuccess && found as? Data == raw
            if preserved {cleaned=SecItemDelete(canaryQuery as CFDictionary)==errSecSuccess}
        }
        let fields:[String:Any]=["kind":"OWN_EMPTY_SIMULATOR_INVALID_SESSION_CANARY","nonce":nonce.uuidString.lowercased(),
            "setup_ACK":raw != nil,"original_invalid_session_preserved":preserved,"owned_canary_cleanup_ACK":cleaned,
            "web_bootstrap_started":Self.webBootstrapStarted]
        if let data=try? JSONSerialization.data(withJSONObject:fields,options:.sortedKeys) {
            FileHandle.standardOutput.write(Data("MIRAY_NATIVE_ONLY_CANARY_V1 ".utf8)+data+Data([10]))
        }
    }
}
#endif
#endif
