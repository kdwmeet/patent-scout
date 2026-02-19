# Patent Scout (특허 침해 가능성 진단 솔루션)

## 1. 프로젝트 개요

Patent Scout는 기업의 R&D 부서, 스타트업, 발명가가 새로운 아이디어나 기술을 기획하는 단계에서 선행 기술(Prior Art)과의 유사성을 분석하고 특허 침해 리스크를 사전에 진단하는 IP(지식재산권) 검증 솔루션입니다.

사용자가 입력한 아이디어를 AI가 분석하여 핵심 기술 키워드를 추출한 뒤, 글로벌 특허 데이터베이스(Google Patents)를 실시간으로 검색합니다. 이후 OpenAI의 **gpt-5-mini** 모델이 '구성요소 완비의 원칙(All Elements Rule)'에 입각하여 사용자의 아이디어와 검색된 선행 특허의 청구항을 문장 단위로 비교 분석하고, 침해 위험도와 회피 설계 전략을 정형화된 리포트로 제공합니다.

### 주요 기능
* **Idea Parsing & Keyword Extraction:** 비정형 자연어로 작성된 아이디어 설명에서 글로벌 특허 검색에 최적화된 영문 기술 키워드를 자동 추출.
* **Targeted Prior Art Search:** 최신 검색 패키지(`ddgs`)를 활용하여 쓰레기 데이터(약관, 안내문 등) 유입을 차단하고 `patents.google.com` 도메인 내의 실제 특허 문헌만 타겟팅하여 검색.
* **Comparative Analysis:** 검색된 선행 특허 요약본/청구항과 사용자의 아이디어를 대조하여 핵심 구성요소의 중복 여부 판단.
* **Risk Scoring & Advice:** 특허 침해 가능성을 0~100점 척도로 정량화하고, 리스크를 회피하기 위한 변리사 관점의 기술적 조언(Design Around) 제공.

## 2. 시스템 아키텍처

본 시스템은 LangChain 프레임워크를 활용하여 검색(Search)과 추론(Reasoning)이 결합된 파이프라인으로 구성되어 있습니다.

1.  **Input:** 사용자의 아이디어 상세 설명 입력.
2.  **Query Generation:** **gpt-5-mini** 모델이 아이디어를 분석하여 3~5개의 핵심 영문 검색어 생성.
3.  **Web Search (Agent Action):** DuckDuckGo Search API(`ddgs`)를 호출하여 구글 특허(Google Patents)에서 선행 기술 검색 수행.
4.  **Synthesis & Evaluation:** 검색 결과를 컨텍스트로 주입하여, 시스템 프롬프트에 정의된 침해 판단 기준(변리사 페르소나)에 따라 텍스트 유사도 및 구성요소 비교.
5.  **Output:** 최종 분석 결과를 JSON 구조로 파싱하여 웹 대시보드에 렌더링.

## 3. 기술 스택

* **Language:** Python 3.10 이상
* **LLM:** OpenAI **gpt-5-mini**
* **Orchestration:** LangChain
* **Search Tool:** DuckDuckGo Search (`ddgs`)
* **Web Framework:** Streamlit
* **Environment Management:** python-dotenv

## 4. 프로젝트 구조

```text
patent-scout/
├── .env                  # 환경 변수 설정 (API Key)
├── requirements.txt      # 의존성 패키지 목록
├── main.py               # 애플리케이션 진입점 및 리스크 리포트 UI
└── app/
    ├── __init__.py
    ├── config.py         # 변리사 페르소나 및 분석 프롬프트, JSON 스키마 정의
    └── scout.py          # 키워드 추출, Google Patents 검색 및 RAG 분석 로직
```

## 5. 설치 및 실행 가이드
### 5.1. 사전 준비
Python 환경이 구성된 상태에서 저장소를 복제하고 프로젝트 디렉토리로 이동하십시오.

```Bash
git clone [레포지토리 주소]
cd patent-scout
```
### 5.2. 의존성 설치
LangChain 및 검색 구동에 필요한 최신 패키지를 설치합니다.

```Bash
pip install -r requirements.txt
```
### 5.3. 환경 변수 설정
프로젝트 루트 경로에 .env 파일을 생성하고, OpenAI API 키를 입력하십시오. 시스템은 dotenv를 통해 실행 시 자동으로 해당 키를 로드합니다.

```Ini, TOML
OPENAI_API_KEY=sk-your-api-key-here
```
### 5.4. 실행
Streamlit 애플리케이션을 실행합니다.

```Bash
streamlit run main.py
```
## 6. 출력 데이터 사양 (JSON Schema)
AI 모델의 분석 결과는 다음의 JSON 구조로 반환되어 시스템의 안정적인 UI 렌더링을 지원합니다.

```JSON
{
  "summary": "검색된 선행 기술들은 대부분 센서를 활용한 자동 급수 제어 방식에 관한 것입니다.",
  "similar_patents": [
    {
      "title": "US1023XXXX: IoT-based Automatic Plant Watering System",
      "similarity": "85%",
      "reason": "토양 습도 센서, 워터 펌프, 모바일 앱 연동이라는 핵심 구성요소가 모두 동일하게 포함되어 있습니다."
    }
  ],
  "risk_score": 85,
  "risk_level": "위험",
  "advice": "단순 습도 기반 급수는 공지 기술이므로, 식물 종류나 날씨 API 데이터를 결합한 인공지능형 급수 알고리즘으로 청구항을 한정하여 회피 설계를 고려하십시오."
}
```
## 7. 실행 화면
<img width="1314" height="786" alt="스크린샷 2026-02-19 145401" src="https://github.com/user-attachments/assets/98e8a119-6410-4fc0-931f-4561dcde1aca" />


## 8. 면책 조항 (Disclaimer)
본 솔루션이 제공하는 특허 침해 가능성 진단 결과는 AI 검색 및 텍스트 유사도 분석에 기반한 1차적인 참고용 데이터입니다. 실제 특허 출원 가능성 판단 및 침해 소송 대응을 위해서는 반드시 대한변리사회의 자격을 갖춘 전문 변리사를 통한 정밀한 선행기술조사(Prior Art Search) 및 감정(FTO)을 진행해야 하며, 본 소프트웨어의 결과물은 법적 증빙 효력을 갖지 않습니다.
