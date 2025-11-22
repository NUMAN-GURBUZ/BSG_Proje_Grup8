# OCPP ve CAN‑bus: Mimariler, Riskler ve Eğitimsel Uygulama Rehberi

Bu doküman OCPP (Open Charge Point Protocol) ile CAN‑bus arasındaki etkileşimi, ortak zayıflıkları ve eğitim amaçlı uygulanabilecek yöntemleri ayrıntılı ve teknik olarak açıklamaktadır. İçerik, PoC (Session Fork Attack) bağlamında pratik ve tekrar üretilebilir öneriler içerir.

## 1. Temel Kavramlar
### 1.1 OCPP (Open Charge Point Protocol)
- OCPP, şarj istasyonları (Charge Points, CP) ile merkezi yönetim sistemleri (CSMS) arasında haberleşmeyi sağlayan bir protokoldür.
- Yaygın sürüm: **OCPP 1.6** — WebSocket (JSON) üzerinde çalışır; TLS üzerinden koruma desteklenir.
- Mesaj türleri: **Call** (istemciden sunucuya istek) ve **CallResult/CallError** (sunucudan istemciye cevap). Payload imzaları ve parametre isimleri sürüme göre değişir.

### 1.2 CAN‑bus (Controller Area Network)
- CAN, gömülü cihazlar arasında kısa ve güvenilir mesajlaşma sağlar; otomotiv ve endüstride yaygın kullanılır.
- CAN, kriptografik bütünlük veya kimlik doğrulama sunmaz — güvenlik varsayımı “fiziksel kontrollü erişim” üzerinedir.
- Tipik saldırılar: frame enjeksiyonu, ID spoofing, flooding, replay.

## 2. OCPP → CAN Köprüsü (Gateway) Mimarisinin Yapısı
- **CP Agent:** OCPP yığına (WebSocket) bağlanan yazılım komponentidir; gelen OCPP isteklerini uygulama mantığına çevirir.
- **Gateway/Mapper:** CP Agent ile CAN arayüzü arasında çalışır. Örneğin:
  - `RemoteStartTransaction` → CAN ID `0x200`, payload: `{cp_hash, connector_id, start_cmd}`
  - `RemoteStopTransaction` → CAN ID `0x201`, payload: `{tx_id, stop_cmd}`
  - `MeterValues` → CAN ID `0x300` (meter module → CP agent)
- **CAN Transceiver / vcan0:** Fiziksel/veya sanal CAN arayüzü. Eğitim ortamı için `vcan0` önerilir.

## 3. Yaygın Risk Senaryoları
1. **MitM (Man‑in‑The‑Middle) / Mesaj Değiştirme:** Düz WS veya zayıf TLS ile trafiği yakalayıp `RemoteStartTransaction` → `RemoteStopTransaction` olarak değiştirme.
2. **Transaction ID Hırsızlığı / Replay:** Transaction ID bilgisi ele geçirilip yeniden kullanıldığında Session Fork oluşur.
3. **Firmware/Config Süreci Kötüye Kullanımı:** Imzasız güncelleme mekanizmaları CP’ye kötü kod yüklenmesine izin verebilir; sonuç CAN enjeksiyonudur.
4. **CAN Enjeksiyonu (Yerel):** CP yazılımı ele geçirilince doğrudan CAN’e sahte frame’ler gönderilir; fiziksel etkiler (röle kontrolü, güç değişimi) gerçekleşir.

## 4. Eğitimsel Uygulama Önerileri (Adım‑adım)
### 4.1 Hazırlık
- VM üzerinde `vcan0` oluşturun (`modprobe vcan`, `ip link add dev vcan0 type vcan`, `ip link set up vcan0`).
- Python ortamı: `python3 -m venv opp-env`, `source opp-env/bin/activate`, `pip install -r requirements.txt` (requirements.txt: ocpp==0.10.0, websockets, python-can).
- Dosyalar: `csms_vistim.py`, `legit_cp.py`, `attacker.py`, `can_gateway.py` (basit mapping).

### 4.2 Normal Akış (Demonstrasyon)
1. CSMS başlatılır (WebSocket server).  
2. CP (legit) bağlanır ve `BootNotification` yollar; CSMS `BootNotification` yanıtı verir.  
3. CSMS `RemoteStartTransaction` gönderir; CP agent bunu CAN frame’e çevirir (0x200).  
4. Meter modülü (simüle) 0x300 ile `MeterValues` gönderir; CSMS loglar.

### 4.3 Saldırı Senaryosu (MitM veya Attacker)
- **MitM Proxy Yöntemi:** Öğrenciler CP’i proxy’e bağlar; proxy gelen `RemoteStartTransaction`'ı `RemoteStopTransaction` olarak değiştirir. Bu değişiklik CAN üzerinde gözlemlenir (start yerine stop frame).  
- **Attacker CP Yöntemi:** Saldırgan, aynı CP id ile bağlanıp sahte `StopTransaction` gönderir; CSMS bunu işler ve CAN üzerinde stop frame oluşur.

## 5. Loglama ve Kanıt Toplama
- Her adımda terminal loglarını alın; zaman damgası, transaction_id ve CP id’leri mutlaka kaydedilsin.  
- Önemli olaylar: `BootNotification accepted`, `RemoteStart sent/received`, `MeterValues`, `StopTransaction received`.
- Ekran görüntüleri ve kısa terminal kaydı (OBS veya `asciinema`) rapora eklenmelidir.

## 6. Önerilen Savunma ve İyileştirmeler
- **mTLS ve sertifika yönetimi:** Hem CP hem CSMS arasında karşılıklı TLS doğrulaması uygulayın.  
- **Gateway whitelist & schema validation:** OCPP→CAN dönüşümlerini sadece beklenen ID/payload yapısına izin verin.  
- **Firmware imzalama:** OTA güncellemelerini imzalanmış paketlerle sınırlandırın.  
- **CAN‑IDS:** Basit frekans/entropy tabanlı anomali tespit mekanizmaları geliştirin.  
- **Audit & Monitoring:** Merkezi loglama (JSON formatı) ile anomali deteksiyonuna altyapı sağlayın.

## 7. Ek Kaynaklar ve Araçlar
- `python-can`, `cantools`, `can-utils` (Linux)  
- `mitmproxy` veya basit WebSocket proxy örnekleri  
- OCPP 1.6 spesifikasyonu (Open Charge Alliance)  
- vcan0 (sanal CAN) kullanımı

---
Bu belge, PoC’nin hem öğretici hem de güvenlik değerlendirme amaçlı olarak kullanılmasını sağlamak üzere teknik ama uygulamalı içeriğe odaklanmıştır.