import secrets, json, random, base64, hashlib, os
from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import qrcode
from datetime import datetime

FEATURE_POOL = [
    "coinjoin_integration", "zkp_enabled", "ip_masking", "backup_recovery",
    "stealth_address", "encrypted_memo", "decoy_transactions", "tor_gateway"
]

def generate_private_key():
    return secrets.token_hex(32)

def generate_wallet(features=None):
    priv_key = generate_private_key()
    return {
        "private_key": priv_key,
        "address": "invisible_" + priv_key[:10],
        "balance": round(random.uniform(0.01, 10.0), 4),
        "features": features if features else random.sample(FEATURE_POOL, random.randint(3, 6)),
        "created_at": datetime.utcnow().isoformat()
    }

def derive_key(password): return hashlib.sha256(password.encode()).digest()

def encrypt_json(data, password):
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(json.dumps(data).encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct)

def decrypt_json(encrypted, password):
    raw = base64.b64decode(encrypted)
    key = derive_key(password)
    iv, ct = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return json.loads(unpad(cipher.decrypt(ct), AES.block_size))

def save_encrypted_wallet(data, filename, password):
    enc = encrypt_json(data, password)
    with open(filename, "wb") as f: f.write(enc)
    print(f"✅ Wallet terenkripsi tersimpan di {filename}")

def load_encrypted_wallet(filename, password):
    with open(filename, "rb") as f: enc = f.read()
    return decrypt_json(enc, password)

def export_qr(address):
    img = qrcode.make(address)
    filename = f"qr_{address}.png"
    img.save(filename)
    print(f"🧾 QR code disimpan: {filename}")

def export_html(wallets, outname="wallet_export.html"):
    with open(outname, "w") as f:
        f.write("<html><body><h2>👻 Invisible Wallet Export</h2><table border='1' cellpadding='5'>")
        f.write("<tr><th>Address</th><th>Balance</th><th>Features</th><th>Created</th></tr>")
        for w in wallets:
            f.write(f"<tr><td>{w['address']}</td><td>{w['balance']} ETH</td><td>{', '.join(w['features'])}</td><td>{w['created_at']}</td></tr>")
        f.write("</table></body></html>")
    print(f"📄 Export HTML: {outname}")

def search_wallet(wallets, query):
    results = [w for w in wallets if query.lower() in w['address'].lower()]
    if not results:
        print("❌ Tidak ditemukan.")
    else:
        for w in results:
            print(json.dumps(w, indent=2))
            export_qr(w["address"])

def main():
    print("\n👻 Invisible Wallet System (QR + Export Edition)")
    print("1️⃣ Buat & Simpan wallet terenkripsi")
    print("2️⃣ Buka & Cari wallet")
    print("3️⃣ Export QR & HTML")

    pilihan = input("Pilih mode (1/2/3): ").strip()

    if pilihan == "1":
        jumlah = int(input("Berapa wallet? "))
        password = getpass("Password enkripsi: ")
        wallets = [generate_wallet() for _ in range(jumlah)]
        save_encrypted_wallet(wallets, "wallet_data.enc", password)

    elif pilihan == "2":
        password = getpass("Password untuk buka file: ")
        wallets = load_encrypted_wallet("wallet_data.enc", password)
        print("✅ Data berhasil dibuka.\n")
        search = input("Cari alamat wallet: ").strip()
        search_wallet(wallets, search)

    elif pilihan == "3":
        password = getpass("Password untuk decrypt: ")
        wallets = load_encrypted_wallet("wallet_data.enc", password)
        export_html(wallets)
        for w in wallets:
            export_qr(w['address'])

    else:
        print("🚫 Opsi tidak dikenali.")

if __name__ == "__main__":
    main()
