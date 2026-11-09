import Foundation

// Serializes comparison and deletion with this app's main-thread vault writers.
// This is not an OS Keychain compare-and-swap across processes. No SDK/provider
// storage or server/account/whole-erasure receipt can be inferred from it.
@MainActor public enum SessionVaultConditionalRemoval {
    public static func removeIfValueMatches(expected:Data?,maximumDataBytes:Int,
        read:@MainActor () throws->Data?,invalidate:@MainActor ()->Void,
        delete:@MainActor () throws->Void)throws->Bool {
        try ownerRequire(maximumDataBytes>0 && (expected?.count ?? 0)<=maximumDataBytes)
        let current=try read()
        try ownerRequire((current?.count ?? 0)<=maximumDataBytes)
        guard current==expected else{return false}
        guard current != nil else{return true}
        invalidate()
        // Synchronous invalidation observers must not let a replacement value
        // inherit an old removal operation.
        let checked=try read()
        try ownerRequire((checked?.count ?? 0)<=maximumDataBytes)
        guard checked==current else{return false}
        try delete()
        try ownerRequire(try read()==nil)
        return true
    }
}
