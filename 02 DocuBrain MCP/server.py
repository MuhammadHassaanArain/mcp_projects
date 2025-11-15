import os
import aiofiles
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
from mcp.types import SamplingMessage, TextContent


mcp = FastMCP(name="DocuBrain-Server", stateless_http=False)

documents = {
    "doc1": {"uri": "file://documents/doc1.txt", "title": "Doc 1"},
    "doc2": {"uri": "file://documents/doc2.txt", "title": "Doc 2"},
    "report": {"uri": "https://medium.com/@shutuphassaan/about", "title": "Report"}
}

@mcp.tool(name="list_documents", description="Show available documents (local + remote)")
async def list_documents():
    """Show all available documents with URI, title, and size."""
    result = []
    for doc in documents.values():
        uri = doc["uri"]
        size = "unknown"
        try:
            if uri.startswith("file://"):
                size = f"{os.path.getsize(uri.replace('file://',''))/1024:.1f} KB"
            elif uri.startswith("http"):
                async with httpx.AsyncClient() as client:
                    resp = await client.head(uri)
                    size_bytes = int(resp.headers.get("Content-Length", 0))
                    if size_bytes: size = f"{size_bytes/1024:.1f} KB"
        except: pass
        result.append({"uri": uri, "title": doc["title"], "size": size})
    return result

@mcp.resource("docs://documents/{doc_id}")
async def read_document(doc_id: str):
    """
    Fetch document content dynamically by doc_id.
    Supports local files (file://) and remote URLs (https://).
    """
    doc = documents.get(doc_id)
    if not doc:
        return {"error": f"Document '{doc_id}' not found."}

    uri = doc["uri"]
    content = ""
    try:
        if uri.startswith("file://"):
            async with aiofiles.open(uri.replace("file://", ""), mode="r", encoding="utf-8") as f:
                content = await f.read()
        elif uri.startswith("http"):
            async with httpx.AsyncClient() as client:
                resp = await client.get(uri)
                resp.raise_for_status()
                content = resp.text
        else:
            return {"error": f"Unsupported URI: {uri}"}
    except Exception as e:
        return {"error": f"Failed to read document: {e}"}

    return {"uri": uri, "title": doc["title"], "content": content}


@mcp.prompt("summarize_document")
def summarize_prompt(content: str):
    """
    Summarize the following document:
    {content}
    """
    return f"Summarize the following document:{content}"


@mcp.tool()
async def summarize_content(ctx:Context, prompt:str):
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
        role="user",
        content=TextContent(type="text", text=prompt)
        )
        ], max_tokens=200
    )
    if result.content.type == "text":
        return result.content.text
    return str(result.content)  
    
mcp_app = mcp.streamable_http_app()
