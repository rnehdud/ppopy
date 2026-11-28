"""PPO-46 Step 2: 신규 합성 발화·후보를 조립해요. 파일럿/코어는 쓰지 않아요.

작성된 의미 단위와 표현 변형을 조합하는 재현 도구예요. 외부 모델 호출,
독립 Critic 또는 사람 승인이 아니에요. 같은 의미 조합의 7개 표현은
같은 가족/분할에 고정해요. 자동 구조 검사와 의미 검수는 구분해요.
"""
from __future__ import annotations
import hashlib,json,re,sys
from collections import Counter
from pathlib import Path
COS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(COS))
from beauty_agent.nlu_schema import ALLOWED_SYMPTOMS,ALLOWED_TOPICS,load_nlu_whitelist,verify_nlu_extraction
from beauty_agent.slm.prompt_builder import build_nlu_messages
from beauty_agent.v3_contracts import NLURequest,NLUExtractionResult
HERE=COS/'data/nlu/v1'
BASE='d1e9cbecad9741ed014013876c3fc4a8c8472a67'
CORE_SLOTS=['method.body_site','method.water_temperature','method.tools','method.friction','method.drying',
 'cleansing.target_load','cleansing.repeat_wash','cleansing.steps','method.current_routine','method.sequence',
 'method.skin_wetness','method.rinse','method.mixing','moisturizing.after_wash_delay','moisturizing.comfort',
 'moisturizing.coverage','moisturizing.dryness_return','moisturizing.reapplication','sun.outdoor_time',
 'sun.water_contact','sun.sweat','sun.coverage_gaps','sun.exposed_sites','sun.shade_clothing','sun.reapplication',
 'storage.opened_at','storage.decanting','storage.container','storage.sensory_change','storage.expiry',
 'storage.pao','storage.water_ingress','storage.light_air','skin.eye_symptom_context']
A={}
def atom(key,forms,*,slots=(),symptoms=(),products=(),topics=(),hints=()):
    A[key]={'forms':forms.split('|'),'slots':list(slots),'symptoms':list(symptoms),
            'products':list(products),'topics':list(topics),'hints':list(hints)}
def sa(key,var,value,forms,topic,polarity='affirmed'):
    atom(key,forms,slots=[(var,value,polarity)],topics=[topic])

# 값은 발화에 쓴 것만 사용하고 evidence_span에는 선택한 절 전체를 써요.
sa('face','method.body_site','face','얼굴만 씻어요|세안 부위는 얼굴이에요|얼굴 씻는 얘기예요','cleansing_method')
sa('hands','method.body_site','hands','손만 씻는 중이에요|손 씻는 얘기예요|이번엔 손을 씻어요','cleansing_method')
sa('body','method.body_site','body','몸을 씻어요|몸 씻는 얘기예요|이번 세정 부위는 몸이에요','cleansing_method')
sa('warm','method.water_temperature','lukewarm','물은 미지근해요|미지근한 물 써요|물 온도 미지근함','cleansing_method')
sa('hot','method.water_temperature','hot','뜨거운 물 써요|물 온도가 뜨거워요|물은 뜨겁게 해요','cleansing_method')
sa('cold','method.water_temperature','cold','찬물 써요|물은 차가워요|차가운 물로 해요','cleansing_method')
sa('hand_tool','method.tools','hands','손으로 씻어요|세정 도구는 손이에요|손만 도구로 써요','cleansing_method')
sa('brush','method.tools','scrub_brush','세안 브러시 써요|도구는 세안용 브러시예요|브러시로 세안해요','cleansing_method')
sa('cloth','method.tools','washcloth','세정용 천으로 씻어요|도구는 세정용 천이에요|씻을 때 세정 천을 써요','cleansing_method')
sa('sponge','method.tools','sponge','스펀지로 씻어요|세정 도구로 스펀지 써요|스펀지를 세정에 써요','cleansing_method')
sa('gentle','method.friction','gentle','살살 문질러요|문지를 때 힘 약하게 줘요|문지르는 힘은 약해요','cleansing_method')
sa('strong','method.friction','strong','세게 문질러요|문지르는 힘이 세요|박박 문질러요','cleansing_method')
sa('pat','method.drying','pat_gently','물기는 톡톡 두드려 닦아요|물기 닦을 땐 가볍게 두드려요|문지르지 않고 물기를 톡톡 닦아요','cleansing_method')
sa('rub','method.drying','rubbing_strongly','물기는 수건으로 세게 비벼 닦아요|수건으로 물기를 박박 닦아요|물기 닦을 때 세게 문질러요','cleansing_method')
sa('wet','method.skin_wetness','젖은 상태','씻기 전에 피부를 물로 적셔요|씻기 전 피부가 젖어 있어요|피부를 적신 상태에서 씻어요','cleansing_method')
sa('dry_skin','method.skin_wetness','마른 상태','피부가 마른 상태로 씻기 시작해요|씻기 시작할 때 피부는 말라 있어요|물 적시기 전에 씻기 시작해요','cleansing_method')
sa('rinse','method.rinse','물로 헹굼','마무리는 물로 헹궈요|마지막에 물로 씻어내요|끝에는 물 헹굼 해요','cleansing_method')
sa('mix','method.mixing','두 세정제를 손바닥에서 섞음','세정제 둘을 손바닥에서 섞어요|손바닥에 세정제 두 개 섞어서 써요|두 세정제를 손바닥에서 혼합해요','cleansing_method')
sa('makeup','cleansing.target_load','makeup_requires_removal','지워야 할 색조 화장이 있어요|제거할 메이크업이 남아 있어요|세정 대상은 색조 화장이에요','repeat_cleansing')
sa('soil','cleansing.target_load','heavy_soiling','피부에 흙이 많이 묻었어요|피부에 묻은 흙이 많아요|흙이 잔뜩 피부에 묻음','repeat_cleansing')
sa('no_load','cleansing.target_load','no_additional_removal_need','추가로 지울 건 없어요|더 제거할 것은 없어요|따로 더 지울 게 없음','repeat_cleansing')
sa('habit','cleansing.repeat_wash','habitual_without_reason','이유 없이 습관으로 반복 세안해요|그냥 습관이라 세안을 반복해요|특별한 이유는 없고 반복해서 씻어요','repeat_cleansing')
sa('matched','cleansing.repeat_wash','purpose_matched','남은 화장 제거하려고 반복 세안해요|색조 잔여물 제거가 반복 세안 이유예요|반복하는 이유는 남은 화장을 지우려는 거예요','repeat_cleansing')
sa('one','cleansing.steps',1,'한 번만 해요|세안은 한 차례예요|세수 한번함|씻는 횟수는 1회요|딱 한 번 씻어요|한 번으로 끝내요|세안 1번만 해요','repeat_cleansing')
sa('two','cleansing.steps',2,'두 번 해요|세안은 두 차례예요|세수 두번함|씻는 횟수는 2회요|딱 두 번 씻어요|두 번으로 끝내요|세안 2번 해요','repeat_cleansing')
sa('label_steps','cleansing.steps','according_to_product_removal_instructions',
 '제품 표시대로 해요|제품에 적힌 제거 방법대로 씻어요|횟수는 안 정하고 제거 안내를 따라요|표시된 세정 순서대로만 해요|제품의 제거 지시에 맞춰요|제거 방법은 제품 표시를 따름|제품 표시의 제거법 그대로 해요','repeat_cleansing')
