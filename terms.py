import os, json, time, hashlib
TERMS_FILE="terms_acceptance.json"
TERMS_TEXT="""
HoodBot By Anthony Hood TERMS & CONDITIONS
THIS SOFTWARE IS PROVIDED AS-IS.
TRADING CRYPTOCURRENCIES INVOLVES HIGH RISK.
NO PROFITS GUARANTEED.
ALL LOSSES ARE YOUR RESPONSIBILITY.
DONATIONS VOLUNTARY BTC ONLY.
"""
def require_terms_acceptance():
    if not os.path.exists(TERMS_FILE):
        print(TERMS_TEXT)
        name = input("Type full name to accept terms: ")
        sig={"name":name,"timestamp":time.time(),"hash":hashlib.sha256(name.encode()).hexdigest()}
        with open(TERMS_FILE,"w") as f:
            json.dump(sig,f)
