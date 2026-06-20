#!/usr/bin/env bash
# 교육용 도서 정보 MCP(book-data) 등록 예시입니다.
# stdio 전송으로 로컬 server.py를 띄웁니다.
# user scope로 등록하면 모든 프로젝트에서 사용할 수 있습니다.

claude mcp add --scope user book-data -- python server.py
