<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Ödev Not Sistemi</title>
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5; }
        .card { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 300px; }
        h2 { text-align: center; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #0056b3; }
        #sonuc { margin-top: 15px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Not Hesapla</h2>
        <input type="number" id="vize" placeholder="Vize Notunuz">
        <input type="number" id="final" placeholder="Final Notunuz">
        <button onclick="hesapla()">HESAPLA</button>
        <div id="sonuc"></div>
    </div>

    <script>
        async function hesapla() {
            const vize = document.getElementById('vize').value;
            const finalNotu = document.getElementById('final').value;
            const sonucDiv = document.getElementById('sonuc');

            try {
                // Backend'e istek atıyoruz (8000 portuna)
                const response = await fetch('http://localhost:8000/hesapla', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer gizlisifre123' // Token burada gönderiliyor
                    },
                    body: JSON.stringify({
                        vize_notu: parseFloat(vize),
                        final_notu: parseFloat(finalNotu)
                    })
                });

                if (response.status === 401) {
                    sonucDiv.innerText = "Hata: Yetkisiz Giriş (Token Geçersiz)!";
                    sonucDiv.style.color = "red";
                    return;
                }

                const data = await response.json();
                sonucDiv.innerText = data.durum + " - " + data.aciklama;
                sonucDiv.style.color = data.durum === "Geçti" ? "green" : "red";

            } catch (error) {
                sonucDiv.innerText = "Sunucuya bağlanılamadı!";
                sonucDiv.style.color = "red";
            }
        }
    </script>
</body>
</html>
