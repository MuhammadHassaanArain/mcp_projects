import asyncio
from typing import Optional
from mcp import ClientSession
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import ListToolsResult, CallToolResult, ListResourcesResult, ListResourceTemplatesResult, ReadResourceResult, ListPromptsResult, GetPromptResult

class MCPClient:
    def __init__(self, server_url):
        self._server_url : str = server_url
        self._session: Optional[ClientSession] = None
        self._exit_stack:AsyncExitStack= AsyncExitStack()

    async def connection(self):
        _read, _write, _ = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read,_write)
        )
        await self._session.initialize()
        return self._session
    
    async def Cleanup(self):
        await self._exit_stack.aclose()

    async def __aenter__(self):
        await self.connection()
        return self
    
    async def __aexit__(self,*args):
        await self.Cleanup()
        self._session = None

    # Tools
    async def tool_list(self)-> ListToolsResult:
        assert self._session, "Session Not Found"
        res = await self._session.list_tools()
        return res.tools
    
    async def tool_call(self, tool_name:str, arguments:dict[str,any])->CallToolResult:
        assert self._session, "Session Not Found"
        res = await self._session.call_tool(name=tool_name, arguments=arguments)
        return res.content
    
    

async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        print("LIST TOOLS ⚙")
        list_tools = await client.tool_list()
        for tool in list_tools:
            print("Tool Name : ", tool.name)
        
        print("\n TOOL CALLS 🔧")
        tool_call = await client.tool_call("save_message", arguments={"user":"user1","msg":"what's up"})
        print("Tool Result: ", tool_call[0].text)

        print("\n TOOL CALLS 🔧")
        tool_call = await client.tool_call("get_recent_message", arguments={"limit":10})
        for data in tool_call:
            print("Users Message: ", data.text)



asyncio.run(main())