sa('both_steps','cleansing.steps',2,'제품 표시대로 하고 두 번 씻어요|제거 안내를 따르는데 횟수는 두 번이에요|표시 준수해서 세수 두번함|제품 제거법 따르고 총 2회 씻어요|제품 표시대로 하되 두 차례예요|표시 보고 씻는데 두 번으로 끝내요|제품 지시를 따르며 세안 2번 해요','repeat_cleansing')
sa('delay','moisturizing.after_wash_delay','3분','씻고 3분 뒤에 보습해요|세안 후 보습까지 3분 걸려요|보습은 세안하고 삼 분 뒤예요','moisturizing')
sa('sticky','moisturizing.comfort','끈적함','보습 후 느낌이 끈적해요|보습하고 나면 끈적함|보습 뒤 감촉은 끈적해요','moisturizing')
sa('comfort','moisturizing.comfort','편안함','보습 후 느낌은 편해요|보습하고 나면 편안해요|보습 뒤 사용감은 편안함','moisturizing')
sa('coverage','moisturizing.coverage','볼에만 도포','보습은 볼에만 해요|보습 바르는 범위는 볼뿐이에요|볼만 보습해요','moisturizing')
sa('dry_return','moisturizing.dryness_return','2시간',
 '보습 후 2시간쯤 지나면 다시 건조해져요|보습하고 두 시간 뒤엔 다시 건조해요|보습한 뒤 2시간 지나 건조감 돌아와요','moisturizing')
