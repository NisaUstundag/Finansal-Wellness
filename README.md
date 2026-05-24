# Yapay Zeka Destekli Finansal Wellness Asistanı 🚀

> Bireylerin finansal okuryazarlığını artırmak, bütçe yönetimini kolaylaştırmak ve kişisel tasarruf stratejileri oluşturmalarına yardımcı olmak amacıyla geliştirilmiş, Üretken Yapay Zeka (Generative AI) tabanlı kişisel danışmanlık platformudur.

## Proje Hakkında

Finansal Wellness Asistanı, yalnızca önceden belirlenmiş metin tabanlı yanıtlar üreten klasik sohbet botlarının ötesine geçerek; doğal dil işleme (NLP), Büyük Dil Modelleri (LLM) ve sesten metne (Voice-to-Text) teknolojilerini entegre eden hibrit bir mimari üzerine inşa edilmiştir. Kullanıcıdan gelen sesli veya metinsel girdileri anlık olarak analiz eder, Türkçenin semantik yapısına hakim özel prompt mühendisliği teknikleriyle işler ve Google Gemini LLM altyapısı üzerinden kişiselleştirilmiş finansal tavsiyeler üretir.

## Temel Özellikler

* **Sesli Komut Entegrasyonu (Voice-to-Text):** Web Speech API kullanılarak kullanıcıların doğal konuşma diliyle asistanla iletişim kurması sağlanır.
* **Akıllı Yönlendirme ve Niyet Analizi:** Kullanıcının girdisinden niyet analizi (intent recognition) yapılarak JSON formatında yapılandırılmış raporlar, akıllı başlıklar ve eylem butonları üretilir.
* **Vektör Tabanlı Bellek (RAG & Semantic Cache):** Kullanıcının geçmiş sohbetleri ve finansal profili kalıcı olarak hafızada tutulur, yapay zeka her yeni diyalogda bağlamı korur.
* **Çok Katmanlı Güvenlik (JWT & SMTP OTP):** Sisteme erişim JSON Web Token (JWT) ile şifrelenir. Yeni kayıtlarda SMTP üzerinden asenkron Tek Kullanımlık Şifre (OTP) doğrulaması zorunlu tutulur.
* **İstemci Taraflı Görsel Sıkıştırma:** Profil fotoğrafları HTML5 Canvas API ile istemci (client) tarafında sıkıştırılıp Base64 formatında sunucuya iletilerek bant genişliği optimize edilir.

## Kullanılan Teknolojiler

| Katman | Teknoloji / Araç | Açıklama |
| :--- | :--- | :--- |
| **Önyüz (Frontend)** | React.js, Material-UI (MUI) | Component tabanlı, dinamik ve tam duyarlı (responsive) kullanıcı arayüzü. |
| **Arkayüz (Backend)** | Python, FastAPI | Asenkron, yüksek performanslı ve düşük gecikmeli sunucu mimarisi. |
| **Veritabanı** | PostgreSQL, SQLAlchemy | İlişkisel veri modellemesi ve ORM tabanlı güvenli veri yönetimi. |
| **Yapay Zeka (AI)** | Google Gemini API | Büyük Dil Modeli (LLM) tabanlı niyet analizi ve içerik üretimi. |
| **Güvenlik** | JWT, Bcrypt, SMTP | Şifre hashleme, oturum yönetimi ve asenkron e-posta doğrulaması. |

## Sistem Mimarisi

Proje, asenkron iletişim prensiplerine dayalı bir İstemci-Sunucu (Client-Server) modeline sahiptir:
1. **İstemci Katmanı:** Kullanıcı metin veya sesli komut girer. Girdi JSON formatına paketlenerek REST API üzerinden sunucuya iletilir.
2. **Sunucu Katmanı:** FastAPI, JWT doğrulaması yapar. Veritabanından kullanıcının finansal profilini çekerek dinamik bir istem (prompt) hazırlar.
3. **LLM Çıkarımı:** Gemini API niyet analizi yapar; akıllı başlık, ana metin ve butonları içeren yapılandırılmış veriyi döndürür.
4. **Sunum Katmanı:** Dönen veri React tarafında ayrıştırılır ve arayüzde etkileşimli sohbet balonları/butonlar olarak render edilir.

## Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin.

### 1. Arkayüz (Backend) Kurulumu

```bash
# Proje dizinine gidin
cd backend

# Sanal ortam oluşturun ve aktif edin
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Çevresel değişkenleri (.env) ayarlayın
# (DATABASE_URL, GEMINI_API_KEY, JWT_SECRET, SMTP bilgileri vb.)

# FastAPI sunucusunu başlatın
uvicorn main:app --reload

### 2. Önyüz Kurulumu

# Frontend dizinine gidin
cd frontend

# Bağımlılıkları yükleyin
npm install

# Geliştirme sunucusunu başlatın
npm start
