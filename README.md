# ⚡ Elektrikli Araç Şarj İstasyonlarında Anomali Tespiti ve Siber-Fiziksel Zafiyet Analizi

Bu proje, akıllı ulaşım sistemlerinin kritik bir bileşeni olan Elektrikli Araç (EV) şarj altyapılarında ortaya çıkabilecek güvenlik açıklarını simüle etmek, analiz etmek ve tespit yöntemleri geliştirmek amacıyla hazırlanmıştır.

Proje kapsamında, **OCPP (Open Charge Point Protocol)** ve ilgili standartlar üzerinde durulmuş; faturalama, enerji yönetimi ve operasyonel güvenliği tehdit eden gerçek dünya senaryoları incelenmiştir.



## 🎯 Projenin Amacı

Bu çalışmanın temel amacı, şarj istasyonları ve Merkezi Yönetim Sistemleri (CSMS) arasındaki haberleşme altyapısında oluşabilecek siber-fiziksel tehditlerin nasıl işlediğini anlamaktır. Proje, protokol zafiyetlerinden donanımsal sorunlara kadar geniş bir yelpazedeki anomalileri teknik olarak ele alır.

## 🕵️‍♂️ İncelenen Anomaliler ve Saldırı Vektörleri

Bu proje kapsamında aşağıdaki 9 kritik anomali türü simüle edilmiş ve analiz edilmiştir:

| Anomali Türü | Açıklama ve Etki |
| :--- | :--- |
| **1. Diferansiyel Gecikme Enjeksiyonu (DLI)** | Sayaç verilerinin zaman damgaları manipüle edilerek raporların geciktirilmesi ve gizli enerji hırsızlığı yapılması. |
| **2. Bellek Sızıntısı (Memory Leak)** | Yazılım hataları nedeniyle RAM kullanımının sürekli artması ve istasyonun hizmet dışı kalarak DoS (Hizmet Reddi) durumuna düşmesi. |
| **3. Finansal Manipülasyon (Tampering)** | `StopTransaction` mesajına müdahale edilerek sayaç değerinin düşük gösterilmesi ve fatura tutarının düşürülmesi. |
| **4. Ghost RFID Event** | Fiziksel bir kart olmadan, elektromanyetik parazit veya replay saldırısı ile "hayalet" yetkilendirme yapılarak oturum açılması. |
| **5. GPS Spoofing** | İstasyonun konum verilerinin değiştirilerek bölgesel tarife farklarından haksız kazanç (arbitraj) sağlanması. |
| **6. Phantom Fleet (Sanal Filo)** | Gerçekte var olmayan araçlardan V2G (Vehicle-to-Grid) enerji katkısı raporlanarak piyasa manipülasyonu yapılması. |
| **7. Session Fork (Oturum Çatallama)** | Aynı istasyon kimliği (ID) ile ikinci bir WebSocket bağlantısı açılarak sunucunun yanıltılması ve sahte komutların işlenmesi. |
| **8. Stop Transaction Bastırılması (Zombi Oturum)** | Şarj bitmesine rağmen `StopTransaction` mesajının ağda düşürülmesi (MitM) ve oturumun açık kalarak enerji/veri tutarsızlığı yaratması. |
| **9. Token/Nonce Replay** | Önceden yakalanmış yetkilendirme tokenlarının tekrar kullanılarak yetkisiz şarj oturumu başlatılması. |
| **10. OCPP Bağlantısı Kesilmesi** |  OCPP bağlantısının kopmasına rağmen güç aktarımının sürmesi; (Kural Tabanlı + Makine Öğrenimi (ML) Destekli Hibrit Anomali Tespiti). |

## ⚠️ Tespit Edilen Ortak Güvenlik Zafiyetleri

Yapılan analizler sonucunda, saldırıların temelinde yatan ortak protokol ve sistem eksiklikleri şunlardır:

* **Protokol Güvenliği:** OCPP 1.6'da TLS şifrelemesinin zorunlu olmaması ve mesaj imzalama eksikliği MitM saldırılarını kolaylaştırmaktadır.
* **Kimlik Doğrulama:** CP (Charge Point) kimliğinin ve oturumların tekilliğinin (session uniqueness) yeterince doğrulanamaması.
* **Zaman Senkronizasyonu:** Kritik altyapılarda gereken 2ms hassasiyetin sağlanamaması ve log tutarsızlıkları.
* **Siber-Fiziksel Ayrışma:** Siber ortamda üretilen verilerin (örn: GPS, V2G verisi) fiziksel gerçeklikle örtüşüp örtüşmediğinin kontrol edilememesi.

## 🛡️ Önerilen Çözüm ve Savunma Mekanizmaları

Proje sonucunda, bu tehditlere karşı aşağıdaki savunma mekanizmalarının entegrasyonu önerilmektedir:

* 🔒 **TLS/mTLS Zorunluluğu:** İletişim güvenliği için.
* ✍️ **Mesaj İmzalama:** HMAC veya ECDSA kullanımı ile veri bütünlüğü.
* 🔑 **Tek Kullanımlık Token:** Replay saldırılarına karşı nonce/token sistemleri.
* 🛡️ **Anomali Tabanlı IDS:** Saldırıları gerçek zamanlı tespit eden Saldırı Tespit Sistemleri.
* 🌍 **Çapraz Doğrulama:** IP ve Coğrafi konum verilerinin eşleştirilmesi.

## 📊 Proje Sonucu

Elektrikli araç şarj altyapıları sadece bir enerji dağıtım noktası değil, karmaşık siber-fiziksel sistemlerdir. Bu proje, söz konusu sistemlerdeki zafiyetlerin hem ciddi finansal kayıplara hem de şebeke istikrarı sorunlarına yol açabileceğini başarılı simülasyonlarla ortaya koymuştur.

---
*Bu proje, "Elektrikli Araç Şarj İstasyonlarında Anomali Tespiti" dersi kapsamında hazırlanan genel proje raporlarına dayanmaktadır.*
