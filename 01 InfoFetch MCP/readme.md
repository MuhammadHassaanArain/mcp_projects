# 🌐 InfoFetch MCP — Async MCP Server & Client Example

This project demonstrates how to build an **asynchronous MCP server and client** using the **OpenAI Model Context Protocol (MCP)** and **FastMCP**.  
It provides real-time data fetching tools for:
- 🌤️ Weather  
- 💰 Cryptocurrency Prices  
- 📰 News Headlines  

All interactions are asynchronous using `httpx` and `asyncio`.

---

## 🚀 Features

- Fully asynchronous MCP server (`FastMCP`)
- Three live API-integrated tools:
  - `get_weather` → Fetch live weather via WeatherAPI
  - `get_crypto_price` → Fetch live crypto prices via CoinGecko
  - `get_latest_news` → Fetch recent news via GNews
- Client connects via `streamablehttp_client`
- Minimal, clean async structure with context management

---

## 🧰 Project Setup

### 1. Clone and Install
```bash
git clone https://github.com/yourusername/infofetch-mcp.git
cd infofetch-mcp
pip install -r requirements.txt
