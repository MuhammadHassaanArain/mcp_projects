# 📄 DocuBrain — MCP Document Summarizer  
### (Built with MCP + Sampling + OpenAI Agent SDK + Gemini)

DocuBrain is a complete end-to-end project showing how to build an **MCP Server + MCP Client** that uses **Sampling** to run an LLM-powered Summarizer Agent via the **OpenAI Agent SDK**.  
It supports **local documents, remote URLs, prompts**, and real-time **LLM summarization using Gemini**.

---

## 🚀 Features

- 🔧 **MCP Tools** → List documents, read documents, summarize text  
- 📡 **MCP Resources** → Load documents dynamically (local + remote)  
- 📘 **MCP Prompts** → Reusable summarization templates  
- 🧠 **Sampling** → Server defers summarization to the client  
- 🤖 **Agent SDK Integration** → Summarizer Agent using `gemini-2.5-flash`  
- ⚡ **Async I/O** → Uses `aiofiles` + `httpx` for fast file/network access  


## Project Structure

📂 documind_mcp/
 ┣ 📜 server.py           # Main MCP server with tools and resources
 ┣ 📜 client.py           # MCP client to interact with tools
 ┣ 📂 documents/          # Local .txt / .md / .pdf files
 ┣ 📜 prompts.yaml        # Summarization prompt template
 ┗ 📜 .env                # Any needed configs

## 🛠 MCP Server (server.py)

### Server Capabilities
- **`list_documents`** → Returns available docs + size  
- **`read_document`** → Reads local files or remote URLs  
- **`summarize_document`** → Prompt template  
- **`summarize_content`** → Calls LLM via Sampling  

### 🔄 How the Server Works (Flow)
1. Client calls **summarize_content** tool  
2. Server creates a **SamplingMessage**  
3. MCP client receives it and triggers **real_summarize**  
4. Summarizer Agent runs via OpenAI Agent SDK  
5. Agent produces a summary  
6. Summary sent back to MCP server  
7. Server returns it as tool output  

---

## 🧠 MCP Client (client.py)

### Client Responsibilities
- Connects to the MCP server  
- Registers a **sampling callback** (`real_summarize`)  
- Creates a **Summarizer Agent** using Gemini  
- Runs the agent using **Runner.run()**  
- Sends back LLM output to MCP  

---
