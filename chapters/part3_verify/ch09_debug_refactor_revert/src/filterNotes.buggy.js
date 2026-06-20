// 주의: 이 파일에는 버그 3종이 일부러 심어져 있습니다. 학생이 고칠 대상입니다.
//
// 심긴 버그:
//   버그 ① 앞뒤 공백 미처리 — query에 trim()을 하지 않는다.
//   버그 ② 대소문자 구분 — 양쪽을 소문자로 정규화하지 않는다.
//   버그 ③ 원본 변경 — 결과를 만들면서 원본 notes 배열을 직접 건드린다.
//
// 8강과 같은 테스트(test/filterNotes.test.js)를 돌리면 위 버그 때문에 일부가 실패합니다.
// 정답은 src/filterNotes.fixed.js를 참고하세요.

export function filterNotes(notes, query) {
  // 버그 ①: trim()이 없어 " python "처럼 공백이 붙으면 일치하지 않는다.
  // 버그 ②: toLowerCase()가 없어 대소문자가 다르면 일치하지 않는다.
  const q = query;

  if (q === "") {
    return notes;
  }

  const result = [];
  for (const note of notes) {
    // 버그 ②: note 쪽도 소문자로 바꾸지 않아 "Python"과 "python"이 다르게 취급된다.
    const matched =
      note.title.includes(q) ||
      note.author.includes(q) ||
      note.memo.includes(q);

    if (matched) {
      result.push(note);
    } else {
      // 버그 ③: 안 맞는 항목을 원본 배열에서 빼 버린다(원본 직접 변경).
      const idx = notes.indexOf(note);
      if (idx !== -1) {
        notes.splice(idx, 1);
      }
    }
  }

  return result;
}
