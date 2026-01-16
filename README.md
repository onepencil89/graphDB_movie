# graph DB(neo4j) 활용 영화 추천
## graph RAG 소개
- Graph 데이터베이스를 기반으로 한 질의 응답 시스템(GraphRAG)은 전통적인 벡터 기반 RAG 시스템보다 더 정확하고 연관성 있는 답변을 제공함. 
- 자연어 질문을 Neo4j Cypher 쿼리로 변환하여 지식 그래프를 효과적으로 탐색함.

### 특장점:
- 정확한 관계 검색: 그래프 데이터베이스의 관계 중심 구조를 활용해 복잡한 연결 패턴을 찾을 수 있음.
- 컨텍스트 유지: 엔티티 간의 관계를 유지하여 더 풍부한 컨텍스트를 제공함.
구조화된 정보 검색: 단순 텍스트 검색이 아닌 구조화된 방식으로 정보를 검색함.


# 설치 라이브러리
```
pip install langchain, langchain-neo4j, langchain-openai
pip install pandas
```
# 실습 설명
## 실습1
- 파일 : 1.neo4j_movie_graphdb구축_csv.ipynb
### 내용


1. langchain을 활용한 neo4j 객체 생성 및 연결.

2. 영화 추천 모델 생성을 위한 제약조건/ 인덱스 생성.(스키마 설정)

3. CSV데이터 로드 후 노드 및 관계 생성.

노드 : 
[id, type(Movie, Person, Genre), properties]
관계 
[Person -[ACTED_IN]-> MOVIE,
Person -[DIRECTED_IN]-> MOVIE,
Movie -[IN_GENRE]-> Genre]

4. GraphDB 저장
>>>>>>> Stashed changes

## 실습2
- 파일 : 2.neo4j_movie_basic_search.ipynb
### 내용

핵심 분석 및 기능
본 프로젝트는 다음과 같은 단계별 분석 과정을 거쳐 고도화된 데이터를 도출

① 기초 통계 분석
- 평점 기반 분석: 평점이 높은 상위 영화를 추출하여 양질의 콘텐츠를 식별

- 다작 배우 분석: 배우별 출연 횟수 순위를 분석하여 영화 산업 내 핵심 인물을 파악

- 장르 분포 분석: 장르별 영화 수 분포를 확인하여 데이터의 편향성을 점검

② 관계 기반 심층 분석
- 공동 출연 분석: 특정 배우(예: Tom Hanks)와 가장 많이 호흡을 맞춘 배우들을 추적하여 인적 네트워크를 파악

- 협업 시너지 분석: 특정 배우가 특정 감독과 작업한 횟수를 계산하여 배우-감독 간의 전문적인 협업 관계를 분석

③ 그래프 기반 추천 로직 (Recommendation)
- 장르 기반 추천: 동일한 장르를 공유하면서 평점이 검증된 영화를 선별하여 추천

- 복합 가중치 추천: 장르 공유와 출연 배우 공유 여부를 수식화하여 연관성이 가장 높은 영화를 정교하게 도출

4. 기술 스택
Database: Neo4j Graph Database

Language: Python, Cypher Query Language

Library: LangChain (Neo4jGraph), Pandas


## 실습3
- 파일 : 3.neo4j_movie_full-text_search.ipynb
### 내용

 핵심 분석 및 기능

① 기초 통계 및 전문 검색(Full-Text Search) 분석
- 평점 및 다작 분석: 평점이 높은 상위 영화 및 배우별 출연 횟수 순위 분석을 통한 핵심 데이터 식별.

- 전문 검색 인덱싱: Movie의 제목/태그라인 및 Person의 이름에 대한 전문 검색 인덱스를 생성하여 고속 검색 환경 구축.

- 지능형 검색 쿼리: 퍼지 검색(오타 허용), 와일드카드, 논리 연산자(AND/OR/NOT), 가중치 부여(Boosting) 검색 기능 구현.

② 관계 기반 심층 및 복합 분석
- 공동 출연 및 협업 분석: 특정 인물 중심의 인적 네트워크 및 배우-감독 간의 전문적인 협업 시너지 분석.

- 검색과 탐색의 결합: 전문 검색으로 시작 노드를 찾은 후, 그래프 탐색을 통해 출연 배우 목록 등 연관 데이터를 실시간 추출.

- 다중 인덱스 복합 검색: 영화 제목 인덱스와 인물 이름 인덱스를 동시에 활용하여 "특정 배우가 출연한 특정 키워드 제목의 영화" 도출.

③ 그래프 기반 추천 로직 (Recommendation)
- 장르 기반 추천: 동일 장르 공유 및 평점 검증 데이터를 바탕으로 한 유사 영화 추천.

- 복합 가중치 추천: 장르 공유와 출연 배우 공유 여부를 수식화하여 연관성이 가장 높은 영화를 정교하게 도출.


## 실습4
- 파일 : 4.neo4j_movie_vector_search.ipynb
### 내용

목적: 텍스트 의미 유사성을 바탕으로 한 비정형 데이터 검색 환경 구축

