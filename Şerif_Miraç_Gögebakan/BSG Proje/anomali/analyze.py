# analyze.py
import pandas as pd
from datetime import datetime

# CSMS log
csms = pd.read_csv("csms_logs.csv", parse_dates=["received_time","payload_time"])
# EVSE log (opsiyonel, doğrulama için)
evse = pd.read_csv("evse_logs.csv", parse_dates=["send_time","payload_time"])

# TDD: received_time - payload_time
csms["delay_sec"] = (csms["received_time"] - csms["payload_time"]).dt.total_seconds()

print("=== TDD (Zaman Farkı) Özet ===")
print(csms["delay_sec"].describe())

# ESC: enerji/süre tutarlılığı (basit)
total_energy = csms["energy_value"].astype(float).sum()
total_seconds = (csms["received_time"].max() - csms["received_time"].min()).total_seconds()
if total_seconds == 0:
    avg_power = None
else:
    # energy in kWh, total_seconds->hours
    total_hours = total_seconds / 3600
    avg_power = total_energy / total_hours

print("\nToplam enerji (kWh):", total_energy)
print("Toplam süre (s):", total_seconds)
print("Ortalama güç (kW):", round(avg_power,3) if avg_power else "N/A")

# Basit eşiklerle anomali satırları yaz
anomalies = csms[csms["delay_sec"] > 2]   # eşik: 2 saniye (ayarlanabilir)
if len(anomalies) == 0:
    print("\nAnomali bulunamadı (TDD eşiği 2s).")
else:
    print(f"\n{len(anomalies)} adet potansiyel DLI anomali kaydı (delay > 2s):")
    print(anomalies[["received_time","payload_time","energy_value","delay_sec"]])

# Rapor dosyası oluştur
with open("anomaly_report.txt", "w") as f:
    f.write("=== DLI Anomaly Report ===\n\n")
    f.write("TDD özet:\n")
    f.write(str(csms["delay_sec"].describe()) + "\n\n")
    f.write(f"Toplam enerji (kWh): {total_energy}\n")
    f.write(f"Ortalama güç (kW): {round(avg_power,3) if avg_power else 'N/A'}\n\n")
    f.write(f"Potansiyel anomali sayısı (delay>2s): {len(anomalies)}\n")
    if len(anomalies) > 0:
        f.write("\nÖrnek anomali satırları:\n")
        f.write(anomalies.head(10).to_string(index=False))

print("\n✅ Analiz tamamlandı. Rapor -> anomaly_report.txt")
