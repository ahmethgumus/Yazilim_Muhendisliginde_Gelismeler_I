from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# --- Modeller ---

class NotHesaplamaRequest(BaseModel):
    vize_notu: float
    final_notu: float
    butunleme_notu: Optional[float] = None 
    
    class Config:
        schema_extra = {
            "example": {
                "vize_notu": 70,
                "final_notu": 50,
                "butunleme_notu": 85
            }
        }

class NotHesaplamaResponse(BaseModel):
    kullanilan_vize_notu: float
    kullanilan_final_notu: float
    gecme_notu: float
    durum: str
    aciklama: str

# --- Uygulama ---
app = FastAPI(
    title="Not Hesaplama API",
    description="Vize ve Final/Bütünleme notlarına göre geçme durumunu hesaplar.",
    version="1.0.0"
)

@app.post("/hesapla", response_model=NotHesaplamaResponse, tags=["Not Hesaplama"])
def hesapla_not(request: NotHesaplamaRequest):
    vize = request.vize_notu
    
    # Bütünleme varsa final yerine geçer
    if request.butunleme_notu is not None:
        son_not = request.butunleme_notu
        kaynak = "Bütünleme"
    else:
        son_not = request.final_notu
        kaynak = "Final"

    # Hesaplama: Vize %40 + Final/Büt %60
    gecme_notu = (vize * 0.40) + (son_not * 0.60)
    
    # Geçme Kuralı: Ortalama >= 55 VE (Final veya Büt) >= 55
    if gecme_notu >= 55 and son_not >= 55:
        durum = "Geçti"
        detay = f"Ortalama ({gecme_notu:.2f}) ve {kaynak} notu ({son_not}) 55 barajını geçti."
    else:
        durum = "Geçmedi"
        if son_not < 55:
            detay = f"{kaynak} notu ({son_not}) 55'in altında."
        else:
            detay = f"Ortalama ({gecme_notu:.2f}) 55'in altında."
            
    return NotHesaplamaResponse(
        kullanilan_vize_notu=vize,
        kullanilan_final_notu=son_not,
        gecme_notu=round(gecme_notu, 2),
        durum=durum,
        aciklama=detay
    )

@app.get("/", tags=["Genel"])
def read_root():
    return {"mesaj": "API çalışıyor. Dokümantasyon için /docs adresine gidin."}