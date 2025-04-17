"""
CBOT Kurulum Asistanı - Admin Paneli
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Session state yönetimi
def initialize_admin_state():
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if 'users' not in st.session_state:
        st.session_state.users = {
            "admin": "admin123",  # Basit şifre - gerçek uygulamada güçlü şifreleme kullanılmalıdır
        }
    
    if 'saved_configs' not in st.session_state:
        st.session_state.saved_configs = []
        # Kayıtlı konfigürasyonları yükle (eğer varsa)
        if os.path.exists("data/configs.json"):
            try:
                with open("data/configs.json", "r") as f:
                    st.session_state.saved_configs = json.load(f)
            except:
                pass

def admin_login():
    st.markdown("<h1 style='text-align: center;'>CBOT Kurulum Asistanı - Admin Paneli</h1>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        submit = st.form_submit_button("Giriş")
        
        if submit:
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Geçersiz kullanıcı adı veya şifre")

def save_configuration():
    # data dizini kontrolü
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Mevcut konfigürasyonları kaydet
    with open("data/configs.json", "w") as f:
        json.dump(st.session_state.saved_configs, f, indent=4)

def admin_dashboard():
    st.markdown("<h1 style='text-align: center;'>CBOT Kurulum Asistanı - Admin Paneli</h1>", unsafe_allow_html=True)
    
    # Sekmeler
    tab1, tab2, tab3 = st.tabs(["Kayıtlı Yapılandırmalar", "Kullanıcı Yönetimi", "Sistem Ayarları"])
    
    with tab1:
        st.subheader("Kayıtlı Kurulum Yapılandırmaları")
        
        if not st.session_state.saved_configs:
            st.info("Henüz kaydedilmiş yapılandırma bulunmamaktadır.")
        else:
            # Konfigürasyonları DataFrame'e dönüştür
            df_data = []
            for config in st.session_state.saved_configs:
                row = {
                    "Kurum": config.get("organization_name", ""),
                    "Proje Kodu": config.get("project_code", ""),
                    "Tarih": config.get("created_at", ""),
                    "Ortam": ", ".join(config.get("environment_type", [])),
                    "Modüller": ", ".join([m for m, v in config.get("modules", {}).items() if v]),
                    "Veritabanı": config.get("database", ""),
                }
                df_data.append(row)
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Seçili konfigürasyonu görüntüleme
            if st.session_state.saved_configs:
                selected_index = st.selectbox("Detayları görüntülemek için bir yapılandırma seçin:", 
                                            range(len(st.session_state.saved_configs)),
                                            format_func=lambda i: f"{st.session_state.saved_configs[i]['organization_name']} - {st.session_state.saved_configs[i]['created_at']}")
                
                selected_config = st.session_state.saved_configs[selected_index]
                with st.expander("Konfigürasyon Detayları", expanded=True):
                    st.json(selected_config)
                
                # Konfigürasyonu silme
                if st.button("Bu Yapılandırmayı Sil"):
                    st.session_state.saved_configs.pop(selected_index)
                    save_configuration()
                    st.success("Yapılandırma başarıyla silindi.")
                    st.rerun()
    
    with tab2:
        st.subheader("Kullanıcı Yönetimi")
        
        # Kullanıcı tablosu
        users_df = pd.DataFrame(
            [{"Kullanıcı Adı": username} for username in st.session_state.users.keys()]
        )
        st.dataframe(users_df, use_container_width=True)
        
        # Yeni kullanıcı ekleme
        with st.form("add_user_form"):
            st.subheader("Yeni Kullanıcı Ekle")
            new_username = st.text_input("Kullanıcı Adı")
            new_password = st.text_input("Şifre", type="password")
            add_user = st.form_submit_button("Kullanıcı Ekle")
            
            if add_user:
                if new_username and new_password:
                    if new_username in st.session_state.users:
                        st.error("Bu kullanıcı adı zaten mevcut")
                    else:
                        st.session_state.users[new_username] = new_password
                        st.success(f"Kullanıcı {new_username} başarıyla eklendi")
                        st.rerun()
                else:
                    st.error("Kullanıcı adı ve şifre gereklidir")
    
    with tab3:
        st.subheader("Sistem Ayarları")
        
        # Veritabanı bağlantı ayarları (örnek)
        st.write("Veritabanı Ayarları")
        db_host = st.text_input("Veritabanı Host", "localhost")
        db_port = st.text_input("Veritabanı Port", "27017")
        
        # Webhook URL ayarları
        st.write("Webhook URL Ayarları")
        webhook_url = st.text_input("Webhook URL", "https://aiflow.test.cbot.ai/webhook-test/cbot-setup-assistant/gereklilikler")
        
        if st.button("Ayarları Kaydet"):
            st.success("Sistem ayarları başarıyla güncellendi")

def admin_panel():
    initialize_admin_state()
    
    if not st.session_state.admin_logged_in:
        admin_login()
    else:
        admin_dashboard()
        
        # Çıkış butonu
        if st.sidebar.button("Çıkış Yap"):
            st.session_state.admin_logged_in = False
            st.rerun()

if __name__ == "__main__":
    admin_panel()