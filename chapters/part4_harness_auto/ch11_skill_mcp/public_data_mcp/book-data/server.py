"""교육용 MCP 서버 스텁: 도서 정보 조회(book-data)

ISBN으로 도서 정보를 조회하는 lookup_isbn 도구를 노출하는 골격입니다.
이 스텁은 실제 네트워크 호출 대신 샘플 응답을 반환합니다. 의존성을 최소화해
구조를 익히는 데 집중합니다. 실제 연동은 아래 두 provider 주석을 참고합니다.

provider 1) Open Library
  - 엔드포인트: https://openlibrary.org/api/books
  - 키 없이 조회 가능. 입문용으로 적합합니다.
  - 예: ?bibkeys=ISBN:9780134685991&format=json&jscmd=data

provider 2) 네이버 책검색
  - 엔드포인트: https://openapi.naver.com/v1/search/book_adv.json
  - 클라이언트 ID/Secret 필요. 토큰은 환경변수에서 읽습니다.
  - 헤더: X-Naver-Client-Id, X-Naver-Client-Secret

토큰은 코드에 직접 쓰지 않고 os.environ에서 읽습니다.
  - NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
  - NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")
"""

import os
import sys
import json

# 실제 연동 시 환경변수에서 토큰을 읽습니다(여기서는 사용하지 않습니다).
NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")


# 샘플 응답입니다. 실제 서버는 provider를 호출해 동일한 형태로 반환합니다.
SAMPLE_BOOKS = {
    "9780134685991": {
        "isbn": "9780134685991",
        "title": "Effective Java",
        "author": "Joshua Bloch",
        "provider": "openlibrary",
        "source_url": "https://openlibrary.org/api/books?bibkeys=ISBN:9780134685991&format=json&jscmd=data",
    },
    "9791112211507": {
        "isbn": "9791112211507",
        "title": "게임인공지능 첫걸음",
        "author": "이수미",
        "publisher": "부크크",
        "year": "2026",
        "provider": "naver",
        "source_url": "https://openapi.naver.com/v1/search/book_adv.json?d_isbn=9791112211507",
    },
}


def lookup_isbn(isbn):
    """ISBN으로 도서 정보를 조회합니다(읽기 전용).

    실제 구현에서는 위 provider 중 하나를 호출합니다. 이 스텁은 샘플만 반환합니다.
    원본 데이터를 바꾸지 않으며, 조회 실패해도 상태가 변하지 않습니다.
    """
    isbn = (isbn or "").strip().replace("-", "")
    book = SAMPLE_BOOKS.get(isbn)
    if book is None:
        return {"isbn": isbn, "found": False, "note": "샘플 데이터에 없는 ISBN입니다."}
    result = dict(book)
    result["found"] = True
    return result


# MCP 도구 정의(골격). 실제 런타임은 stdio로 요청을 받아 lookup_isbn을 호출합니다.
TOOLS = [
    {
        "name": "lookup_isbn",
        "description": "ISBN으로 도서 제목·저자·출처를 조회합니다(읽기 전용).",
        "input_schema": {
            "type": "object",
            "properties": {"isbn": {"type": "string"}},
            "required": ["isbn"],
        },
    }
]


def _handle(request):
    """최소 골격: lookup_isbn 호출만 처리합니다."""
    method = request.get("method")
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        params = request.get("params", {})
        if params.get("name") == "lookup_isbn":
            args = params.get("arguments", {})
            return lookup_isbn(args.get("isbn"))
    return {"error": "지원하지 않는 요청입니다."}


if __name__ == "__main__":
    # 동작 확인용 최소 골격: 한 줄씩 JSON 요청을 받아 응답을 출력합니다.
    # 실제 MCP 서버는 MCP SDK로 stdio 핸드셰이크를 구현합니다.
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            print(json.dumps({"error": "JSON 파싱 실패"}, ensure_ascii=False))
            continue
        print(json.dumps(_handle(req), ensure_ascii=False))