# 재건조 증상도 병행 추출하되 시작일·지속 기간은 만들지 않아요.
A['dry_return']['symptoms']=[('dryness','affirmed','unknown')]
A['dry_return']['topics'].append('discomfort_report')
sa('reapply_moist','moisturizing.reapplication','건조할 때 덧바름','건조할 때 보습을 덧발라요|건조감 있을 때만 보습 추가해요|보습 덧바르는 때는 건조할 때예요','moisturizing')
# 건조 조건문 자체를 현재 증상 발생으로 만들지 않아요.
sa('outside','sun.outdoor_time','prolonged','야외에 오래 있었어요|밖에서 오래 머물렀어요|오랫동안 야외에 있었음','outdoor_sun')
sa('indoors','sun.outdoor_time','none','야외에는 안 나갔어요|밖에 나간 적은 없어요|야외 활동 안 했어요','outdoor_sun')
sa('water','sun.water_contact','yes','물에 들어갔어요|수영했어요|물놀이 했어요','outdoor_sun')
sa('no_water','sun.water_contact','yes','물이 닿지는 않았어요|물 접촉은 없었어요|물에 닿은 적 없음','outdoor_sun','denied')
sa('sweat','sun.sweat','yes','땀이 났어요|땀 흘렸어요|땀이 많이 남','outdoor_sun')
sa('no_sweat','sun.sweat','yes','땀은 안 났어요|땀 안 흘렸어요|땀난 건 아니에요','outdoor_sun','denied')
sa('gaps','sun.coverage_gaps',['귀','목'],'차단제 바를 때 귀랑 목은 빼먹었어요|귀와 목을 차단제 바를 때 빼먹었어요|귀 목은 차단제 누락했어요','outdoor_sun')
sa('exposed','sun.exposed_sites',['손등','팔'],'노출된 곳은 손등과 팔이에요|손등이랑 팔이 드러나 있어요|손등 팔이 노출됐어요','outdoor_sun')
sa('hat','sun.shade_clothing','모자 착용','모자를 썼어요|모자 쓰고 있었어요|모자 착용했어요','outdoor_sun')
sa('shade','sun.shade_clothing','그늘에 머묾','그늘에 머물렀어요|그늘에서 있었어요|그늘에 있었음','outdoor_sun')
sa('sun_reapply','sun.reapplication','2시간마다 덧바름','차단제는 2시간마다 덧발라요|차단제 덧바르는 간격은 두 시간이에요|차단제 두 시간 간격으로 덧바름','outdoor_sun')
atom('no_sun','선크림 안 발랐어요|차단제는 안 바른 상태예요|선크림 안바름',topics=['outdoor_sun'])
# 단일 비도포 보고를 과거 사용 중단으로 추론하지 않아요.
sa('opened','storage.opened_at','지난 금요일','지난 금요일에 열었어요|개봉한 날은 지난 금요일이에요|지난주 금욜에 개봉함','storage_label')
sa('decant','storage.decanting','작은 공병으로 소분','작은 공병에 덜어뒀어요|작은 공병으로 소분했어요|작은 빈 병에 나눠 담음','storage_label')
sa('jar','storage.container','단지형 용기','용기는 단지형이에요|단지 형태 용기예요|통 모양은 단지형임','storage_label')
sa('pump','storage.container','펌프형 용기','용기는 펌프형이에요|펌프가 달린 용기예요|통에 펌프가 있어요','storage_label')
sa('odor','storage.sensory_change','전과 다른 냄새','전이랑 냄새가 달라졌어요|이전과 다른 냄새가 나요|냄새가 예전과 달라짐','storage_label')
sa('expiry','storage.expiry','2027년 8월','사용기한은 2027년 8월로 적혀요|2027년 8월이 사용기한이에요|사용기한 표시 2027년 8월임','storage_label')
sa('pao','storage.pao','개봉 후 6개월','개봉 후 6개월 표시예요|개봉 뒤 여섯 달이라고 써 있어요|열고 6개월 이내라고 적혀요','storage_label')
sa('ingress','storage.water_ingress',True,'용기 안에 물이 들어갔어요|안으로 물이 유입됐어요|통 안에 물 들어감','storage_label')
sa('no_ingress','storage.water_ingress',True,'용기 안에 물은 안 들어갔어요|안으로 물이 들어간 건 아니에요|통 안 물 유입은 없어요','storage_label','denied')
sa('window','storage.light_air','창가 보관','창가에 두고 있어요|보관 장소는 창가예요|창 옆에 보관 중이에요','storage_label')
sa('dark','storage.light_air','서랍 안 보관','서랍 안에 둬요|서랍 안쪽에 보관해요|보관하는 곳은 서랍 안이에요','storage_label')
sa('unknown_open','storage.opened_at',None,'언제 열었는지 몰라요|개봉한 날짜는 기억 안 나요|개봉일 잘 모르겠어요','storage_label','unknown')
sa('unknown_steps','cleansing.steps',None,'횟수는 잘 모르겠어요|몇 번 씻는지는 기억 안 나요|세안 횟수는 모르겠음','repeat_cleansing','unknown')
sa('not_hot','method.water_temperature','hot','뜨거운 물은 안 써요|물은 뜨겁지는 않아요|뜨겁게는 안 해요','cleansing_method','denied')
sa('not_brush','method.tools','scrub_brush','브러시는 안 써요|세안 브러시 안 씀|도구로 브러시 쓰진 않아요','cleansing_method','denied')
sa('not_strong','method.friction','strong','세게 문지르진 않아요|박박 비비는 건 아니에요|강하게 문지르는 건 안 해요','cleansing_method','denied')
sa('not_rub','method.drying','rubbing_strongly','수건으로 세게 비비진 않아요|물기 닦을 때 박박 문지르지 않아요|수건으로 강하게 문지르진 않음','cleansing_method','denied')

# 빈도/시간대 포함 실제 사용은 제품 언급과 current_routine을 함께 남겨요.
for key,forms,raw,value,topic in [
 ('routine_lotion','매일 로션을 써요|로션은 매일 발라요|매일 로션 바름','로션','매일 로션 사용','moisturizing'),
 ('routine_cream','저녁에는 크림을 발라요|크림은 저녁에 써요|저녁에 크림 바름','크림','저녁 크림 사용','moisturizing'),
 ('routine_sun','아침마다 선크림 발라요|선크림은 매일 아침 써요|매일 아침 선크림 바름','선크림','매일 아침 선크림 사용','outdoor_sun'),
 ('routine_gel','아침저녁 젤 세정제 써요|젤 세정제는 아침저녁으로 써요|아침과 저녁에 젤 세정제 씀','젤 세정제','아침저녁 젤 세정제 사용','cleansing_method'),
 ('sequence','저녁마다 로션 다음 선크림 발라요|로션을 바른 뒤 선크림을 저녁마다 써요|매일 저녁 로션 먼저 선크림 나중에 발라요','로션','매일 저녁 로션 후 선크림 사용','routine_conflict')]:
    atom(key,forms,slots=[('method.current_routine',value,'affirmed')],products=[(raw,'using',None)],topics=[topic])
A['sequence']['slots'].append(('method.sequence','로션 다음 선크림','affirmed'))
A['sequence']['products'].append(('선크림','using',None))
A['sequence']['topics']+=['moisturizing','outdoor_sun']

# 증상 11종의 시작·반복·지속·미상을 발화로 구별하고 진단/부위를 보태지 않아요.
SYM={
 'dryness':('건조해요','건조함','건조해'), 'breakout':('트러블이 나요','트러블 남','트러블이 나'),
 'redness':('붉어져요','붉어짐','붉어져'), 'stinging':('따가워요','따가움','따가워'),
 'itching':('가려워요','가려움','가려워'), 'pain':('아파요','통증 있음','아파'),
 'burning':('화끈거려요','화끈거림','화끈거려'), 'swelling':('부어올라요','부어오름','부어올라'),
 'eye_stinging':('눈이 시려요','눈따가움','눈이 시려'), 'peeling':('각질이 벗겨져요','각질 벗겨짐','각질이 벗겨져'),
 'tightness':('당겨요','당김','당겨')}
