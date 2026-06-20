# 「바이브코딩(VIBE CODING) — 프롬프트에서 하네스까지」 실습 자료

이수미 지음. 이 저장소는 책 「바이브코딩」의 **공식 실습 자료**입니다. 책을 읽다가 실습 표시가 나오면 해당 장의 폴더를 열고 `README.md`를 먼저 확인한 뒤 순서대로 따라 하면 됩니다.

## 무엇이 들어 있나

- **[`chapters/`](chapters/)** — 4부 13장 + 종합(capstone)의 장별 실습. 각 폴더에 학습 목표·프롬프트 예시·실습 안내·예제 파일·체크리스트.
  - 실습 인덱스(장 → 폴더): **[`chapters/README.md`](chapters/README.md)** ← 여기서 시작
- **[`examples/`](examples/)** — 여러 장에 걸쳐 이어 쓰는 예제 앱(할 일 목록 화면, 할 일 API).
- **[`appendix-kit/`](appendix-kit/)** — 부록 즉시활용 자료(설치 트러블슈팅·오류 사전·요금 가이드·프롬프트 치트시트).
- **[`WORKBOOK.md`](WORKBOOK.md)** — 장별 연습문제 + 자기평가 루브릭 + 수료 기준.

## 예제 앱과 실습 스택

이 책은 작은 예제 앱을 여러 장에 걸쳐 이어 쓴다. 언어가 둘인 것은 의도된 구성이며, 바이브코딩의 원리는 언어·프레임워크에 매이지 않는다.

| 예제 앱 | 폴더 | 스택 | 등장 | 확인 |
|---|---|---|---|---|
| 글자 수 세기 | `chapters/part1_foundation/ch03_first_vibecoding/starter/` | HTML·JS | 3장 | 브라우저로 열기 |
| 할 일 목록 화면 | `examples/todo-web/` | HTML·JS | 1·3·4장 | 브라우저로 열기 |
| 할 일 API | `examples/todo-api/` | Python·Flask·pytest | 본문 스크린샷 | `pytest -q` |
| 도서 메모 검색 | `chapters/part3_verify/ch08_done_criteria_tests/` | JavaScript | 8~13장 | `node --test` |

## 코드 받는 법

**git이 있으면**
```
git clone https://github.com/sumilee-pcu/vibecoding-book.git
cd vibecoding-book
```

**git이 처음이라면** — 이 페이지 오른쪽 위 초록색 **Code** 버튼 → **Download ZIP** 으로 내려받아 압축을 풉니다.

**실습 환경**
- 화면 예제(글자 수 세기·할 일 목록): 브라우저에서 해당 `index.html`을 더블클릭해 엽니다. 설치 불필요.
- 자바스크립트 테스트: Node.js 설치 후 해당 폴더에서 `node --test`(또는 `npm test`).
- 파이썬 예제: `pip install -r examples/todo-api/requirements.txt` 후 `pytest -q`.
- Claude Code 설치·첫 실행은 책 2장과 `appendix-kit/`의 설치 트러블슈팅을 참고하세요.

## 라이선스

이 저장소의 **실습 코드와 안내 자료는 학습 목적으로 자유롭게 사용·수정**할 수 있습니다([MIT](LICENSE)). 책 본문 텍스트와 표지는 별도 저작권(저자·부크크)에 속하며 이 저장소에 포함되어 있지 않습니다.

## 책 정보

- 제목: 「바이브코딩(VIBE CODING) — 프롬프트에서 하네스까지」
- 지은이: 이수미 · 펴낸곳: 부크크
- 자매편: 「LLM 애플리케이션 입문」
