"""
CBOT Kurulum Asistanı - Chat Bot Modülü
"""

import requests
import json
import streamlit as st
from datetime import datetime

def init_chat_session():
    """Sohbet oturumunu başlatır"""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant", 
                "content": "Merhaba! CBOT kurulum asistanı olarak size nasıl yardımcı olabilirim? Modül ve servisler hakkında bilgi alabilir veya kurulum gereksinimleri hakkında sorular sorabilirsiniz."
            }
        ]
    
    if "chat_session_id" not in st.session_state:
        st.session_state.chat_session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"

def send_message_to_n8n(message, form_data=None):
    """N8n webhook'una mesaj gönderir ve yanıt alır"""
    try:
        # Webhook URL'nizi buraya girin
        webhook_url = "https://aiflow.test.cbot.ai/webhook-test/cbot-setup-assistant/gereklilikler"
        
        # İsteği hazırla
        payload = {
            "message": message,
            "userId": st.session_state.get("user_id", "anonymous"),
            "conversationId": st.session_state.chat_session_id,
        }
        
        # Eğer form verisi varsa, context olarak ekle
        if form_data:
            payload["context"] = {
                "modules": {k: v for k, v in form_data["modules"].items() if v},
                "services": {k: v for k, v in form_data["auxiliary_services"].items() if v},
                "database": form_data["database"],
                "environment_type": form_data["environment_type"],
                "use_ldap": form_data["use_ldap"],
                "deployment_type": form_data["deployment_type"]
            }
        
        # N8n webhook'una POST isteği gönder
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        # Yanıtı kontrol et
        if response.status_code == 200:
            # Webhook yanıtı bir dizi içinde nesne olarak geliyor, ilk öğeyi al
            response_data = response.json()
            
            # Yanıt dizi ise ve içinde veri varsa
            if isinstance(response_data, list) and len(response_data) > 0:
                # İlk öğeden output alanını çıkar
                if "output" in response_data[0]:
                    return response_data[0]["output"]
            
            # Eğer "response" anahtarı varsa, onu döndür
            elif isinstance(response_data, dict) and "response" in response_data:
                return response_data["response"]
                
            return "Bir hata oluştu, yanıt alınamadı."
        else:
            return f"Sunucu hatası: HTTP {response.status_code}"
    
    except requests.RequestException as e:
        return f"Bağlantı hatası: {str(e)}"
    except json.JSONDecodeError:
        return "Geçersiz yanıt formatı"
    except Exception as e:
        return f"Beklenmeyen hata: {str(e)}"

def render_chat_interface(form_data=None):
    """Chat arayüzünü oluşturur"""
    # Sohbet oturumunu başlat
    init_chat_session()
    
    st.markdown('<div class="step-title">CBOT Kurulum Öneri Asistanı</div>', unsafe_allow_html=True)
    
    # Kısa açıklama
    st.markdown("""
        Bu asistan, CBOT kurulum gereksinimleri hakkında sorularınızı yanıtlamak için yapay zeka 
        teknolojilerini kullanır. Modül ve servisler hakkında bilgi alabilir, sistem gereksinimleri 
        hakkında sorular sorabilirsiniz.
    """)
    
    # Mevcut form seçimleri hakkında bilgi ver
    if form_data and any(form_data["modules"].values()):
        selected_modules = [m.capitalize() for m, v in form_data["modules"].items() if v]
        if selected_modules:
            st.markdown(f"**Seçilen modüller:** {', '.join(selected_modules)}")
        
        selected_services = [s.capitalize() for s, v in form_data["auxiliary_services"].items() if v]
        if selected_services:
            st.markdown(f"**Seçilen yardımcı servisler:** {', '.join(selected_services)}")
        
        st.markdown(f"**Veritabanı:** {form_data['database'].upper()}")
        st.markdown(f"**Ortam:** {', '.join([e.capitalize() for e in form_data['environment_type']])}")
    
    # Konuşma geçmişini göster
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Kullanıcı girişi
    user_input = st.chat_input("Kurulum gereksinimleri hakkında bir soru sorun...")
    
    if user_input:
        # Kullanıcı mesajını göster
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Mesajı kaydet
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        # N8n'e gönder ve yanıt al
        with st.spinner("Yanıt üretiliyor..."):
            bot_response = send_message_to_n8n(user_input, form_data)
        
        # Asistan yanıtını göster
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        
        # Yanıtı kaydet
        st.session_state.chat_messages.append({"role": "assistant", "content": bot_response})