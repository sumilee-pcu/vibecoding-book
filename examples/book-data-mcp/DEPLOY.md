# book-data 웹앱 배포 가이드

`app.py`는 `server.py`(book-data MCP)의 조회 로직을 그대로 재사용하는 FastAPI 웹앱이다.
키 없이 동작하며(공개 도서 API), 한국어 신간 커버리지를 높이려면 네이버/카카오/구글 키를 환경변수로 넣는다.

## 로컬 실행

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt   # Windows
.venv\Scripts\python -m uvicorn app:app --host 127.0.0.1 --port 8000
# http://127.0.0.1:8000 접속
```

## 배포 — Render (무료, 권장)

저장소는 이미 GitHub(`sumilee-pcu/vibecoding-book`)에 있고, 웹앱은 하위 폴더
`examples/book-data-mcp/`에 있다. Blueprint는 `render.yaml`이 저장소 루트에 있어야
자동 인식하므로, 여기서는 **New Web Service + Root Directory 지정** 방식을 쓴다
(이 폴더의 `Dockerfile`을 Render가 자동으로 인식한다).

1. https://render.com 로그인 → **New +** → **Web Service**.
2. **Build and deploy from a Git repository** → `vibecoding-book` 연결.
3. 설정:
   - **Root Directory**: `examples/book-data-mcp`
   - **Runtime**: Docker(Dockerfile 자동 감지) — 또는 Python으로 두면
     Build `pip install -r requirements.txt`, Start `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
   - **Instance Type**: Free
4. (선택) **Environment** 탭에 `NAVER_CLIENT_ID`/`NAVER_CLIENT_SECRET`,
   `GOOGLE_BOOKS_API_KEY` 입력(한국어 신간 커버리지).
5. **Create Web Service** → 빌드 후 `https://<이름>.onrender.com` 공개 URL 생성.
   - API 문서: `/api/docs`.
   - 무료 플랜은 일정 시간 미사용 시 슬립하며, 첫 요청에 수십 초가 걸릴 수 있다.

> 루트에 `render.yaml`을 두고 Blueprint로 하고 싶다면 `render.yaml`을 저장소 루트로
> 옮긴다(이미 `rootDir: examples/book-data-mcp`가 들어 있다).

## 배포 — Hugging Face Spaces (Docker)

1. https://huggingface.co 에서 **New Space** → SDK: **Docker** → Blank.
2. 이 폴더의 `Dockerfile`, `app.py`, `server.py`, `requirements.txt`를 Space 저장소에 올린다(`git push`).
3. HF가 자동 빌드하고 `https://<id>-book-data-web.hf.space` 공개 URL을 준다.
4. (선택) Space Settings의 **Secrets**에 도서 API 키를 넣는다.

## 환경변수

| 변수 | 효과 |
|---|---|
| `GOOGLE_BOOKS_API_KEY` | Google Books 쿼터 상향 — **클라우드 배포 시 사실상 필수** |
| `NAVER_CLIENT_ID` / `NAVER_CLIENT_SECRET` | 한국 책·전자책 ISBN 커버리지 |
| `KAKAO_REST_KEY` | 네이버가 놓친 신간 보강 |

> ⚠️ **클라우드(Render/HF 등)에서는 키 없이 거의 조회가 안 된다.** 데이터센터 IP에서는
> Google Books가 익명 일일 쿼터 초과로 `429`를 주고, Open Library가 연결을 리셋한다
> (집/사무실 IP에서는 무키로도 잘 된다). 따라서 공개 배포본이 실제 데이터를 돌려주게 하려면
> **무료 `GOOGLE_BOOKS_API_KEY`를 발급해 환경변수에 넣는 것이 핵심이다.** 한국어 책까지
> 잘 잡으려면 네이버 책검색 키도 함께 넣는다.

### Google Books API 키 발급(무료) 후 Render에 넣기

1. https://console.cloud.google.com 에서 프로젝트 생성 → **APIs & Services → Library**에서
   **Books API** 사용 설정 → **Credentials → Create credentials → API key**로 키 발급.
2. Render 서비스 → **Environment** 탭 → **Add Environment Variable**:
   `GOOGLE_BOOKS_API_KEY` = 발급받은 키 → **Save**. 저장하면 자동으로 재배포된다.
3. 배포 후 `/api/search?q=clean+code` 로 결과가 돌아오는지 확인한다.
