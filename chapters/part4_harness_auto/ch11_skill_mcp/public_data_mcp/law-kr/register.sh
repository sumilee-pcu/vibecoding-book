#!/usr/bin/env bash
# 법령 검색 MCP(law-kr) 등록 예시입니다.
# YOUR_LAW_MCP_SERVER 자리는 실제 법령 MCP 서버 주소로 바꿉니다(플레이스홀더).
# 처음에는 읽기 전용으로 동작을 확인합니다.

claude mcp add --transport http law-kr https://YOUR_LAW_MCP_SERVER/mcp
