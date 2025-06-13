import requests
import time

TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": pesan}
    requests.post(url, data=data)

def get_binance():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        return float(r.json()['price'])
    except:
        return None

def get_mexc():
    try:
        r = requests.get("https://api.mexc.com/api/v3/ticker/price?symbol=BTCUSDT")
        return float(r.json()['price'])
    except:
        return None

def cek_arbit():
    harga = {
        "Binance": get_binance(),
        "MEXC": get_mexc()
    }

    harga = {k: v for k, v in harga.items() if v is not None}
    if len(harga) < 2:
        print("❌ Tidak cukup data")
        return

    max_ex = max(harga, key=harga.get)
    min_ex = min(harga, key=harga.get)
    spread = ((harga[max_ex] - harga[min_ex]) / harga[min_ex]) * 100

    pesan = (
        f"📊 BTC/USDT Arbitrase:\n\n" +
        "\n".join([f"{ex}: ${price:,.2f}" for ex, price in harga.items()]) +
        f"\n\n📈 Spread: {spread:.2f}%\n💰 Buy: {min_ex} — Sell: {max_ex}"
    )

    print(pesan)
    if spread >= 0.5:
        kirim_telegram("🚨 ALERT 🚨\n\n" + pesan)

while True:
    cek_arbit()
    time.sleep(60)
