from dotenv import load_dotenv
import os
from tavily import TavilyClient

_ = load_dotenv()

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

city = "San Francisco"

query = f"""
    what is the current weather in {city}?
    Should I travel there today?
    "weather.com"
""" 

# run search
result = client.search(query, max_results=1)

# print first result
data = result["results"][0]["content"]

print(data)