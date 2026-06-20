# book-data 조회 예시

## 그림11-3 Open Library 조회

- provider: Open Library
- 입력 ISBN: 9780134685991
- 반환: 제목 Effective Java / 저자 Joshua Bloch
- 출처: https://openlibrary.org/api/books?bibkeys=ISBN:9780134685991&format=json&jscmd=data

## 그림11-4 네이버 책검색 조회

- provider: 네이버 책검색
- 입력 ISBN: 9791112211507
- 반환: 제목 게임인공지능 첫걸음 / 저자 이수미 / 출판사 부크크 / 연도 2026
- 출처: https://openapi.naver.com/v1/search/book_adv.json?d_isbn=9791112211507

## 활용 프롬프트

조회와 저장을 분리해 줘. ISBN으로 도서 정보를 조회하는 단계와, 그 결과를 도서 메모로 저장하는 단계를 나누고, 저장은 내 승인 뒤에만 진행해 줘.

출처를 먼저 보여 줘. lookup_isbn이 반환한 원자료(제목·저자·출처 URL)를 먼저 그대로 보여 주고, 그 위에 네 요약을 따로 표시해 줘.

쓰기 전 승인. 조회 결과를 도서 메모에 추가하기 전에, 추가할 항목을 보여 주고 내 승인을 받아 줘. 승인 전에는 데이터를 바꾸지 마.
