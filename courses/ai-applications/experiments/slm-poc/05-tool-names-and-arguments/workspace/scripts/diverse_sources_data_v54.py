"""Small reviewed-source feasibility trial, not a large or independent gold set."""
import collections
import copy
import hashlib
import json
import random
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.audit_trajectory_sources_v51 import prefix_packet
from scripts.build_tool_decision_mix_v1 import validate_calls,native_calls
from scripts.retention_options_data_v50 import read,save,digest,DATA as PREVIOUS_DATA
from agent.generic_fixture_v41 import ASK,NONE
from agent.choice_agent_v1 import TOOL_QUESTION
from agent.decision_context_v37r1 import make_view

DATA=ROOT/'data/processed/diverse-sources-v54';OUT=ROOT/'output/diagnostics/diverse-sources-v54'
START=ROOT/'output/diagnostics/retention-options-v50/balanced/final-adapter'
SEED=540054
PAIRED=(509,534,568,660,672,698,710,711,738)
INITIAL=(6034,7718,6731,302,9829,484,10433,3811,5,156,9605)
REQUESTS={
509:'John Doe의 부모 정보를 모으고 싶어요. 먼저 그의 친족 관계를 조회한 다음 부모에 관한 자세한 정보를 알려 주세요.',
534:"ID가 '98765'인 전시회에 관해 더 알고 싶어요. 전시회 정보를 찾아보고 New York에서 열리는 행사가 포함되는지도 확인해 주세요.",
568:'고객 데이터를 분석해야 해요. 먼저 고객 데이터셋을 가져온 다음 그 데이터의 크기를 조회해 주세요.',
660:'자동차 로봇이 이상하게 작동해요. 먼저 ID 42인 로봇의 센서 데이터를 조회한 다음 같은 로봇에 보고된 오류가 있는지 확인해 주세요.',
672:'미생물학 과제로 E.coli의 대사를 공부하고 있어요. 먼저 E.coli의 일반적인 대사 정보를 확인한 다음 혐기성 호흡에 관한 자세한 정보를 알려 주세요.',
698:"저녁 촬영용 조명을 준비해야 해요. 먼저 'Key Light'의 광도를 확인하고, 현재 값이 50보다 낮으면 밝기를 50으로 조정해 주세요.",
710:'ID가 12345인 제 환자의 정신 건강 평가 결과를 조회하고, 그 결과를 바탕으로 New York에서 이용할 수 있는 관련 사회적 지원 서비스를 찾아 주세요.',
711:"IT 지원 요청 ID가 '12345'예요. 상태와 담당자 배정 여부를 확인하고, 담당자가 없으면 'john_doe'에게 배정해 주세요.",
738:'주식 투자를 계획 중이고 거래 수수료를 줄일 수 있는 프로모션을 받아 보고 싶어요. 먼저 john.doe@example.com을 프로모션 메일 목록에 등록해 주세요. 등록한 다음 ID 102인 시장의 데이터를 확인하고 싶어요.',
6034:'Ben Tennyson에 관해 알려 주세요.',
7718:'다음 지역 모임에서 쓸 보고서를 준비하고 있어요. Austin의 지난 1년간 지역사회 참여 지표를 조회해 주세요.',
6731:"최근 NFL 경기의 박스 스코어를 조회해 주세요. 경기 ID는 '20231217_PIT@KC'예요.",
302:'주방 가전 카테고리에 있는 여러 블렌더를 찾아 주세요. 처음 5개 결과는 건너뛰고 그다음 10개를 보여 주세요.',
9829:'축구 경기 이벤트 7845와 관련된 사건의 자세한 정보를 조회해 주세요.',
484:'제 소셜 미디어에 올릴 수 있는 인내에 관한 격려의 명언을 찾아 주세요.',
10433:'제 Solana 주소의 현재 잔액을 확인해 주세요. 주소는 3aV1hG7f934F6h2Cdkse50982uwq예요. 감사합니다.',
3811:'최근 암호화폐를 조금 접하면서 Bitcoin에 관심이 생겼어요. 현재 시가총액을 알려 주세요.',
5:'YouTube에서 최근 인기를 끄는 동영상을 보여 주세요.',
156:'마음에 드는 TikTok 영상을 워터마크, 표지, 음악 없이 저장하고 싶어요. 주소는 https://www.tiktok.com/@user123/video/1234567890 이에요. 원본 영상을 가져와 주세요.',
9605:'생명윤리를 연구하고 있어요. 이 주제를 다루는 평판 좋은 학술지를 찾아 주세요.'}
DESCRIPTIONS={
'getKinshipInfo':'친족 관계에 관한 정보를 조회한다.','getKinshipRelations':'지정한 사람의 친족 관계를 조회한다.',
'getExhibition':'전시회 정보를 조회한다.','getExhibitionDetails':'전시회의 자세한 정보를 조회한다.',
'fetchData':'빅데이터 정보를 가져온다.','getDataSize':'빅데이터의 크기를 조회한다.',
'getRobotSensors':'자동차 로봇의 센서 데이터를 조회한다.','getRobotErrors':'자동차 로봇에 현재 발생한 오류나 고장을 조회한다.','driveRobot':'자동차 로봇의 이동을 제어한다.',
'getMetabolismInfo':'미생물의 대사 정보를 조회한다.','getMicrobialMetabolismInfo':'지정한 미생물 대사에 관한 자세한 정보를 조회한다.',
'lighting.get_intensity':'영화 촬영 장면에서 지정한 광원의 광도를 조회한다.','lighting.adjust_brightness':'영화 촬영 장면에서 지정한 광원의 밝기를 조정한다.',
'getMentalHealthAssessment':'정신 건강 평가 결과를 조회한다.','getSocialSupport':'사회적 지원 서비스를 조회한다.',
'getSupportTicketStatus':'제출된 IT 지원 요청의 상태를 조회한다.','assignTicket':'IT 지원 요청을 지원 담당자에게 배정한다.','resolveTicket':'제출된 IT 지원 요청을 해결한다.',
'subscribe':'추가 할인 혜택을 위한 프로모션 메일을 구독한다.','Get Market Data':'지정한 시장의 시장 데이터를 조회한다.',
'GetPageCheckBoxFields':'PDF 문서의 지정한 페이지에 있는 체크박스 필드를 조회한다.','GetProjectList':'PWA(Project Web Access) API를 사용해 Project Online의 프로젝트 목록을 조회한다.','Ben 10 API':'Ben 10 시리즈에 관한 JSON 형식의 데이터를 조회한다.',
'getCommunityEngagement':'지역사회의 참여 지표를 조회한다.','sendCommunityNewsletter':'지역사회 구성원에게 소식지를 보낸다.',
'Get NFL Game Box Score - Live Real Time':'현재 시즌의 진행 중이거나 종료된 경기의 전체 박스 스코어를 조회한다. 보통 박스 스코어나 판타지 게임에 쓰이는 통계가 포함된다.','Get Final Four Team Nicknames':'역대 Final Four 팀의 별칭을 알파벳순으로 조회한다.','NCAA Final Four Location':'지정한 연도 Final Four 개최 도시와 경기장을 조회한다.',
'Get Products in Category':'지정한 카테고리에 속한 상품 목록을 조회한다.','Check Social Media Availability':'여러 소셜 미디어 플랫폼에서 사용자 이름을 사용할 수 있는지 확인한다.','Tumblr Username Checker':'Tumblr에서 사용자 이름을 사용할 수 있는지 확인한다.',
'Get Incidents by Event':'지정한 이벤트와 관련된 사건을 조회한다.','Football Team Statistics':'지정한 시즌의 축구팀 통계를 조회한다.','Get Sample Predictions':'여러 시장에 대한 예측이 포함된 전날 경기의 예시를 조회한다.',
'get_quotes_by_keyword':'지정한 키워드와 관련된 명언을 조회한다.','Search Followers by Username and Query':'지정한 Instagram 계정의 팔로워 중 사용자 이름이나 프로필에 지정한 검색어가 있는 사용자를 검색한다.','Story by URL':'URL로 Instagram 스토리를 가져온다.',
'Get Solana Balance':'지정한 Solana 주소의 잔액을 조회한다.','Get Banks by Country':'지정한 나라의 은행 목록과 각 은행의 SWIFT 코드를 조회한다.','Get Historical Stock Data':'지정한 종목 코드와 날짜 범위의 과거 주가 데이터를 조회한다.',
'Get Market Capitalization':'암호화폐의 시가총액을 미국 달러로 조회한다.','Most Active Stocks by Performance with Respect to Country':'지정한 나라에서 실적 기준으로 가장 활발히 거래되는 주식을 조회한다.','Get Exchange Information':'Coinranking에 등록된 지정한 암호화폐 거래소의 자세한 정보를 조회한다. 거래소는 암호화폐를 거래하는 곳이다.',
'Trending Videos':'지역 언어, 국가, 유형 조건에 따라 YouTube 인기 동영상 목록을 조회한다.','Get All Characters':'Throne of Glass 시리즈의 등장인물 목록을 조회한다.','Get EuroMillions Draw Results':'지정한 날짜의 EuroMillions 복권 추첨 결과를 조회한다.',
'Get Original TikTok Video':'TikTok에서 워터마크, 표지, 음악이 없는 원본 영상 내용을 가져온다.','Similar Hashtags API':'지정한 키워드와 비슷한 해시태그 목록을 만든다.','Rising Popular Posts':'Reddit에서 인기가 오르는 게시물을 조회한다.',
'getBioethicsOrganizations':'생명윤리 관련 단체를 조회한다.','getBioethicsIssues':'현재의 생명윤리 쟁점을 조회한다.','getBioethicsJournals':'생명윤리 학술지를 조회한다.'}

