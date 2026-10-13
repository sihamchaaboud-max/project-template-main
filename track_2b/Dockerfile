FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    HF_HOME=/models

WORKDIR /app

# PyTorch version CPU (beaucoup plus leger que la version CUDA par defaut)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Lecture de photos (OCR) : Tesseract avec le francais et l'allemand
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-fra tesseract-ocr-deu \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 7860
CMD ["python", "app.py"]