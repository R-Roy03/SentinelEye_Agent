import re

class Planner:
    def __init__(self):
        # 1. Web Search Keywords
        self.search_triggers = [
            "news", "latest", "price", "search", "update", "weather", "score", 
            "ceo", "who is", "current", "india", "gold", "stock", 
            "kaun hai", "kya hai", "kya chal raha", "samachar", "khabar"
        ]
        
        # 2. Image Generation Keywords (NEW)
        self.image_triggers = [
            "imagine", "generate image", "photo banao", "tasveer banao", 
            "draw", "create an image", "picture of", "image of"
        ]

    def decide_action(self, message_text: str, media_category: str = None) -> dict:
        """
        Decides the next action based on user input.
        """
        clean_text = message_text.lower().strip()

        # A. Agar User ne Photo bheji hai (Vision Mode)
        if media_category == "image":
            return {"action": "vision", "query": message_text or "Describe this image."}

        # B. Agar User Photo banvana chahta hai (Image Gen Mode) <-- NEW
        if any(word in clean_text for word in self.image_triggers):
            print(f"🎨 PLANNER: Image Generation Requested")
            return {"action": "generate_image", "query": message_text}

        # C. Agar Web Search chahiye
        if any(word in clean_text for word in self.search_triggers):
            return {"action": "search", "query": self._clean_query(message_text)}
            
        # D. Normal Chat
        return {"action": "chat", "query": message_text}

    def _clean_query(self, text: str) -> str:
        # Faltu words hatata hai search query se
        text = re.sub(r'(?i)sentinel\s?eye|sentinel', '', text)
        return text.replace('"', '').replace("'", "").strip()