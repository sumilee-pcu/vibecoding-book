# 커밋 단위 예시 (verbatim)

버그를 한 번에 하나씩 고치면서, 작업 단위마다 아래처럼 커밋합니다. 한 커밋은 한 가지 일만 합니다.

```
test: add book note search acceptance tests
feat: implement book note filtering
fix: trim search query before filtering
refactor: extract text normalization helper
test: cover no-result search state
```

- `test:` 로 시작하는 커밋은 테스트만 추가/변경합니다.
- `feat:` 는 새 기능 구현, `fix:` 는 버그 수정, `refactor:` 는 동작을 바꾸지 않는 정리입니다.
- 커밋 메시지는 "무엇을 왜"가 한눈에 보이게 한 줄로 적습니다.
