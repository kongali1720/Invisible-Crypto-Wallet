import secrets
import json
import os

def generate_private_key():
    """Generate 256-bit private key as hex string."""
    return secrets.token_hex(32)  # 64 hex chars

def create_wallet_data(private_key):
    """Buat data wallet dengan format sederhana."""
    return {
        "private_key": private_key,
        "address": "invisible_wallet_" + private_key[:8],
        "balance": 0.0,
        "alerts_enabled": True,
        "features": [
            "coinjoin_integration",
            "zero_knowledge_proof",
            "ip_masking",
            "backup_recovery"
        ]
    }

def save_wallet_to_json(wallet_data, filename="wallet.json"):
    """Simpan data wallet ke file JSON."""
    with open(filename, "w") as f:
        json.dump(wallet_data, f, indent=2)
    print(f"✅ Wallet berhasil disimpan ke '{filename}'")

def load_wallet_from_json(filename="wallet.json"):
    """Load data wallet dari file JSON."""
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' tidak ditemukan!")
        return None
    with open(filename, "r") as f:
        data = json.load(f)
    print(f"✅ Wallet berhasil dimuat dari '{filename}'")
    return data

def main():
    print("👻 Invisible-Crypto-Wallet Generator\n")
    priv_key = generate_private_key()
    print(f"🔑 Private Key: {priv_key}\n")

    wallet = create_wallet_data(priv_key)
    save_wallet_to_json(wallet)

    print("\n💾 Contoh load wallet dari file:")
    loaded_wallet = load_wallet_from_json()
    if loaded_wallet:
        print(json.dumps(loaded_wallet, indent=2))

if __name__ == "__main__":
    main()
