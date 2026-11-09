import Foundation

// Fixed vocabulary only: no identifiers, credentials, HTTP bodies or errors.
public enum WithdrawalNativePreparationStage:String,Sendable {
    case notStarted="not_started", platformPrerequisites="platform_prerequisites"
    case SDKAdapter="sdk_adapter", checkpointAdapter="checkpoint_adapter"
    case validatingPolicies="validating_policies", readingVault="reading_vault"
    case fetchingBinding="fetching_binding", validatingBinding="validating_binding"
    case bindingVerified="binding_verified", providerAdapter="provider_adapter", ready="ready"
}
@MainActor public final class WithdrawalNativePreparationTrace {
    public private(set) var stage=WithdrawalNativePreparationStage.notStarted
    public private(set) var bindingReadAttempts=0
    public init() {}
    public func mark(_ next:WithdrawalNativePreparationStage) {
        stage=next
        if next == .fetchingBinding {bindingReadAttempts += 1}
    }
}