for name,(a,b,c) in SYM.items():
    for persistence,forms in [
      ('unknown',f'{a}|{b}|지금 {a}'),
      ('recent',f'방금 처음 {a}|조금 전에 처음 {b}|아까 처음 {c}서 말해요'),
      ('repeated',f'자꾸 {a}|반복해서 {b}|괜찮다가 또 {a}'),
      ('persistent',f'며칠째 계속 {a}|며칠 동안 내내 {b}|며칠째 끊이지 않고 {a}')]:
        atom(name+'_'+persistence,forms,symptoms=[(name,'affirmed',persistence)],topics=['discomfort_report'])
    # 부정 증상은 지속 여부를 추측하지 않아요.
    denied={'dryness':'건조하지 않아요|건조함은 없어요|건조한 건 아님',
     'breakout':'트러블은 안 났어요|트러블 난 건 아니에요|트러블은 없어요',
     'redness':'붉어지지 않았어요|붉어짐은 없어요|붉어진 건 아님',
     'stinging':'따갑지는 않아요|따가움은 없어요|따갑진 않음',
     'itching':'가렵지는 않아요|가려움은 없어요|가려운 건 아님',
     'pain':'아프지는 않아요|통증은 없어요|아픈 건 아님',
     'burning':'화끈거리지 않아요|화끈거림은 없어요|화끈거린 건 아님',
     'swelling':'부어오르진 않았어요|부어오름은 없어요|붓지는 않았어요',
     'eye_stinging':'눈은 시리지 않아요|눈따가움은 없어요|눈시림은 아님',
     'peeling':'각질은 벗겨지지 않아요|각질 벗겨짐은 없어요|각질 일어난 건 아님',
     'tightness':'당기지는 않아요|당김은 없어요|당기는 건 아님'}[name]
    atom(name+'_denied',denied,symptoms=[(name,'denied','unknown')],topics=['discomfort_report'])

for key,forms,value,raw in [
 ('eye_wash','씻을 때마다 눈이 시려요|세안할 때마다 눈따가움|세수할 때마다 눈이 따가워요','씻을 때',''),
 ('eye_water','물이 닿을 때마다 눈이 시려요|눈에 물 닿을 때마다 눈따가움|물이 닿으면 매번 눈이 따가워요','물 닿을 때',''),
 ('eye_sweat','땀이 흐를 때마다 눈이 시려요|땀 흐르면 매번 눈따가움|땀이 흘러내릴 때마다 눈이 따가워요','땀 흐를 때',''),
 ('eye_sun','선크림 쓰고 나면 매번 눈이 시려요|선크림 바르면 매번 눈따가움|선크림 쓸 때마다 눈이 따가워요','선크림 사용 후','선크림')]:
    atom(key,forms,slots=[('skin.eye_symptom_context',value,'affirmed')],
      symptoms=[('eye_stinging','affirmed','repeated')],products=[(raw,'using',None)] if raw else [],
      topics=['discomfort_report']+(['outdoor_sun'] if raw else ['cleansing_method'] if key=='eye_wash' else []))

# 가상 상품명. prefix 힌트는 전체 span이 다르면 연결하지 않아요.
for key,raw,state,forms in [
 ('p_use','누리 로션 A','using','요즘 누리 로션 A 써요|누리 로션 A 쓰고 있어요|현재 누리 로션 A 사용 중'),
 ('p_stop','보라 크림 B','stopped','보라 크림 B는 끊었어요|보라 크림 B 사용 중단했어요|보라 크림 B 이제 안 써요'),
 ('p_consider','다온 젤 C','considering','다온 젤 C 살까 고민해요|다온 젤 C 써볼까 생각 중|다온 젤 C 구매 고려 중이에요'),
 ('p_unknown','해솔 토너 D','unknown','해솔 토너 D라는 이름 봤어요|해솔 토너 D 이름만 들었어요|해솔 토너 D라는 이름이 기억나요'),
 ('p_prefix','누리 로션 AB','using','누리 로션 AB 쓰는 중이에요|요즘 누리 로션 AB 써요|누리 로션 AB 사용 중임'),
 ('p_exact','가온 크림 E','using','가온 크림 E 쓰는 중이에요|요즘 가온 크림 E 써요|가온 크림 E 사용 중임'),
 ('p_suffix','다온 젤 CC','considering','다온 젤 CC 사볼까 해요|다온 젤 CC 구매 고민 중이에요|다온 젤 CC 써볼까 생각해요'),
 ('generic','폼클렌저','using','폼클렌저 쓰고 있어요|요즘 폼클렌저 써요|현재 폼클렌저 사용 중이에요')]:
    atom(key,forms,products=[(raw,state,'syn-catalog-gaon-e' if key=='p_exact' else None)],topics=['cleansing_method' if '젤' in raw or key=='generic' else 'moisturizing'])
A['p_prefix']['hints']=[('누리 로션 A','syn-catalog-nuri-a')]
A['p_suffix']['hints']=[('다온 젤 C','syn-catalog-daon-c')]
A['p_exact']['hints']=[('가온 크림 E','syn-catalog-gaon-e')]
A['p_consider']['topics']=['other']
A['p_suffix']['topics']=['other']
A['p_unknown']['topics']=['other']
A['matched']['slots'].append(('cleansing.target_load','makeup_requires_removal','affirmed'))

