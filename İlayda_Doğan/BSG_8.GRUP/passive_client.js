// Pasif İstemci Kodu (Log Analizi Veri Kaynağı - Terminal 2)

const WebSocket = require('ws');
// CSMS'in yeni portu: 9220
const CSMS_URL = 'ws://localhost:9220/EVSE-006'; 

const ws = new WebSocket(CSMS_URL);

ws.on('open', function open() {
    console.log('Pasif İstemci: Bağlantı Kuruldu.');

    // LOG ANALİZİ KANITI: Şifresiz Yetkilendirme Mesajı
    const authMessage = JSON.stringify([
        2, 
        "100001", 
        "Authorize", 
        { "idTag": "B7E8F9G0H1I2" } // Kritik, çalınabilir kullanıcı ID'si
    ]);

    ws.send(authMessage); 
    console.log('Log verisi gönderildi. Kontrol edebilirsiniz.');
    
    setTimeout(() => { ws.close(); }, 500);
});

ws.on('error', (error) => { console.error('Hata:', error.code || error.message); });