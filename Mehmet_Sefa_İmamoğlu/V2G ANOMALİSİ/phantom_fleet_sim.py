import random
import time
import logging
from datetime import datetime

# ============= AYARLAR =============
ARAC_SAYISI = 10
SIMULASYON_SURESI = 30  # saniye
ANOMALI_ESIGI = 5       # aynı anda discharge yapan minimum araç sayısı
LOG_DOSYASI = "phantom_fleet_logs.txt"
# ===================================

# --- LOG AYARLARI ---
logging.basicConfig(
    filename=LOG_DOSYASI,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# --- ARAÇ SINIFI ---
class Arac:
    def __init__(self, id):
        self.id = id
        self.sarj = random.uniform(40, 100)  # % cinsinden
        self.mod = "idle"  # charge / discharge / idle
        self.log_kaydi("Oluşturuldu (başlangıç şarj: %.1f%%)" % self.sarj)

    def karar_ver(self, fiyat):
        """Fiyata ve şarj durumuna göre karar ver"""
        if self.sarj > 70 and fiyat > 0.6:
            self.mod = "discharge"
            self.sarj -= random.uniform(5, 10)
        elif self.sarj < 50 and fiyat < 0.4:
            self.mod = "charge"
            self.sarj += random.uniform(5, 10)
        else:
            self.mod = "idle"
        self.sarj = max(0, min(100, self.sarj))
        self.log_kaydi(f"Durum: {self.mod.upper()}, Şarj: {self.sarj:.1f}%, Fiyat: {fiyat:.2f}")

    def log_kaydi(self, mesaj):
        logging.info(f"ARAÇ-{self.id:03d}: {mesaj}")

# --- ANOMALİ ALGILAYICI ---
class AnomaliDedektor:
    def __init__(self, esik):
        self.esik = esik

    def kontrol_et(self, araclar, fiyat):
        aktif_discharge = [a for a in araclar if a.mod == "discharge"]
        if len(aktif_discharge) >= self.esik:
            ids = [a.id for a in aktif_discharge]
            mesaj = f"⚠️ ANOMALİ TESPİTİ: {len(aktif_discharge)} araç ayni anda discharge yapti! Araçlar: {ids}"
            logging.warning(mesaj)
            print(mesaj)  # terminale de yaz
        else:
            print(f"{datetime.now().strftime('%H:%M:%S')} | Aktif discharge: {len(aktif_discharge)} | Fiyat: {fiyat:.2f}")

# --- SİMÜLASYON BAŞLANGICI ---
def main():
    logging.info("=== Phantom Fleet V2G Simülasyonu Başladi ===")
    araclar = [Arac(i+1) for i in range(ARAC_SAYISI)]
    dedektor = AnomaliDedektor(ANOMALI_ESIGI)

    baslangic = time.time()
    while time.time() - baslangic < SIMULASYON_SURESI:
        # Dinamik enerji fiyatı (0.3 - 0.8 arası dalgalanır)
        fiyat = random.uniform(0.3, 0.8)
        for a in araclar:
            a.karar_ver(fiyat)
        dedektor.kontrol_et(araclar, fiyat)
        time.sleep(1)

    logging.info("=== Simülasyon Bitti ===")

    # --- SONUÇLARI TXT DOSYASINA YAZ ---
    with open("phantom_fleet_summary.txt", "w", encoding="utf-8") as f:
        f.write("=== Phantom Fleet V2G Simülasyon Özeti ===\n")
        f.write(f"Tarih: {datetime.now()}\n")
        f.write(f"Arac Sayisi: {ARAC_SAYISI}\n")
        f.write(f"Anomali Esigi: {ANOMALI_ESIGI}\n\n")

        for a in araclar:
            f.write(f"ARAÇ-{a.id:03d} | Son Şarj: {a.sarj:.1f}% | Son Durum: {a.mod}\n")

        f.write("\n(Tüm detayli kayitlar 'phantom_fleet_logs.txt' dosyasina yazilmistir.)\n")

    print("\n✅ Simülasyon tamamlandı! Sonuçlar 'phantom_fleet_summary.txt' dosyasına kaydedildi.")

# --- ÇALIŞTIR ---
if __name__ == "__main__":
    main()
