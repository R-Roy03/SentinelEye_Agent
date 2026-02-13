# 1. Base Image: Python 3.11 (Lightweight version)
FROM python:3.11-slim

# 2. Work Directory set karein
WORKDIR /app

# 3. Pehle requirements copy karein (Caching ke liye fast hota hai)
COPY requirements.txt .

# 4. Libraries install karein
RUN pip install --no-cache-dir -r requirements.txt

# 5. Baaki sara code copy karein
COPY . .

# 6. Static images folder create karein (Safety ke liye)
RUN mkdir -p static_images

# 7. Port expose karein (Render default 10000 use karta hai, par hum standard 8000 rakhenge)
EXPOSE 8000

# 8. Command to start SentinelEye
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]