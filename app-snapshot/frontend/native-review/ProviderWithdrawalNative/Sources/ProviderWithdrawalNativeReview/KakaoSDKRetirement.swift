import Foundation

public struct KakaoSDKLocalSnapshot:Equatable,Sendable,CustomStringConvertible,CustomDebugStringConvertible {
    public let accessToken:String
    public let recordFingerprint:String
    public init(accessToken:String,recordFingerprint:String)throws {
        try ownerRequire(ownerMatches(accessToken,"^[A-Za-z0-9._~+/=-]{20,2048}$") && ownerMatches(recordFingerprint,"^[0-9a-f]{64}$"))
        self.accessToken=accessToken;self.recordFingerprint=recordFingerprint
    }
    public var description:String{"<KakaoSDKLocalSnapshot redacted>"}
    public var debugDescription:String{description}
}

// A false SDK boolean alone cannot establish persistent-store absence.
public enum KakaoSDKLocalObservation:Equatable,Sendable {
    case absent,present(KakaoSDKLocalSnapshot),unavailable
}

@MainActor public enum KakaoSDKConditionalRetirement {
    public static func retire(expectedVault:Data,verifier:KakaoSDKOwnerProofReview,now:Date,
        readVault:@MainActor ()throws->Data?,observeSDK:@MainActor ()throws->KakaoSDKLocalObservation,
        invalidate:@MainActor ()->Void,removeSDK:@MainActor (KakaoSDKLocalSnapshot)throws->Void,
        removeVault:@MainActor ()throws->Void)throws->Bool {
        let owner=try verifier.verifyVaultForRetirement(expectedVault,now:now)
        guard try readVault()==expectedVault else{return false}
        let original=try observeSDK()
        if case .unavailable=original{throw WithdrawalNativeReviewError.held}
        if case let .present(snapshot)=original{
            guard try owner.matchesKakaoAccessToken(snapshot.accessToken) else{return false}
        }
        return try SessionVaultConditionalRemoval.removeIfValueMatches(expected:expectedVault,maximumDataBytes:4096,
            read:readVault,invalidate:invalidate,delete:{
                guard try observeSDK()==original else{throw WithdrawalNativeReviewError.held}
                if case let .present(snapshot)=original{try removeSDK(snapshot)}
                guard try observeSDK() == .absent else{throw WithdrawalNativeReviewError.held}
                guard try readVault()==expectedVault else{throw WithdrawalNativeReviewError.held}
                try removeVault()
            })
    }
}
