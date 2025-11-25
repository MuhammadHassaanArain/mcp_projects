import asyncio
from typing import Optional, Any
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from contextlib import AsyncExitStack
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


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
    


console = Console()
def pretty(title, text, emoji="✨", color="cyan", box_style=box.ROUNDED):
    console.print(
        Panel.fit(
            f"{emoji} [bold {color}]{title}[/bold {color}]\n\n{text}",
            title=f"[{color}]{title.upper()}[/]",
            box=box_style
        )
    )

async def main():
    async with MCPCient("http://localhost:8000/mcp") as client:
# List Tools Availabe
        tools = await client.list_tools()
        table = Table(title="Available MCP Tools", box=box.SIMPLE_HEAVY)
        table.add_column("Tool Name", style="cyan", no_wrap=True)
        for tool in tools:
            table.add_row(tool.name)
        console.print(table)

# Add Tasks
        add_task1 = await client.call_tool("add_task", arguments={"task": "Push the code to GitHub Repo"})
        pretty("Task Added", add_task1[0].text, emoji="📌", color="green")

        add_task2 = await client.call_tool("add_task", arguments={"task": "Post on LinkedIn"})
        pretty("Task Added", add_task2[0].text, emoji="📌", color="green")

        add_task3 = await client.call_tool("add_task", arguments={"task": "Complete Class Assignment"})
        pretty("Task Added", add_task3[0].text, emoji="📌", color="green")
# GET Tasks 
        get_task = await client.call_tool("get_task", arguments={"task_id": 1})
        pretty("Task Details", get_task[0].text, emoji="🔎", color="yellow", box_style=box.DOUBLE_EDGE)

# Mark Done
        mark_done = await client.call_tool("mark_done", arguments={"task_id": 1})
        pretty("Task Completed", mark_done[0].text, emoji="✅", color="magenta")

        mark_done = await client.call_tool("mark_done", arguments={"task_id": 3})
        pretty("Task Completed", mark_done[0].text, emoji="✅", color="magenta")

# Delete Task
        delete_task = await client.call_tool("delete_task", arguments={"task_id": 3})
        pretty("Task Deleted", delete_task[0].text, emoji="🗑️", color="red")


asyncio.run(main())