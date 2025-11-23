import time
import os
import psutil
import random
import string

class EVChargingStation:
    """
    Elektrikli Araç Şarj İstasyonu Simülatörü.
    Bu sınıf, hem normal çalışmayı hem de bellek sızıntısı anomalisini simüle eder.
    """
    def __init__(self):
        # ANOMALİ KAYNAĞI: Bu liste asla temizlenmeyecek. 
        self.session_logs = [] 
        
        # İzleme için mevcut işlemi (kendi kendini) bul
        self.process = psutil.Process(os.getpid())
        self.previous_memory = 0
        
        # Senaryo belgesinden gelen tespit kriteri. 
        self.alert_threshold = 1.20 # %20 artış eşiği

    def simulate_charging_session(self, data_size_mb=5):
        """
        Bir şarj oturumunu ve ürettiği büyük log verisini simüle eder.
        """
        session_data = {
            "station_id": f"TR-KAYSERI-{random.randint(1,5):02d}",
            "vehicle_id": f"38-TOGG-{random.randint(1000,9999)}",
            "energy_kwh": random.uniform(20.0, 80.0),
            # Bellek sızıntısına neden olacak büyük veri bloğu
            "raw_logs": ''.join(random.choices(string.ascii_letters, k=data_size_mb * 1024 * 1024))
        }
        return session_data

    def normal_operation(self):
        """
        Normal Mod: Şarj verisi işlenir, merkeze gönderilir ve RAM'den silinir.
        [cite: 6, 9, 10]
        """
        data = self.simulate_charging_session(data_size_mb=2) # Normalde daha küçük veri
        # Veri işlendi, 'data' değişkeni kapsam dışı kaldı ve silindi.
        # RAM kullanımı sabit kalır. 

    def anomalous_operation(self):
        """
        Anomali Modu: Şarj verileri listeye eklenir ama ASLA SİLİNMEZ.
        
        """
        data = self.simulate_charging_session(data_size_mb=5) # Sızıntıyı hızlandırmak için 5MB
        
        # HATA BURADA: Veri sürekli listeye ekleniyor.
        self.session_logs.append(data) 
        print(f"[HATA] Şarj kaydı RAM'de birikti. Toplam: {len(self.session_logs)} kayıt.")

    def monitor_status(self):
        """
        Sistemi ve belleği izler (Senaryo Bölüm 3: Algılama Mantığı)
        
        """
        # Mevcut RAM kullanımını MB cinsinden al
        current_memory = self.process.memory_info().rss / 1024 / 1024
        
        growth_percent = 0
        if self.previous_memory > 0:
            growth_percent = ((current_memory - self.previous_memory) / self.previous_memory) * 100

        print(f"[İSTASYON İZLEME] | RAM: {current_memory:.2f} MB | Artış: %{growth_percent:.1f}")

        # ANOMALİ TESPİT KURALI [cite: 22, 23]
        if self.previous_memory > 0 and current_memory > self.previous_memory * self.alert_threshold:
             print(f"\n>>> [ALARM] BELLEK SIZINTISI TESPİT EDİLDİ! (Eşik: %20 aşıldı)\n")
        
        self.previous_memory = current_memory

    def run(self, duration_sec=60, mode='normal'):
        """Simülasyonu çalıştırır."""
        print(f"\n--- İSTASYON BAŞLATILIYOR (Mod: {mode.upper()}) ---")
        start_time = time.time()
        
        cycle_count = 0
        while time.time() - start_time < duration_sec:
            cycle_count += 1
            print(f"\n--- Döngü {cycle_count} ---")
            
            if mode == 'normal':
                self.normal_operation()
            elif mode == 'leak':
                self.anomalous_operation()
            
            self.monitor_status()
            time.sleep(2) # Her 2 saniyede bir yeni araç/durum kontrolü

if __name__ == '__main__':
    station = EVChargingStation()

    print("Senaryo 1: Normal Çalışma Testi (10 saniye)")
    station.run(duration_sec=10, mode='normal')
    
    time.sleep(2)
    print("\n\nSenaryo 2: Hatalı Yazılım Modu Testi (Memory Leak) (20 saniye)")
    station.run(duration_sec=20, mode='leak')
    
    print("\n--- Simülasyon Tamamlandı ---")