# 실제 제품명을 명시한 세정제 혼합·차단제 덧바름은 제품 후보도 남겨요.
A['mix']['products']=[('세정제','using',None)]
A['sun_reapply']['products']=[('차단제','using',None)]
A['sun_reapply']['slots'].append(('method.current_routine','차단제 2시간마다 덧바름','affirmed'))
# 도포 중 일부 부위 누락으로 통일해 실제 사용을 보존해요. 타인은 render에서 other_person이에요.
A['gaps']['products']=[('차단제','using',None)]
# 비도포는 단발 행위일 수 있어 stopped로 바꾸지 않아요. 사용 상태는 unknown이에요.
A['no_sun']['products']=[('선크림','unknown',None)]
A['no_sun']['forms'][1]='선크림은 안 바른 상태예요'
atom('app_menu','이 상담 화면의 메뉴가 궁금해요|이 서비스 화면 메뉴를 찾고 있어요|상담 앱 메뉴 위치 알고 싶어요',topics=['other'])

# 기분·날씨 등에서 피부 상태나 제품 소유를 만들지 않는 독립 잡담 단위.
NOISE={
 'hello':'처음 뵙겠어요|반갑습니다|인사드려요', 'thanks':'고맙네요|정말 고마워요|감사드려요',
 'bye':'이만 갈게요|나중에 다시 올게요|다음에 봬요', 'filler':'음 그러니까|어 잠깐만요|흠 뭐였더라',
 'train':'기차가 늦네요|열차가 지연됐어요|기차 기다리는 중이에요',
 'music':'노래 듣고 있어요|음악 듣는 중이에요|노래 재생했어요',
 'book':'책 읽는 중이에요|책장을 넘겼어요|독서하고 있어요',
 'movie':'영화 봤어요|영화 보고 왔어요|영화 한 편 봄',
 'food':'점심 먹었어요|점심 식사 했어요|밥 먹고 왔어요',
 'coffee':'커피 마셨어요|커피 한 잔 마심|커피 마시고 왔어요',
 'work':'회의 끝났어요|회의 마쳤어요|회의가 끝났네요',
 'home':'집에 도착했어요|집에 왔어요|방금 귀가했어요',
 'battery':'휴대폰 배터리가 없네요|폰 배터리가 거의 없어요|휴대폰 충전이 필요해요',
 'parcel':'택배가 내일 온대요|내일 배송된대요|택배 도착은 내일이래요',
 'keyboard':'키보드가 안 눌려요|키보드 한 키가 안 먹어요|키보드 고장났네요',
 'window_noise':'창밖이 시끄럽네요|밖에서 소리가 나네요|창밖 소음이 커요',
 'game':'게임 끝났어요|게임 한 판 마쳤어요|한 판 하고 왔어요',
 'ticket':'표를 예매했어요|티켓 예약했어요|예매 완료했네요',
 'photo':'풍경 사진 봤어요|경치 사진 보고 왔어요|풍경 사진을 구경했어요',
 'clock':'벽시계가 멈췄어요|시계가 안 가네요|벽시계 고장났네요',
 'sorry':'말이 늦었네요|답장이 늦었어요|좀 늦게 왔네요',
 'listen':'말씀 잘 들었어요|이야기 들었어요|내용 읽었어요'}
for key,forms in NOISE.items():atom('noise_'+key,forms)

PLANS=[]
def plan(bucket,key,*atoms,subject='self',subjects=None,previous=None,target=None,val=False,why='원문에 명시된 의미만 후보로 남겨요.'):
    PLANS.append(dict(bucket=bucket,key=key,atoms=atoms,subject=subject,subjects=subjects,previous=previous,target=target,val=val,why=why))

# 각 버킷 20개 의미 가족 × 7개 표현. 마지막 2개 가족은 통째로 검증용.
for key,atoms in [
 ('face_warm_hand',('face','warm','hand_tool')),('body_cold_cloth',('body','cold','cloth')),
 ('brush_force',('brush','strong','rub')),('sponge_gentle',('sponge','gentle','pat')),
 ('wet_rinse',('wet','rinse')),('dry_mix',('dry_skin','mix')),('makeup_count',('makeup','two')),
 ('no_load_habit',('no_load','habit')),('soil_matched',('soil','matched')),
 ('lotion_delay',('routine_lotion','delay','comfort')),('cream_coverage',('routine_cream','coverage','sticky')),
 ('dry_return_reapply',('dry_return','reapply_moist')),('sun_plan',('routine_sun','outside','hat')),
 ('water_sweat',('water','sweat','exposed')),('gaps_reapply',('gaps','sun_reapply','shade')),
 ('opened_window',('opened','window','app_menu')),('decant_jar',('decant','jar','app_menu')),
 ('expiry_pao',('expiry','pao')),('ingress_pump',('ingress','pump')),('odor_dark',('odor','dark'))]:
    plan('turn1_utterance',key,*atoms,val=key in {'ingress_pump','odor_dark'})

