# Python'un resmi imajını temel al
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıkları kopyala ve kur
COPY requirements.txt .
RUN apt-get update && apt-get install -y curl && \
    pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Uygulamayı çalıştır
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
