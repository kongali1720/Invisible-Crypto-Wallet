import secrets
import json
import random
import base64
import hashlib
from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

FEATURE_POOL = [
    "coinjoin_integration",
    "zero_knowledge_proof",
    "ip_masking",
    "backup_recovery",
    "stealth_address",
    "encrypted_memo"
]

def generate_private_key():
    return secrets.token_hex(32)

def generate_random_balance():
    return round(random.uniform(0, 20), 3)

def generate_random_features():
    return random.sample(FEATURE_POOL, random.randint(2, 4))

def generate_wallet(features=None):
    priv_key = generate_private_key()
    return {
        "private_key": priv_key,
        "address": "invisible_wallet_" + priv_key[:8],
        "balance": generate_random_balance(),
        "alerts_enabled": random.choice([True, False]),
        "features": features if features else generate_random_features()
    }

def generate_wallets(n=5, features=None):
    return [generate_wallet(features) for _ in range(n)]

# 🔐 AES encryption helpers
def derive_key(password: str):
    return hashlib.sha256(password.encode()).digest()

def encrypt_json(data: dict, password: str) -> bytes:
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(json.dumps(data).encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes)

def decrypt_json(encrypted_data: bytes, password: str) -> dict:
    raw = base64.b64decode(encrypted_data)
    key = derive_key(password)
    iv = raw[:16]
    ct = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return json.loads(unpad(cipher.decrypt(ct), AES.block_size))

def save_encrypted_wallet(data, filename, password):
    encrypted = encrypt_json(data, password)
    with open(filename, "wb") as f:
        f.write(encrypted)
    print(f"\n🔐 Wallet terenkripsi disimpan ke '{filename}'")

def load_encrypted_wallet(filename, password):
    with open(filename, "rb") as f:
        encrypted = f.read()
    try:
        data = decrypt_json(encrypted, password)
        print(json.dumps(data, indent=2))
    except:
        print("❌ Password salah atau file rusak.")

# 🧠 Main CLI
def main():
    print("\n👻 Invisible Wallet CLI [Secure Edition]")
    print("1. 🔨 Buat wallet terenkripsi")
    print("2. 🔓 Buka wallet terenkripsi")
    choice = input("\nPilih mode (1/2): ")

    if choice.strip() == "1":
        try:
            count = int(input("📦 Berapa banyak wallet? (cth: 5): "))
        except:
            print("❌ Masukkan angka valid.")
            return

        print("\n🎛️  Pilih fitur:")
        print("1. 🎲 Acak")
        print("2. ✍️  Manual")

        fmode = input("Fitur (1/2): ")
        features = None

        if fmode.strip() == "2":
            for i, f in enumerate(FEATURE_POOL, 1):
                print(f"{i}. {f}")
            picked = input("Pilih fitur (1,3,5,...): ")
            try:
                idx = [int(i.strip()) - 1 for i in picked.split(",")]
                features = [FEATURE_POOL[i] for i in idx if 0 <= i < len(FEATURE_POOL)]
            except:
                print("❌ Input salah. Gunakan fitur acak.")

        password = getpass("🔐 Masukkan password enkripsi: ")
        wallets = generate_wallets(count, features)
        save_encrypted_wallet(wallets, "wallet_samples.json.enc", password)

    elif choice.strip() == "2":
        password = getpass("🔑 Masukkan password untuk dekripsi: ")
        load_encrypted_wallet("wallet_samples.json.enc", password)

    else:
        print("❌ Pilihan tidak dikenal.")

if __name__ == "__main__":
    main()
