# SMART Hedefler — OCPP Session Fork Attack Eğitimi

Bu doküman, öğrenci gruplarının veya proje ekiplerinin bu PoC tabanlı çalışmada ulaşması gereken SMART hedeflerini (Specific, Measurable, Achievable, Relevant, Time‑bound) listeler. Her hedefin altına uygulanabilir başarı kriterleri eklenmiştir.

## Hedef 1 — Temel İletişim ve Altyapı Kurulumu
- **Specific:** CSMS ve CP simülasyonunu çalıştıracak ve sanal CAN (`vcan0`) üzerinden temel mesaj alışverişini sağlayacak bir deney ortamı kuracağım.  
- **Measurable:** BootNotification, RemoteStartTransaction ve MeterValues mesajlarının her birinin ilgili loglarda gözlemlenmesi.  
- **Achievable:** Hazır örnek kodlar (csms_vistim.py, legit_cp.py) ve `vcan0` talimatları sağlanmıştır.  
- **Relevant:** Bu adım temel PoC’yi çalıştırmak için gereklidir.  
- **Time‑bound:** 3 iş günü içinde tamamlanacak.  
- **Başarı ölçütü:** `logs/csms.log` içinde BootNotification accepted ve `logs/legit.log` içinde MeterValues mesajları görünüyor.

## Hedef 2 — Saldırı Senaryosunu Tekrar Üretme
- **Specific:** Attacker ile sahte StopTransaction gönderip CSMS üzerinde StopTransaction alındığını gözlemleyeceğim.  
- **Measurable:** CSMS loglarında `StopTransaction alındı` mesajı ve ilgili `transaction_id` kaydı.  
- **Achievable:** Attacker script’i hazır; çalıştırma adımları belge halinde.  
- **Relevant:** Bu doğrudan öğrenme hedefidir — saldırının etkisini gözlemlemek.  
- **Time‑bound:** 2 iş günü içinde tamamlanacak.  
- **Başarı ölçütü:** `logs/csms.log` içinde StopTransaction logu var ve `transaction_id` eşleşmesi doğrulandı.

## Hedef 3 — Mitigation Deneyi (mTLS ve Gateway Whitelist)
- **Specific:** mTLS ve gateway whitelist uygulayarak saldırının başarısını azaltacağım.  
- **Measurable:** Saldırı senaryosu tekrar çalıştırıldığında StopTransaction mesajı kabul edilmeyecek veya CAN üzerinde stop frame oluşmayacak.  
- **Achievable:** mTLS için self‑signed sertifikalar ve whitelist için basit mapping modülü geliştirilecek.  
- **Relevant:** Savunma mekanizmalarının etkinliğini ölçmek öğretici bir hedeftir.  
- **Time‑bound:** 2 hafta içinde tamamlanacak.  
- **Başarı ölçütü:** Saldırı sonrası CSMS/CP loglarında hata veya reddedilen isteğe dair kayıt ve CAN trafiğinde hedef ID için beklenen frame yok.

## Hedef 4 — Anomali Tespiti (Basit CAN‑IDS)
- **Specific:** vcan0 trafiği üzerinde frekans tabanlı bir IDS yazarak anomali algılayacağım.  
- **Measurable:** IDS, sahte StopTransaction kaynaklı anormalliği en az %80 doğrulukla tespit edecek.  
- **Achievable:** Basit istatistiksel metriklerle (ID frekansı, beklenen sıra) başlayıp gerekirse ML’ye geçilebilir.  
- **Relevant:** Tespit mekanizmaları gerçek dünyada kritik önem taşır.  
- **Time‑bound:** 3 hafta içinde tamamlanacak.  
- **Başarı ölçütü:** Test senaryolarında IDS alarmı tetiklenmesi; raporlanan FP/FN oranları.

## Hedef 5 — Raporlama ve Sunum
- **Specific:** Çalışmanın sonuçlarını içeren profesyonel bir rapor ve 10 slayttan oluşan sunum hazırlayacağım.  
- **Measurable:** Rapor .docx ve slaytlar .pptx formatında teslim edilecek; sunum 10–15 dakikada tamamlanacak.  
- **Achievable:** Hazır rapor şablonu ve slayt taslağı sağlanmıştır.  
- **Relevant:** Akademik teslimat için gereklidir.  
- **Time‑bound:** 1 hafta içinde tamamlanacak.  
- **Başarı ölçütü:** Rapor ve sunum teslim edildi; değerlendirme rubriğine göre minimum başarı puanı alındı.

---
Her hedef için görev listesi, sorumlu kişi ve risk/önlem planı ekleyerek proje yönetimini kolaylaştırabiliriz. İstersen bu şablonu team assignment ve Gantt ile genişleteyim.
