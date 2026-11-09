import Foundation

public struct GoogleSDKLocalSnapshot: Equatable, Sendable, CustomStringConvertible, CustomDebugStringConvertible {
    public let subject: String
    public let recordFingerprint: String
    public init(subject:String,recordFingerprint:String)throws {
        try ownerRequire(!subject.isEmpty && subject.utf8.count<=512 && ownerMatches(recordFingerprint,"^[0-9a-f]{64}$"))
        self.subject=subject;self.recordFingerprint=recordFingerprint
    }
    public var description:String{"<GoogleSDKLocalSnapshot redacted>"}
    public var debugDescription:String{description}
}

// .absent requires a successful SDK memory + persistent-store observation.
// An API such as hasPreviousSignIn returning false alone cannot supply it.
public enum GoogleSDKLocalObservation: Equatable, Sendable {
    case absent, present(GoogleSDKLocalSnapshot), unavailable
}

@MainActor public enum GoogleSDKConditionalRetirement {
    public static func retire(expectedVault:Data,verifier:GoogleSDKOwnerProofReview,now:Date,
        readVault:@MainActor ()throws->Data?,observeSDK:@MainActor ()throws->GoogleSDKLocalObservation,
        invalidate:@MainActor ()->Void,removeSDK:@MainActor (GoogleSDKLocalSnapshot)throws->Void,
        removeVault:@MainActor ()throws->Void)throws->Bool {
        let owner=try verifier.verifyVaultForRetirement(expectedVault,now:now)
        guard try readVault()==expectedVault else{return false}
        let original=try observeSDK()
        if case .unavailable=original {throw WithdrawalNativeReviewError.held}
        if case let .present(snapshot)=original {
            guard try owner.matchesGoogleSubject(snapshot.subject) else{return false}
        }
        return try SessionVaultConditionalRemoval.removeIfValueMatches(expected:expectedVault,maximumDataBytes:4096,
            read:readVault,invalidate:invalidate,delete:{
                // Member invalidation may synchronously replace an SDK owner.
                // Compare both identity and opaque persistent record snapshot.
                guard try observeSDK()==original else {throw WithdrawalNativeReviewError.held}
                if case let .present(snapshot)=original {try removeSDK(snapshot)}
                guard try observeSDK() == .absent else {throw WithdrawalNativeReviewError.held}
                // SDK callbacks cannot make a replacement app credential inherit
                // this original deletion, even when SDK retirement succeeded.
                guard try readVault()==expectedVault else {throw WithdrawalNativeReviewError.held}
                try removeVault()
            })
    }
}

public extension GoogleSDKOwnerProofReview {
    func verifyVaultForRetirement(_ data:Data,now:Date)throws->GoogleSDKRetirementOwner {
        let raw=try withdrawalFlatObject(data,maximumBytes:4096)
        try ownerRequire(Set(raw.keys)==["contract_version","session_token","expires_at","native_cleanup_proof"]
            && raw["contract_version"] as? String=="1.1.0-google-sdk-owner-review")
        guard let bearer=raw["session_token"] as? String,let expiry=raw["expires_at"] as? String,
            let envelope=raw["native_cleanup_proof"] as? String else {throw WithdrawalNativeReviewError.held}
        return try verifyForRetirement(Data(envelope.utf8),bearer:bearer,sessionExpiresAt:withdrawalUTCDate(expiry),now:now)
    }
}
