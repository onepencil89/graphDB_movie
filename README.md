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

- 


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

- 


1. 평점 높은 영화 상위 10개 조회
-----------------------------------
데이터베이스 내 영화 노드를 탐색하여 평점이 높은 순서대로 상위 10개의 작품 정보를 추출함.

쿼리 패턴 정의
대상 노드: (m:Movie)

필터링 조건: m.rating IS NOT NULL (평점 데이터 누락 노드 제외)

주요 로직 설명
MATCH: Movie 라벨을 가진 모든 노드를 탐색함

WHERE: 평점(rating) 속성이 존재하는 영화만 선별하여 데이터 무결성 확보함

RETURN:

영화 제목(m.title), 개봉 연도(m.released), 평점(m.rating)을 각각의 별칭으로 지정하여 반환함

ORDER BY:

DESC(내림차순) 정렬을 사용하여 평점이 높은 고득점 영화부터 정렬함

LIMIT: 전체 결과 중 최상위 10개 레코드만 제한하여 출력함
-----------------------------------

2. 다작 출연 배우 상위 10개 조회

-----------------------------------
그래프 패턴: (p:Person)-[:ACTED_IN]->(m:Movie)

핵심 관계: Person 노드와 Movie 노드 사이의 ACTED_IN(출연) 관계 탐색함

주요 로직 설명
MATCH:

Person 노드에서 시작하여 ACTED_IN 관계를 통해 연결된 모든 Movie 노드 패턴을 찾음

p 변수는 배우를, m 변수는 해당 배우가 출연한 개별 영화를 참조함

RETURN:

배우 이름(p.name)을 'Actor'라는 별칭으로 반환함

count(m) 집계 함수를 사용하여 각 배우별로 연결된 영화 노드의 총 개수를 계산하고 'MovieCount'로 명명함

ORDER BY:

MovieCount 기준 DESC(내림차순) 정렬을 수행하여 다작 배우부터 순차적으로 배치함

LIMIT:

정렬된 전체 리스트 중 상위 10개 레코드만 제한하여 최다 출연 배우 10명을 확정함
-----------------------------------

3. 장르별 영화 수
-----------------------------------
쿼리 패턴 정의

그래프 패턴: (m:Movie)-[:IN_GENRE]->(g:Genre)

핵심 관계: Movie 노드와 Genre 노드 사이의 IN_GENRE(장르 소속) 관계 탐색함

주요 로직 설명
MATCH:
Movie 라벨 노드에서 시작하여 IN_GENRE 관계를 통해 연결된 모든 Genre 노드 패턴을 식별함
m 변수는 영화 노드를, g 변수는 장르 노드를 참조함

RETURN:
장르 노드의 이름(g.name)을 'Genre'라는 별칭으로 반환함
count(m) 집계 함수를 활용하여 동일한 장르 노드에 연결된 영화 노드의 총 합계를 계산함

ORDER BY:
집계된 영화 수(MovieCount)를 기준으로 DESC(내림차순) 정렬을 수행함
이를 통해 가장 많은 작품이 등록된 주요 장르부터 순차적으로 나열함

-----------------------------------
4. 특정 배우와 함께 출연한 배우 및 작품 수 찾기
-----------------------------------
쿼리 패턴 정의
그래프 패턴: (배우A:Person)-[:ACTED_IN]->(영화:Movie)<-[:ACTED_IN]-(배우B:Person)

동적 매개변수: $actor_name 변수를 사용하여 쿼리 재사용성 높임

주요 로직 설명
MATCH:

$actor_name에 해당하는 Person 노드 탐색

해당 배우가 출연한 Movie 노드와 연결된 다른 Person(co_actor) 노드로 경로 확장

WHERE: actor <> co_actor 조건을 통해 결과 집합에서 본인 제외

RETURN & ORDER:

동료 배우 이름과 공동 출연 영화 개수(count(m)) 반환

DESC(내림차순) 정렬로 협업 횟수 상위 배우부터 표시

LIMIT: 상위 5명의 결과만 출력하여 가독성 확보
-----------------------------------

5. 특정 배우(매개변수)가 특정 감독이 만든 작품에 출연한 횟수(상위 5개)
-----------------------------------
쿼리 패턴 정의
->(Movie)<-[:DIRECTED]-(Person)]

그래프 패턴: (배우:Person)-[:ACTED_IN]->(영화:Movie)<-[:DIRECTED]-(감독:Person)

동적 매개변수: $actor_name 변수를 통해 특정 배우를 지정하여 쿼리 결과의 유연성 확보함

주요 로직 설명
MATCH:

특정 배우(a)가 출연(ACTED_IN)한 영화(m)를 탐색함

