# 디버깅 리포트 양식

버그 하나를 고칠 때마다 아래 양식을 채웁니다. 한 번에 한 버그만 다룹니다.

## 빈 템플릿

- 문제 증상:
- 기대 동작:
- 재현 방법:
- 실패한 테스트:
- 의심 원인:
- 실제 수정 파일:
- 실행한 확인 명령:
- diff에서 확인한 범위 침범:
- 커밋 메시지:
- 되돌리는 방법:

## 작성 예시 (버그 ① 앞뒤 공백 미처리)

- 문제 증상: 검색창에 "  python  "처럼 공백을 붙여 입력하면 결과가 하나도 안 나온다.
- 기대 동작: 앞뒤 공백을 무시하고 "python"과 같은 결과를 보여 줘야 한다.
- 재현 방법: `filterNotes(loadNotes(), "  python  ")`를 호출한다. 데이터는 data/sample-notes.json.
- 실패한 테스트: "완료기준: 검색어 앞뒤 공백을 무시한다" (padded는 빈 배열, plain은 2개로 길이가 다름).
- 의심 원인: filterNotes.buggy.js에서 query에 trim()을 하지 않아 공백이 검색어에 섞여 있다.
- 실제 수정 파일: src/filterNotes.buggy.js (정규화 부분 한 곳).
- 실행한 확인 명령: `node --test`
- diff에서 확인한 범위 침범: 정규화 한 줄만 바뀌었고 data/나 test/는 건드리지 않았다.
- 커밋 메시지: `fix: trim search query before filtering`
- 되돌리는 방법: 문제가 생기면 `git restore src/filterNotes.buggy.js` 또는 해당 커밋을 `git revert`.
