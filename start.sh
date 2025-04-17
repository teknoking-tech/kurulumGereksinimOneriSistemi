#!/bin/bash

# CBOT Kurulum Asistanı başlatma betiği

# Sanal ortam var mı kontrol et, yoksa oluştur
if [ ! -d "venv" ]; then
    echo "Sanal ortam bulunamadı, oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı etkinleştir
source venv/bin/activate

# Gereksinimleri yükle
pip install -r requirements.txt

# Uygulamayı başlat
streamlit run app.py

# Sanal ortamdan çık
deactivate