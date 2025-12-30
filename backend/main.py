from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
# Yeni eklenen kütüphane:
from pymongo import MongoClient 
import datetime

# --- GÜVENLİK ---
security = HTTPBearer()
GIZLI_TOKEN = "gizlisifre123"

def token_dogrula(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != GIZLI_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz Token!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# --- VERİTABANI BAĞLANTISI ---
# Docker içinde servis adı "mongodb" olduğu için host olarak onu yazıyoruz.
client = MongoClient("mongodb://mongodb:27017")
db = client["okul_veritabani"]   # Veritabanı adı
koleksiyon = db["notlar"]        # Tablo (Collection) adı

# --- MODELLER ---
class NotHesaplamaRequest(BaseModel):
    vize_notu: float
    final_notu: float
    butunleme_notu: Optional[float] = None 

class NotHesaplamaResponse(BaseModel):
    kullanilan_vize_notu: float
    kullanilan_final_notu: float
    gecme_notu: float
    durum: str
    aciklama: str

# --- UYGULAMA ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/hesapla", response_model=NotHesaplamaResponse, dependencies=[Depends(token_dogrula)])
def hesapla_not(request: NotHesaplamaRequest):
    vize = request.vize_notu
    if request.butunleme_notu is not None:
        son_not = request.butunleme_notu
        kaynak = "Bütünleme"
    else:
        son_not = request.final_notu
        kaynak = "Final"

    gecme_notu = (vize * 0.40) + (son_not * 0.60)
    
    if gecme_notu >= 60 and son_not >= 60:
        durum = "Geçti"
        aciklama = f"Tebrikler! Ortalama: {gecme_notu:.2f}"
    else:
        durum = "Geçmedi"
        aciklama = f"Maalesef kaldınız. Ortalama: {gecme_notu:.2f}"
    
    # --- VERİTABANINA KAYDETME İŞLEMİ ---
    kayit = {
        "vize": vize,
        "final_veya_but": son_not,
        "ortalama": round(gecme_notu, 2),
        "durum": durum,
        "tarih": datetime.datetime.now()
    }
    koleksiyon.insert_one(kayit) # MongoDB'ye yaz
    # ------------------------------------

    return NotHesaplamaResponse(
        kullanilan_vize_notu=vize,
        kullanilan_final_notu=son_not,
        gecme_notu=round(gecme_notu, 2),
        durum=durum,
        aciklama=aciklama
    )

# Veritabanının çalıştığını test etmek için basit bir endpoint
@app.get("/gecmis-kayitlar")
def gecmis_listele():
    kayitlar = []
    # Son 10 kaydı getir, _id alanını (ObjectId) stringe çevir
    for k in koleksiyon.find().sort("tarih", -1).limit(10):
        k["_id"] = str(k["_id"])
        kayitlar.append(k)
    return kayitlar
