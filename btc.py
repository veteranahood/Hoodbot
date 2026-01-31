import requests
def usd_to_btc(usd):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price",params={"ids":"bitcoin","vs_currencies":"usd"}).json()
        return usd/r["bitcoin"]["usd"]
    except:
        return None
