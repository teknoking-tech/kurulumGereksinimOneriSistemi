"""
CBOT Kurulum Asistanı - Ana Uygulama
"""

import streamlit as st
import base64
import os
from datetime import datetime

# Uygulama modülleri
from config import DEFAULT_FORM_VALUES, STYLES, calculate_requirements
from utils import (
    get_environment_label, get_deployment_label, get_service_label,
    calculate_total_hardware, format_file_name, get_binary_file_downloader_html,
    streamlit_header, streamlit_footer
)
from document_generator import generate_document, generate_markdown_content

# Uygulama modülleri
from config import DEFAULT_FORM_VALUES, STYLES, calculate_requirements
from utils import (
    get_environment_label, get_deployment_label, get_service_label,
    calculate_total_hardware, format_file_name, get_binary_file_downloader_html,
    streamlit_header, streamlit_footer
)
from document_generator import generate_document, generate_markdown_content
from chat_bot import render_chat_interface  # Yeni eklenen satır

# Cache mekanizmasını kullanarak, performansı iyileştirme
@st.cache_data(ttl=600)
def get_cached_requirements(form_data_str):
    """Form verilerine göre önbelleğe alınmış gereksinimleri döndürür"""
    import json
    form_data = json.loads(form_data_str)
    return calculate_requirements(form_data)

