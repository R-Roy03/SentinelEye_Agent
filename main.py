import os
import logging
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Import our custom Agent Architecture
from agent.agent import SentinelAgent

# 1. SETUP PROFESSIONAL LOGGING
# Cloud (Render/Railway) par 'print' statement kabhi-kabhi miss ho jate hain.
# Logging module har cheez timestamp ke sath record karega.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("SentinelEye")

# 2. LOAD ENVIRONMENT VARIABLES
load_dotenv()

# 3. INITIALIZE FASTAPI APP
app = FastAPI(title="SentinelEye Agent API", version="1.0.0")

# 4. MOUNT STATIC DIRECTORY
# Ye folder images ko temporary hold karega taaki WhatsApp unhe access kar sake via URL
if not os.path.exists("static_images"):
    os.makedirs("static_images")
app.mount("/images", StaticFiles(directory="static_images"), name="images")

# 5. INITIALIZE THE AGENT (GLOBAL INSTANCE)
# Hum server start hote hi agent load karte hain taaki database connect ho jaye.
try:
    agent = SentinelAgent()
    logger.info("✅ SentinelAgent: System Initialized & Ready")
except Exception as e:
    logger.critical(f"🔥 CRITICAL: Failed to initialize SentinelAgent. Error: {e}")
    agent = None

# --- ROUTES ---

@app.get("/")
async def health_check():
    """
    Health Check Endpoint.
    Cloud server check karta hai ki app zinda hai ya nahi.
    """
    status = "Online 🟢" if agent else "Offline (Agent Error) 🔴"
    return {
        "status": status,
        "service": "SentinelEye Autonomous Agent",
        "mode": "Production Ready"
    }

@app.post("/api/webhook")
async def whatsapp_webhook(
    Body: str = Form(""),  # Default to empty if missing
    From: str = Form(...),
    MediaUrl0: str = Form(None),
    MediaContentType0: str = Form(None)
):
    """
    Main Entry Point for Twilio/WhatsApp Webhooks.
    """
    try:
        # 1. Log Incoming Request Details
        user_id = From
        message_text = Body.strip()
        has_media = "Yes" if MediaUrl0 else "No"
        
        # Log incoming activity (Masking user number partially for privacy in logs if needed)
        logger.info(f"📩 INCOMING: User={user_id} | Text='{message_text[:50]}...' | Media={has_media}")

        # 2. Check Agent Status
        if not agent:
            logger.error("❌ Agent is not initialized.")
            return "System Error: SentinelEye is currently offline for maintenance."

        # 3. Determine Media Category
        media_category = None
        # Agar future mein media download logic add karna ho, toh wo yahan aayega.
        # Currently, hum sirf category pass kar rahe hain vision ke liye.
        if MediaContentType0:
            if "image" in MediaContentType0:
                media_category = "image"
            elif "pdf" in MediaContentType0:
                media_category = "pdf"
            logger.info(f"📎 Media Detected: {media_category} ({MediaContentType0})")

        # 4. Process Request via Agent Pipeline
        response_text = await agent.process_request(
            user_id=user_id,
            message_text=message_text,
            media_data=None, # Future: Downloaded bytes here
            mime_type=MediaContentType0,
            media_category=media_category
        )

        # 5. Return Response to Twilio
        logger.info(f"📤 RESPONSE SENT to {user_id}")
        return response_text

    except Exception as e:
        # Unexpected crashes catch karna zaroori hai
        logger.error(f"❌ PROCESS ERROR: {str(e)}", exc_info=True)
        return "SentinelEye encountered a critical error. Please try again later."

if __name__ == "__main__":
    # Local Development Run
    # Cloud par ye part execute nahi hota, wahan Gunicorn/Uvicorn command chalta hai.
    port = int(os.getenv("PORT", 8000))
    logger.info(f"🚀 Starting Server on Port {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)