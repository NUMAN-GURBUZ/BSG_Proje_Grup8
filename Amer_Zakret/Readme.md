# Elektrikli Araç Şarj İstasyonu - Bellek Sızıntısı (Memory Leak) Anomali Simülasyonu

Bu proje, Elektrikli Araç Şarj İstasyonlarında karşılaşılan kritik bir yazılım hatası olan Bellek Sızıntısı (Memory Leak) durumunu simüle etmek ve tespit etmek amacıyla geliştirilmiştir.

## 📌 Proje Özeti
Bu çalışma, 7/24 çalışan bir elektrikli araç şarj istasyonunun kontrol ünitesini modeller. Yazılım, iki farklı modda çalıştırılarak bellek yönetiminin önemi gösterilir:

* **Normal Mod:** Şarj verileri işlenir ve işlem bitince bellekten temizlenir.
* **Anomali Modu:** Şarj verileri hafızada (RAM) tutulur ve temizlenmez, bu da sistemin kaynaklarının tükenmesine yol açar.

Proje, sistemin bellek kullanımını anlık olarak izler ve %20'lik ani artış tespit ettiğinde otomatik olarak alarm üretir.

## 📂 Senaryo Detayları
* **Senaryo Konusu:** Sürekli Çalışan İzleme Servisinde Bellek Sızıntısı.
* **Uygulama Alanı:** Elektrikli Araç (EV) Şarj İstasyonu.
* **Hata Kaynağı:** Tamamlanan şarj oturumlarına ait log verilerinin (nesnelerin) global bir listede birikmesi ve Garbage Collector tarafından temizlenmemesi.
* **Tespit Yöntemi:** psutil kütüphanesi ile her döngüde RSS (Resident Set Size) bellek ölçümü.

## 💻 Kullanım
Simülasyonu başlatmak için terminalde aşağıdaki komutu çalıştırın:

```bash
python anomali_demo.py