임베딩 데이터 생성: OpenAI text-embedding-3-small 모델을 사용하여 영화 줄거리(Overview)를 고차원 벡터로 변환.

벡터 인덱스 구축: Neo4j 내 vector 타입 속성에 임베딩 데이터를 저장하고 벡터 인덱스(movie_content_embeddings) 생성.

시맨틱 검색 구현: 키워드가 일치하지 않아도 "전쟁 중의 우정"과 같은 의미적 문맥을 파악하여 유사 영화 도출.

유사도 기반 결과 추출: 코사인 유사도 등을 바탕으로 질문과 가장 가까운 상위 K개의 영화 노드 반환.

## 실습5
- 파일 : 5.neo4j_movie_text2cypher.ipynb

### 내용

목적: 자연어 질문을 그래프 쿼리(Cypher)로 자동 변환하여 데이터 질의

그래프 스키마 정보 활용: DB 스키마 정보를 LLM에 전달하여 정확한 노드와 관계를 참조하도록 설정.

Cypher Query Generation: 사용자의 일상어 질문을 Neo4j 전용 쿼리문으로 변환하는 GraphCypherQAChain 구현.

복합 질의 처리: "특정 배우와 특정 감독이 함께 작업한 영화" 등 다단계 관계가 필요한 질문에 대한 자동 쿼리 생성 및 실행.

자연어 답변 생성: 쿼리 실행 결과로 얻은 데이터를 LLM이 다시 자연어 문장으로 정제하여 사용자에게 전달.

## 실습6
- 파일 : 6.neo4j_movie_graphVector_RAG.ipynb

### 내용

목적: 벡터 검색의 유연성과 그래프 탐색의 정확성을 결합한 고도화된 RAG 구현

하이브리드 검색 아키텍처: 벡터 검색을 통해 검색 진입점(Entry Point)을 찾고, 그래프 탐색으로 연관 데이터를 확장하는 구조.

데이터 컨텍스트 확장: 검색된 영화와 연결된 배우들의 필모그래피, 상세 메타데이터 등을 그래프 탐색을 통해 풍부하게 수집.

Orchestrator 구현: similarity_search ➔ graph_query ➔ format_context로 이어지는 데이터 파이프라인 구축.

고도화된 응답 생성: 단순 검색 결과 나열이 아닌, 관계 기반으로 확장된 정보를 바탕으로 LLM이 심층적인 답변 제공.

## 실습7
- 파일 : 7.neo4j_movie_graphRAG_hybrid.ipynb

1. 프로젝트 개요
벡터 검색의 유연한 탐색 능력과 그래프 DB의 엄밀한 관계 추론 능력을 결합한 완성형 GraphRAG 파이프라인 구축. 단순한 데이터 검색을 넘어 데이터 간의 연결성을 활용하여 인간의 기억 모델과 유사한 방식으로 정보를 확장하고 답변을 생성하는 것이 목적.

2. 핵심 프로세스 (Core Architecture)
① Entry Point 탐색 (Vector Search)
비정형 데이터 검색: 사용자의 자연어 질문과 가장 유사한 영화 노드를 벡터 인덱스에서 빠르게 식별.

임베딩 모델: OpenAI text-embedding-3-small을 사용하여 고차원 의미 분석 수행.

② 지식 확장 (Knowledge Expansion)
그래프 탐색: 식별된 노드를 기점으로 :ACTED_IN 관계 등을 추적하여 연관된 배우 및 메타데이터 수집.

필모그래피 확장: 검색된 배우의 ID를 기반으로 해당 배우가 출연한 다른 작품들을 추가로 조회하여 문맥에 포함.

③ 문맥 풍부화 및 답변 생성 (Augmentation & Generation)
Orchestrator 엔진: Vector Search ➔ Graph Search ➔ Data Formatting 과정을 하나의 함수로 총괄.

LCEL 체인 구축: RunnablePassthrough와 RunnableLambda를 활용하여 데이터 파이프라인을 선언적으로 구성.

전문가 페르소나: 주어진 정보에만 기반하여 객관적이고 사실적인 답변을 하도록 프롬프트 가이드라인 설정.

3. 주요 기능 요약 (Features)
구조적 하이브리드: 검색의 시작은 벡터(비정형), 정보의 확장은 그래프(정형) 데이터 활용.

중복 제거 로직: 수집된 배우 ID들의 중복을 제거하여 쿼리 효율성을 높이고 데이터 일관성 유지.

동적 컨텍스트: 질문에 따라 관련 영화, 평점, 출연진, 배우의 타 출연작까지 포함된 풍부한 배경지식(Context) 생성.

4. 기술 스택
Graph Database: Neo4j (Enhanced Schema 활용)
LLM: OpenAI GPT-4o-mini
Framework: LangChain (Neo4jVector, Neo4jGraph, LCEL)
Language: Python (dotenv 활용 환경 제어)

### Neo4j 기반 하이브리드 RAG
- Vector RAG + Graph RAG를 활용한 서비스 구현하기


