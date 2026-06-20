# -*- coding: utf-8 -*-
"""
도서 데이터 MCP 서버 (book-data)

VIBE CODING 11.5 공공데이터 MCP 실습용. 키가 필요 없는 공개 도서 API를
감싼 읽기 전용 MCP다. ISBN이나 제목으로 책의 서지 정보를 조회하고,
항상 조회 출처 URL을 함께 돌려준다.

데이터 소스(둘 다 키 불필요):
  1순위 Google Books   https://www.googleapis.com/books/v1/volumes
  폴백   Open Library   https://openlibrary.org/api/books
  - Google Books가 익명 쿼터(429)나 일시 오류를 내면 Open Library로 넘어간다.

설계 원칙 (책 11.5와 동일):
- 읽기 전용: 조회 도구만 둔다. 저장/수정 도구는 일부러 두지 않는다.
  메모 반영·파일 저장은 Claude Code 쪽에서 사람의 승인을 받아 처리한다.
- 출처 표시: 모든 결과에 source(조회한 API URL)와 provider를 포함한다.
- 키 불필요: 공개 엔드포인트로 바로 시작한다.

실행: python server.py   (stdio MCP 서버)
등록: claude mcp add book-data -- python "<이 파일의 절대경로>"
"""
import os
import re
import time
import httpx
from mcp.server.fastmcp import FastMCP

# 선택: 키를 넣으면 Google Books 쿼터가 올라간다(무키는 일일 한도가 낮음).
GOOGLE_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY")
# 선택: 네이버 책검색 키를 넣으면 한국 책·전자책 ISBN이 잘 잡힌다(무키 소스의 빈 구멍).
NAVER_ID = os.environ.get("NAVER_CLIENT_ID")
NAVER_SECRET = os.environ.get("NAVER_CLIENT_SECRET")
# 선택: 카카오 책검색 REST 키. 다른 카탈로그라 네이버가 놓친 신간을 잡기도 한다.
KAKAO_KEY = os.environ.get("KAKAO_REST_KEY")

mcp = FastMCP("book-data")

GOOGLE_BOOKS = "https://www.googleapis.com/books/v1/volumes"
OPEN_LIBRARY = "https://openlibrary.org/api/books"
OPEN_LIBRARY_SEARCH = "https://openlibrary.org/search.json"
NAVER_BOOK = "https://openapi.naver.com/v1/search/book_adv.json"
KAKAO_BOOK = "https://dapi.kakao.com/v3/search/book"
HEADERS = {"User-Agent": "book-data-mcp/1.0 (VIBE CODING 11.5 example)"}


def _strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def _from_naver(it: dict, isbn: str, source: str) -> dict:
    authors = [a for a in re.split(r"[\^|]", it.get("author", "")) if a]
    pub = it.get("pubdate", "") or ""
    pubdate = f"{pub[:4]}-{pub[4:6]}-{pub[6:8]}" if len(pub) >= 8 else (pub or None)
    return {
        "title": _strip_tags(it.get("title")),
        "subtitle": None,
        "authors": authors,
        "publisher": it.get("publisher") or None,
        "published_date": pubdate,
        "isbn_13": isbn if len(isbn) == 13 else None,
        "isbn_10": isbn if len(isbn) == 10 else None,
        "thumbnail": it.get("image") or None,
        "info_link": it.get("link") or None,
        "provider": "Naver 책검색",
        "source": source,
    }


def _naver_isbn(clean: str):
    if not (NAVER_ID and NAVER_SECRET):
        return None
    h = {**HEADERS, "X-Naver-Client-Id": NAVER_ID, "X-Naver-Client-Secret": NAVER_SECRET}
    r = httpx.get(NAVER_BOOK, params={"d_isbn": clean}, headers=h, timeout=10.0)
    r.raise_for_status()
    items = r.json().get("items", []) or []
    if items:
        book = _from_naver(items[0], clean, str(r.url))
        book["found"] = True
        return book
    return None


