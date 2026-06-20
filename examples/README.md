# examples — 여러 장에 걸쳐 이어 쓰는 예제 앱

이 책은 작은 예제 앱을 한 장에서 끝내지 않고 여러 장에 걸쳐 다듬어 간다. 여러 장이 함께 쓰는 예제 앱은 여기 `examples/`에 모았다. 한 장에서만 쓰는 예제(글자 수 세기 등)는 해당 장 폴더 안에 있다.

| 예제 앱 | 폴더 | 언어·스택 | 등장하는 곳 | 확인 방법 |
|---|---|---|---|---|
| 글자 수 세기 도구 | `chapters/part1_foundation/ch03_first_vibecoding/starter/` | 순수 HTML·자바스크립트 | 3장 첫 실습 | 브라우저에서 `index.html` 열기 |
| 할 일 목록 앱(화면) | `examples/todo-web/` | 순수 HTML·자바스크립트 | 1·3·4장 화면 | 브라우저에서 `index.html` 열기 |
| 할 일 API | `examples/todo-api/` | 파이썬·Flask·pytest | 본문 스크린샷(6·8·9장 그림) | `pytest -q` |
| 도서 메모 검색 도구 | `chapters/part3_verify/ch08_done_criteria_tests/` 외 | 자바스크립트 | 8~13장 연속 실습 | `node --test` |

## todo-web — 할 일 목록 화면 (HTML·자바스크립트)
입력창과 추가 버튼, 그 아래 목록으로 이뤄진 한 페이지 앱이다. 빈 제목은 추가되지 않고, 우선순위를 고를 수 있으며, 항목을 누르면 완료로 표시(취소선)된다. 데이터는 메모리에만 둔다. 4.1의 강한 프롬프트 예시가 그대로 동작하는 형태다.

- 실행: `examples/todo-web/index.html`을 브라우저에서 연다(설치 불필요).

## todo-api — 할 일 API (Flask·pytest)
같은 할 일 앱을 백엔드 관점에서 본다. 목록 조회·추가·완료 토글·삭제 엔드포인트와 그에 대한 테스트가 들어 있다. 책 본문의 스크린샷(계획 검토, 테스트 통과, git diff)이 이 앱이다.

- 설치: `pip install -r examples/todo-api/requirements.txt`
- 테스트: `cd examples/todo-api && pytest -q`
- 서버: `cd examples/todo-api && flask --app app run`
- `CLAUDE.md`에 이 프로젝트의 작업 규칙(테스트 먼저 작성 등)이 들어 있다.

> 노트: todo-web과 todo-api는 같은 "할 일" 앱을 화면(자바스크립트)과 서버·테스트(파이썬) 두 관점에서 본 것이다. 바이브코딩의 흐름은 언어와 무관하게 똑같이 반복된다.
