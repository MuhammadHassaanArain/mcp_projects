from mcp.server.fastmcp import FastMCP
import json
from datetime import datetime
STORAGE = "storage.json"

mcp = FastMCP(name="ChatArchive Server", stateless_http=False)
messages_cache = []

try:
    with open(STORAGE, "r") as f:
        messages_cache = json.load(f).get("messages", [])
except FileNotFoundError:
    messages_cache =  []
    
def write_message():
    with open(STORAGE, "w") as f:
        json.dump({"messages":messages_cache}, f, indent=4)
    

@mcp.tool()
async def save_message(user:str, msg:str):
    """Save a new message from a user into local storage"""
    msg_obj = {
        "user":user,
        "message":msg,
        "timestamp":datetime.utcnow().isoformat()
    }
    messages_cache.append(msg_obj)
    write_message()
    return f"Message Saved for {user}."


@mcp.tool()
async def get_recent_message(limit:int):
    """ Retrieve the most recent 'limit' number of messages. """
    recent_msg = messages_cache[-limit:]
    return [
        f"{m['user']}: {m['message']} ({m['timestamp']})" 
        for m in recent_msg
    ]



mcp_app = mcp.streamable_http_app()