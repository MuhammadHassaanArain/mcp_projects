import asyncio
from bs4 import BeautifulSoup
import os
from contextlib import AsyncExitStack
from mcp import ClientSession
from typing import Optional
from mcp.client.streamable_http import streamablehttp_client
from mcp.shared.context import RequestContext
from mcp.types import CreateMessageRequestParams, CreateMessageResult, TextContent
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)


async def mock_sampler(context:RequestContext[ClientSession, any], params:CreateMessageRequestParams):

    llm_resonse = "321 Pillay 😂"
    return (
        CreateMessageResult(
            role="assistant",
            content=TextContent(
                type="text",
                text=llm_resonse
            ),
            model="static response"
        )
    )

async def real_summarize(context:RequestContext[ClientSession, any], params:CreateMessageRequestParams):
    Summarizer_agent = Agent(
        name="Summarizer Agent", 
        instructions ="You are a Summarizer Agent and your role is to Summarize the provided Content.",
        model=model
    )
    result = await Runner.run(Summarizer_agent, params.messages[0].content.text)
    
    return (
        CreateMessageResult(
            role="assistant",
            content=TextContent(type="text", text=result.final_output),
            model=model.model,
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
            ClientSession(read_stream=_read_stream, write_stream=_write_stream, sampling_callback=real_summarize)
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
    
    
    async def list_resources(self):
        assert self._session, "Session Not Found"
        result = await self._session.list_resources()
        return result.resources
    async def list_temp_resources(self):
        assert self._session, "Session Not Found"
        result  = await self._session.list_resource_templates()
        return result.resourceTemplates
    async def read_list_res(self, uri):
        assert self._session, "Session Not Found"
        result = await self._session.read_resource(uri=uri)
        return result.contents


    async def list_prompt(self):
        result =  await self._session.list_prompts()
        return result.prompts
    async def get_prompt(self, prompt_name:str, args:dict[str, any]):
        result = await self._session.get_prompt(name=prompt_name, arguments=args)
        return result.messages

async def main():
    async with MCPCient("http://localhost:8000/mcp") as client:

        print("\n🧰 Listing Tools...")
        list_tools = await client.list_tools()
        for tool in list_tools:
            print("Tool Name: ",tool.name)
            
        
        print("\n🧰 Call Tools...")
        call_tool = await client.call_tool("list_documents", arguments={"doc_id":"doc1"})
        print("Tool Call: ",call_tool[0].text)
        


        print("\n🧰 Listing Resources...")
        list_res = await client.list_resources()
        for resourcs in list_res:
            print("Resource Name: ",resourcs.name)

        print("\n🧰 Listing Template Resources...") 
        list_temp_res = await client.list_temp_resources()
        for list_resourcs in list_temp_res:
            print("Temp Resource Name: ",list_resourcs.name)
        
        
        doc_ids = ["doc1", "doc2", "report"]  # From  documents dict
        print("\n🧰 Reading Resources...") 
        for doc_id in doc_ids:
            uri = f"docs://documents/{doc_id}" 
            read_res = await client.read_list_res(uri)
            for res in read_res:
                html = res.text
                soup = BeautifulSoup(html, "html.parser")
                print(soup.get_text())



        print("\n🧰 Listing Prompt...")
        list_prompt = await client.list_prompt()
        print("List Prompt: ",list_prompt[0].name)

        print("\n🧰 Getting Prompt...")
        getting_prompt = await client.get_prompt("summarize_document",args={"content":"How are you robert,i just got your email, actually i am quitting from this job and moving to Pakistan. "})
        print("List Prompt: ",getting_prompt[0].content.text)

        
        print("\n🧰 Call Sampling Tool...")
        sampling_tool_call = await client.call_tool(tool_name="summarize_content",arguments={"prompt":getting_prompt[0].content.text})
        print("Sampling Tool Call : ",sampling_tool_call[0].text)
        
if __name__ == "__main__":
    asyncio.run(main())