# DevAssistant MCP

DevAssistant MCP is a **stateful Model Context Protocol (MCP) server** and client that allows users to analyze and fix code snippets using AI-powered assistants. The server leverages Gemini API for code understanding and suggestions.

## 🚀 Features

- **Analyze Code**: Get detailed analysis of a code snippet including potential bugs, optimizations, code smells, and improvements.
- **Suggest Fix**: Receive rewritten, optimized, and cleaner code for your snippets.
- **Stateful MCP Server**: Maintains context across requests.
- **Prompts as tools**: Separate prompts for analysis and fixes for easy extensibility.
- **Gemini API integration**: Uses Google Gemini 2.5 for high-quality code assistance.

## 📂 Project Structure
```
DevAssistant-MCP/
├─ server.py # MCP server (stateful)
├─ client.py # MCP client with Gemini sampling
├─ .env # Environment variables (GEMINI_API_KEY)
├─ README.md # Project documentation
```