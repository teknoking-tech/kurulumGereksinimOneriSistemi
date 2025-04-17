"""
CBOT Kurulum Asistanı - Yardımcı Fonksiyonlar
"""

import streamlit as st
import math
import base64
from datetime import datetime


def get_environment_label(env_type):
    """Ortam tipini okunabilir etikete dönüştürün"""
    if env_type == "test":
        return "Test"
    elif env_type == "live":
        return "Canlı"
    return env_type.capitalize()


def get_deployment_label(deployment_type):
    """Deployment tipini okunabilir etikete dönüştürün"""
    if deployment_type == "on-prem":
        return "On-Premises"
    elif deployment_type == "cloud":
        return "Bulut"
    return deployment_type.capitalize()


def get_service_label(service_name):
    """Servis adını okunabilir etikete dönüştürün"""
    if service_name == "ocr":
        return "OCR"
    elif service_name == "file_to_markdown":
        return "File to Markdown"
    elif service_name == "hf_model_hosting":
        return "HF Model Hosting"
    return service_name.capitalize()


def calculate_total_hardware(requirements, form_data):
    """Toplam donanım gereksinimlerini hesaplayın"""
    totals = {
        "test": {"cpu": 0, "ram": 0, "disk": 0},
        "live": {"cpu": 0, "ram": 0, "disk": 0}
    }
    
    # Her modül için gereksinimleri toplayın
    for module_req in requirements["hardware"].values():
        if "test" in form_data["environment_type"] and "test" in module_req:
            # CPU çekirdekleri için sayısal değerleri çıkarın
            cpu_cores = int(module_req["test"]["cpu"].split(' ')[0])
            totals["test"]["cpu"] += cpu_cores
            
            # RAM (GB) için sayısal değerleri çıkarın
            ram_gb = int(module_req["test"]["ram"].split(' ')[0])
            totals["test"]["ram"] += ram_gb
            
            # Disk alanı (GB) için sayısal değerleri çıkarın
            disk_gb = int(module_req["test"]["disk"].split(' ')[0])
            totals["test"]["disk"] += disk_gb
        
        if "live" in form_data["environment_type"] and "live" in module_req:
            # CPU çekirdekleri için sayısal değerleri çıkarın
            cpu_cores = int(module_req["live"]["cpu"].split(' ')[0])
            totals["live"]["cpu"] += cpu_cores
            
            # RAM (GB) için sayısal değerleri çıkarın
            ram_gb = int(module_req["live"]["ram"].split(' ')[0])
            totals["live"]["ram"] += ram_gb
            
            # Disk alanı (GB) için sayısal değerleri çıkarın
            disk_gb = int(module_req["live"]["disk"].split(' ')[0])
            totals["live"]["disk"] += disk_gb
    
    return totals


def format_file_name(org_name, format_type):
    """Güvenli bir dosya adı oluşturun"""
    if not org_name:
        org_name = "Organizasyon"
    
    # Güvenli bir dosya adı oluşturun (boşlukları ve özel karakterleri alt çizgi ile değiştirin)
    safe_name = "".join(c if c.isalnum() else "_" for c in org_name)
    
    # Uzantıyı düzelt
    extension = format_type
    if format_type == "word":
        extension = "docx"
    
    # Dosya adını biçimlendirin
    date_str = datetime.now().strftime("%Y%m%d")
    return f"CBOT_Kurulum_{safe_name}_Gereksinimleri_{date_str}.{extension}"


def get_binary_file_downloader_html(bin_file, file_label='Dosya', button_text='İndir'):
    """İndirme bağlantısı oluşturan HTML kodu"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}" class="download-button">{button_text}</a>'
    
    return href


def streamlit_header():
    """Streamlit uygulaması için başlık oluşturun"""
    st.markdown(
        """
        <style>
        .header-container {
            background: linear-gradient(90deg, #1E40AF, #172554);
            color: white;
            padding: 1.5rem;
            border-radius: 0.5rem 0.5rem 0 0;
            margin-bottom: 0;
        }
        .header-title {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .header-subtitle {
            color: #BFDBFE;
            font-size: 1rem;
        }
        </style>
        
        <div class="header-container">
            <div class="header-title">CBOT Kurulum Asistanı</div>
            <div class="header-subtitle">Modül seçimi ve kurulum gereksinimleri oluşturma aracı</div>
        </div>
        """, 
        unsafe_allow_html=True
    )


def streamlit_footer():
    """Streamlit uygulaması için altbilgi oluşturun"""
    st.markdown(
        """
        <style>
        .footer-container {
            background: #1F2937;
            color: #D1D5DB;
            padding: 1.5rem;
            border-radius: 0 0 0.5rem 0.5rem;
            margin-top: 2rem;
            display: flex;
            justify-content: space-between;
        }
        .footer-copyright {
            font-size: 0.875rem;
        }
        .footer-version {
            font-size: 0.75rem;
        }
        </style>
        
        <div class="footer-container">
            <div class="footer-copyright">© 2025 CBOT. Tüm hakları saklıdır.</div>
            <div class="footer-version">v2.0.0 | Kurulum Asistanı</div>
        </div>
        """, 
        unsafe_allow_html=True
    )