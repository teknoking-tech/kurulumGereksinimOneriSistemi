"""
CBOT Kurulum Asistanı - Yapılandırma Dosyası
"""

# Varsayılan form değerleri
DEFAULT_FORM_VALUES = {
    "environment_type": ["test"],
    "modules": {
        "core": True,
        "panel": True,
        "livechat": False,
        "fusion": False,
        "classifier": False,
        "aiflow": False,
        "analytics": False
    },
    "auxiliary_services": {
        "ocr": False,
        "masking": False,
        "file_to_markdown": False,
        "crawler": False,
        "hf_model_hosting": False
    },
    "database": "mongodb",
    "use_ldap": False,
    "deployment_type": "on-prem",
    "organization_name": "",
    "project_code": "",
    "contact_email": ""
}

# Görsel ayarlar ve stiller
STYLES = {
    "PRIMARY_COLOR": "#1E40AF",  # Blue-700
    "SECONDARY_COLOR": "#172554",  # Blue-900
    "GRADIENT": "linear-gradient(90deg, #1E40AF, #172554)",
    "PRIMARY_TEXT_COLOR": "#FFFFFF",  # White
    "SECONDARY_TEXT_COLOR": "#1F2937",  # Gray-800
    "PADDING": "1.5rem",
    "BORDER_RADIUS": "0.5rem"
}

# Simüle edilmiş gereksinim hesaplama mantığı
# Gerçek uygulamada bu bir API çağrısı olabilir
def calculate_requirements(form_data):
    """Form verilerine dayanarak gereksinimleri hesaplayın"""
    
    calculated_reqs = {
        "hardware": {},
        "database": {},
        "network": {
            "dns_records": []
        },
        "docker": {
            "registry": "registry.cbot.ai",
            "port_requirement": "443 portu açık olmalı"
        },
        "ldap": {},
        "additional_requirements": []
    }
    
    # Ana modüller için donanım gereksinimleri hesaplanıyor
    if form_data["modules"]["core"]:
        calculated_reqs["hardware"]["core"] = {
            "test": {"cpu": "4 core", "ram": "16 GB", "disk": "100 GB"},
            "live": {"cpu": "8 core", "ram": "32 GB", "disk": "200 GB"}
        }
        
        calculated_reqs["network"]["dns_records"].extend([
            {"name": "cbot-core", "port": 5351},
            {"name": "cbot-socket", "port": 5000, "note": "WebSocket desteği gerekli"}
        ])
        
        if "test" in form_data["environment_type"]:
            calculated_reqs["network"]["dns_records"].extend([
                {"name": "cbot-core-test", "port": 5351},
                {"name": "cbot-socket-test", "port": 5000, "note": "WebSocket desteği gerekli"}
            ])
    
    if form_data["modules"]["panel"]:
        calculated_reqs["hardware"]["panel"] = {
            "test": {"cpu": "2 core", "ram": "8 GB", "disk": "50 GB"},
            "live": {"cpu": "4 core", "ram": "16 GB", "disk": "100 GB"}
        }
        
        calculated_reqs["network"]["dns_records"].append(
            {"name": "cbot-panel", "port": 3000}
        )
        
        if "test" in form_data["environment_type"]:
            calculated_reqs["network"]["dns_records"].append(
                {"name": "cbot-panel-test", "port": 3000}
            )
    
    if form_data["modules"]["livechat"]:
        calculated_reqs["hardware"]["livechat"] = {
            "test": {"cpu": "2 core", "ram": "8 GB", "disk": "50 GB"},
            "live": {"cpu": "4 core", "ram": "16 GB", "disk": "100 GB"}
        }
    
    if form_data["modules"]["fusion"]:
        calculated_reqs["hardware"]["fusion"] = {
            "test": {"cpu": "4 core", "ram": "16 GB", "disk": "100 GB"},
            "live": {"cpu": "8 core", "ram": "32 GB", "disk": "200 GB"}
        }
        
        calculated_reqs["network"]["dns_records"].append(
            {"name": "cbot-fusion", "port": 9600}
        )
        
        if "test" in form_data["environment_type"]:
            calculated_reqs["network"]["dns_records"].append(
                {"name": "cbot-fusion-test", "port": 9600}
            )
    
    if form_data["modules"]["classifier"]:
        calculated_reqs["hardware"]["classifier"] = {
            "test": {"cpu": "8 core", "ram": "32 GB", "disk": "100 GB"},
            "live": {"cpu": "16 core", "ram": "64 GB", "disk": "500 GB"}
        }
        
        calculated_reqs["additional_requirements"].append(
            "Classifier modülü MSSQL ile çalışmaktadır."
        )
        
        if form_data["database"] != "mssql":
            calculated_reqs["additional_requirements"].append(
                "DİKKAT: Classifier modülü için MSSQL gereklidir!"
            )
    
    if form_data["modules"]["aiflow"]:
        calculated_reqs["hardware"]["aiflow"] = {
            "test": {"cpu": "10 core", "ram": "8 GB", "disk": "150 GB"},
            "live": {"cpu": "16 core", "ram": "32 GB", "disk": "300 GB"}
        }
        
        if form_data["database"] == "postgresql":
            calculated_reqs["additional_requirements"].append(
                "AI Flow için ek olarak 4 GB disk alanı (PostgreSQL) gereklidir."
            )
    
    # Veritabanı gereksinimleri
    if form_data["database"] == "mongodb":
        calculated_reqs["database"] = {
            "type": "MongoDB",
            "port": "27017",
            "collation": "N/A",
            "permissions": "OWNER yetkili kullanıcı"
        }
    elif form_data["database"] == "mssql":
        calculated_reqs["database"] = {
            "type": "Microsoft SQL Server",
            "port": "1433",
            "collation": "SQL_Latin1_General_CP1_CI_AS",
            "permissions": "OWNER yetkili kullanıcı"
        }
    elif form_data["database"] == "postgresql":
        calculated_reqs["database"] = {
            "type": "PostgreSQL",
            "port": "5432",
            "collation": "N/A",
            "permissions": "OWNER yetkili kullanıcı"
        }
    
    # LDAP gereksinimleri
    if form_data["use_ldap"]:
        calculated_reqs["ldap"] = {
            "fields": ["LDAP_URL", "BIND_DN", "SEARCH_BASE", "SEARCH_FILTER"],
            "mapping": ["Email", "Role", "Name"],
            "note": "Rollerin panelde LDAP ile birebir eşleşmesi gerekir"
        }
    
    # HF Model Hosting için GPU gereksinimleri
    if form_data["auxiliary_services"]["hf_model_hosting"]:
        calculated_reqs["additional_requirements"].append(
            "HF Model Hosting için GPU destekli sunucu gereklidir (min. 8GB VRAM)"
        )
    
    return calculated_reqs