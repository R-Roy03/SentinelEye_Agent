import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        # Naya SDK Client use kar rahe hain
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash"

    async def generate_response(self, system_prompt: str, media_data: bytes = None, mime_type: str = None):
        try:
            # Simple content structure for the new SDK
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=system_prompt
            )
            
            if response.text:
                return response.text.strip()
            return "Koshish ki par samajh nahi paya."
            
        except Exception as e:
            print(f"❌ Gemini SDK Error: {e}")
            return "Technical issue hai, wapas try karein."