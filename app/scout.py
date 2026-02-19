import json
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.prompts import ChatPromptTemplate
from app.config import MODEL_NAME, SYSTEM_PROMPT

def analyze_patent_risk(user_idea):
    """아이디어를 받아 선행 기술을 검색하고 리스크를 분석"""

    llm = ChatOpenAI(model=MODEL_NAME, reasoning_effort="low")
    search_tool = DuckDuckGoSearchRun()

    # 검색 키워드 추출
    # 사용자의 설명을 검색용 키워드로 변환
    keyword_prompt = ChatPromptTemplate.from_messages([
        ("system", "사용자의 아이디어에서 특허 검색에 필요한 핵심 기술 키워드 3~5개를 영어로 추출해줘. 콤마로 구분."),
        ("human", "{idea}")
    ])
    chain1 = keyword_prompt | llm
    keywords = chain1.invoke({"idea": user_idea}).content

    # 선행 기술 검색
    # 구글 특허 등을 타겟팅하여 검색
    search_query = f"{keywords} site:patents.google.com"
    search_results = search_tool.invoke(search_query)

    # 비교 분석
    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"""
        [내 아이디어]
        {user_idea}
        
        [검색된 선행 기술]
        {search_results}
        
        위 내용을 비교 분석해줘.
        """)
    ])

    chain3 = analysis_prompt | llm
    result_text = chain3.invoke({}).content

    # JSON 파싱 시도
    try:
        return json.loads(result_text)
    except:
        return {"error": "분석 실패", "raw": result_text}