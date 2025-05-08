# Alap image
FROM python:3.12.8-slim-bullseye

# Munkakönyvtár beállítása
WORKDIR /app

# Követelmények másolása és telepítése
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Forráskód másolása
COPY . .

# FastAPI indítása Uvicorn-nal
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
