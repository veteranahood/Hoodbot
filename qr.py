import qrcode
def generate_qr(address):
    img=qrcode.make("bitcoin:"+address)
    img.save("btc_qr.png")
