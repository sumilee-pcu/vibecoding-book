#!/usr/bin/env bash
# MCP 추가 명령 모음입니다. 필요한 줄만 골라 실행합니다.
# 처음에는 읽기 전용 서버를 local scope로 붙이길 권합니다.

# http 전송으로 원격 MCP 추가
claude mcp add --transport http my-data https://example.com/mcp

# 토큰 헤더가 필요한 경우(YOUR_TOKEN 자리에 실제 토큰 대신 환경변수 사용을 권장)
claude mcp add --transport http my-data https://example.com/mcp \
  --header "Authorization: Bearer YOUR_TOKEN"

# stdio 전송으로 로컬 MCP 추가(로컬 프로세스를 띄움)
claude mcp add --transport stdio local-data -- node server.js

# 연결된 MCP 목록 확인
claude mcp list

# 특정 MCP의 상세 정보 확인
claude mcp get my-data

# Claude Code 안에서는 슬래시 명령으로 MCP 상태를 확인합니다.
# /mcp
