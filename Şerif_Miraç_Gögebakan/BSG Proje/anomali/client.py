# client.py
import asyncio
import websockets
import json
from datetime import datetime, timedelta
import random
import argparse
import csv
import time

LOG_FILE = "evse_logs.csv"

# Başlık
with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["send_time", "payload_time", "energy_value", "injected_delay_seconds", "client_id"])

async def run(client_id="EVSE1", normal_interval=10, run_for_seconds=60, anomaly_rate=0.4):
    uri = "ws://localhost:9000/ws"
    end_time = time.time() + run_for_seconds
    async with websockets.connect(uri) as ws:
        print(f"{client_id}: Connected to CSMS")

        while time.time() < end_time:
            # Normal gönderim aralığı
            base = normal_interval

            # Anomali kararı: rastgele olarak anomali uygula
            if random.random() < anomaly_rate:
                # Gecikme enjeksiyonu (saniye)
                injected = random.choice([5, 10, 15])
            else:
                injected = 0

            # Bekleme (block sleep kullanıyorum basitlik için)
            await asyncio.sleep(base + injected)

            # Payload zaman damgası: hile yapmak için zaman kaydır (ör. ileri/geri)
            # Burada "zaman damgasını 5 saniye geri alma" örneği:
            payload_time = (datetime.utcnow() - timedelta(seconds=5)).isoformat()

            energy = round(random.uniform(0.4, 1.6), 3)  # kWh örneği

            msg = {
                "client_id": client_id,
                "payload_time": payload_time,
                "energy": energy
            }

            await ws.send(json.dumps(msg))
            send_time = datetime.utcnow().isoformat()

            # Log kendinde de tut
            with open(LOG_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([send_time, payload_time, energy, injected, client_id])

            print(f"[{client_id} SENT] send={send_time} payload={payload_time} energy={energy} inj_delay={injected}s")

            # Opsiyonel: sunucudan ack bekle (zaman aşımı riskine karşı kısa bekle)
            try:
                ack = await asyncio.wait_for(ws.recv(), timeout=2)
                # ignore content or print
            except Exception:
                pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="EVSE1")
    parser.add_argument("--interval", type=int, default=10, help="normal gönderim aralığı (saniye)")
    parser.add_argument("--duration", type=int, default=60, help="çalışma süresi (saniye)")
    parser.add_argument("--anomaly", type=float, default=0.4, help="anomali (DLI) oranı 0-1 arası")
    args = parser.parse_args()

    asyncio.run(run(client_id=args.id, normal_interval=args.interval, run_for_seconds=args.duration, anomaly_rate=args.anomaly))