# 후속 발화에서 다른 슬롯을 답하면 질문한 슬롯의 값을 임의로 채우지 않아요.
for key,atoms,target,question in [
 ('pure_one',('one',),'cleansing.steps','세안은 몇 번 하세요?'),
 ('pure_two',('two',),'cleansing.steps','세안을 몇 차례 하나요?'),
 ('label_only',('label_steps',),'cleansing.steps','제거 단계는 어떻게 정하나요?'),
 ('explicit_over_label',('both_steps',),'cleansing.steps','몇 번 씻는지 알려 주세요.'),
 ('warm_answer',('warm','gentle'),'method.water_temperature','쓰는 물 온도는 어떤가요?'),
 ('tools_answer',('cloth','rinse'),'method.tools','어떤 도구로 씻나요?'),
 ('delay_answer',('delay','coverage'),'moisturizing.after_wash_delay','씻고 얼마 뒤 보습하나요?'),
 ('sun_answer',('no_water','hat'),'sun.water_contact','물에 들어간 적 있나요?'),
 ('opened_unknown',('unknown_open','jar'),'storage.opened_at','언제 개봉했나요?'),
 ('count_unknown',('unknown_steps','hand_tool'),'cleansing.steps','몇 번 세안하나요?'),
 ('offtopic_temperature',('p_stop','sticky'),'method.water_temperature','물 온도는 어떤가요?'),
 ('offtopic_symptom',('itching_recent','pain_denied'),'cleansing.steps','몇 번 씻으세요?'),
 ('offtopic_storage',('pao','expiry'),'sun.sweat','땀이 났나요?'),
 ('offtopic_product',('p_consider','warm'),'storage.opened_at','언제 열었는지 알려 주세요.'),
 ('offtopic_eye',('eye_sweat','outside'),'moisturizing.coverage','어디에 보습제를 바르나요?'),
 ('offtopic_other',('sweat','shade'),'method.tools','세정 도구는 뭔가요?')]:
    plan('turn2_followup',key,*atoms,target=target,previous=question,subject='other' if key=='offtopic_other' else 'self',
      why='후속 발화에 실제 나온 슬롯만 추출하고, 질문한 슬롯의 답을 만들지 않아요. 횟수·표시 동시 언급은 정수를 우선해요.')
for key,forms,target,question in [
 ('refuse','그 질문은 패스할게요|이건 답하고 싶지 않아요|이번 질문은 건너뛸게요|이 질문엔 응답 안 할게요|대답은 안 할래요|지금 질문은 넘어가요|이건 말하지 않을게요','storage.opened_at','개봉일은 언제인가요?'),
 ('uncertain_bare','잘 모르겠어요|그건 기억 안 나요|확실히는 몰라요|잘 생각이 안 나네요|답을 모르겠네요|그건 모르겠음|정확히 기억 못 해요','sun.reapplication','차단제는 언제 덧발랐나요?'),
 ('topic_drift','기차가 또 늦었네요|방금 노래가 끝났어요|저 지금 표 예매 중이에요|영화표 예약했어요|벽시계 멈춘 거 같네요|키보드가 고장났어요|택배 조회하고 있었어요','cleansing.steps','몇 번 씻으세요?'),
 ('refuse_val','그건 비공개로 할게요|그 내용은 공유 안 할래요|사적인 답은 보류할게요|그 질문은 개인적으로 남길게요|이 답은 공개하고 싶지 않아요|이 부분은 알려드리지 않을게요|그 정보는 말하지 않겠습니다','method.current_routine','지금 루틴을 알려 주세요.')]:
    atom(key,forms)
    # 잘 모름은 질문 대상 자체가 있으므로 null 후보로 남긴다. 거부/잡담은 빈 후보.
    if key=='uncertain_bare':A[key]['slots']=[(target,None,'unknown')];A[key]['topics']=['outdoor_sun']
    plan('turn2_followup',key,key,previous=question,target=target,val=key in {'topic_drift','refuse_val'},
      why='거부·잡담은 빈 후보예요. 단순 모름은 직전 질문의 대상 슬롯을 null/unknown으로 남기며 근거는 현재 발화만 써요.')

for i,(key,atoms) in enumerate([
 ('water_negative',('no_water','outside')),('sweat_negative',('no_sweat','hat')),
 ('two_negatives',('no_water','no_sweat','shade')),('not_hot_hand',('not_hot','hand_tool')),
 ('not_brush_warm',('not_brush','warm')),('not_force_face',('not_strong','face')),
 ('not_rubbing',('not_rub','body')),('not_ingress',('no_ingress','jar')),
 ('pain_not_itch',('pain_denied','itching_unknown')),('itch_not_red',('itching_denied','redness_recent')),
 ('red_not_dry',('redness_denied','dryness_repeated')),('dry_not_tight',('dryness_denied','tightness_persistent')),
 ('tight_not_sting',('tightness_denied','stinging_unknown')),('sting_not_burn',('stinging_denied','burning_recent')),
 ('burn_not_swollen',('burning_denied','swelling_repeated')),('swollen_not_pain',('swelling_denied','pain_persistent')),
 ('breakout_not_peel',('breakout_denied','peeling_recent')),('peel_not_eye',('peeling_denied','eye_stinging_unknown')),
 ('eye_not_sun',('eye_stinging_denied','no_sun')),('neg_water_routine',('no_water','routine_gel','gaps'))]):
    plan('denied_polarity',key,*atoms,val=i>=18,why='부정된 사실의 범위를 유지해요. 물·땀 부정은 yes/denied이며 반대 상태를 추가하지 않아요.')

