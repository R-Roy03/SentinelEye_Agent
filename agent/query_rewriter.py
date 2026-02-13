import os
from google import genai

class QueryRewriter:
    def __init__(self):
        # API Key load karna
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("❌ QueryRewriter: API Key nahi mili!")
            
        # Naya GenAI SDK use kar rahe hain for stability
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash"

    async def rewrite(self, user_query: str, history_context: str) -> str:
        """
        User Query + History = Perfect Search Query
        """
        prompt = f"""
        You are an Expert Search Engineer. Your task is to rewrite the user's input into a specific, 
        detailed, and optimized search query for a search engine (Tavily/Google).

        ### RULES:
        1. USE CONTEXT: If the user says "price kya hai?" and history mentions "Mustang", 
           rewrite as "current market price of Ford Mustang Shelby GT500".
        2. BE SPECIFIC: Add relevant years (2026) or locations if applicable.
        3. REMOVE NOISE: Remove words like "please", "find", "search for", "mujhe batao".
        4. OUTPUT ONLY: Return only the rewritten string. No chatter.

        ### CONTEXT FROM CONVERSATION:
        {history_context}

        ### USER'S RAW INPUT:
        "{user_query}"

        OPTIMIZED SEARCH QUERY:
        """

        try:
            # Sync call ko async mein handle karne ke liye hum standard client use kar rahe hain
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
            if response and response.text:
                return response.text.strip().replace('"', '')
            return user_query # Fallback if empty
            
        except Exception as e:
            print(f"❌ Rewriter Error: {e}")
            return user_query # Error hone par original query hi bhej do