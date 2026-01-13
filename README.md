# Öğrenci Not Hesaplama Sistemi

Bu proje, Docker üzerinde çalışan mikroservis mimarisine sahip bir not hesaplama uygulamasıdır.

## Proje İçeriği ve Puanlama Kriterleri
- **Docker & Compose:** Tüm sistem `docker-compose up` ile ayağa kalkar.
- **Backend:** FastAPI (Python) - Port 8000
- **Frontend:** HTML/JS (Nginx) - Port 8080
- **Veritabanı:** MongoDB - Port 27017
- **Dokümantasyon:** Swagger UI (`http://localhost:8000/docs`) adresinde aktiftir.

## 1. MermaidJS Akış Diyagramı (10 Puan)
Sistemin çalışma mantığını gösteren Sequence (Sıralama) diyagramı aşağıdadır:

```mermaid
sequenceDiagram
    participant User as Kullanıcı
    participant Front as Frontend (Web)
    participant API as Backend (FastAPI)
    participant DB as MongoDB

    User->>Front: Vize ve Final Notunu Girer
    Front->>API: POST /hesapla (Bearer Token ile)
    Note right of Front: Authorization: Bearer gizlisifre123
    
    alt Token Geçerli ise
        API->>API: Notu Hesapla (Vize %40 + Final %60)
        API->>DB: Sonucu Kaydet (Insert)
        DB-->>API: Kayıt Başarılı
        API-->>Front: Sonuç JSON (Geçti/Kaldı)
        Front-->>User: Ekrana Yazdır (Yeşil/Kırmızı)
    else Token Geçersiz ise
        API-->>Front: 401 Unauthorized
        Front-->>User: Hata Mesajı Göster
    end
