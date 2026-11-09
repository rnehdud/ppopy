import Foundation

// Only fixed, non-identifying text leaves the native read-only handle.
public struct WithdrawalLookupPresentation: Sendable, Equatable {
    public let title: String, account: String, connection: String, dataDeletion: String
    public init(result: WithdrawalNativeStatusReviewResult) {
        title = "탈퇴 처리 상태"
        account = result.accountClosedInRecord ? "계정 이용 종료 기록을 확인했어요" : "계정 이용 종료 기록이 아직 없어요"
        connection = result.providerAcknowledgedInRecord
            ? "연결 해제 응답이 기록돼 있어요. 기기 연결 상태는 아직 확인되지 않았어요."
            : "연결 해제 완료 여부를 아직 확인하지 못했어요."
        dataDeletion = "전체 데이터 삭제 완료 여부는 아직 확인되지 않았어요."
    }
}
#if canImport(SwiftUI)
import SwiftUI

// A presentation owns one visible lifetime. Cancellation retires it even when
// a read port ignores cancellation; it cannot publish a late status or retry.
@MainActor final class WithdrawalLookupScreenState: ObservableObject {
    @Published private(set) var result: WithdrawalLookupPresentation?
    @Published private(set) var loading = false
    @Published private(set) var failed = false
    @Published private(set) var retired = false
    private let reader: any WithdrawalLookupReadOnlyPort
    private let retireHost: @MainActor () -> Void
    private var visible = false
    private var readTask: Task<Void, Never>?

    init(reader: any WithdrawalLookupReadOnlyPort, retireHost: @escaping @MainActor () -> Void = {}) {
        self.reader = reader; self.retireHost = retireHost
    }
    func appear() { if !retired { visible = true } }
    func disappear() {
        guard !retired else { return }
        visible = false; retired = true
        result = nil; failed = false; loading = false
        readTask?.cancel()
        retireHost()
    }
    func confirmLookup() {
        guard visible && !retired && readTask == nil else { return }
        // A previous response does not describe the outcome of this new read.
        result = nil; failed = false; loading = true
        readTask = Task { @MainActor [weak self, reader] in
            defer {
                self?.readTask = nil
                if self?.retired == false { self?.loading = false }
            }
            do {
                try Task.checkCancellation()
                let value = try await reader.readOriginalStatusExplicit()
                try Task.checkCancellation()
                guard let self, self.visible && !self.retired else { return }
                self.result = WithdrawalLookupPresentation(result:value)
            } catch {
                guard !Task.isCancelled, let self, self.visible && !self.retired else { return }
                self.failed = true
            }
        }
    }
}

// Local UI review only. There is no login, consent, close or automatic polling
// action. Accepted policy has no operating plugin or transport registration.
@MainActor public struct WithdrawalLookupStatusScreenReview: View {
    @StateObject private var state: WithdrawalLookupScreenState
    @Environment(\.dismiss) private var dismiss
    @Environment(\.colorScheme) private var colorScheme
    private var actionTint: Color {
        colorScheme == .dark ? Color(red: 0.60, green: 0.88, blue: 0.79) : Color(red: 0.094, green: 0.302, blue: 0.278)
    }
    private var actionInk: Color { colorScheme == .dark ? .black : .white }
    public init(reader: any WithdrawalLookupReadOnlyPort) {
        _state = StateObject(wrappedValue:WithdrawalLookupScreenState(reader:reader))
    }
    init(state: WithdrawalLookupScreenState) { _state = StateObject(wrappedValue:state) }
    public var body: some View {
        ScrollView {
            VStack(alignment:.leading,spacing:24) {
                Text("탈퇴 처리 상태").font(.largeTitle.bold()).accessibilityAddTraits(.isHeader)
                Text("앞서 요청한 탈퇴 작업의 상태만 확인해요.").foregroundStyle(.primary)
                if let result = state.result {
                    VStack(alignment:.leading,spacing:20) {
                        Text(result.account).font(.headline)
                        Text(result.connection)
                        Text(result.dataDeletion).foregroundStyle(.primary)
                    }.padding(24).frame(maxWidth:.infinity,alignment:.leading)
                        .background(Color.secondary.opacity(0.08),in:RoundedRectangle(cornerRadius:24))
                }
                if state.failed {
                    Text("상태를 확인하지 못했어요. 탈퇴 요청을 다시 보내지 않았어요.")
                        .foregroundStyle(.primary).accessibilityLabel("상태 확인 실패. 탈퇴 요청을 다시 보내지 않았어요.")
                }
                if state.retired {
                    Text("이 화면의 상태 확인을 중단했어요. 다시 열어 확인해 주세요.").foregroundStyle(.primary)
                }
                Button { state.confirmLookup() } label: {
                    HStack {
                        if state.loading { ProgressView().tint(actionInk).accessibilityLabel("상태 확인 중") }
                        Text(state.loading ? "상태 확인 중" : "탈퇴 처리 상태 확인").font(.headline)
                    }.foregroundStyle(actionInk).frame(maxWidth:.infinity,minHeight:52)
                }.buttonStyle(.borderedProminent).disabled(state.loading || state.retired)
                Button { state.disappear(); dismiss() } label: {
                    Text("닫기").frame(maxWidth:.infinity,minHeight:52)
                }.buttonStyle(.bordered).accessibilityLabel("탈퇴 처리 상태 화면 닫기")
            }.padding(24).tint(actionTint)
        }.onAppear { state.appear() }.onDisappear { state.disappear() }
    }
}
#endif
