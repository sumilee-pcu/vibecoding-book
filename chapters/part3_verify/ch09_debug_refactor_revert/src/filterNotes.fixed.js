// 정답 구현. 버그 3종을 모두 고친 상태입니다.
// 9강 실습에서 학생이 filterNotes.buggy.js를 고쳐 도달해야 하는 목표 코드입니다.
//
// 고친 내용:
//   ① 앞뒤 공백 처리: query에 trim()을 적용.
//   ② 대소문자 무시: 양쪽을 모두 toLowerCase()로 정규화.
//   ③ 원본 불변: 원본 배열을 건드리지 않고 filter로 새 배열을 만든다.
//
// 안전 리팩터링: 정규화 로직을 normalizeText 도우미로 추출(동작은 그대로).

function normalizeText(value) {
  // 텍스트를 비교용으로 정규화: 앞뒤 공백 제거 + 소문자.
  return String(value).trim().toLowerCase();
}

export function filterNotes(notes, query) {
  // ① + ②: 검색어를 trim 후 소문자로.
  const normalizedQuery = normalizeText(query);

  // 빈 검색어면 전체 목록을 새 배열로 반환(원본과 분리).
  if (normalizedQuery === "") {
    return notes.slice();
  }

  const includesQuery = (note) => {
    // ②: note 쪽도 소문자로 정규화해 대소문자 무시 비교.
    return (
      normalizeText(note.title).includes(normalizedQuery) ||
      normalizeText(note.author).includes(normalizedQuery) ||
      normalizeText(note.memo).includes(normalizedQuery)
    );
  };

  // ③: filter는 원본을 바꾸지 않고 새 배열을 만든다.
  return notes.filter(includesQuery);
}
