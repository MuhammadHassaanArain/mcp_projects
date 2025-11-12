import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession
from typing import Optional
from mcp.client.streamable_http import streamablehttp_client

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

    # tools
    async def list_tools(self):
        """List available tools from the MCP server."""
        assert self._session, "Session Not Found"
        result = await self._session.list_tools()
        return result.tools
    
    async def call_tool(self, name:str, arg:dict[str,any]):
        """Call a tool by name with provided arguments."""
        assert self._session, "Session Not Found"
        result = await self._session.call_tool(name=name, arguments=arg)
        if not result.content:
            return "No content returned."
        return result.content[0].text


async def main():
    async with MCPCient("http://localhost:8000/mcp") as client:
        print("\n🧰 Listing Tools...")
        res = await client.list_tools()
        for tools in res:
            print("Tool Name: ",tools.name)

        print("\n🌤️ Testing Weather Tool...")
        weather_tool_call = await client.call_tool(name="get_weather", arg={"location":"Karachi"})
        print("Weather Tool Call: ", weather_tool_call)

        print("\n💰 Testing Crypto Tool...")
        crypto_tool_call = await client.call_tool(name="get_crypto_price", arg={"symbol":"bitcoin"})
        print("Crypto Tool Call: ", crypto_tool_call)

        print("\n📰 Testing News Tool...")
        news_tool_call = await client.call_tool(name="get_latest_news", arg={"topic":"ai","max_res":2})
        print("News Tool Call: ", news_tool_call)

if __name__ == "__main__":
    asyncio.run(main())