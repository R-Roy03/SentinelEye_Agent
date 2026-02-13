from tools.web_search import search_web
from tools.image_gen import generate_image_tool  # <-- Ye niche banayenge

# --- CONFIGURATION ---
# Apna LATEST Ngrok URL yahan paste karein (Example: https://abcd-1234.ngrok-free.app)
CURRENT_NGROK_URL = "https://stilliform-katharine-distichous.ngrok-free.dev" 

class Executor:
    async def execute(self, plan: dict, llm_client, media_data: bytes = None):
        action = plan.get("action")
        query = plan.get("query")
        context_data = ""

        # 1. Web Search
        if action == "search":
            print(f"⚙️ EXECUTOR: Web Search for '{query}'")
            results = search_web(query)
            context_data = f"\n[SEARCH RESULTS]:\n{results}\n"

        # 2. Image Generation (NEW)
        elif action == "generate_image":
            print(f"⚙️ EXECUTOR: Creating Image for '{query}'...")
            
            # Tool call karein
            filename = generate_image_tool(query)
            
            if filename:
                # Full URL banayein taaki WhatsApp par dikhe
                image_url = f"{CURRENT_NGROK_URL}/images/{filename}"
                
                # LLM ko batayein ki image ban gayi hai aur URL ye raha
                context_data = f"SUCCESS: Image generated. URL: {image_url}. Please send this URL to the user."
            else:
                context_data = "[Error: Image generation failed.]"

        # 3. Vision (Image Analysis)
        elif action == "vision":
            context_data = "[User uploaded an image. Analyze it.]"

        return context_data