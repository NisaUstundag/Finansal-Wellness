from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

print("Duygu analizi modeli yükleniyor...")
sentiment_classifier = pipeline(
    "sentiment-analysis",
    model="savasy/bert-base-turkish-sentiment-cased"
)
print("Model başarıyla yüklendi.")
app = FastAPI()

origins = [
    "http://localhost:5173", # Vite (React) development server'ının varsayılan adresi
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

@app.post("/api/analyze")
def analyze_text(request: TextInput):
    # --- BU FONKSİYONUN İÇİNDEKİ HER ŞEYİN GİRİNTİSİ DÜZELTİLDİ ---
    user_text = request.text
    user_text_lower = user_text.lower()
    print(f"Analiz edilecek metin: {user_text}")

    # Adım 1 & 2: Duygu ve Konu Tespiti
    analysis_result = sentiment_classifier(user_text)[0]
    sentiment_label = analysis_result['label']
    topic = "Genel Finans"
    if "kredi" in user_text_lower or "borç" in user_text_lower:
        topic = "Kredi ve Borçlar"
    elif "birikim" in user_text_lower or "tasarruf" in user_text_lower or "yatırım" in user_text_lower:
        topic = "Birikim ve Yatırım"
    elif "maaş" in user_text_lower or "gelir" in user_text_lower:
        topic = "Maaş ve Gelir"
    elif "fatura" in user_text_lower or "kira" in user_text_lower:
        topic = "Faturalar ve Harcamalar"
    
    # Adım 3: GELİŞMİŞ TAVSİYE MOTORU (TERAPİST + KOÇ)
    main_recommendation = ""
    action_buttons = []

    # --- YENİ KURAL: Koçluk modunu garantiye al ---
    if topic == "Maaş ve Gelir":
        sentiment_label = "positive" # Model ne derse desin, biz bunu pozitif olarak kabul ediyoruz.

    # Nüansları yakalama (Terapist Modu)
    if topic == "Kredi ve Borçlar" and ("ödedim" in user_text_lower or "bitti" in user_text_lower or "mutluyum" in user_text_lower):
        sentiment_label = "positive"
        main_recommendation = "Harika bir haber! Borcunuzu yönetme konusunda önemli bir adım attınız. Bu başarıyı kutlayın!"
        action_buttons = ["Yeni Bir Hedef Belirleyelim mi?", "Tasarruf İpuçları İster misin?"]
    elif topic == "Kredi ve Borçlar" and sentiment_label == "negative":
        main_recommendation = "Kredi ve borçlar stresli olabilir. Durumu kontrol altına almak için küçük adımlarla başlayabilirsiniz."
        action_buttons = ["Bana Bir Eylem Planı Öner", "Harcamalarımı Nasıl Takip Ederim?"]

    # KOÇLUK MODU
    elif topic == "Birikim ve Yatırım" and sentiment_label == "positive":
        main_recommendation = "Tebrikler! Birikim hedefinize ulaşmanız, finansal disiplininizin bir göstergesi. Şimdi bu momentumu koruma ve büyütme zamanı."
        action_buttons = ["Bir Sonraki Adım Ne Olmalı?", "Birikimimi Enflasyondan Nasıl Korurum?"]
    elif topic == "Maaş ve Gelir" and sentiment_label == "positive":
        main_recommendation = "Gelirinizin artması veya maaşınızı almanız harika. Bu, finansal planlama yapmak için en doğru zaman."
        action_buttons = ["Bu Fazla Parayı Nasıl Değerlendiririm?", "Acil Durum Fonu Nedir?"]

    # Diğer tüm durumlar için genel cevaplar
    else:
        if sentiment_label == "positive":
            main_recommendation = "Finansal durumunuzla ilgili olumlu duygular içinde olmanız harika! Bu motivasyonu bir sonraki adıma taşıyalım mı?"
            action_buttons = ["Genel Tasarruf İpuçları", "Yatırımın Temelleri"]
        else: # negative ve neutral
            main_recommendation = "Finansal konularda endişeli hissetmek yaygındır. Unutmayın, her sorunun bir çözümü vardır."
            action_buttons = ["Küçük Adımlarla Başlayalım", "Pozitif Finansal Alışkanlıklar"]

    # Final cevabı oluştur
    final_response = {
        "duygu": sentiment_label.capitalize(),
        "konu": topic,
        "tavsiye": {
            "ana_metin": main_recommendation,
            "aksiyonlar": action_buttons
        }
    }
    
    return final_response


@app.get("/")
def read_root():
    return {"message": "Finansal Wellness Asistanı API'ına hoş geldiniz!"}