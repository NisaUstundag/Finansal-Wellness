from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# API sunucumuzu oluşturuyoruz
app = FastAPI()

# Bu olmazsa, tarayıcı güvenlik nedeniyle React'ın API'a bağlanmasını engeller.
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

# İçinde "text" adında bir metin (string) olacak.
class TextInput(BaseModel):
    text: str

# React, analiz isteklerini bu adrese POST metoduyla yapacak.
@app.post("/api/analyze")
def analyze_text(request: TextInput):
    # React'tan gelen metni terminalde görelim (test için harika bir yöntem)
    print(f"Analiz edilecek metin: {request.text}")

    # Yapay zeka modelini daha sonra buraya entegre edeceğiz.
    fake_analysis = {
        "duygu": "Heyecan",
        "konu": "Yeni Proje",
        "tavsiye": "Bu harika bir başlangıç! Planlı bir şekilde ilerlersen her şey yolunda gidecektir. İlk adım temel kurulumu tamamlamaktı ve başardın!"
    }
    
    return fake_analysis

# Ana sayfaya basit bir karşılama mesajı ekleyelim.
@app.get("/")
def read_root():
    return {"message": "Wellness Asistanı API'ına hoş geldiniz!"}