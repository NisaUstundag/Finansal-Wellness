# Gerekli importlar
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from transformers import pipeline
from . import models, schemas
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

# Veritabanı tablolarını oluşturur
models.Base.metadata.create_all(bind=engine)

# Fine-tune edilmiş yerel NLP modelini yükler
print("Özel NLP modeli yükleniyor...")
sentiment_classifier = pipeline(
    "sentiment-analysis",
    model="./finansal_model"
)
print("Model yüklendi.")

# FastAPI uygulamasını oluşturur
app = FastAPI()

# Frontend'den gelen isteklere izin vermek için CORS ayarları
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Her istek için veritabanı oturumu açıp kapatan dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Veritabanına yeni bir 'interaction' kaydı ekleyen CRUD fonksiyonu
def create_interaction(db: Session, interaction: schemas.InteractionCreate):
    db_interaction = models.Interaction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

# Ana analiz endpoint'i
@app.post("/api/analyze", response_model=schemas.Interaction)
def analyze_text(request: schemas.TextInput, db: Session = Depends(get_db)):
    
    user_text = request.text
    user_text_lower = user_text.lower()
    
    # NLP modeli ile duygu analizi
    analysis_result = sentiment_classifier(user_text)[0]
    sentiment_label = analysis_result['label']
    
    # Anahtar kelimelerle konu tespiti
    topic = "Genel Finans"
    if "kredi" in user_text_lower or "borç" in user_text_lower:
        topic = "Kredi ve Borçlar"
    elif "birikim" in user_text_lower or "tasarruf" in user_text_lower or "yatırım" in user_text_lower:
        topic = "Birikim ve Yatırım"
    elif "maaş" in user_text_lower or "gelir" in user_text_lower:
        topic = "Maaş ve Gelir"
    elif "fatura" in user_text_lower or "kira" in user_text_lower:
        topic = "Faturalar ve Harcamalar"
    
    # Kural tabanlı tavsiye motoru
    main_recommendation = ""
    action_buttons = []

    # Modelin olası hatalarını düzelten ve senaryoları zenginleştiren kurallar
    if topic == "Maaş ve Gelir":
        sentiment_label = "POZITIF_GELIR" 
    
    if topic == "Kredi ve Borçlar" and ("ödedim" in user_text_lower or "bitti" in user_text_lower or "mutluyum" in user_text_lower):
        sentiment_label = "POZITIF_ODEME"
    
    # Duygu ve konuya göre tavsiye ve aksiyon belirleme mantığı
    if sentiment_label == "POZITIF_ODEME":
        main_recommendation = "Harika bir haber! Borcunuzu yönetme konusunda önemli bir adım attınız. Bu başarıyı kutlayın!"
        action_buttons = ["Yeni Bir Hedef Belirleyelim mi?", "Tasarruf İpuçları İster misin?"]
    elif sentiment_label == "NEGATIF_HARCAMA" or sentiment_label == "NEGATIF_YETERSİZLİK":
        main_recommendation = "Bu durumun stresli olabileceğini anlıyorum. Durumu kontrol altına almak için küçük adımlarla başlayabilirsiniz."
        action_buttons = ["Bana Bir Eylem Planı Öner", "Harcamalarımı Nasıl Takip Ederim?"]
    elif sentiment_label == "POZITIF_GELIR":
        main_recommendation = "Gelirinizin artması veya maaşınızı almanız harika. Bu, finansal planlama yapmak için en doğru zaman."
        action_buttons = ["Bu Fazla Parayı Nasıl Değerlendiririm?", "Acil Durum Fonu Nedir?"]
    else: # NOYTR_PLANLAMA ve diğerleri için
        main_recommendation = "Finansal durumunuzu planlamak için bir adım atmanız harika. Hadi bu motivasyonu bir sonraki adıma taşıyalım."
        action_buttons = ["Genel Tasarruf İpuçları", "Yatırımın Temelleri"]
    
    # Analiz sonuçlarını veritabanına kaydeder
    interaction_to_save = schemas.InteractionCreate(
        user_text=user_text,
        predicted_emotion=sentiment_label,
        predicted_topic=topic,
        final_recommendation=main_recommendation
    )
    db_record = create_interaction(db=db, interaction=interaction_to_save)
    
    # Frontend'e döndürülecek nihai cevabı oluşturur
    final_response = {
        "id": db_record.id,
        "timestamp": db_record.timestamp,
        "duygu": sentiment_label.capitalize(),
        "konu": topic,
        "tavsiye": {
            "ana_metin": main_recommendation,
            "aksiyonlar": action_buttons
        }
    }
    
    return final_response

# API'ın çalıştığını test etmek için root endpoint
@app.get("/")
def read_root():
    return {"message": "Finansal Wellness Asistanı API'ına hoş geldiniz!"}