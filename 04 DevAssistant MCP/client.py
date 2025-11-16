import asyncio
from typing import Optional, Any
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from contextlib import AsyncExitStack
from mcp.shared.context import RequestContext
from mcp.types import CreateMessageRequestParams, CreateMessageResult, TextContent
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set. Check your .env file.")

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

async def real_sampling(context:RequestContext[ClientSession, Any], params:CreateMessageRequestParams):
    agent = Agent(
        name="Assistant",
        instructions=params.messages[0].content.text,
        model=model,
    )
    response = await Runner.run(agent,params.messages[1].content.text )
    result = response.final_output
    return (
        CreateMessageResult(
            role="assistant",
            content=TextContent(
                type="text",
                text=result
            ),
            model=model.model
        )
    )

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
            ClientSession(read_stream=_read_stream, write_stream=_write_stream,sampling_callback=real_sampling)
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

    async def list_prompt(self):
        result =  await self._session.list_prompts()
        return result.prompts
    async def get_prompt(self, prompt_name:str, args:dict[str, any]):
        result = await self._session.get_prompt(name=prompt_name, arguments=args)
        return result.messages

async def main():
    async with MCPCient("http://localhost:8000/mcp") as client:
        tool_list = await client.list_tools()
        for tool in tool_list:
            print("TOOL  : ", tool.name)

        prompts = await client.list_prompt()
        for prompt in prompts:
            print("PROMPT : ", prompt.name)

            get_prompt = await client.get_prompt(prompt_name=prompt.name, args={})
            print("GET Prompt : ", get_prompt[0].content.text)

        call_tool = await client.call_tool("analyze_code", arguments={"snippet":'''
def main():
    print("Hello world")
'''})
        print("CALL Tool : ", call_tool[0].text)

        call_tool = await client.call_tool("sugest_fix", arguments={"snippet":'''
async def greeting(name)-> str:
    return f"Hello ${name}"
'''})
        print("CALL Tool : ", call_tool[0].text)



asyncio.run(main())