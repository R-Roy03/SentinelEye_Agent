import os
import time
from google import genai
from google.genai import types

def generate_image_tool(prompt: str):
    """
    Latest Google GenAI SDK ka use karke Image banata hai.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        client = genai.Client(api_key=api_key)
        
        print(f"🎨 Imagen 3.0 call for: {prompt}")
        
        # Imagen Model call
        response = client.models.generate_image(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImageConfig(
                number_of_images=1,
                include_rai_reasoning=True,
                output_mime_type='image/png'
            )
        )

        # File save logic
        save_dir = "static_images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        filename = f"gen_{int(time.time())}.png"
        filepath = os.path.join(save_dir, filename)
        
        # Save image bytes
        with open(filepath, "wb") as f:
            f.write(response.generated_images[0].image_bytes)

        print(f"✅ Image Generated: {filepath}")
        return filename

    except Exception as e:
        print(f"❌ Imagen Error: {e}")
        return None