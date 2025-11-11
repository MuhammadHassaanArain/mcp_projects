Description:
    A tool based mcp server that connects to multiple pulblic apis (like weather, crypto prices, and news)
    It provides structured data respources and tools for any mcp client (like open ai agent sdk) to querry in real life
    KEY Learning :
        Tools,resources,schema design, stateless http

Example tools:
    get_weather(location)
    get_crypto_price(symbol)
    get_latest_news(topic)
    
<!-- ------------------------------------------------------------------------ -->

# 🚀 Multi-API Real-World Data MCP Server  
*A tool-based MCP server using real public APIs (Weather, Crypto, News)*

---

## ✅ Project Overview

This MCP server acts as a bridge between **real-world data** and **MCP clients** such as the OpenAI Agent SDK.  
It exposes tools and structured resources that fetch live information from public APIs.

---

## 🧩 Key Learning Objectives

- ✅ MCP Tools Development  
- ✅ Stateless HTTP MCP Server  
- ✅ JSON Schema Design & Validation  
- ✅ Integrating Real Public APIs  
- ✅ Error + Rate Limit Handling  
- ✅ Making MCP server usable by any Agent SDK client

---

## 🛠️ MCP Tools List

| Tool Name | Inputs | Outputs | Description |
|----------|--------|---------|-------------|
| `get_weather(location: str)` | City or geo query | Temperature, humidity, condition | Fetch live weather data |
| `get_crypto_price(symbol: str)` | Cryptocurrency symbol | Price in USD + market info | Fetch real-time crypto prices |
| `get_latest_news(topic: str = "general")` | Interest/topic string | Articles list with URLs | Fetch trending news |

---

## 🗃️ Suggested Public APIs

| Category | Provider | Auth | Notes |
|---------|----------|------|------|
| Weather | **OpenWeather** | ✅ Key required | Free tier available |
| Crypto | **CoinGecko** | ❌ No auth needed | Best for beginners |
| News | **NewsAPI** | ✅ Key required | Easy structured headlines |

---

## 📑 Unified Response Schema

Every tool returns structured JSON like:

```json
{
  "status": "success",
  "data": {
    "source": "api_name",
    "result": {}
  }
}
