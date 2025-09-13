from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Duygu analizi için önceden eğitilmiş bir modeli yüklüyoruz.
# Bu model, ilk çalıştığında internetten indirilecektir ve bu işlem birkaç dakika sürebilir.
print("Duygu analizi modeli yükleniyor...")
sentiment_classifier = pipeline(
    "sentiment-analysis",
    model="savasy/bert-base-turkish-sentiment-cased"
)
print("Model başarıyla yüklendi.")
# API sunucumuzu oluşturuyoruz
app = FastAPI()

# CORS Ayarları: Frontend'in (React) bizimle konuşmasına izin vermek için.
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

# React'tan bize nasıl bir veri geleceğini tanımlıyoruz:
# İçinde "text" adında bir metin (string) olacak.
class TextInput(BaseModel):
    text: str

# Sunucumuzda /api/analyze adında bir adres oluşturuyoruz.
# React, analiz isteklerini bu adrese POST metoduyla yapacak.
@app.post("/api/analyze")
def analyze_text(request: TextInput):
    user_text = request.text
    user_text_lower = user_text.lower()
    print(f"Analiz edilecek metin: {user_text}")

    # 1. ADIM: DUYGU ANALİZİ
    analysis_result = sentiment_classifier(user_text)[0]
    sentiment_label = analysis_result['label']
    print(f"Analiz sonucu: Label={sentiment_label}")

    # 2. ADIM: KONU TESPİTİ
    topic = "Genel Finans"
    if "kredi" in user_text_lower or "borç" in user_text_lower:
        topic = "Kredi ve Borçlar"
    elif "birikim" in user_text_lower or "tasarruf" in user_text_lower or "yatırım" in user_text_lower:
        topic = "Birikim ve Yatırım"
    elif "maaş" in user_text_lower or "gelir" in user_text_lower:
        topic = "Maaş ve Gelir"
    elif "fatura" in user_text_lower or "kira" in user_text_lower:
        topic = "Faturalar ve Harcamalar"

    # 3. ADIM: YENİ - AKILLI TAVSİYE MOTORU
    recommendation = "Finansal durumunuzu takip etmeniz harika. İşte size özel bir tavsiye:"

    # Nüansları yakalama: Borç hakkında pozitif bir cümle -> Ödeme yapılmıştır.
    if topic == "Kredi ve Borçlar" and ("ödedim" in user_text_lower or "bitti" in user_text_lower or "kapattım" in user_text_lower or "mutluyum" in user_text_lower):
         sentiment_label = "positive" # Modelin hatasını elle düzeltiyoruz!
         recommendation = "Harika bir haber! Borcunuzu yönetme konusunda önemli bir adım attınız. Bu başarıyı kutlayın ve bir sonraki finansal hedefinize odaklanın."
    elif topic == "Kredi ve Borçlar" and sentiment_label == "negative":
        recommendation = "Kredi ve borçlar stresli olabilir. Durumu kontrol altına almak için küçük adımlarla başlayabilirsiniz. Haftalık harcamalarınızı bir yere not almayı denediniz mi?"
    elif topic == "Birikim ve Yatırım" and sentiment_label == "positive":
        recommendation = "Tebrikler! Birikim ve yatırım hedeflerinize ulaşmak için doğru yoldasınız. Disiplininiz meyvelerini veriyor."
    elif topic == "Birikim ve Yatırım" and sentiment_label == "negative":
        recommendation = "Birikim veya yatırım konusunda endişeli hissetmek normaldir. Belki de hedeflerinizi daha küçük, yönetilebilir adımlara bölmek stresi azaltabilir."
    else: # Diğer tüm durumlar için genel bir cevap
        if sentiment_label == "positive":
            recommendation = "Finansal durumunuzla ilgili olumlu duygular içinde olmanız harika! Bu motivasyonu sürdürmeye devam edin."
        elif sentiment_label == "negative":
            recommendation = "Finansal konularda olumsuz hissetmek yaygındır. Unutmayın, her sorunun bir çözümü vardır ve küçük adımlar büyük farklar yaratabilir."
        else:
             recommendation = "Finansal durumunuzu bizimle paylaştığınız için teşekkürler. Her adımı planlı bir şekilde atmak önemlidir."


    # Final cevabı oluştur
    final_response = {
        "duygu": sentiment_label.capitalize(), # İlk harfi büyük yapalım
        "konu": topic,
        "tavsiye": recommendation
    }

    return final_response