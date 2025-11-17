import asyncio
from typing import Optional, Any
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from contextlib import AsyncExitStack


class MCPCient():
    def __init__(self, server_url):
        self._server_url = server_url
        self._session:Optional[ClientSession] = None
        self._exit_stack:AsyncExitStack = AsyncExitStack()
    async def connection(self):
        """Establish a session with the MCP server."""
        _read_stream, _write_stream, _session_id = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(read_stream=_read_stream, write_stream=_write_stream)
        )
        await self._session.initialize()
        return self._session
    
    async def closeup(self):
        """Close the MCP session and exit stack."""
        await self._exit_stack.aclose()
        self._session = None
        print("\n 🔒 Connection closed.")
        
        
    async def __aenter__(self):
        await self.connection()
        return self
    
    async def __aexit__(self,*args):
        await self.closeup()

    async def list_tools(self):
        result = await self._session.list_tools()
        return result.tools
    async def call_tool(self, tool_name:str, arguments:dict[str,any] | None):
        result = await self._session.call_tool(name=tool_name, arguments=arguments or {})
        return result.content


async def main():
    async with MCPCient("http://localhost:8000/mcp") as client:
        list_tool = await client.list_tools()
        for tool in list_tool:
            print("TOOL : ", tool.name)

        add_task1  = await client.call_tool("add_task", arguments={"task":"Push the code in GitHub Repo"})
        print("Task Added : ", add_task1[0].text)

        add_task2 = await client.call_tool("add_task", arguments={"task":"Post In LinkedIn"})
        print("Task Added : ", add_task2[0].text)

        add_task3 = await client.call_tool("add_task",arguments={"task":"Complete the Class Assignment"})
        print("Task Added : ", add_task3[0].text)

        get_task = await client.call_tool("get_task", arguments={"task_id":1})
        print("GET TASK : ", get_task[0].text)

        mark_done = await client.call_tool("mark_done", arguments={"task_id" : 1})
        print("MARK DONE : ", mark_done[0].text)

        mark_done = await client.call_tool("mark_done", arguments={"task_id" : 3})
        print("MARK DONE : ", mark_done[0].text)

        delete_task = await client.call_tool("delete_task", arguments={"task_id":3})
        print("DELETE TASK : ", delete_task[0].text)
asyncio.run(main())