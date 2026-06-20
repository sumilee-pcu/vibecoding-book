// 9강 실습 테스트. 8강과 같은 완료 기준을 검사하지만,
// buggy 구현을 import하므로 처음 실행하면 버그 3종 때문에 일부가 실패합니다.
//
// 실행: node --test  (처음엔 실패 → 버그를 하나씩 고치면 통과)
// 버그를 다 고친 정답은 src/filterNotes.fixed.js를 참고하세요.
// 정답으로 통과를 확인하려면 아래 import 경로를 filterNotes.fixed.js로 바꿔 실행합니다.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

// 학생이 고치는 대상은 buggy 파일입니다.
import { filterNotes } from "../src/filterNotes.buggy.js";

const here = dirname(fileURLToPath(import.meta.url));
const sampleRaw = readFileSync(join(here, "..", "data", "sample-notes.json"), "utf8");
function loadNotes() {
  return JSON.parse(sampleRaw);
}

// 정상 1: 제목 검색.
test("완료기준: 제목에 검색어가 들어간 메모를 찾는다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "SQL");
  assert.equal(result.length, 1);
  assert.equal(result[0].title, "SQL 노트");
});

// 정상 2: 저자 검색.
test("완료기준: 저자에 검색어가 들어간 메모를 찾는다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "Park");
  assert.equal(result.length, 1);
  assert.equal(result[0].author, "Park");
});

// 정상 3: 메모 검색.
test("완료기준: 메모에 검색어가 들어간 메모를 찾는다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "스레드");
  assert.equal(result.length, 1);
  assert.equal(result[0].title, "운영체제");
});

// 경계 1: 빈 검색어는 전체.
test("완료기준: 빈 검색어면 전체 목록을 반환한다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "");
  assert.equal(result.length, notes.length);
});

// 경계 2: 대소문자 무시 — 버그 ②가 있으면 실패한다.
test("완료기준: 대소문자를 구분하지 않는다", () => {
  const notes = loadNotes();
  const lower = filterNotes(loadNotes(), "python");
  const upper = filterNotes(loadNotes(), "Python");
  assert.equal(lower.length, upper.length);
  assert.ok(lower.length >= 2);
});

// 경계 3: 앞뒤 공백 무시 — 버그 ①이 있으면 " python "이 빈 배열이 되어 실패한다.
test("완료기준: 검색어 앞뒤 공백을 무시한다", () => {
  const padded = filterNotes(loadNotes(), "  python  ");
  const plain = filterNotes(loadNotes(), "python");
  assert.equal(padded.length, plain.length);
  assert.ok(padded.length >= 2);
});

// 실패/없음 1: 일치 없음은 빈 배열.
test("완료기준: 일치 항목이 없으면 빈 배열을 반환한다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "없는검색어zzz");
  assert.deepEqual(result, []);
});

// 실패/없음 2: 결과 없음과 있음을 구분.
test("완료기준: 결과 없음과 결과 있음을 길이로 구분한다", () => {
  const none = filterNotes(loadNotes(), "없는검색어zzz");
  const some = filterNotes(loadNotes(), "SQL");
  assert.equal(none.length, 0);
  assert.ok(some.length > 0);
});

// 불변 1: 원본 불변 — 버그 ③이 있으면 splice로 원본이 줄어 실패한다.
test("완료기준: 검색은 원본 데이터를 변경하지 않는다", () => {
  const notes = loadNotes();
  const before = JSON.stringify(notes);
  filterNotes(notes, "python");
  const after = JSON.stringify(notes);
  assert.equal(before, after);
});
