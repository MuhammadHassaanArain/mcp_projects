from mcp.server.fastmcp import FastMCP
import json
mcp = FastMCP("ToolFlow Server", stateless_http=True)

TASKS = []

def save_task():
    with open("TASK.json","w") as f:
        json.dump(TASKS, f, indent=2)

def load_task():
    global TASKS
    try:
        with open("TASK.json", "r") as f:
            TASKS = json.load(f)
    except:
        TASKS = []



def generate_id():
    if not TASKS:
        return 1
    return max(t["id"] for t in TASKS) + 1



@mcp.tool()
async def add_task(task:str):
    load_task()
    new_task = {
        "id":generate_id(),
        "task":task,
        "done":False
    }
    TASKS.append(new_task)
    save_task()
    return {
        "message": "Task added successfully!",
        "task": new_task
    }

@mcp.tool()
async def get_task(task_id:int):
    load_task()
    for t in TASKS:
        if t["id"] == task_id:
            return t
    return {
        "error":"Task ID not found"
    }



@mcp.tool()
async def mark_done(task_id:int):
    load_task()
    for t in TASKS:
        if t["id"] == task_id:
            t["done"] = True
            save_task()
            return {
                "message": "Task marked as done!",
                "task": t
            }
    return {
        "error":"task not found"
    }


@mcp.tool()
async def delete_task(task_id:int):
    load_task()
    for t in TASKS:
        if t["id"] == task_id:
            TASKS.remove(t)
            save_task()
            return {
                "message" : "Task Remove Succesfully"
            }
    return {
        "error":"Task Not Found"
    }


mcp_app = mcp.streamable_http_app()