해당 영화를 감독(DIRECTED)한 감독(d) 노드를 추적하여 경로 완성함

WHERE: 입력받은 매개변수 $actor_name과 배우 노드의 이름이 일치하는 데이터만 필터링함

RETURN:

감독의 이름(d.name)과 배우-감독 간의 협업 영화 개수(count(m))를 반환함

ORDER BY:

협업 횟수(CollaborationCount) 기준 DESC(내림차순) 정렬을 적용함

LIMIT: 최다 협업 감독 상위 5명만 결과에 포함함
-----------------------------------
6. 특정 영화(매개변수)와 동일한 장르의 영화 중 최고 평점 기준 top 5 추출

-----------------------------------
쿼리 패턴 정의
->(Genre)<-[:IN_GENRE]-(Movie)]

그래프 패턴: (기준영화:Movie)-[:IN_GENRE]->(장르:Genre)<-[:IN_GENRE]-(추천영화:Movie)

핵심 로직: 장르 노드를 매개체로 활용하여 두 영화 간의 공통 분모를 찾아내는 협업 필터링 방식 적용함

주요 로직 설명
MATCH:

$movie_title에 해당하는 기준 영화(m)가 속한 장르(g)를 찾음

해당 장르에 동시에 속해 있는 다른 영화(rec)들로 경로를 확장함

WHERE:

m <> rec: 자기 자신을 추천 결과에서 제외함

rec.rating > 7.0: 평점 7.0을 초과하는 검증된 작품만 선별하여 추천 품질을 유지함

RETURN:

추천 영화 제목과 평점 정보를 반환함

collect(g.name): 기준 영화와 공유하는 모든 장르 이름을 리스트 형태로 수집함

ORDER BY:

평점(Rating) 높은 순서로 1차 정렬함

공유 장르 개수(size(SharedGenres))가 많은 순서로 2차 정렬하여 유사도가 높은 작품을 우선 배치함

LIMIT: 최적의 추천 후보 상위 5개만 출력함
-----------------------------------

7. 특정 영화(매개변수)를 기준, 장르 및 주연배우를 기준으로 가중치 부여하고 합산으로 추천영화 추출.
-----------------------------------
쿼리 패턴 정의
그래프 패턴:

(기준영화)-[:IN_GENRE]->(장르)<-[:IN_GENRE]-(추천영화)

(기준영화)<-[:ACTED_IN]-(배우)-[:ACTED_IN]->(추천영화)

핵심 로직: OPTIONAL MATCH를 활용하여 장르나 배우 정보가 일부 일치하지 않더라도 잠재적 추천 후보군을 유지하며 점수를 산출함

주요 로직 설명
MATCH & OPTIONAL MATCH:

특정 제목($movie_title)의 영화와 평점 7.0 초과인 타 영화들을 대상으로 선정함

장르 공유(IN_GENRE) 및 배우 공유(ACTED_IN) 여부를 각각 탐색하되, 해당 관계가 없는 경우를 대비하여 OPTIONAL MATCH로 처리함

WITH & COLLECT:

COLLECT() 함수를 통해 여러 개의 공유 장르와 배우 이름을 각각 배열 형태로 수집함

Score 계산:

추천 점수(score) 알고리즘 적용: (장르 수 × 2) + (배우 수 × 3)

장르보다 출연 배우의 일치에 더 높은 가중치를 부여하여 유사성을 판단함

WHERE & ORDER BY:

점수가 0보다 큰 영화만 필터링하여 최소한 하나의 공통점이 있는 작품만 남김

계산된 추천 점수(score)를 1순위, 평점(Rating)을 2순위로 하여 내림차순 정렬함

LIMIT: 최종 계산된 상위 5개의 맞춤형 영화 정보만 반환함

- 특정영화(hide & seek)의 장르가 [호러, 미스테리, 스릴러] 참여 배우가 로버트 디 니로 일때,
- 어느 영화가 호러, 미스테리이고 배우가 로버티 디 니로 이면 
- 장르가중치 2점, 배우 가중치 3점 - > 2*2 + 1*3 = 7점
-----------------------------------


## 실습3
- 파일 : 3.neo4j_movie_full-text_search.ipynb
### 내용

- 




## 실습4
- 파일 : 4.neo4j_movie_vector_search.ipynb
### 내용


## 실습5
- 파일 : 5.neo4j_movie_text2cypher.ipynb

### 내용


## 실습6
- 파일 : 6.neo4j_movie_graphVector_RAG.ipynb

### 내용

## 실습7
- 파일 : 7.neo4j_movie_graphRAG_hybrid.ipynb

### Neo4j 기반 하이브리드 RAG
- Vector RAG + Graph RAG를 활용한 서비스 구현하기


