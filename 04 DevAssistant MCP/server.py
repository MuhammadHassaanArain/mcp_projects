from mcp.server.fastmcp import FastMCP
from mcp.types import SamplingMessage, TextContent
from mcp.server.fastmcp.server import Context

mcp = FastMCP(name="DevAssistant Server", stateless_http=False)

@mcp.prompt()
async def analyze_code_prompt():
    return """
    You are a senior software engineer. Analyze the following code snippet.
Explain clearly:
- What the code does
- Any bugs or errors
- Potential optimizations
- Code smells or anti-patterns
- Suggested improvements (without rewriting the code)
"""

@mcp.prompt()
async def suggest_fix_prompt():
    return """
    You are a code-fixing assistant. Rewrite the provided code snippet with:
- Corrected logic
- Better structure
- Cleaner formatting
- Modern best practices
- Proper error handling (if needed)

After rewriting, explain what you fixed and why.

    """

async def run_tool(ctx: Context, snippet: str, prompt_func, max_tokens: int = 100):
    prompt = await prompt_func()
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(role="assistant", content=TextContent(type="text", text=prompt)),
            SamplingMessage(role="user", content=TextContent(type="text", text=snippet))
        ],
        max_tokens=max_tokens
    )
    return result.content.text if result.content.type == "text" else str(result.content)



@mcp.tool()
async def analyze_code(ctx : Context, snippet):
  try:
    return await run_tool(ctx, snippet, analyze_code_prompt)
  except Exception as e:
    return f"Error: {e}"

@mcp.tool()
async def sugest_fix(ctx : Context, snippet):
  try:
    return await run_tool(ctx, snippet, analyze_code_prompt)
  except Exception as e:
    return f"Error: {e}"


mcp_app = mcp.streamable_http_app()