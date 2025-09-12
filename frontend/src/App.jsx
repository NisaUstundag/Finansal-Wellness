import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Stil dosyasını dahil ediyoruz

function App() {
  // Kullanıcının metin kutusuna yazdığı yazıyı saklamak için bir "hafıza kutusu" (state)
  const [inputText, setInputText] = useState('');
  
  // Backend'den gelen analiz sonucunu saklamak için başka bir hafıza kutusu
  const [analysisResult, setAnalysisResult] = useState(null);

  // Butona basıldığında çalışacak olan fonksiyon
  const handleAnalysis = async () => {
    // Eğer metin kutusu boşsa bir şey yapma
    if (!inputText.trim()) {
      alert("Lütfen analiz edilecek bir metin girin.");
      return;
    }
    
    try {
      // Backend'imize POST isteği gönderiyoruz
      const response = await axios.post('http://127.0.0.1:8000/api/analyze', {
        text: inputText
      });
      
      // Gelen cevabı hafıza kutumuza kaydediyoruz
      setAnalysisResult(response.data);
      
    } catch (error) {
      console.error("API'a bağlanırken bir hata oluştu:", error);
      alert("Sunucuya bağlanırken bir hata oluştu. Backend'in çalıştığından emin misin?");
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Finansal Wellness Asistanı</h1>
        <p>Finansal durumunuz hakkında ne hissettiğinizi bizimle paylaşın.</p>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Bugün parayla ilgili canımı sıkan şey..."
          rows="4"
          cols="50"
        />
        <br />
        <button onClick={handleAnalysis}>Analiz Et</button>
        
        {/* Eğer bir analiz sonucu varsa, bu bölümü göster */}
        {analysisResult && (
          <div className="result-box">
            <h3>Analiz Sonucu:</h3>
            <p><strong>Duygu:</strong> {analysisResult.duygu}</p>
            <p><strong>Konu:</strong> {analysisResult.konu}</p>
            <p><strong>Tavsiye:</strong> {analysisResult.tavsiye}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;