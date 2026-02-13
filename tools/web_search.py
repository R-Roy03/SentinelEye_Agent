import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Tavily Client Initialize karo
tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=tavily_api_key)

def search_web(query: str):
    print(f"🔎 SEARCHING TAVILY FOR: {query}...")
    
    try:
        # Tavily specifically 'answers' dhundta hai, bas links nahi
        response = tavily.search(query=query, search_depth="basic", max_results=3)
        
        results = response.get("results", [])
        print(f"👀 DATA FOUND: {len(results)} results")
        
        if not results:
            return "Search kiya par koi data nahi mila."
            
        summary = ""
        for res in results:
            summary += f"- {res['content']} (Source: {res['url']})\n"
            
        return summary

    except Exception as e:
        print(f"❌ Search Error: {e}")
        return "Search tool error. Please check API Key."

# Test block
if __name__ == "__main__":
    print(search_web("Gold price in India today 24k"))