from mcp.server.fastmcp import FastMCP
import requests

# Servisimizin adı
mcp = FastMCP("Ders Odev MCP Servisi")

# 1. ARAÇ: Basit Toplama İşlemi (Tool)
@mcp.tool()
def toplama_yap(sayi1: int, sayi2: int) -> int:
    """İki sayıyı toplar."""
    return sayi1 + sayi2

# 2. ARAÇ: Public API'den Veri Çekme (Requests ile)
@mcp.tool()
def kripto_fiyat_getir(coin_id: str = "bitcoin") -> str:
    """
    CoinGecko Public API kullanarak belirtilen kripto paranın 
    (bitcoin, ethereum vb.) güncel dolar fiyatını getirir.
    """
    try:
        # Hoca 'requests' kullanın dediği yer:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        
        # Gelen JSON verisini işle
        data = response.json()
        
        if coin_id in data:
            fiyat = data[coin_id]["usd"]
            return f"1 {coin_id} şu an {fiyat} USD değerindedir."
        else:
            return "Hata: Geçersiz coin ismi girdiniz."
            
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"

# Docker içinde çalışması için
if __name__ == "__main__":
    mcp.run()
