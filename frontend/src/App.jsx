import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { createTheme, ThemeProvider, CssBaseline, Container, Box, Typography, TextField, Button, Card, Paper, CircularProgress, Stack, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#D1242B', 
    },
    secondary: {
      main: '#006442', 
    },
    background: {
      default: '#f5f7fa'
    }
  },
  typography: {
    fontFamily: '"Montserrat", "Helvetica", "Arial", sans-serif', 
    h5: {
      fontWeight: 700,
    },
    h6: {
      fontWeight: 700,
    }
  },
});

const MotivationalQuote = () => (
  <Typography variant="body2" color="text.secondary" sx={{ mb: 4, fontStyle: 'italic' }}>
    "Financial peace isn't the acquisition of stuff. It's learning to live on less than you make, so you can give money back and have money to invest. You can't win until you do this."
  </Typography>
);


function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Merhaba! Ben Finansal Wellness Asistanı. Finansal durumunla ilgili ne hissettiğini benimle paylaşabilirsin.' }
  ]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;
    const userMessage = { sender: 'user', text: inputText };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/analyze', { text: userMessage.text });
      const botResponse = {
        sender: 'bot',
        text: response.data.tavsiye.ana_metin,
        actions: response.data.tavsiye.aksiyonlar,
      };
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const errorResponse = { sender: 'bot', text: 'Üzgünüm, sunucuya bağlanırken bir sorun oluştu.' };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setLoading(false);
    }
  };

  const handleActionClick = (actionText) => {
    const botResponse = { sender: 'bot', text: `'${actionText}' hakkında daha detaylı bilgi ve kişiselleştirilmiş bir eylem planı sunmak için çalışmalarımız devam ediyor.` };
    setMessages(prev => [...prev, botResponse]);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" sx={{ py: 4 }}>
        <MotivationalQuote />

        <Card sx={{ height: '80vh', display: 'flex', flexDirection: 'column', borderRadius: 4, boxShadow: '0 8px 32px 0 rgba(0,0,0,0.1)' }}>
          <Box sx={{ p: 2, borderBottom: '1px solid #ddd', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Typography variant="h6" component="h1" fontWeight="bold" color="secondary">
              Finansal Wellness Asistanı
            </Typography>
          </Box>
          
          <Box sx={{ flexGrow: 1, overflowY: 'auto', p: 2 }}>
            {messages.map((msg, index) => (
              <div key={index} className={`message-bubble ${msg.sender === 'user' ? 'user-bubble' : 'bot-bubble'}`}>
                <Typography variant="body1">{msg.text}</Typography>
                {msg.actions && (
                  <Stack direction="row" spacing={1} sx={{ mt: 1.5, flexWrap: 'wrap', gap: 1 }}>
                    {msg.actions.map((action, i) => (
                      <Button key={i} size="small" variant="outlined" color="secondary" sx={{ borderRadius: '16px', bgcolor: 'white', textTransform: 'none' }} onClick={() => handleActionClick(action)}>
                        {action}
                      </Button>
                    ))}
                  </Stack>
                )}
              </div>
            ))}
            {loading && <CircularProgress size={24} sx={{ display: 'block', margin: '10px auto' }} />}
            <div ref={chatEndRef} />
          </Box>

          <Box sx={{ p: 2, borderTop: '1px solid #ddd', bgcolor: '#f9f9f9' }}>
            <Stack direction="row" spacing={1}>
              <TextField fullWidth variant="outlined" placeholder="Bir mesaj yaz..." value={inputText} onChange={(e) => setInputText(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && !loading && handleSendMessage()} disabled={loading} size="small" />
              <IconButton variant="contained" onClick={handleSendMessage} disabled={loading} color="primary">
                <SendIcon />
              </IconButton>
            </Stack>
          </Box>
        </Card>
      </Container>
    </ThemeProvider>
  );
}

export default App;