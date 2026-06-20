// sort_products.js
// 강한 프롬프트 명세대로 동작하는 정답 예시입니다.
// 명세:
// - 입력은 {name, price} 객체의 배열이다.
// - 원본 배열은 바꾸지 말고 새 배열을 반환한다.
// - 가격 오름차순으로 정렬한다.
// - 가격이 같으면 이름 가나다순으로 정렬한다.

function sortProducts(products) {
  // slice()로 원본을 복사해 새 배열을 만든다. 원본은 바뀌지 않는다.
  return products.slice().sort((a, b) => {
    if (a.price !== b.price) {
      // 가격 오름차순
      return a.price - b.price;
    }
    // 가격이 같으면 이름 가나다순(localeCompare, 한국어 기준)
    return a.name.localeCompare(b.name, 'ko');
  });
}

// 간단 사용 예
// const list = [
//   { name: '바나나', price: 1500 },
//   { name: '사과', price: 1000 },
//   { name: '귤', price: 1000 },
// ];
// const sorted = sortProducts(list);
// 결과: 귤(1000) → 사과(1000) → 바나나(1500)
// list(원본)는 그대로 유지됩니다.

module.exports = { sortProducts };
