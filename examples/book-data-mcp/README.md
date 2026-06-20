# 도서 데이터 MCP (book-data)

VIBE CODING 11.5 「공공데이터 MCP」 실습용 예제. 키가 필요 없는 공개 도서 API를
감싼 **읽기 전용** MCP 서버다. ISBN이나 제목으로 책의 서지 정보를 조회하고,
언제나 조회 출처를 함께 돌려준다.

## 무엇을 하나

- `lookup_isbn(isbn)` — ISBN으로 제목·저자·출판사·출판일 등을 조회한다.
- `search_books(query, limit)` — 제목·저자·키워드로 책을 검색한다(최대 10건).

두 도구 모두 결과에 `provider`(데이터 출처)와 `source`(조회 URL)를 포함한다.

## 데이터 소스

| 소스 | 키 | 비고 |
|---|---|---|
| Open Library | 불필요 | 영문서 ISBN 조회에 안정적. 키 없을 때 기본 |
| Google Books | 선택(`GOOGLE_BOOKS_API_KEY`) | 무키는 일일 쿼터가 낮음. 키 넣으면 쿼터·한국어 향상 |
| 네이버 책검색 | 선택(`NAVER_CLIENT_ID`/`NAVER_CLIENT_SECRET`) | 한국 책·전자책 커버리지 |
| 카카오 책검색 | 선택(`KAKAO_REST_KEY`) | 다른 카탈로그라 신간이 더 잡히기도 함 |

- 조회 우선순위: 네이버·카카오(키 있으면) → Google(키 있으면) → Open Library → Google(무키 폴백).
- 키는 모두 **환경 변수**로만 읽는다(책 11.5 원칙: 설정 파일에 직접 쓰지 않는다).
- 한국 신간(자가출판 등)은 어느 카탈로그에도 색인이 늦을 수 있다. 도서 데이터 MCP의
  효용은 상위 카탈로그의 색인 범위에 종속된다.

## 설계 원칙 (책 11.5와 동일)

1. **읽기 전용** — 조회 도구만 둔다. 저장·수정 도구는 일부러 두지 않는다.
   메모 반영·파일 저장은 Claude Code 쪽에서 사람의 승인을 받아 처리한다.
2. **출처 표시** — 모든 결과에 provider·source URL을 포함한다.
3. **키 불필요** — 공개 엔드포인트로 바로 시작한다.

## 실행과 등록

```bash
# 의존성
pip install mcp httpx

# (선택) 서버 단독 동작 확인
python _test.py        # 조회 로직
python _mcp_smoke.py   # MCP 핸드셰이크 + 도구 호출

# Claude Code에 등록 (stdio, user scope = 모든 프로젝트에서 사용)
claude mcp add --scope user book-data -- python "$(pwd)/server.py"

# 연결 확인
claude mcp list            # book-data: ... - ✓ Connected
# Claude Code 안에서는 /mcp 로도 확인
```

Windows에서는 `python` 자리에 실제 인터프리터 경로를 넣는 것이 안전하다.

```bash
claude mcp add --scope user book-data -- ^
  "C:/Users/<id>/.pyenv/pyenv-win/versions/3.11.9/python.exe" ^
  "C:/.../examples/book-data-mcp/server.py"
```

## 사용 예 (Claude Code 대화)

```
> 연결된 book-data MCP로 ISBN 9780134685991의 제목과 저자를 조회해 줘. 출처도 같이 보여 줘.

● book-data · lookup_isbn(isbn: "9780134685991")
  └ title    : Effective Java
    authors  : Joshua Bloch
    provider : Open Library
    source   : openlibrary.org/api/books?bibkeys=ISBN:9780134685991
```

저장이 필요한 작업은 조회와 분리하고, 출처를 먼저 본 뒤, 쓰기 행동 앞에 승인을 둔다.

## 제거

```bash
claude mcp remove book-data -s user
```
