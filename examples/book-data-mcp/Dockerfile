FROM python:3.11-slim

# 컨테이너에서 파이썬 로그가 즉시 보이도록(버퍼링 끔) — 기동 로그/에러 추적에 필수.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py app.py ./

# 플랫폼이 주입하는 PORT에 바인딩한다(Render는 10000을 주입). 없으면 8000로 폴백.
# EXPOSE/ENV PORT 고정은 일부 플랫폼의 포트 감지와 어긋날 수 있어 두지 않는다.
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
