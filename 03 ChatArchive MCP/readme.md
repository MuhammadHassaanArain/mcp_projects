# 📂 ChatArchive MCP

A **stateful MCP (Model Context Protocol) server** that stores and retrieves past chat messages.  
This project demonstrates **stateful MCP design, persistent storage**, and **response management** using Python and FastMCP.

---

## 🚀 Features

- **Save messages** from users with timestamps.
- **Retrieve recent messages** with a configurable limit.
- **Stateful in-memory cache** for fast access.
- **Persistent JSON storage** (`storage.json`) to survive server restarts.
- **Async MCP client-server communication** using FastMCP.

---

## 🛠️ Tools

### `save_message(user: str, msg: str)`

- Saves a new message from a user.
- Updates the in-memory cache and persists to `storage.json`.
- Returns a confirmation string.

**Example:**

```python

LIST TOOLS ⚙
Tool Name :  save_message
Tool Name :  get_recent_message

 TOOL CALLS 🔧
Tool Result:  Message Saved for user1.

 TOOL CALLS 🔧
Users Message:  Hassaan: Hey (2025-11-15T11:46:00.322454)
Users Message:  Haris: Hello (2025-11-15T11:46:16.001560)    
Users Message:  user1: what's up (2025-11-15T11:46:46.438036)
```

## 📂 Project Structure
```
# ChatArchive-MCP/
├─ server.py              # MCP server
├─ client.py              # MCP client
├─ storage.json           # Persistent storage (auto-generated)
├─ README.md              # Project documentation
```
