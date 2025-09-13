import React, { useState } from 'react';
import axios from 'axios';
import { createTheme, ThemeProvider, CssBaseline, Container, Box, Typography, TextField, Button, Card, CardContent, CircularProgress, Avatar } from '@mui/material';
import SpaIcon from '@mui/icons-material/Spa'; // Wellness'ı temsil eden bir ikon import ediyoruz
import './App.css';

// Renk paletimiz ve arka plan rengi
const theme = createTheme({
  palette: {
    primary: {
      main: '#D1242B', // Kurumsal kırmızı
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

  const handleAnalysis = async () => {
    // ... (handleAnalysis fonksiyonu aynı kalıyor, değiştirmeye gerek yok)
    if (!inputText.trim()) {
      alert("Lütfen analiz edilecek bir metin girin.");
      return;
    }
    setLoading(true);
    setAnalysisResult(null);

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

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        textAlign="center"
        sx={{ p: 2 }}
      >
        <Card sx={{ 
          width: '100%', 
          maxWidth: 600, 
          borderRadius: 4, 
          boxShadow: '0 8px 32px 0 rgba(0,0,0,0.1)',
          borderTop: '4px solid', // --- YENİ EKLENDİ: KIRMIZI VURGU ---
          borderColor: 'primary.main' // Kırmızı rengi temadan alıyor
        }}>
          <CardContent sx={{ p: { xs: 3, sm: 4 } }}>

            <img 
  src="/logo.png" 
  alt="Finansal Wellness Logosu" 
  style={{ height: '50px', marginBottom: '1.5rem' }} 
/>


            <Typography variant="h4" component="h1" gutterBottom fontWeight="700">
              Finansal Wellness Asistanı
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
              Finansal durumunuz hakkında ne hissettiğinizi bizimle paylaşın.
            </Typography>
            
            <TextField
              fullWidth
              multiline
              rows={4}
              variant="outlined"
              placeholder="Bugün parayla ilgili canımı sıkan şey..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={loading}
            />

            <Box sx={{ mt: 2, position: 'relative' }}>
              <Button
                variant="contained"
                color="primary"
                size="large"
                onClick={handleAnalysis}
                disabled={loading}
                sx={{ textTransform: 'none', fontSize: '1rem', padding: '10px 30px', borderRadius: 2 }}
              >
                {loading ? <CircularProgress size={24} color="inherit" /> : "Analiz Et"}
              </Button>
            </Box>

            {analysisResult && (
              <div className="result-box">
                <Typography variant="h6" gutterBottom>Analiz Sonucu:</Typography>
                <Typography><strong>Duygu:</strong> {analysisResult.duygu}</Typography>
                <Typography><strong>Konu:</strong> {analysisResult.konu}</Typography>
                <Typography sx={{ mt: 2 }}><strong>Tavsiye:</strong> {analysisResult.tavsiye}</Typography>
              </div>
            )}
          </CardContent>
        </Card>
      </Box>
    </ThemeProvider>
  )
}

export default App;