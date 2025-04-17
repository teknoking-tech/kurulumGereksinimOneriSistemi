@echo off
REM CBOT Kurulum Asistanı başlatma betiği (Windows)

REM Sanal ortam var mı kontrol et, yoksa oluştur
if not exist venv\ (
    echo Sanal ortam bulunamiyor, olusturuluyor...
    python -m venv venv
)

REM Sanal ortamı etkinleştir
call venv\Scripts\activate.bat

REM Gereksinimleri yükle
pip install -r requirements.txt

REM Uygulamayı başlat
streamlit run app.py

REM Sanal ortamdan çık
deactivate