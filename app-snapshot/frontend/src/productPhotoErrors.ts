const messages = {
  photo_test_database_warming: "사진 검색 DB를 다시 켜는 중이에요. 잠시 후 다시 시도해 주세요.",
  photo_test_provider_configuration: "사진 검색 서비스의 서버 설정을 확인해야 해요.",
  photo_test_access_required: "사진 검색 연결 코드가 필요해요. 비공개 TEST 연결 설정을 확인해 주세요.",
  photo_test_access_denied: "사진 검색 연결 코드가 승인되지 않았어요. 비공개 TEST 연결 설정을 확인해 주세요.",
  photo_test_unavailable: "AI 사진 검색은 아직 연결 준비 중이에요. 제품명으로 검색해 주세요.",
  photo_test_busy: "이전 사진 검색이 진행 중이에요. 완료 후 다시 시도해 주세요.",
  photo_test_timeout: "사진 검색이 지연되고 있어요. 제품명으로 검색해 주세요.",
  photo_test_network: "사진 검색 서버에 연결하지 못했어요. 네트워크 연결을 확인해 주세요.",
  photo_test_limit: "사진 TEST 검색 한도에 도달했어요. 연결 상태와 시험 한도를 확인해야 해요.",
  photo_test_input_invalid: "서버가 사진 입력을 처리하지 못했어요. 다른 사진을 선택해 주세요.",
  photo_test_provider_failure: "AI 사진 검색 서비스 응답을 받지 못했어요. 잠시 후 다시 시도해 주세요.",
  photo_test_server_unavailable: "사진 TEST 서버를 사용할 수 없어요. 서버 연결 상태를 확인해야 해요.",
  photo_test_route_missing: "사진 검색 서버 경로를 찾지 못했어요. 앱 연결 설정을 확인해야 해요.",
  photo_test_identity_invalid: "제품명 후보를 확인하지 못했습니다. 서버 응답 형식을 확인해야 해요.",
} as const;
export class ProductPhotoSearchError extends Error {
  constructor(readonly code: keyof typeof messages) { super(`${messages[code]} (${code})`); this.name = "ProductPhotoSearchError"; }
}
export function safeNativePhotoError(error: unknown): Error {
  const code = typeof error === "object" && error !== null && "code" in error ? error.code : undefined;
  if (typeof code === "string" && Object.hasOwn(messages, code)) return new ProductPhotoSearchError(code as keyof typeof messages);
  return new Error("AI 사진 검색을 완료하지 못했어요. 제품명으로 검색해 주세요.");
}