def fit(row,tok,korean=False):
    r=copy.deepcopy(row);packet=r['packet'];options=copy.deepcopy(r['options'])
    if korean:
        packet['request']=REQUESTS[int(r['source_id'])]
        for t in r['tools']:
            original=t['description'];translated=DESCRIPTIONS[t['name']]
            if not options[t['name']].startswith(original+'\n'):raise ValueError('Description boundary')
            options[t['name']]=translated+options[t['name']][len(original):]
    v,meta=make_view(TOOL_QUESTION,options,packet,tok)
    if meta['tokens']>512:raise ValueError(('No truncation',r['id'],meta['tokens']))
    target=r['source_target']['tool_calls'][0]['function']['name']
    return {'id':r['id']+(':ko' if korean else ':en'),'question':v['question'],'options':v['options'],'context':v['context'],'target':target,
        'kind':r['kind'],'source_id':r['source_id'],'tokens':meta['tokens'],'source_packet':packet,
        'schema_unchanged':True,'label_source':'assistant reviewed source call; not independent human gold'}

def prepare():
    if DATA.exists() or OUT.exists():raise FileExistsError('V54 protected')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(ROOT/'models/ko-decision-roberta-large',local_files_only=True);tok.model_max_length=1000000
    raw=[json.loads(s) for s in (ROOT/'data/processed/fact-policy-audit-v53/candidates.jsonl').read_text(encoding='utf-8').splitlines()]
    selected=[r for r in raw if (int(r['source_id']) in PAIRED and r['kind'] in ('initial_call','after_tool_call')) or (int(r['source_id']) in INITIAL and r['kind']=='initial_call')]
    if len(selected)!=29 or len({r['source_id'] for r in selected})!=20:raise ValueError(('Source selection',len(selected)))
    for r in selected:
        if not r['single_user_prefix']:raise ValueError('Ambiguous cross-user event attribution')
        validate_calls(native_calls(r['source_target']),r['tools'])
        for m in r['source_prefix']:
            if m.get('tool_calls'):validate_calls(native_calls(m),r['tools'])
        if prefix_packet(r['source_prefix'])!=r['packet'] | {'available_actions': []}:raise ValueError('Prefix facts changed')
    languages={lang:[fit(r,tok,lang=='ko') for r in selected] for lang in ('en','ko')}
    control=read(PREVIOUS_DATA/'balanced-groups.json');refs=read(PREVIOUS_DATA/'references.json')
    groups={'control':control};rng=random.Random(SEED)
    stages={'initial_call':[i for i,r in enumerate(selected) if r['kind']=='initial_call'],
            'after_tool_call':[i for i,r in enumerate(selected) if r['kind']=='after_tool_call']}
    order={k:[] for k in stages}
    needed={'initial_call':60,'after_tool_call':50}
    for kind,pool in stages.items():
        while len(order[kind])<needed[kind]:
            shuffled=pool.copy();rng.shuffle(shuffled);order[kind]+=shuffled
        order[kind]=order[kind][:needed[kind]]
    for lang in ('en','ko'):
        counters=collections.Counter();new=[]
        for g in control:
            batch=[]
            for r in g:
                if r.get('semantic_target') in ('a','b','c') and r['step'] in (0,1):
                    kind='initial_call' if r['step']==0 else 'after_tool_call'
                    batch.append(languages[lang][order[kind][counters[kind]]]);counters[kind]+=1
                else:batch.append(copy.deepcopy(r))
            new.append(batch)
        assert dict(counters)==needed
        groups[lang]=new
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    for arm,g in groups.items():save(DATA/(arm+'-groups.json'),g)
    save(DATA/'references.json',refs);save(DATA/'source29.json',selected)
    save(DATA/'translations.json',{'requests':REQUESTS,'descriptions':DESCRIPTIONS,'reviewer':'assistant translation and semantic review, not independent human review',
        'limits':'Only request and tool description translated. Tool names, argument/property keys, parameter descriptions, JSON results, dates and schemas unchanged. This is Korean-centred mixed input, not fully Korean.'})
    save(OUT/'data-audit.json',{'source_decisions':29,'source_conversations':20,'source_after_tool_decisions':9,
        'source_tool_names':len({t['name'] for r in selected for t in r['tools']}),
        'presentations_replaced':needed,'not_unique_counts':True,'all_target_and_prefix_calls_schema_valid':True,
        'same_no_call_and_skin_rows_and_reference_rows':True,'max_tokens':{lang:max(r['tokens'] for r in rr) for lang,rr in languages.items()},
        'review_exclusions':{'toolace:528:4':'philosophical truth represented as unquestioned boolean; not needed for this feasibility trial',
            'toolace:624:4':'requested robot identity not expressible in selected grabObject schema',
            'toolace:627:4':'player_id fabricated, not returned in live-score output',
            'toolace:633:4':'suitable-event condition underdetermined',
            'toolace:723:4':'medication and specialist both requested; more than one valid next choice',
            'toolace:778:4':'water-quality threshold unspecified',
            'toolace:10615:2':'current gas-price request but historical date fabricated and schema required/default disagreement'}})
    files=list(DATA.glob('*.json'))+[START/'adapter_model.safetensors',ROOT/'data/processed/read-continue-v45/cases.json',ROOT/'data/processed/read-continue-v45/teacher-rows.json',ROOT/'data/processed/description-pairs-v41/cases.json',ROOT/'data/processed/description-pairs-v41/train.json']+[ROOT/p for p in ('scripts/diverse_sources_data_v54.py','scripts/diverse_sources_learning_v54.py','tests/test_diverse_sources_v54.py')]
    save(OUT/'plan.json',{'arms':['control','en','ko'],'seed':SEED,'updates':200,'presentations':600,'lr':1e-5,
        'start':str(START.relative_to(ROOT)),'budget':'400 main + same200 references; only110 positive generic-tool presentations replaced (60initial+50after-tool); all no-call examples unchanged. Same seed, CE, q/v LoRA, optimizer and final-only evaluation.',
        'hypothesis':'A small feasibility test of broader tool descriptions and result-conditioned calls. English vs Korean request/description is a language control. Not enough examples for large-scale or causal tool-variety-only claims.',
        'evaluation':'Freeze all finals before scoring. Old matched72 snapshots,24 heldout-split episodes,previous56 episodes,old360 judgments. These suites have already been repeatedly evaluated. No claim of independent unknown-domain validation.',
        'adoption':'Must beat both initial and replay control on matched-test strict and read-then-write continuation; retain prior needed-tools/old360; no increase in unwanted changes. No deployment. If neither added-source arm passes, reject this small-data variant; do not retune on test.',
        'scope':'20 English source conversations,29 source decisions,9 after-tool continuations; assistant reviewed/translated only. Source tools are never actually invoked; actual execution measured only in existing local fixtures. Historical pretraining/prior source exposure not excluded.',
        'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files}})
    print('V54 frozen; 3 arms, 200 updates, 600 presentations each. Source29 only.',flush=True)

def verify():
    p=read(OUT/'plan.json')
    for path,h in p['frozen_files'].items():
        if digest(ROOT/path)!=h:raise ValueError('Frozen changed: '+path)
    return p

if __name__=='__main__':prepare()
