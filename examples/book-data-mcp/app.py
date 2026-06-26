# -*- coding: utf-8 -*-
"""
도서 데이터 웹앱 (book-data web)

book-data MCP(server.py)의 조회 로직을 그대로 재사용하는 웹 UI다.
ISBN이나 제목·키워드로 서지 정보를 조회하고, 언제나 조회 출처를 함께 보여 준다.

- 같은 폴더의 server.py에서 lookup_isbn / search_books 를 import 한다(단일 출처).
- 읽기 전용. 저장·수정 기능은 두지 않는다(책 11.5 원칙과 동일).

실행:  python -m uvicorn app:app --host 0.0.0.0 --port 8000
배포:  Dockerfile / render.yaml / Procfile 참고
"""
import server  # 같은 폴더의 MCP 서버 모듈(조회 로직 단일 출처)

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="도서 데이터 (book-data)", docs_url="/api/docs", redoc_url=None)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/isbn")
def api_isbn(isbn: str = Query(..., description="조회할 ISBN(10/13자리, 하이픈 허용)")):
    return JSONResponse(server.lookup_isbn(isbn))


@app.get("/api/search")
def api_search(
    q: str = Query(..., description="검색어(제목·저자·키워드)"),
    limit: int = Query(5, ge=1, le=10),
):
    return JSONResponse(server.search_books(q, limit))


@app.get("/api/_diag")
def api_diag():
    """임시 진단: 외부 도서 API로의 아웃바운드 호출 결과(상태/예외)를 그대로 돌려준다."""
    import httpx
    out = {}
    targets = {
        "openlibrary": ("https://openlibrary.org/search.json", {"q": "design patterns", "limit": 1}),
        "googlebooks": ("https://www.googleapis.com/books/v1/volumes", {"q": "design patterns", "maxResults": 1}),
    }
    for name, (url, params) in targets.items():
        try:
            r = httpx.get(url, params=params, headers=server.HEADERS, timeout=20.0)
            body = r.text[:200]
            out[name] = {"status": r.status_code, "len": len(r.text), "body_head": body}
        except Exception as e:
            out[name] = {"error": f"{type(e).__name__}: {e}"}
    return JSONResponse(out)


