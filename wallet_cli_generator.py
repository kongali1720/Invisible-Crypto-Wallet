import secrets
import json
import random

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
    wallet = {
        "private_key": priv_key,
        "address": "invisible_wallet_" + priv_key[:8],
        "balance": generate_random_balance(),
        "alerts_enabled": random.choice([True, False]),
        "features": features if features else generate_random_features()
    }
    return wallet

def generate_wallets(n=5, features=None):
    return [generate_wallet(features) for _ in range(n)]

def save_wallets_to_json(wallets, filename="wallet_samples.json"):
    with open(filename, "w") as f:
        json.dump(wallets, f, indent=2)
    print(f"\n🔥 {len(wallets)} wallets berhasil disimpan ke '{filename}'")

def main():
    print("👻 Invisible Wallet CLI Generator")
    print("💡 Pilih mode generate wallet\n")

    try:
        count = int(input("📦 Berapa banyak wallet yang mau dibuat? (cth: 5): "))
    except ValueError:
        print("❌ Masukkan angka yang valid!")
        return

    print("\n🔧 Mau pakai fitur acak atau pilih sendiri?")
    print("1. 🎲 Fitur Acak")
    print("2. ✍️  Pilih Fitur Manual")

    choice = input("Pilih (1/2): ")

    features = None
    if choice.strip() == "2":
        print("\n✅ Pilih fitur dari daftar berikut:")
        for i, feat in enumerate(FEATURE_POOL, 1):
            print(f"{i}. {feat}")
        selected = input("Masukkan nomor fitur (pisahkan dengan koma): ")
        try:
            indexes = [int(i.strip()) - 1 for i in selected.split(",")]
            features = [FEATURE_POOL[i] for i in indexes if 0 <= i < len(FEATURE_POOL)]
        except:
            print("❌ Input fitur tidak valid. Gunakan fitur acak saja.")
            features = None

    wallets = generate_wallets(count, features)
    save_wallets_to_json(wallets)

if __name__ == "__main__":
    main()
