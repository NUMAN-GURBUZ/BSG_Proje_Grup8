# server.py
import asyncio
from aiohttp import web, WSMsgType
import csv
from datetime import datetime

LOG_FILE = "csms_logs.csv"

# Başlangıçta başlık yaz
with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["received_time", "payload_time", "energy_value", "client_id"])

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("CSMS: Client connected")

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                data = msg.json()
                # Beklenen format: {"client_id":"EVSE1", "payload_time":"...", "energy": 1.23}
                recv_time = datetime.utcnow().isoformat()
                payload_time = data.get("payload_time")
                energy = data.get("energy")
                client_id = data.get("client_id", "unknown")

                # Kaydet
                with open(LOG_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([recv_time, payload_time, energy, client_id])

                print(f"[CSMS LOG] recv={recv_time} payload={payload_time} energy={energy} from={client_id}")

                # Opsiyonel: sunucudan cevap (ack)
                await ws.send_json({"status":"ok","recv_time":recv_time})
            except Exception as e:
                print("CSMS: Hata parsing mesaj:", e)
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())

    print("CSMS: Client disconnected")
    return ws

app = web.Application()
app.router.add_get('/ws', websocket_handler)

if __name__ == '__main__':
    web.run_app(app, port=9000)
