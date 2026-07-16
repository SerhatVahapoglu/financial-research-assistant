# 1. Hafif bir Python imajı seçiyoruz
FROM python:3.11-slim

# 2. Çalışma dizinini belirliyoruz
WORKDIR /app

# 3. Gerekli kütüphaneleri yüklemek için önce requirements dosyasını kopyalıyoruz
COPY requirements.txt .

# 4. Kütüphaneleri yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tüm proje kodlarını kopyalıyoruz
COPY . .

# 6. Uygulamanın çalışacağı portu açıyoruz
EXPOSE 8501

# 7. Streamlit uygulamasını başlatıyoruz
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]