def _from_kakao(d: dict, isbn: str, source: str) -> dict:
    dt = d.get("datetime", "") or ""
    return {
        "title": d.get("title"),
        "subtitle": None,
        "authors": d.get("authors", []),
        "publisher": d.get("publisher") or None,
        "published_date": dt[:10] if dt else None,
        "isbn_13": isbn if len(isbn) == 13 else None,
        "isbn_10": isbn if len(isbn) == 10 else None,
        "thumbnail": d.get("thumbnail") or None,
        "info_link": d.get("url") or None,
        "provider": "Kakao 책검색",
        "source": source,
    }


def _kakao_isbn(clean: str):
    if not KAKAO_KEY:
        return None
    h = {**HEADERS, "Authorization": f"KakaoAK {KAKAO_KEY}"}
    r = httpx.get(KAKAO_BOOK, params={"target": "isbn", "query": clean}, headers=h, timeout=10.0)
    r.raise_for_status()
    docs = r.json().get("documents", []) or []
    if docs:
        book = _from_kakao(docs[0], clean, str(r.url))
        book["found"] = True
        return book
    return None


def _clean_isbn(isbn: str) -> str:
    return "".join(ch for ch in isbn if ch.isdigit() or ch in "Xx").upper()


def _get_json(url: str, params: dict, retries: int = 1):
    """429/5xx면 짧게 backoff 후 재시도. 실패하면 마지막 응답으로 예외를 올린다."""
    if url == GOOGLE_BOOKS and GOOGLE_KEY:
        params = {**params, "key": GOOGLE_KEY}
    last = None
    for attempt in range(retries + 1):
        resp = httpx.get(url, params=params, headers=HEADERS, timeout=10.0)
        if resp.status_code == 200:
            return resp
        last = resp
        # 일시 throttle(429)·서버오류(5xx)는 짧게 한 번 재시도한다.
        if resp.status_code in (429, 500, 502, 503) and attempt < retries:
            time.sleep(0.6 * (attempt + 1))
            continue
        break
    last.raise_for_status()


def _from_google(item: dict, source: str) -> dict:
    info = item.get("volumeInfo", {})
    ids = {i.get("type"): i.get("identifier") for i in info.get("industryIdentifiers", [])}
    return {
        "title": info.get("title"),
        "subtitle": info.get("subtitle"),
        "authors": info.get("authors", []),
        "publisher": info.get("publisher"),
        "published_date": info.get("publishedDate"),
        "page_count": info.get("pageCount"),
        "language": info.get("language"),
        "isbn_13": ids.get("ISBN_13"),
        "isbn_10": ids.get("ISBN_10"),
        "thumbnail": (info.get("imageLinks") or {}).get("thumbnail"),
        "info_link": info.get("infoLink"),
        "provider": "Google Books",
        "source": source,
    }


def _from_openlibrary(rec: dict, isbn: str, source: str) -> dict:
    return {
        "title": rec.get("title"),
        "subtitle": rec.get("subtitle"),
        "authors": [a.get("name") for a in rec.get("authors", []) if a.get("name")],
        "publisher": ", ".join(p.get("name", "") for p in rec.get("publishers", [])) or None,
        "published_date": rec.get("publish_date"),
        "page_count": rec.get("number_of_pages"),
        "language": None,
        "isbn_13": isbn if len(isbn) == 13 else None,
        "isbn_10": isbn if len(isbn) == 10 else None,
        "thumbnail": (rec.get("cover") or {}).get("medium"),
        "info_link": rec.get("url"),
        "provider": "Open Library",
        "source": source,
    }


def _google_isbn(clean: str):
    r = _get_json(GOOGLE_BOOKS, {"q": f"isbn:{clean}"})
    items = r.json().get("items")
    if items:
        book = _from_google(items[0], str(r.url))
        book["found"] = True
        return book
    return None


def _ol_isbn(clean: str):
    r = _get_json(OPEN_LIBRARY, {"bibkeys": f"ISBN:{clean}", "format": "json", "jscmd": "data"})
    rec = r.json().get(f"ISBN:{clean}")
    if rec:
        book = _from_openlibrary(rec, clean, str(r.url))
        book["found"] = True
        return book
    return None


