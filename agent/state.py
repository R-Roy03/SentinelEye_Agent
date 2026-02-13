import os
import time
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class AgentState:
    def __init__(self, user_id: str):
        """
        user_id: WhatsApp number (e.g., 'whatsapp:+919006545634')
        Is id ke basis par hum unique document maintain karte hain.
        """
        self.user_id = user_id
        
        # MongoDB Connection
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("❌ Error: MONGO_URI not found in .env file.")
            
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client["sentineleye_db"]
        self.collection = self.db["user_memories"]
        
        # Print for Debugging (Sirf pehli baar check karne ke liye)
        # print(f"🗄️ State initialized for User: {self.user_id}")

    async def add_message(self, role: str, content: str, metadata: dict = None):
        """
        Is user ke unique document mein naya message push karta hai.
        """
        try:
            message_data = {
                "role": role,
                "content": content,
                "timestamp": time.time(),
                "metadata": metadata or {}
            }

            # 'upsert=True' ka matlab hai agar user ka doc nahi hai toh naya bana do
            await self.collection.update_one(
                {"user_id": self.user_id},
                {
                    "$push": {"history": message_data},
                    "$set": {"last_active": time.time()}
                },
                upsert=True
            )
        except Exception as e:
            print(f"❌ State Error (add_message): {e}")

    async def get_formatted_history(self, limit: int = 15):
        """
        Database se is user ki pichli 'limit' messages fetch karke string format mein deta hai.
        """
        try:
            user_doc = await self.collection.find_one({"user_id": self.user_id})
            
            if not user_doc or "history" not in user_doc:
                return "No previous conversation context."

            # Last 'limit' messages nikalna
            history = user_doc["history"][-limit:]
            
            # Text format mein badalna (Gemini ke samajhne ke liye)
            formatted_history = []
            for msg in history:
                role = "User" if msg["role"] == "user" else "Sentinel"
                formatted_history.append(f"{role}: {msg['content']}")
            
            return "\n".join(formatted_history)
        
        except Exception as e:
            print(f"❌ State Error (get_history): {e}")
            return "Context retrieval failed."

    async def clear_history(self):
        """
        Sirf is specific user ki history saaf karne ke liye.
        """
        await self.collection.delete_one({"user_id": self.user_id})
        print(f"🗑️ Memory cleared for user: {self.user_id}")