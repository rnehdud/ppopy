// swift-tools-version: 6.0
import PackageDescription
let package = Package(name: "PublicAppTransportReview", platforms: [.macOS(.v13), .iOS(.v15)], products: [.library(name: "PublicAppTransportReview", targets: ["PublicAppTransportReview"])], dependencies: [.package(path: "../ProviderWithdrawalNative")], targets: [.target(name: "PublicAppTransportReview", dependencies: [.product(name: "ProviderWithdrawalNativeReview", package: "ProviderWithdrawalNative")])], swiftLanguageModes: [.v5])
