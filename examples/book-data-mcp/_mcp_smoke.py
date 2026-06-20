# -*- coding: utf-8 -*-
"""MCP stdio 핸드셰이크 + tools/list + 도구 호출 스모크 테스트."""
import sys, io, json, asyncio
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("TOOLS:", [t.name for t in tools.tools])
            res = await session.call_tool("lookup_isbn", {"isbn": "9780134685991"})
            txt = res.content[0].text if res.content else "(empty)"
            data = json.loads(txt)
            print("CALL lookup_isbn(9780134685991):")
            print("  title  =", data.get("title"))
            print("  authors=", data.get("authors"))
            print("  provider=", data.get("provider"))
            print("  source =", data.get("source"))

asyncio.run(main())