PAGE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>도서 데이터 · book-data</title>
<style>
  :root{
    --bg:#0f1115; --panel:#171a21; --line:#262b36; --ink:#e8eaed;
    --muted:#9aa3b2; --accent:#6ea8fe; --accent2:#8ce0c0; --chip:#1f2530;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans KR",sans-serif;
    line-height:1.55;-webkit-font-smoothing:antialiased}
  .wrap{max-width:820px;margin:0 auto;padding:48px 20px 80px}
  header h1{font-size:1.55rem;margin:0 0 6px;letter-spacing:-.01em}
  header p{margin:0;color:var(--muted);font-size:.95rem}
  .tabs{display:flex;gap:6px;margin:28px 0 14px}
  .tab{padding:8px 16px;border-radius:999px;background:var(--chip);color:var(--muted);
    border:1px solid var(--line);cursor:pointer;font-size:.9rem;user-select:none}
  .tab.on{background:var(--accent);color:#0b0d12;border-color:var(--accent);font-weight:600}
  form{display:flex;gap:8px}
  input,select{background:var(--panel);border:1px solid var(--line);color:var(--ink);
    border-radius:10px;padding:12px 14px;font-size:1rem;outline:none}
  input{flex:1}
  input:focus,select:focus{border-color:var(--accent)}
  button{background:var(--accent);color:#0b0d12;border:0;border-radius:10px;
    padding:0 20px;font-size:1rem;font-weight:600;cursor:pointer}
  button:disabled{opacity:.55;cursor:default}
  .status{color:var(--muted);font-size:.88rem;margin:16px 2px 0;min-height:1.2em}
  .card{display:flex;gap:16px;background:var(--panel);border:1px solid var(--line);
    border-radius:14px;padding:16px;margin-top:14px}
  .cover{width:78px;height:112px;flex:none;border-radius:8px;object-fit:cover;
    background:var(--chip);border:1px solid var(--line)}
  .meta{min-width:0}
  .meta h3{margin:0 0 4px;font-size:1.08rem;letter-spacing:-.01em}
  .meta .sub{color:var(--muted);font-size:.9rem;margin:0 0 8px}
  .row{font-size:.9rem;margin:2px 0}
  .row b{color:var(--muted);font-weight:500;display:inline-block;min-width:64px}
  .src{margin-top:10px;font-size:.78rem;color:var(--muted);word-break:break-all}
  .src .chip{display:inline-block;background:var(--chip);border:1px solid var(--line);
    color:var(--accent2);border-radius:6px;padding:1px 8px;margin-right:6px;font-weight:600}
  a{color:var(--accent)}
  footer{margin-top:40px;color:var(--muted);font-size:.8rem;text-align:center}
  .hide{display:none}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>도서 데이터 <span style="color:var(--accent2)">book-data</span></h1>
    <p>ISBN 또는 제목·키워드로 서지 정보를 조회합니다. 결과에는 항상 조회 출처가 붙습니다(읽기 전용).</p>
  </header>

  <div class="tabs">
    <div class="tab on" data-mode="search">제목·키워드</div>
    <div class="tab" data-mode="isbn">ISBN</div>
  </div>

  <form id="f">
    <input id="q" placeholder="예: design patterns" autocomplete="off" autofocus>
    <select id="limit" title="결과 수">
      <option>3</option><option selected>5</option><option>10</option>
    </select>
    <button id="go" type="submit">조회</button>
  </form>

  <div class="status" id="status"></div>
  <div id="results"></div>

  <footer>VIBE CODING · 도서 데이터 MCP(server.py) 조회 로직 재사용 · 공개 도서 API(Google Books / Open Library 등)</footer>
</div>

<script>
const $ = (s)=>document.querySelector(s);
let mode = "search";

document.querySelectorAll(".tab").forEach(t=>{
  t.onclick = ()=>{
    document.querySelectorAll(".tab").forEach(x=>x.classList.remove("on"));
    t.classList.add("on");
    mode = t.dataset.mode;
    $("#limit").classList.toggle("hide", mode==="isbn");
    $("#q").placeholder = mode==="isbn" ? "예: 978-0-13-468599-1" : "예: design patterns";
    $("#q").focus();
  };
});

function esc(s){return (s==null?"":String(s)).replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}

function card(b){
  const authors = (b.authors&&b.authors.length)? b.authors.join(", ") : "—";
  const cover = b.thumbnail
    ? `<img class="cover" src="${esc(b.thumbnail)}" alt="">`
    : `<div class="cover"></div>`;
  const isbn = b.isbn_13 || b.isbn_10 || "—";
  const link = b.info_link ? ` · <a href="${esc(b.info_link)}" target="_blank" rel="noopener">상세</a>` : "";
  return `<div class="card">
    ${cover}
    <div class="meta">
      <h3>${esc(b.title)||"제목 미상"}</h3>
      <p class="sub">${esc(b.subtitle||"")}</p>
      <div class="row"><b>저자</b> ${esc(authors)}</div>
      <div class="row"><b>출판</b> ${esc(b.publisher||"—")} · ${esc(b.published_date||"—")}</div>
      <div class="row"><b>ISBN</b> ${esc(isbn)}</div>
      <div class="src"><span class="chip">${esc(b.provider||"출처")}</span>${esc(b.source||"")}${link}</div>
    </div>
  </div>`;
}

async function run(ev){
  ev.preventDefault();
  const q = $("#q").value.trim();
  if(!q) return;
  $("#go").disabled = true;
  $("#status").textContent = "조회 중…";
  $("#results").innerHTML = "";
  try{
    let url = mode==="isbn"
      ? `/api/isbn?isbn=${encodeURIComponent(q)}`
      : `/api/search?q=${encodeURIComponent(q)}&limit=${$("#limit").value}`;
    const r = await fetch(url);
    const d = await r.json();
    if(mode==="isbn"){
      if(d.found===false){ $("#status").textContent = d.message || "조회 결과가 없습니다."; }
      else { $("#status").textContent = `출처: ${d.provider||"—"}`; $("#results").innerHTML = card(d); }
    } else {
      if(!d.count){ $("#status").textContent = "검색 결과가 없습니다."; }
      else { $("#status").textContent = `${d.count}건 · 출처: ${d.provider||"—"}`;
             $("#results").innerHTML = d.results.map(card).join(""); }
    }
  }catch(e){
    $("#status").textContent = "오류: " + e.message;
  }finally{
    $("#go").disabled = false;
  }
}
$("#f").addEventListener("submit", run);
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return PAGE
