# CBOT Kurulum Asistanı

CBOT Kurulum Asistanı, modül seçimi yaparak kurulum gereksinimleri belgesi oluşturmayı sağlayan bir Streamlit uygulamasıdır. Bu uygulama, React tabanlı bir web uygulamasının Python ve Streamlit kullanılarak yeniden tasarlanmış halidir.

![CBOT Kurulum Asistanı](https://i.imgur.com/mj5Pnbb.png)

## Özellikler

- Proje bilgilerini kaydetme
- Modül ve servis seçimi
- Donanım gereksinimlerini otomatik hesaplama
- Veritabanı, ağ ve LDAP gereksinimlerini belirleme
- PDF, Word ve Markdown formatlarında kurulum belgesi oluşturma

## Kurulum

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/kullanici/cbot-kurulum-asistani.git
   cd cbot-kurulum-asistani
   ```

2. Sanal ortam oluşturun ve etkinleştirin (isteğe bağlı ama önerilir):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Çalıştırma

Uygulamayı başlatmak için:

```bash
streamlit run app.py
```

Uygulama varsayılan olarak http://localhost:8501 adresinde çalışacaktır.

## Proje Yapısı

```
cbot-kurulum-asistani/
│
├── app.py                  # Ana uygulama kodu
├── config.py               # Yapılandırma ve varsayılan değerler
├── utils.py                # Yardımcı fonksiyonlar
├── document_generator.py   # Belge oluşturma işlevleri
├── requirements.txt        # Gerekli Python paketleri
└── README.md               # Bu dosya
```

## Kullanım Senaryoları

1. **Proje Bilgileri**: Kurum adı, proje kodu, iletişim e-postası, ortam tipi ve deployment tipini ayarlayın.
2. **Modül ve Servis Seçimi**: Kurulumda kullanılacak ana modülleri, yardımcı servisleri ve veritabanını seçin.
3. **Gereksinimler ve Onay**: Hesaplanan donanım, veritabanı, network ve diğer gereksinimleri inceleyin.
4. **Belge Oluşturma**: Seçimlerinize göre kurulum gereksinimleri belgesini indirin.

## Teknolojiler

- Python 3.7+
- Streamlit
- FPDF2 (PDF oluşturma)
- python-docx (Word belgesi oluşturma)
- Markdown (Markdown belgeleri)

## Katkıda Bulunma

1. Bu repoyu fork edin
2. Kendi branch'inizi oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik: Açıklama'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Bir Pull Request açın

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.