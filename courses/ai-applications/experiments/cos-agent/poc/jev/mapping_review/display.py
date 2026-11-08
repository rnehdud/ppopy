"""Human-readable app handoff display; never changes mapping data."""

FIELDS = {
    'kind': '기록 종류', 'observed_at': '관찰 시각', 'concern_presence': '피부 고민 여부',
    'persistence': '고민 지속성', 'recent_change': '최근 변화',
    'discomfort_presence': '불편 반응 여부', 'discomfort_types': '불편 반응 종류',
    'sensitivity_history': '민감 반응 이력', 'version': '계약 버전',
}
VALUES = {
    'reported': '보고됨', 'none_reported': '없다고 보고함', 'unknown': '모름',
    'not_asked': '아직 묻지 않음', 'user_refused': '답변 거절',
    'baseline': '기준 상태', 'checkin': '후속 기록',
    'stinging': '따가움', 'burning': '화끈거림', 'itching': '가려움',
    'tightness': '당김', 'increased_scaling': '각질 증가',
    'redness_tendency': '붉어짐 경향', 'other_no_free_text': '기타',
    'recent': '최근', 'recurring': '반복됨', 'persistent': '지속됨',
    'not_applicable': '해당 없음', 'better': '좋아졌다고 보고함',
    'worse': '나빠졌다고 보고함', 'unchanged': '변화 없음', 'fluctuating': '변동 있음',
}
STATUS = {
    'needs_information': '추가 입력 필요', 'needs_confirmation': '사용자 확인 대기',
    'invalid_input': '입력값 수정 필요', 'blocked': '검증 보류',
    'prepared_disabled': '입력 준비 완료 · 전송 비활성',
}
EXTENSIONS = {
    'distinct_concern_types': '건조함·트러블 등 고민 종류',
    'symptom_observation_details': '증상별 강도·시작 시점 등 상세 정보',
    'product_usage_events': '제품 사용·미사용·계획 사건',
}
ERRORS = {
    'extraction_warnings_require_review': '추출 중 오류 또는 제한이 있어 재확인이 필요합니다.',
    'symptom_information_declined': '증상 정보 제공 거절이 보고되었습니다.',
    'source_revision_invalid_or_missing': '입력 원문의 버전을 확인할 수 없습니다.',
    'confirmation_revision_or_payload_mismatch': '확인 후 입력이 바뀌었습니다. 다시 확인해 주세요.',
    'legacy_assessment_metadata_requires_review': '이전 버전 결과의 판정 정보를 확인해 주세요.',
    'discomfort_presence_mismatch': '불편 반응 여부와 종류가 서로 맞지 않습니다.',
    'observed_at_invalid_utc': '관찰 시각을 UTC 날짜·시간으로 입력해 주세요.',
    'skin_state_keys_mismatch': '필수 필드의 누락 또는 허용되지 않은 필드가 있습니다.',
}


def print_handoff(handoff):
    print('\n' + '=' * 56)
    print('  피부 상태 매핑 결과  |  ' + STATUS.get(handoff['status'], '상태 확인 필요'))
    print('=' * 56)
    payload = handoff.get('payload')
    state = payload if payload is not None else handoff['candidate_skin_state']
    print('\n  ' + ('검증된 입력' if payload is not None else '매핑 후보 · 사용자 확인 전'))
    if not state:
        print('    매핑 가능한 값이 없습니다. 증상이 없다는 뜻은 아닙니다.')
    for field, value in state.items():
        if isinstance(value, list):
            rendered = ', '.join(VALUES.get(v, v) for v in value) or '없음'
        else:
            rendered = VALUES.get(value, str(value))
        print(f"    {FIELDS.get(field, field)}: {rendered}")
    if handoff['questions']:
        print('\n  추가 입력 필요')
        for question in handoff['questions']:
            print('    - ' + FIELDS.get(question['field'], question['field']))
    if handoff['extension_proposals']:
        print('\n  현재 백엔드에서 직접 표현하지 못하는 정보')
        for extension in handoff['extension_proposals']:
            print('    - ' + EXTENSIONS.get(extension, extension))
    if handoff['errors']:
        print('\n  확인할 문제')
        for error in handoff['errors']:
            print('    - ' + ERRORS.get(error, '입력 형식을 확인해 주세요. 상세 사유는 --app-json으로 볼 수 있습니다.'))
    print('\n  DB 전송·저장: 비활성')
    print('  상세 JSON: --app-json  |  추출 디버그: --verbose')
    print('=' * 56)
