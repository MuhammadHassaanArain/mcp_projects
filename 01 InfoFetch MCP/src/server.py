import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
load_dotenv()

mcp = FastMCP("InfoFetch_Server", stateless_http=True)

weather_api_key = os.getenv("weather_api_key")
news_api_key = os.getenv("news_api_key")

# 🌤️ WEATHER TOOL
@mcp.tool(name="get_weather", description="Get current weather by city name.")
async def get_weather(location:str):
    """
    Get the current weather for a city using WeatherAPI.com.
    
    Args:
        city (str): Name of the city to get weather for
    """
    print(f"🌤️  Weather Tool Called for city: {location}")
    try:
        async with httpx.AsyncClient() as client:
            url =  f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}&aqi=no"
            response =await client.get(url)
            response.raise_for_status()
            data = response.json()
            loc = data["location"]["name"]
            cond = data["current"]["condition"]["text"]
            temp_c = data["current"]["temp_c"]
            humidity = data["current"]["humidity"]
            return f"Weather in {loc}: {cond}, {temp_c}°C, humidity {humidity}%."
    except Exception as e:
        return f"Error fetching weather: {e}"
    
# 📰 NEWS TOOL
@mcp.tool(name="get_latest_news",  description="Fetch the latest news articles for a given topic.")
async def get_latest_news(topic:str, max_res:int = 3):
    """
    Fetches the latest news articles for a topic from GNews API. 
    Returns a list of formatted strings with article number, title, description, URL, and published date.
    Returns a message if no articles are found or on error.
    """
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://gnews.io/api/v4/search"
            params = {
                "q":topic,
                "lang":"us",
                "country":"us",
                "max":max_res,
                "apikey":news_api_key
            }
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles",[])
            if not articles:
                return f"No articles found for topic '{topic}'."
            result = []
            for i, article in enumerate(articles, start=1):
                article_str = (
                    f"Article No: {i}, "
                    f"Title: {article.get('title')}, "
                    f"Description: {article.get('description')}, "
                    f"URL: {article.get('url')}, "
                    f"Published At: {article.get('publishedAt')}"
                )
                result.append(article_str)
            
            return result
    except Exception as e:
        return f"Error fetching news: {e}"
  
# 💰 CRYPTO TOOL
@mcp.tool(name="get_crypto_price")
async def get_crypto_price(symbol:str):
    """
    Fetches the current USD price of a cryptocurrency from CoinGecko
    and returns it as a formatted string.
    """
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids":symbol.lower(),
                "vs_currencies": "usd"
            }
            response = await client.get(url,params=params)
            response.raise_for_status()
            data = response.json()
            price = data.get(symbol.lower(), {}).get("usd")
            if price is None:
                return f"Price not found for '{symbol}'."
            
            return f"The current price of {symbol.capitalize()} is ${price}"
    except Exception as e :
        return f"Error Fecting Prices : {e}"


mcp_app = mcp.streamable_http_app()