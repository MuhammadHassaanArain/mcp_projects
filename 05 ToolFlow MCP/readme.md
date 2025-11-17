# 📝 MCP Task Manager — ToolFlow Server

A simple **personal task manager** powered by **MCP (Model Context Protocol)**.  
This project demonstrates how to build **CRUD operations** for tasks with an MCP server and client.

It allows an agent or client to:

- Add a task  
- Get a task by ID  
- Mark a task as done  
- Delete a task  
- (Optional) List all tasks  

This project is **stateless**, lightweight, and showcases **MCP Tools + Resource Management**.

---

## 🚀 Features

- **MCP Tools**:  
  - `add_task(task)` → Add a new task  
  - `get_task(task_id)` → Retrieve a task by ID  
  - `mark_done(task_id)` → Mark a task as completed  
  - `delete_task(task_id)` → Delete a task  
  - `get_tasks()` → List all tasks (optional addition)  

- **Persistent Storage**: Tasks are saved in `TASK.json`  
- **ID Management**: Automatically generates unique IDs  
- **Stateless HTTP Server**: Uses `FastMCP` with `stateless_http=True`  

---