for i,(key,atoms) in enumerate([
 ('other_wash',('hands','cold','hand_tool')),('other_tool',('brush','gentle','rinse')),
 ('other_routine',('routine_lotion','coverage')),('other_order',('sequence','delay')),
 ('other_sun',('routine_sun','water','sweat','exposed')),('other_storage',('opened','decant','pump')),
 ('other_expiry',('expiry','pao','window')),('other_no_water',('no_water','no_sweat')),
 ('other_eye_wash',('eye_wash','pain_denied')),('other_eye_water',('eye_water','hat')),
 ('other_eye_sweat',('eye_sweat','gaps')),('other_eye_sun',('eye_sun','shade')),
 ('other_dry',('dryness_persistent','comfort','reapply_moist')),('other_breakout',('breakout_repeated','no_load')),
 ('other_red',('redness_recent','cold')),('other_itch',('itching_unknown','jar')),
 ('other_stop',('p_stop','tightness_denied')),('other_consider',('p_consider','dry_skin')),
 ('other_symptoms',('swelling_persistent','pain_recent')),('other_label',('label_steps','p_prefix'))]):
    plan('other_subject',key,*atoms,subject='other',subjects=('self','other') if key in {'other_red','other_itch'} else None,
      previous='친구분은 세안 단계를 어떻게 정하나요?' if key=='other_label' else None,
      target='cleansing.steps' if key=='other_label' else None,val=i>=18,
      why='주체를 절별로 보존해요. 자기/타인 혼합 발화도 있으며 타인의 실제 제품 사용은 other_person이에요. 구매 고려는 실제 사용으로 바꾸지 않아요. 표시 준수의 대상은 후속 질문으로 한정해요.')

symplans=[('dryness_recent','tightness_unknown'),('breakout_persistent','redness_denied'),
 ('redness_repeated','stinging_recent'),('stinging_persistent','pain_denied'),
 ('itching_repeated','dryness_unknown'),('pain_unknown','swelling_denied'),
 ('burning_persistent','redness_unknown'),('swelling_recent','itching_denied'),
 ('eye_stinging_persistent','peeling_denied'),('peeling_repeated','tightness_recent'),
 ('tightness_repeated','burning_denied'),('eye_wash','routine_gel'),('eye_water','cold'),
 ('eye_sweat','no_water'),('eye_sun','no_sweat'),('dry_return','routine_cream'),
 ('breakout_recent','itching_persistent'),('pain_repeated','swelling_unknown'),
 ('burning_unknown','peeling_persistent'),('redness_persistent','tightness_denied')]
for i,atoms in enumerate(symplans):
    plan('high_risk_symptom','symptom_'+str(i+1),*atoms,val=i>=18,
      why='직접 표현된 증상·극성·지속성만 추출해요. 눈시림의 명시적 상황은 context 슬롯을 병행하며 질환·원인은 판단하지 않아요.')

for i,(key,atoms) in enumerate([
 ('using_no_freq',('p_use','warm')),('stopped',('p_stop','odor')),('considering',('p_consider','comfort')),
 ('unknown',('p_unknown','dark')),('prefix',('p_prefix','delay')),('exact',('p_exact','coverage')),
 ('suffix',('p_suffix','jar')),('generic',('generic','hand_tool')),
 ('routine_lotion',('routine_lotion','gaps')),('routine_cream',('routine_cream','dry_skin')),
 ('routine_sun',('routine_sun','no_sweat')),('routine_gel',('routine_gel','pat')),
 ('sequence_mix',('sequence','mix')),('two_products',('p_use','p_consider','sticky')),
 ('stopped_consider',('p_stop','p_suffix','expiry')),('two_names',('p_prefix','p_exact','rinse')),
 ('unknown_generic',('p_unknown','generic','water')),('eye_product',('eye_sun','decant')),
 ('other_product',('p_use','p_exact','pao')),('other_new',('routine_cream','p_unknown','no_ingress'))]):
    plan('product_mention',key,*atoms,subject='other' if i>=18 else 'self',val=i>=18,
      why='제품명 전체 span과 실제 사용 상태만 추출해요. 빈도 없는 사용은 current_routine을 만들지 않고, 명시적 빈도·시간대 사용은 함께 추출해요. 부분 힌트는 null이에요.')

noise_pairs=[('hello','thanks'),('bye','sorry'),('filler','listen'),('train','music'),
 ('book','coffee'),('movie','food'),('work','home'),('parcel','battery'),('game','ticket'),
 ('photo','window_noise'),('hello','book'),('thanks','work'),('bye','movie'),('food','music'),
 ('train','coffee'),('home','game'),('ticket','photo'),('filler','parcel'),('keyboard','listen'),('clock','sorry')]
for i,(a,b) in enumerate(noise_pairs):
    plan('no_signal_noise','noise_'+str(i+1),'noise_'+a,'noise_'+b,val=i>=18,
      why='피부·방법·제품 사용 정보가 없는 잡담이에요. 다른 사람·제품·피부 상태를 추측하지 않고 모든 후보와 토픽을 비워요.')

