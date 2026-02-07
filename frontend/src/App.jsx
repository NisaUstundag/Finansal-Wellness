import React, { useState } from 'react';
import axios from 'axios';
import { createTheme, ThemeProvider, CssBaseline, Container, Box, Typography, TextField, Button, Card, CardContent, CircularProgress, Chip } from '@mui/material';
import './App.css';

// Tema ayarları aynı kalıyor
const theme = createTheme({
  palette: {
    primary: {
      main: '#D1242B',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: `
        body {
          background: linear-gradient(135deg, #f5f7fa 0%, #e1e8f0 100%);
        }
      `,
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});

function App() {
  const [inputText, setInputText] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detailedRecommendation, setDetailedRecommendation] = useState(''); // --- YENİ: Detaylı tavsiye için state

  const handleAnalysis = async () => {
    if (!inputText.trim()) {
      alert("Lütfen analiz edilecek bir metin girin.");
      return;
    }
    setLoading(true);
    setAnalysisResult(null);
    setDetailedRecommendation(''); // Her yeni analizde detaylı tavsiyeyi sıfırla

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/analyze', {
        text: inputText
      });
      setAnalysisResult(response.data);
    } catch (error) {
      console.error("API'a bağlanırken bir hata oluştu:", error);
      alert("Sunucuya bağlanırken bir hata oluştu. Backend'in çalıştığından emin misin?");
    } finally {
      setLoading(false);
    }
  };

  // --- YENİ: Aksiyon butonlarına tıklandığında çalışacak fonksiyon ---
  const handleActionClick = (action) => {
    // Bu kısım, bootcamp sunumu için basit ama etkili "sanki" mantığı içerir.
    if (action === "Bana Bir Eylem Planı Öner") {
      setDetailedRecommendation("Harika. İşte 3 adımlık basit bir başlangıç planı: 1. Tüm harcamalarını bir hafta boyunca not al. 2. Zorunlu ve keyfi harcamalarını ayır. 3. Keyfi harcamalardan sadece bir tanesini %10 azaltmayı hedefle.");
    } else if (action === "Harcamalarımı Nasıl Takip Ederim?") {
      setDetailedRecommendation("Harcama takibi için birçok yöntem var: Basit bir not defteri kullanabilir, bir Excel tablosu oluşturabilir veya mobil bankacılık uygulamalarının bütçe araçlarından faydalanabilirsiniz.");
    } else {
      setDetailedRecommendation(`'${action}' hakkında daha fazla bilgi sunmak için çalışmalarımız devam ediyor.`);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" minHeight="100vh" textAlign="center" sx={{ p: 2 }}>
        <Card sx={{ width: '100%', maxWidth: 600, borderRadius: 4, boxShadow: '0 8px 32px 0 rgba(0,0,0,0.1)', borderTop: '4px solid', borderColor: 'primary.main' }}>
          <CardContent sx={{ p: { xs: 3, sm: 4 } }}>
            {/* Logo ve başlık kısımları aynı kalıyor */}
            <Typography variant="h4" component="h1" gutterBottom fontWeight="700">
              Finansal Wellness Asistanı
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
              Finansal durumunuz hakkında ne hissettiğinizi bizimle paylaşın.
            </Typography>
            <TextField fullWidth multiline rows={4} variant="outlined" placeholder="Bugün parayla ilgili canımı sıkan şey..." value={inputText} onChange={(e) => setInputText(e.target.value)} disabled={loading} />
            <Box sx={{ mt: 2, position: 'relative' }}>
              <Button variant="contained" color="primary" size="large" onClick={handleAnalysis} disabled={loading} sx={{ textTransform: 'none', fontSize: '1rem', padding: '10px 30px', borderRadius: 2 }}>
                {loading ? <CircularProgress size={24} color="inherit" /> : "Yeni Analiz"}
              </Button>
            </Box>

            {analysisResult && (
              <div className="result-box">
                <Typography variant="h6" gutterBottom>Analiz Sonucu:</Typography>
                <Typography><strong>Duygu:</strong> <Chip label={analysisResult.duygu} color={analysisResult.duygu === 'Positive' ? 'success' : 'error'} /></Typography>
                <Typography><strong>Konu:</strong> {analysisResult.konu}</Typography>
                
                {/* --- DEĞİŞİKLİK BURADA BAŞLIYOR --- */}
                <Typography sx={{ mt: 2 }}><strong>Tavsiye:</strong> {analysisResult.tavsiye.ana_metin}</Typography>
                
                <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap', justifyContent: 'center' }}>
                  {analysisResult.tavsiye.aksiyonlar.map((action, index) => (
                    <Button key={index} variant="outlined" size="small" onClick={() => handleActionClick(action)}>
                      {action}
                    </Button>
                  ))}
                </Box>
                
                {detailedRecommendation && (
                  <Typography sx={{ mt: 2, p: 2, bgcolor: '#e9ecef', borderRadius: 2 }}>
                    {detailedRecommendation}
                  </Typography>
                )}
                {/* --- DEĞİŞİKLİK BURADA BİTİYOR --- */}

              </div>
            )}
          </CardContent>
        </Card>
      </Box>
    </ThemeProvider>
  );
}

export default App;