# Streamlit sayfa yapılandırması
st.set_page_config(
    page_title="CBOT Kurulum Asistanı",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Uygulama CSS stilleri
st.markdown(
    """
    <style>
    .main {
        padding: 0 !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .download-button {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        background-color: #1E40AF;
        color: white !important;
        text-decoration: none;
        border-radius: 0.375rem;
        text-align: center;
        transition: all 0.3s;
        font-weight: 500;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    .download-button:hover {
        background-color: #1E3A8A;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .dashboard-card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        transition: all 0.3s;
    }
    .dashboard-card:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
    }
    .stat-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
    }
    .stat-card {
        flex: 1;
        padding: 0.75rem;
        border-radius: 0.375rem;
        text-align: center;
        transition: all 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
    }
    .stat-value {
        font-weight: bold;
        font-size: 1.5rem;
    }
    .stat-label {
        font-size: 0.875rem;
        color: #6B7280;
    }
    .step-container {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s;
    }
    .step-title {
        font-size: 1.25rem;
        font-weight: 600;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem;
        color: #1E40AF;
    }
    .progress-container {
        background-color: rgba(243, 244, 246, 0.8);
        border-radius: 0.5rem;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .progress-step {
        position: relative;
        z-index: 1;
    }
    .progress-step-active {
        color: #1E40AF;
        font-weight: 600;
    }
    .progress-step-inactive {
        color: #6B7280;
    }
    .form-label {
        font-weight: 500;
        margin-bottom: 0.25rem;
        color: #374151;
    }
     /* Chat bot stilleri */
    .stChatMessage {
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-bottom: 0.75rem;
    }
    .stChatMessage[data-testid="stChatMessage-USER"] {
        background-color: rgba(243, 244, 246, 0.8);
    }
    .stChatMessage[data-testid="stChatMessage-ASSISTANT"] {
        background-color: rgba(236, 253, 245, 0.8);
    }
    .stChatInputContainer {
        padding-top: 0.5rem;
        border-top: 1px solid #E5E7EB;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Uygulama başlığı
streamlit_header()

# Oturum durumunu başlat
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

if 'form_data' not in st.session_state:
    st.session_state.form_data = DEFAULT_FORM_VALUES.copy()

if 'requirements' not in st.session_state:
    st.session_state.requirements = {
        "hardware": {},
        "database": {},
        "network": {"dns_records": []},
        "docker": {},
        "ldap": {},
        "additional_requirements": []
    }

if 'document_ready' not in st.session_state:
    st.session_state.document_ready = False

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "hardware"

# Chat bot için eklenen değişken
if 'show_chatbot' not in st.session_state:
    st.session_state.show_chatbot = False

# Chat bot kontrolü
def toggle_chatbot():
    st.session_state.show_chatbot = not st.session_state.show_chatbot

# Formun herhangi bir kısmı değiştiğinde gereksinimleri yeniden hesapla
def update_requirements():
    import json
    # Form verilerini JSON'a dönüştürerek önbelleğe alınmış hesaplamaları kullanabiliyoruz
    form_data_str = json.dumps(st.session_state.form_data)
    st.session_state.requirements = get_cached_requirements(form_data_str)

# Form değişikliği işleyicileri
def handle_environment_change(value):
    env_type = st.session_state.form_data["environment_type"]
    
    # Eğer değer zaten varsa kaldır, yoksa ekle (çoklu seçim)
    if value in env_type:
        env_type.remove(value)
    else:
        env_type.append(value)
    
    # En az bir ortam tipi seçili olmalı
    if not env_type:
        env_type.append("test")  # Varsayılan olarak test'i seç
    
    update_requirements()

def handle_module_change(module_name, value):
    st.session_state.form_data["modules"][module_name] = value
    update_requirements()

def handle_service_change(service_name, value):
    st.session_state.form_data["auxiliary_services"][service_name] = value
    update_requirements()

def handle_database_change(value):
    st.session_state.form_data["database"] = value
    update_requirements()

def handle_ldap_change(value):
    st.session_state.form_data["use_ldap"] = value
    update_requirements()

def handle_deployment_change(value):
    st.session_state.form_data["deployment_type"] = value
    update_requirements()

def handle_text_input(field, value):
    st.session_state.form_data[field] = value

# Adım kontrolü
def go_to_next_step():
    st.session_state.current_step += 1
    st.rerun()  # Sayfayı yeniden yükler

def go_to_previous_step():
    st.session_state.current_step -= 1
    st.rerun()  # Sayfayı yeniden yükler

def set_active_tab(tab):
    st.session_state.active_tab = tab

# Belge oluşturma
def create_download_document(format_type):
    with st.spinner(f"{format_type.upper()} dosyası oluşturuluyor..."):
        file_path = generate_document(
            st.session_state.form_data,
            st.session_state.requirements,
            format_type
        )
        
        # Dosya adını biçimlendir
        file_name = format_file_name(
            st.session_state.form_data["organization_name"],
            format_type
        )
        
        # İndirme bağlantısını döndür
        file_stats = os.stat(file_path)
        st.session_state.document_ready = True
        
        # Dosya içeriğini base64 kodla
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
            # MIME tipini ayarla
            mime_type = f"application/{format_type}"
            if format_type == "word":
                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif format_type == "markdown":
                mime_type = "text/markdown"
            
            # İndirme bağlantısı
            href = f'<a href="data:{mime_type};base64,{b64}" download="{file_name}" class="download-button">{format_type.upper()} Dosyasını İndir</a>'
            st.markdown(href, unsafe_allow_html=True)

# Adım içeriği oluşturma
def render_step_one():
    st.markdown('<div class="step-title">1. Proje Bilgileri</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Session state değişkenlerini başlatma
        if "org_name_input" not in st.session_state:
            st.session_state.org_name_input = st.session_state.form_data["organization_name"]
        
        organization_name = st.text_input(
            "Kurum/Şirket Adı",
            value=st.session_state.form_data["organization_name"],
            key="org_name_input"
        )
        st.session_state.form_data["organization_name"] = organization_name
        
        # Session state değişkenlerini başlatma
        if "project_code_input" not in st.session_state:
            st.session_state.project_code_input = st.session_state.form_data["project_code"]
        
        project_code = st.text_input(
            "Proje Kodu",
            value=st.session_state.form_data["project_code"],
            key="project_code_input"
        )
        st.session_state.form_data["project_code"] = project_code
    
    with col2:
        # Session state değişkenlerini başlatma
        if "contact_email_input" not in st.session_state:
            st.session_state.contact_email_input = st.session_state.form_data["contact_email"]
        
        contact_email = st.text_input(
            "İletişim E-posta",
            value=st.session_state.form_data["contact_email"],
            key="contact_email_input"
        )
        st.session_state.form_data["contact_email"] = contact_email
    
    st.markdown("#### Ortam Tipi")
    col1, col2 = st.columns(2)
    
    with col1:
        test_env = st.checkbox(
            "Test Ortamı",
            value="test" in st.session_state.form_data["environment_type"],
            key="test_env",
            on_change=handle_environment_change,
            args=("test",)
        )
    
    with col2:
        live_env = st.checkbox(
            "Canlı Ortam",
            value="live" in st.session_state.form_data["environment_type"],
            key="live_env",
            on_change=handle_environment_change,
            args=("live",)
        )
    
    st.markdown("#### Deployment Tipi")
    col1, col2 = st.columns(2)
    
    with col1:
        if "deployment_type" not in st.session_state:
            st.session_state.deployment_type = st.session_state.form_data["deployment_type"]
            
        deployment_type = st.radio(
            "Deployment Tipi",
            options=["on-prem", "cloud"],
            format_func=get_deployment_label,
            index=0 if st.session_state.form_data["deployment_type"] == "on-prem" else 1,
            key="deployment_type"
        )
        st.session_state.form_data["deployment_type"] = deployment_type

def render_step_two():
    st.markdown('<div class="step-title">2. Modül ve Servis Seçimi</div>', unsafe_allow_html=True)
    
    # Ana modüller
    st.markdown("### Ana Modüller")
    col1, col2 = st.columns(2)
    
    modules = list(st.session_state.form_data["modules"].items())
    half_len = len(modules) // 2 + (len(modules) % 2)
    
    # İlk yarısı birinci kolonda
    with col1:
        for module_name, is_selected in modules[:half_len]:
            module_key = f"module_{module_name}"
            if module_key not in st.session_state:
                st.session_state[module_key] = is_selected
                
            selected = st.checkbox(
                module_name.capitalize(),
                value=is_selected,
                key=module_key
            )
            st.session_state.form_data["modules"][module_name] = selected
    
    # İkinci yarısı ikinci kolonda
    with col2:
        for module_name, is_selected in modules[half_len:]:
            module_key = f"module_{module_name}"
            if module_key not in st.session_state:
                st.session_state[module_key] = is_selected
                
            selected = st.checkbox(
                module_name.capitalize(),
                value=is_selected,
                key=module_key
            )
            st.session_state.form_data["modules"][module_name] = selected
    
    # Yardımcı servisler
    st.markdown("### Yardımcı Servisler")
    col1, col2 = st.columns(2)
    
    services = list(st.session_state.form_data["auxiliary_services"].items())
    half_len = len(services) // 2 + (len(services) % 2)
    
    # İlk yarısı birinci kolonda
    with col1:
        for service_name, is_selected in services[:half_len]:
            service_key = f"service_{service_name}"
            if service_key not in st.session_state:
                st.session_state[service_key] = is_selected
                
            selected = st.checkbox(
                get_service_label(service_name),
                value=is_selected,
                key=service_key
            )
            st.session_state.form_data["auxiliary_services"][service_name] = selected
    
    # İkinci yarısı ikinci kolonda
    with col2:
        for service_name, is_selected in services[half_len:]:
            service_key = f"service_{service_name}"
            if service_key not in st.session_state:
                st.session_state[service_key] = is_selected
                
            selected = st.checkbox(
                get_service_label(service_name),
                value=is_selected,
                key=service_key
            )
            st.session_state.form_data["auxiliary_services"][service_name] = selected
    
    # Veritabanı ve LDAP
    st.markdown("### Veritabanı ve Ek Seçenekler")
    col1, col2 = st.columns(2)
    
    with col1:
        if "database_selection" not in st.session_state:
            st.session_state.database_selection = st.session_state.form_data["database"]
            
        database = st.radio(
            "Veritabanı Seçimi",
            options=["mongodb", "mssql", "postgresql"],
            format_func=lambda x: {
                "mongodb": "MongoDB",
                "mssql": "Microsoft SQL Server",
                "postgresql": "PostgreSQL"
            }.get(x, x),
            index=["mongodb", "mssql", "postgresql"].index(st.session_state.form_data["database"]),
            key="database_selection"
        )
        st.session_state.form_data["database"] = database
    
    with col2:
        if "use_ldap" not in st.session_state:
            st.session_state.use_ldap = st.session_state.form_data["use_ldap"]
            
        use_ldap = st.checkbox(
            "LDAP Kullan",
            value=st.session_state.form_data["use_ldap"],
            help="Kullanıcı kimlik doğrulaması için LDAP entegrasyonu",
            key="use_ldap"
        )
        st.session_state.form_data["use_ldap"] = use_ldap
    
    # Her değişiklikten sonra gereksinimleri güncelle
    update_requirements()

def render_step_three():
    st.markdown('<div class="step-title">3. Gereksinimler ve Onay</div>', unsafe_allow_html=True)
    
    # Sekme menüsü
    tabs = st.tabs(["Donanım", "Veritabanı", "Network", "Diğer"])
    
    # Sekmeleri oluştur
    with tabs[0]:  # Donanım sekmesi
        render_hardware_tab()
    
    with tabs[1]:  # Veritabanı sekmesi
        render_database_tab()
    
    with tabs[2]:  # Network sekmesi
        render_network_tab()
    
    with tabs[3]:  # Diğer sekmesi
        render_other_tab()

def render_hardware_tab():
    st.markdown("### Toplam Donanım Gereksinimleri")
    
    # Toplam donanım gereksinimlerini hesapla
    total_hardware = calculate_total_hardware(st.session_state.requirements, st.session_state.form_data)
    
    # Ortam tiplerine göre toplam gereksinimleri göster
    cols = st.columns(len(st.session_state.form_data["environment_type"]))
    
    for i, env_type in enumerate(st.session_state.form_data["environment_type"]):
        with cols[i]:
            st.markdown(f"#### {get_environment_label(env_type)} Ortamı")
            
            # Donanım istatistiklerini göster
            st.markdown(
                f"""
                <div class="stat-container">
                    <div class="stat-card" style="background-color: #EFF6FF;">
                        <div class="stat-value" style="color: #1E40AF;">{total_hardware[env_type]["cpu"]}</div>
                        <div class="stat-label">Core CPU</div>
                    </div>
                    <div class="stat-card" style="background-color: #ECFDF5;">
                        <div class="stat-value" style="color: #047857;">{total_hardware[env_type]["ram"]}</div>
                        <div class="stat-label">GB RAM</div>
                    </div>
                    <div class="stat-card" style="background-color: #FFFBEB;">
                        <div class="stat-value" style="color: #B45309;">{total_hardware[env_type]["disk"]}</div>
                        <div class="stat-label">GB Disk</div>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    st.markdown("### Modül Bazlı Gereksinimler")
    
    # Her modül için gereksinimleri göster
    for module, env_reqs in st.session_state.requirements["hardware"].items():
        with st.expander(f"{module.capitalize()} Modülü"):
            cols = st.columns(len(st.session_state.form_data["environment_type"]))
            
            for i, env_type in enumerate(st.session_state.form_data["environment_type"]):
                if env_type in env_reqs:
                    with cols[i]:
                        st.markdown(f"**{get_environment_label(env_type)} Ortamı**")
                        st.markdown(f"- CPU: {env_reqs[env_type]['cpu']}")
                        st.markdown(f"- RAM: {env_reqs[env_type]['ram']}")
                        st.markdown(f"- Disk: {env_reqs[env_type]['disk']}")
    
    st.markdown("**İşletim Sistemi:** CentOS 7/8 veya RHEL")
    st.markdown("**Not:** Gerçek donanım gereksinimleri yük durumuna göre değişebilir.")

def render_database_tab():
    st.markdown("### Veritabanı Gereksinimleri")
    
    if "database" in st.session_state.requirements and st.session_state.requirements["database"]:
        db_req = st.session_state.requirements["database"]
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Tip:** {db_req.get('type', 'Belirtilmemiş')}")
            st.markdown(f"**Port:** {db_req.get('port', 'Belirtilmemiş')}")
            st.markdown(f"**Kullanıcı Yetkisi:** {db_req.get('permissions', 'Belirtilmemiş')}")
        
        with col2:
            if db_req.get('collation') and db_req['collation'] != 'N/A':
                st.markdown(f"**Collation:** {db_req['collation']}")
            
            st.markdown("Veritabanı sunucusunun tüm modüllerden erişilebilir olması gerekmektedir.")
    else:
        st.warning("Veritabanı gereksinimleri hesaplanıyor...")
    
    st.markdown("### Veritabanı Bağımlılıkları")
    
    # Veritabanı uyumluluğu kontrolleri
    st.markdown("- ✅ Core ve Panel modülleri tüm veritabanlarıyla uyumludur.")
    st.markdown("- ✅ AI Flow modülü PostgreSQL ile en iyi performansı gösterir.")
    
    # Classifier modülü uyarısı
    if st.session_state.form_data["modules"]["classifier"]:
        if st.session_state.form_data["database"] != "mssql":
            st.warning("⚠️ Classifier modülü yalnızca MSSQL ile çalışır!")
        else:
            st.markdown("- ✅ Classifier modülü için MSSQL seçilmiş, uyumlu.")

def render_network_tab():
    st.markdown("### DNS Kayıtları")
    
    if ("network" in st.session_state.requirements and 
        "dns_records" in st.session_state.requirements["network"] and 
        st.session_state.requirements["network"]["dns_records"]):
        
        dns_records = st.session_state.requirements["network"]["dns_records"]
        
        # Tablo başlıkları
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown("**DNS Kaydı**")
        with col2:
            st.markdown("**Port**")
        with col3:
            st.markdown("**Not**")
        
        # DNS kayıtları
        for record in dns_records:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.markdown(f"`{record['name']}`")
            with col2:
                st.markdown(f"{record['port']}")
            with col3:
                st.markdown(f"{record.get('note', '-')}")
    else:
        st.info("DNS kayıtları hesaplanıyor veya seçilen modüller için DNS kaydı gerekmemektedir.")
    
    st.markdown("### Firewall / Ağ Gereksinimleri")
    
    st.markdown("- ✅ Sunucular **internet erişimli** olmalıdır.")
    st.markdown("- ✅ Docker imajlarının çekilebilmesi için **registry.cbot.ai** adresine 443 portundan erişim sağlanmalıdır.")
    
    db_port = st.session_state.requirements.get("database", {}).get("port", "?")
    st.markdown(f"- ✅ Veritabanı portu (**{db_port}**) tüm modüllerden erişilebilir olmalıdır.")
    st.markdown("- ✅ Load Balancer kullanılıyorsa, **5000 portunda WebSocket desteği** sağlanmalıdır.")

def render_other_tab():
    # LDAP gereksinimleri
    if st.session_state.form_data["use_ldap"] and "ldap" in st.session_state.requirements and st.session_state.requirements["ldap"]:
        st.markdown("### LDAP Gereksinimleri")
        ldap_req = st.session_state.requirements["ldap"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Gerekli Alanlar:**")
            for field in ldap_req.get("fields", []):
                st.markdown(f"- {field}")
        
        with col2:
            st.markdown("**Alan Eşleştirmeleri:**")
            for field in ldap_req.get("mapping", []):
                st.markdown(f"- {field}")
            
            st.markdown(f"*{ldap_req.get('note', '')}*")
    
    # Ek gereksinimler ve uyarılar
    st.markdown("### Ek Gereksinimler ve Uyarılar")
    
    if ("additional_requirements" in st.session_state.requirements and 
        st.session_state.requirements["additional_requirements"]):
        
        for req in st.session_state.requirements["additional_requirements"]:
            if "DİKKAT" in req:
                st.warning(f"⚠️ {req}")
            else:
                st.markdown(f"- ✅ {req}")
    else:
        st.info("Seçilen modül ve servisler için ek gereksinim bulunmamaktadır.")

def render_step_four():
    st.markdown('<div class="step-title">4. Gereksinim Dokümanı</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        ### Kurulum Gereksinimleri Dokümanı
        
        Seçimlerinize göre hazırlanan kurulum gereksinimleri dokümanı oluşturuldu. 
        Dokümanı PDF, Word veya Markdown formatında indirebilirsiniz.
        """
    )
    
    # İndirme butonları
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("PDF İndir"):
            create_download_document("pdf")
    
    with col2:
        if st.button("Word İndir"):
            create_download_document("word")
    
    with col3:
        if st.button("Markdown İndir"):
            create_download_document("markdown")
    
    # Özet bilgiler
    st.markdown("### Özet Bilgiler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Kurum/Şirket:** {st.session_state.form_data['organization_name'] or '-'}")
        st.markdown(f"**Proje Kodu:** {st.session_state.form_data['project_code'] or '-'}")
        st.markdown(f"**Ortam Tipi:** {', '.join([get_environment_label(e) for e in st.session_state.form_data['environment_type']])}")
        st.markdown(f"**Deployment Tipi:** {get_deployment_label(st.session_state.form_data['deployment_type'])}")
    
    with col2:
        selected_modules = [m.capitalize() for m, selected in st.session_state.form_data["modules"].items() if selected]
        st.markdown(f"**Seçilen Modüller:** {', '.join(selected_modules) or '-'}")
        st.markdown(f"**Veritabanı:** {st.session_state.form_data['database']}")
        st.markdown(f"**LDAP Entegrasyonu:** {'Evet' if st.session_state.form_data['use_ldap'] else 'Hayır'}")
    
    if st.session_state.document_ready:
        st.success("✅ Doküman başarıyla oluşturuldu ve indirme başlatıldı.")

# Ana uygulama akışı
def main():
    # Uygulamayı başlat
    # İlerleme çubuğu
    progress_text = f"Adım {st.session_state.current_step} / 4"
    steps = ["Proje Bilgileri", "Modül ve Servis Seçimi", "Gereksinimler ve Onay", "Doküman"]
    
    # Chat bot butonu sidebar'a ekleyin
    with st.sidebar:
        st.markdown("### Yardım ve Destek")
        if st.button("🤖 Kurulum Asistanı ile Konuşun", on_click=toggle_chatbot):
            pass
        
        if st.session_state.show_chatbot:
            st.success("Kurulum Asistanı etkin")
        else:
            st.info("Yardıma ihtiyacınız olursa, kurulum asistanını etkinleştirin")
    
    # Chat bot açıksa göster
    if st.session_state.show_chatbot:
        with st.expander("CBOT Kurulum Asistanı", expanded=True):
            render_chat_interface(st.session_state.form_data)
    
    st.markdown(
        f"""
        <div style="
            background-color: rgba(230, 230, 230, 0.2);
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <div>
                <span style="color: #6B7280; font-size: 0.875rem;">{progress_text}</span>
            </div>
            <div style="display: flex; align-items: center;">
                {' '.join([
                    f'<div style="height: 0.5rem; width: 0.5rem; border-radius: 9999px; margin: 0 0.125rem; background-color: {"#1E40AF" if i+1 <= st.session_state.current_step else "#D1D5DB"};"></div>'
                    + (f'<div style="height: 0.125rem; width: 1rem; background-color: {"#1E40AF" if i+2 <= st.session_state.current_step else "#D1D5DB"};"></div>' if i < 3 else "")
                    for i in range(4)
                ])}
            </div>
            <div>
                <span style="color: #1F2937; font-size: 0.875rem; font-weight: 500;">{steps[st.session_state.current_step-1]}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # İçerik konteynerı ve geri kalan kod aynı kalıyor...
    
    # İçerik konteynerı
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    
    # Geçerli adımı render et
    if st.session_state.current_step == 1:
        render_step_one()
    elif st.session_state.current_step == 2:
        render_step_two()
    elif st.session_state.current_step == 3:
        render_step_three()
    elif st.session_state.current_step == 4:
        render_step_four()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Gezinme butonları
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_step > 1:
            if st.button("Geri"):
                go_to_previous_step()
    
    with col3:
        if st.session_state.current_step < 4:
            next_text = "İleri"
            if st.session_state.current_step == 3:
                next_text = "Doküman Oluştur"
            
            if st.button(next_text):
                go_to_next_step()
    
    # Footer
    streamlit_footer()

if __name__ == "__main__":
    main()