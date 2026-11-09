import Foundation

public final class WithdrawalNativeOriginalDocumentFence:@unchecked Sendable {
    private let lock=NSLock(),origin:String,paths:[String]
    private var first=true
    public init(configuration:Data)throws {
        let expected:[String:Any]=["version":"1.0.0","scope":"closed_TEST_native_original_document_registration_review",
            "runtime_registered":false,"credential_read_on_mount":false,"SDK_start_on_mount":false,
            "initial_origin":"capacitor://localhost","initial_root_path":"","initial_slash_path":"/","initial_index_path":"/index.html",
            "initial_query_fragment_allowed":false,
            "navigation":"allow_one_initial_original_local_document_then_terminal_on_any_main_frame_navigation"]
        let raw=try withdrawalFlatObject(configuration)
        try ownerRequire(try JSONSerialization.data(withJSONObject:raw,options:.sortedKeys)==JSONSerialization.data(withJSONObject:expected,options:.sortedKeys))
        origin=raw["initial_origin"] as! String;paths=["initial_root_path","initial_slash_path","initial_index_path"].map {raw[$0] as! String}
    }
    public func navigationIsTerminal(_ url:URL?)->Bool {
        lock.withLock {
            guard first else {return true};first=false
            guard let url,let scheme=url.scheme,let host=url.host,
                scheme+"://"+host==origin,url.port==nil,url.user==nil,url.password==nil,
                url.query==nil,url.fragment==nil,paths.contains(url.path) else {return true}
            return false
        }
    }
}
