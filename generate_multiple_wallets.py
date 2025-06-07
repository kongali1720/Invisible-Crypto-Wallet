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
    # Random saldo antara 0 sampai 20 dengan 3 desimal
    return round(random.uniform(0, 20), 3)

def generate_random_features():
    # Pilih 2-4 fitur random dari pool
    return random.sample(FEATURE_POOL, random.randint(2, 4))

def generate_wallet():
    priv_key = generate_private_key()
    wallet = {
        "private_key": priv_key,
        "address": "invisible_wallet_" + priv_key[:8],
        "balance": generate_random_balance(),
        "alerts_enabled": random.choice([True, False]),
        "features": generate_random_features()
    }
    return wallet

def generate_wallets(n=5):
    return [generate_wallet() for _ in range(n)]

def save_wallets_to_json(wallets, filename="wallet_samples.json"):
    with open(filename, "w") as f:
        json.dump(wallets, f, indent=2)
    print(f"🔥 {len(wallets)} wallets berhasil disimpan ke '{filename}'")

if __name__ == "__main__":
    count = 10  # jumlah wallet yang mau dibuat
    wallets = generate_wallets(count)
    save_wallets_to_json(wallets)