@mcp.tool()
def lookup_isbn(isbn: str) -> dict:
    """ISBN으로 도서의 서지 정보를 조회한다(읽기 전용).

    제목, 저자, 출판사, 출판일 등을 공개 도서 API에서 가져오고
    조회 출처(provider, source URL)를 함께 돌려준다. 하이픈이 있어도 된다.
    키가 있으면 Google Books를 먼저, 없으면 Open Library를 먼저 쓰고
    서로 자동 폴백한다.

    Args:
        isbn: 조회할 ISBN(10 또는 13자리, 하이픈 허용). 예: 978-89-...
    """
    clean = _clean_isbn(isbn)
    # 우선순위: 네이버·카카오(한국 책) → Google(키 있으면) → Open Library → Google(무키 폴백)
    providers = []
    if NAVER_ID and NAVER_SECRET:
        providers.append(_naver_isbn)
    if KAKAO_KEY:
        providers.append(_kakao_isbn)
    if GOOGLE_KEY:
        providers.append(_google_isbn)
    providers.append(_ol_isbn)
    if not GOOGLE_KEY:
        providers.append(_google_isbn)
    for fn in providers:
        try:
            book = fn(clean)
            if book:
                return book
        except Exception:
            continue
    return {"found": False, "isbn": clean, "source": f"{GOOGLE_BOOKS}?q=isbn:{clean}",
            "message": "해당 ISBN으로 조회된 도서가 없습니다. 한국어 책은 네이버 책검색 키(NAVER_CLIENT_ID/SECRET) 또는 Google Books 키가 필요합니다."}


@mcp.tool()
def search_books(query: str, limit: int = 5) -> dict:
    """제목·저자·키워드로 도서를 검색한다(읽기 전용, 최대 10건).

    ISBN을 모를 때 후보를 찾는 용도. 각 결과에 출처 URL을 포함한다.

    Args:
        query: 검색어(제목, 저자, 키워드 등).
        limit: 가져올 최대 건수(1~10, 기본 5).
    """
    n = max(1, min(int(limit), 10))
    providers = [_google_search, _ol_search] if GOOGLE_KEY else [_ol_search, _google_search]
    for fn in providers:
        try:
            out = fn(query, n)
            if out["count"]:
                return out
        except Exception:
            continue
    return {"count": 0, "query": query, "provider": None,
            "source": OPEN_LIBRARY_SEARCH, "results": []}


def _google_search(query: str, n: int) -> dict:
    r = _get_json(GOOGLE_BOOKS, {"q": query, "maxResults": n})
    items = r.json().get("items", []) or []
    results = [_from_google(it, str(r.url)) for it in items]
    return {"count": len(results), "query": query, "provider": "Google Books",
            "source": str(r.url), "results": results}


def _ol_search(query: str, n: int) -> dict:
    fields = "title,author_name,first_publish_year,isbn,publisher"
    r = _get_json(OPEN_LIBRARY_SEARCH, {"q": query, "limit": n, "fields": fields})
    docs = r.json().get("docs", []) or []
    results = [_from_ol_search(d, str(r.url)) for d in docs[:n]]
    return {"count": len(results), "query": query, "provider": "Open Library",
            "source": str(r.url), "results": results}


def _from_ol_search(doc: dict, source: str) -> dict:
    isbns = doc.get("isbn", []) or []
    isbn13 = next((i for i in isbns if len(i) == 13), None)
    pubs = doc.get("publisher", []) or []
    return {
        "title": doc.get("title"),
        "authors": doc.get("author_name", []),
        "publisher": pubs[0] if pubs else None,
        "published_date": str(doc.get("first_publish_year")) if doc.get("first_publish_year") else None,
        "isbn_13": isbn13,
        "provider": "Open Library",
        "source": source,
    }


if __name__ == "__main__":
    mcp.run()
