// 도서 메모 검색 도구의 핵심 함수.
// notes 배열에서 query를 포함하는 항목만 골라 새 배열로 돌려준다.
//
// 명세:
// - query를 trim() 후 toLowerCase()로 정규화한다.
// - 정규화 결과가 빈 문자열이면 전체 목록을 새 배열로 반환한다.
// - 그 외에는 title/author/memo 중 하나라도(소문자 비교) query를 포함하는 항목만 반환한다.
// - 원본 notes 배열과 각 객체는 절대 변경하지 않는다.

export function filterNotes(notes, query) {
  // 검색어 정규화: 앞뒤 공백 제거 후 소문자로.
  const normalizedQuery = String(query).trim().toLowerCase();

  // 빈 검색어면 전체 목록을 새 배열로 반환(원본과 분리).
  if (normalizedQuery === "") {
    return notes.slice();
  }

  // 한 항목이 검색어를 포함하는지 검사하는 도우미.
  const includesQuery = (note) => {
    const title = String(note.title).toLowerCase();
    const author = String(note.author).toLowerCase();
    const memo = String(note.memo).toLowerCase();
    return (
      title.includes(normalizedQuery) ||
      author.includes(normalizedQuery) ||
      memo.includes(normalizedQuery)
    );
  };

  // filter는 새 배열을 만들고 원본 객체 참조만 담으므로 원본은 그대로 보존된다.
  return notes.filter(includesQuery);
}
