// 8강 실습: 완료 기준을 테스트로 바꾼 결과물.
// 각 테스트 이름은 그 테스트가 보증하는 완료 기준을 설명한다.
// 실행: node --test

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

import { filterNotes } from "../src/filterNotes.js";

// 샘플 데이터 로드(테스트마다 깊은 복사로 신선한 입력을 만든다).
const here = dirname(fileURLToPath(import.meta.url));
const sampleRaw = readFileSync(join(here, "..", "data", "sample-notes.json"), "utf8");
function loadNotes() {
  return JSON.parse(sampleRaw);
}

// 정상 1: 검색어가 제목에 포함되면 결과에 나온다.
test("완료기준: 제목에 검색어가 들어간 메모를 찾는다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "SQL");
  assert.equal(result.length, 1);
  assert.equal(result[0].title, "SQL 노트");
});

// 정상 2: 검색어가 저자에 포함되면 결과에 나온다.
test("완료기준: 저자에 검색어가 들어간 메모를 찾는다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "Park");
  assert.equal(result.length, 1);
  assert.equal(result[0].author, "Park");
});

// 정상 3: 검색어가 메모에 포함되면 결과에 나온다.
test("완료기준: 메모에 검색어가 들어간 메모를 찾는다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "스레드");
  assert.equal(result.length, 1);
  assert.equal(result[0].title, "운영체제");
});

// 경계 1: 빈 검색어면 전체 목록을 돌려준다.
test("완료기준: 빈 검색어면 전체 목록을 반환한다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "");
  assert.equal(result.length, notes.length);
});

// 경계 2: 대소문자를 구분하지 않는다(python == Python).
test("완료기준: 대소문자를 구분하지 않는다", () => {
  const notes = loadNotes();
  const lower = filterNotes(notes, "python");
  const upper = filterNotes(notes, "Python");
  assert.equal(lower.length, upper.length);
  assert.ok(lower.length >= 2); // 제목 "Python 입문" + 메모 "python 예제"
});

// 경계 3: 검색어 앞뒤 공백을 무시한다(" python " == "python").
test("완료기준: 검색어 앞뒤 공백을 무시한다", () => {
  const notes = loadNotes();
  const padded = filterNotes(notes, "  python  ");
  const plain = filterNotes(notes, "python");
  assert.equal(padded.length, plain.length);
  assert.ok(padded.length >= 2);
});

// 실패/없음 1: 일치하는 항목이 없으면 빈 배열을 돌려준다.
test("완료기준: 일치 항목이 없으면 빈 배열을 반환한다", () => {
  const notes = loadNotes();
  const result = filterNotes(notes, "없는검색어zzz");
  assert.deepEqual(result, []);
});

// 실패/없음 2: "결과 없음"은 빈 배열로, "결과 있음"과 구분된다.
test("완료기준: 결과 없음과 결과 있음을 길이로 구분한다", () => {
  const notes = loadNotes();
  const none = filterNotes(notes, "없는검색어zzz");
  const some = filterNotes(notes, "SQL");
  assert.equal(none.length, 0);
  assert.ok(some.length > 0);
});

// 불변 1: 검색은 원본 notes 배열과 각 객체를 바꾸지 않는다.
test("완료기준: 검색은 원본 데이터를 변경하지 않는다", () => {
  const notes = loadNotes();
  const before = JSON.stringify(notes);
  filterNotes(notes, "python");
  filterNotes(notes, "");
  const after = JSON.stringify(notes);
  assert.equal(before, after);
});