def content_hash(row):
    data={k:row[k] for k in ['id','scenario_family_id','split','primary_bucket']}
    data.update(system=row['messages'][0]['content'],request=json.loads(row['messages'][1]['content']),expected=json.loads(row['messages'][2]['content']))
    return hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(path,data,jsonl=False):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data) if jsonl else json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def render(p,v):
    slots=[];symptoms=[];products=[];hints=[];topics=[];clauses=[]
    for j,key in enumerate(p['atoms']):
        a=A[key];forms=a['forms']
        # 2절 이상은 어순/구두점만 바꾸지 않고 3×3의 다른 표현을 조합해요.
        idx=(v if len(p['atoms'])==1 else v%3 if j==0 else (v//3+j-1)%3)%len(forms)
        clause=forms[idx]
        # 가벼운 종결어미 오타도 근거 span에 그대로 남겨요. 제품명은 훼손하지 않아요.
        if v==5:clause=clause.replace('어요','어여').replace('해요','해여')
        subject=p['subjects'][j] if p['subjects'] else p['subject']
        if p['subjects']:clause=('저는 ' if subject=='self' else '친구는 ')+clause
        clauses.append(clause)
        for var,value,polarity in a['slots']:
            slots.append(dict(variable_id=var,value=value,polarity=polarity,subject=subject,confidence='high',evidence_span=clause))
        for name,polarity,persistence in a['symptoms']:
            symptoms.append(dict(symptom=name,polarity=polarity,subject=subject,persistence=persistence,evidence_span=clause))
        for raw,state,hint in a['products']:
            # Other-person actual use maps to other_person; considering/stopped retain their explicit state.
            state='other_person' if subject=='other' and state=='using' else state
            products.append(dict(raw_text=raw,usage_state=state,matched_catalog_hint=hint))
        hints.extend(dict(raw_span=raw,matched_catalog_hint=hint,match_score=.94) for raw,hint in a['hints'])
        topics.extend(a['topics'])
    text=('친구 얘기예요. ' if p['subject']=='other' and not p['subjects'] else '')+['. ', ', ', ' / ', '. ', ' 그리고 ', ', ', ' / '][v].join(clauses)
    # 줄바꿈도 채팅 원문 그대로 유지해요.
    if v in (2,5):text=text.replace(' / ','\n')
    dedup=lambda items:list({json.dumps(x,ensure_ascii=False,sort_keys=True):x for x in items}.values())
    # 동일 raw 명칭의 실제 사용이 명시되면 그 명칭의 단순 언급 unknown을 중복 출력하지 않아요.
    known_raw={m['raw_text'] for m in products if m['usage_state']!='unknown'}
    products=[m for m in products if m['usage_state']!='unknown' or m['raw_text'] not in known_raw]
    return text,dedup(slots),dedup(symptoms),dedup(products),dedup(hints),list(dict.fromkeys(topics))
def main():
    assert len(PLANS)==140 and set(Counter(p['bucket'] for p in PLANS).values())=={20}
    assert set(CORE_SLOTS)<=load_nlu_whitelist().variable_ids
    pilot=HERE/'pilot_nlu_v1.jsonl';pilot_hash=hashlib.sha256(pilot.read_bytes()).hexdigest()
    assert pilot_hash=='c5f96332f52c6ad5e5a5e36e0a1249c55cc04f3818f352fd42388cb4ef443cbe'
    rows=[];requests=[];seen=set();semantic_plans=set()
    for p in PLANS:
        signature=(tuple(sorted(p['atoms'])),p['subject'],p['subjects'],p['target'])
        assert signature not in semantic_plans,p['key']
        semantic_plans.add(signature)
        family='nlu-step2-'+p['key']
        for v in range(7):
            text,slots,symptoms,products,hints,topics=render(p,v)
            # Stronger than the stock whitespace-collapse check.
            normalized=re.sub(r'\s+','',text)
            assert normalized not in seen,(p['key'],v,text)
            seen.add(normalized)
            req=NLURequest(source_text=text,catalog_hints=hints,previous_question=p['previous'],target_slot_id=p['target'],
              allowed_variable_ids=CORE_SLOTS,allowed_symptoms=sorted(ALLOWED_SYMPTOMS),allowed_topics=sorted(ALLOWED_TOPICS))
            ext=NLUExtractionResult(source_text=text,topics=topics,slot_candidates=slots,symptom_candidates=symptoms,product_mentions=products,confirmed_by_user=False)
            verify_nlu_extraction(ext,request=req)
            row=dict(id=f'nlu-step2-{len(rows)+1:04d}',scenario_family_id=family,split='val_internal' if p['val'] else 'train',primary_bucket=p['bucket'],
              messages=build_nlu_messages(req)+[dict(role='assistant',content=ext.model_dump_json())],
              provenance=dict(source_origin='new_synthetic',generator_model='GPT-6 based Codex; exact hosting variant unspecified',generation_method='authored semantic atoms and grouped composition variants',critic_status='unreviewed',human_review='unreviewed',base_commit=BASE),
              runtime_invariants=dict(mode='development_preview',production_enabled=False,requires_approval=True,saved=False))
            rows.append(row)
            requests.append(dict(row_id=row['id'],content_sha256=content_hash(row),scenario_family_id=family,split=row['split'],primary_bucket=p['bucket'],
              request=json.loads(row['messages'][1]['content']),expected=ext.model_dump(mode='json'),author_rationale=p['why'],
              semantic_atoms=list(p['atoms']),variant=v,critic_status='unreviewed',human_review='unreviewed'))
    assert len(rows)==980
    write(HERE/'nlu_sft_v1.jsonl',rows,True)
    write(HERE/'reviews/step2_critic_requests.jsonl',requests,True)
    write(HERE/'validation/step2_generation_manifest.json',dict(base_commit=BASE,rows=980,semantic_families=140,variants_per_family=7,
      splits=dict(Counter(r['split'] for r in rows)),primary_buckets=dict(Counter(r['primary_bucket'] for r in rows)),
      dataset_sha256=hashlib.sha256((HERE/'nlu_sft_v1.jsonl').read_bytes()).hexdigest(),pilot_preserved_sha256=pilot_hash,
      generation_method='140 authored compositions, seven controlled linguistic variants per family; not 980 independent real conversations',
      cross_model_critic_performed=False,human_approved=False,base_zero_shot_executed=False,training_executed=False,
      row_hashes={r['row_id']:r['content_sha256'] for r in requests}))
    assert hashlib.sha256(pilot.read_bytes()).hexdigest()==pilot_hash
    print(json.dumps(dict(rows=len(rows),splits=dict(Counter(r['split'] for r in rows))),ensure_ascii=False))
if __name__=='__main__':main()
