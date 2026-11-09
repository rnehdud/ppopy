import Foundation
import CoreFoundation
import CryptoKit

/// Bytes and SHA must both come from the code-signed app, never a JS call,
/// downloaded configuration or TEST fallback. No OS/SDK operation here.
public struct PublicNativeBundle {
    public let transport: PublicHTTPBinding, verifier: PublicSessionVerifier, maximumArchiveBytes: Int
    public let bootstrap: [String: Any]
    public init(resource: Data, expectedSHA256: String, bundleIdentifier: String, googleClientID: String, kakaoAppID: Int64) throws {
        let digest = SHA256.hash(data: resource).map { String(format:"%02x",$0) }.joined()
        guard resource.count <= 49152, expectedSHA256.count == 64, digest == expectedSHA256,
              let d = try JSONSerialization.jsonObject(with: resource) as? [String:Any],
              (try? JSONSerialization.data(withJSONObject:d,options:[.sortedKeys,.withoutEscapingSlashes])) == resource,
              Set(d.keys) == ["schema_version","scope","bundle_identifier","research_enabled","transport","owner_bindings","google_client_id","kakao_app_id","maximum_sdk_archive_bytes"],
              d["schema_version"] as? String == "1.0.0", d["scope"] as? String == "public_native_bundle_not_GO",
              d["bundle_identifier"] as? String == "com.miraylab.poppy", bundleIdentifier == "com.miraylab.poppy",
              let research = d["research_enabled"] as? NSNumber, CFGetTypeID(research) == CFBooleanGetTypeID(), research.boolValue == false,
              d["google_client_id"] as? String == googleClientID,
              let app = d["kakao_app_id"] as? NSNumber, CFGetTypeID(app) != CFBooleanGetTypeID(), app.stringValue == String(kakaoAppID),
              let maximum = d["maximum_sdk_archive_bytes"] as? NSNumber, CFGetTypeID(maximum) != CFBooleanGetTypeID(), maximum.stringValue == "65536",
              let wire = d["transport"] as? [String:Any], let owners = d["owner_bindings"] as? [String:Any], Set(owners.keys) == ["google","kakao"] else { throw PublicHTTPError.binding }
        func owner(_ provider:String) throws -> (Data,String) {
            guard let row = owners[provider] as? [String:Any], Set(row.keys) == ["public_x963_b64","public_sha256"],
                  let b64 = row["public_x963_b64"] as? String, let data = Data(base64Encoded:b64), data.base64EncodedString() == b64,
                  let sha = row["public_sha256"] as? String else { throw PublicHTTPError.binding }
            return (data,sha)
        }
        let g = try owner("google"), k = try owner("kakao")
        transport = try PublicHTTPBinding(review:JSONSerialization.data(withJSONObject:wire))
        verifier = try PublicSessionVerifier(googlePublicX963:g.0,googleSHA256:g.1,kakaoPublicX963:k.0,kakaoSHA256:k.1,googleClientID:googleClientID,kakaoAppID:kakaoAppID)
        maximumArchiveBytes = maximum.intValue
        bootstrap = ["version":"1.0.0-public-native-bootstrap", "binding":wire["binding"]!, "ownerBindings":owners]
    }
}
