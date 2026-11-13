"""
generate_data.py — Pembuat dataset sintetis untuk DEMO & PENGUJIAN SIAGA.

Kenapa data sintetis?
    1. Reproducible: juri bisa menjalankan ulang dan mendapat hasil sama,
       tanpa perlu kunci API berbayar atau menunggu scraping.
    2. Punya "ground truth": kita tahu akun mana yang SENGAJA kita jadikan
       buzzer, sehingga akurasi SIAGA bisa diukur jujur (precision/recall).
    3. Etis & legal: tidak menyimpan data pribadi orang asli.

Dataset meniru ciri dunia nyata operasi informasi di Indonesia:
    - mayoritas akun ORGANIK: posting beragam, waktu acak, sedikit duplikasi
    - beberapa KLASTER BUZZER: memposting pesan nyaris identik, serempak,
      membanjiri hashtag kampanye tertentu dalam lonjakan waktu singkat

Jalankan:  python generate_data.py --out data/posts.csv --seed 42
Keluaran:  CSV dengan kolom account_id,timestamp,text,is_buzzer,campaign
           (is_buzzer & campaign hanya untuk evaluasi; TIDAK dipakai mesin)
"""

from __future__ import annotations

import argparse
import os
import random
from datetime import datetime, timedelta

import pandas as pd

# ---------------------------------------------------------------------------
# Bahan-bahan teks (sengaja sederhana & netral — ini DATA SINTETIS, bukan
# menyasar pihak nyata). Tim bisa mengganti dengan korpus publik di Minggu 2.
# ---------------------------------------------------------------------------
ORGANIC_TEMPLATES = [
    "Macet parah di tol pagi ini, semoga lancar yang berangkat kerja",
    "Rekomendasi tempat makan enak di sekitar sini dong",
    "Baru selesai nonton film bagus akhir pekan ini",
    "Cuaca mendung terus, jangan lupa bawa payung ya",
    "Lagi belajar coding Python, seru juga ternyata",
    "Harga cabai naik lagi di pasar dekat rumah",
    "Semangat buat yang lagi skripsi, pasti bisa",
    "Timnas main bagus tadi malam, bangga banget",
    "Ada yang tau cara memperbaiki wifi sering putus?",
    "Libur panjang enaknya ke pantai atau ke gunung ya",
    "Kopi pagi ini bikin mood jadi lebih baik",
    "Jalanan sepi banget hari ini tumben",
    "Lagi hemat-hemat nih akhir bulan",
    "Selamat pagi semuanya, semoga harimu menyenangkan",
    "Buku baru sudah sampai, siap dibaca minggu ini",
]

ORGANIC_HASHTAGS = [
    "#weekend", "#kuliner", "#traveling", "#belajar", "#timnas",
    "#cuaca", "#jakarta", "#motivasi", "#teknologi", "#olahraga",
]

# Narasi kampanye buzzer (NETRAL/sintetis). Tiap kampanye punya pesan inti
# yang akan diulang-ulang dengan variasi kecil oleh klaster akunnya.
CAMPAIGNS = {
    "kampanye_A": {
        "core": "Program ini gagal total dan hanya membuang anggaran negara percuma",
        "variants": [
            "Program ini gagal total dan hanya membuang anggaran negara",
            "Faktanya program ini gagal total, anggaran negara terbuang percuma",
            "Jelas program ini gagal total dan membuang anggaran negara sia-sia",
            "Program ini benar benar gagal total, buang buang anggaran negara",
        ],
        "hashtags": ["#programgagal", "#buanganggaran"],
        "n_accounts": 8,
    },
    "kampanye_B": {
        "core": "Dukung penuh kebijakan baru ini demi masa depan bangsa yang lebih baik",
        "variants": [
            "Dukung penuh kebijakan baru ini demi masa depan bangsa lebih baik",
            "Mari dukung kebijakan baru ini untuk masa depan bangsa yang baik",
            "Saya dukung penuh kebijakan baru demi masa depan bangsa lebih baik",
            "Dukung terus kebijakan baru ini, masa depan bangsa jadi lebih baik",
        ],
        "hashtags": ["#dukungkebijakan", "#majubangsa"],
        "n_accounts": 10,
    },
    "kampanye_C": {
        "core": "Awas berita ini hoaks jangan mudah percaya sebarkan yang benar",
        "variants": [
            "Awas berita ini hoaks, jangan mudah percaya, sebarkan yang benar",
            "Hati hati berita ini hoaks, jangan percaya, sebar yang benar saja",
            "Berita ini hoaks ya, jangan mudah percaya, mari sebarkan yang benar",
        ],
        "hashtags": ["#stophoaks", "#saringbelumsharing"],
        "n_accounts": 6,
    },
}


def _rand_account(prefix: str, i: int) -> str:
    return f"{prefix}_{i:04d}"


def generate(
    n_organic_accounts: int = 120,
    n_organic_posts: int = 1500,
    start: datetime = datetime(2026, 10, 18, 8, 0, 0),
    seed: int = 42,
) -> pd.DataFrame:
    random.seed(seed)
    rows = []

    # ------------------------------------------------------------------
    # 1. LALU LINTAS ORGANIK — waktu acak selama ~2 hari, teks beragam
    # ------------------------------------------------------------------
    organic_accounts = [_rand_account("user", i) for i in range(n_organic_accounts)]
    for _ in range(n_organic_posts):
        acc = random.choice(organic_accounts)
        text = random.choice(ORGANIC_TEMPLATES)
        if random.random() < 0.3:
            text += " " + random.choice(ORGANIC_HASHTAGS)
        ts = start + timedelta(minutes=random.randint(0, 60 * 40))
        rows.append((acc, ts, text, 0, "organik"))

    # ------------------------------------------------------------------
    # 2. KLASTER BUZZER — tiap kampanye: sekelompok akun memposting pesan
    #    nyaris identik, SEREMPAK (dalam jendela waktu sempit), membanjiri
    #    hashtag kampanye. Inilah sinyal yang harus ditangkap SIAGA.
    # ------------------------------------------------------------------
    for cname, cfg in CAMPAIGNS.items():
        buzz_accounts = [_rand_account(cname, i) for i in range(cfg["n_accounts"])]
        # pilih 2-3 "gelombang" serempak
        n_waves = random.randint(2, 3)
        for _ in range(n_waves):
            # semua akun klaster memposting dalam jendela ~8 menit (sinkron)
            wave_start = start + timedelta(minutes=random.randint(0, 60 * 38))
            for acc in buzz_accounts:
                # tiap akun kirim 1-3 post pada gelombang ini
                for _ in range(random.randint(1, 3)):
                    variant = random.choice(cfg["variants"])
                    tag = random.choice(cfg["hashtags"])
                    text = f"{variant} {tag}"
                    # sedikit "penyamaran": kadang tambah hashtag organik
                    if random.random() < 0.25:
                        text += " " + random.choice(ORGANIC_HASHTAGS)
                    ts = wave_start + timedelta(seconds=random.randint(0, 8 * 60))
                    rows.append((acc, ts, text, 1, cname))

    df = pd.DataFrame(rows, columns=["account_id", "timestamp", "text", "is_buzzer", "campaign"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


def main():
    ap = argparse.ArgumentParser(description="Generator dataset sintetis SIAGA")
    ap.add_argument("--out", default="data/posts.csv")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    df = generate(seed=args.seed)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    df.to_csv(args.out, index=False)

    n_buzz = int(df["is_buzzer"].sum())
    print(f"[OK] {len(df)} post dibuat -> {args.out}")
    print(f"     Akun unik      : {df['account_id'].nunique()}")
    print(f"     Post buzzer     : {n_buzz} ({n_buzz/len(df)*100:.1f}%)")
    print(f"     Kampanye        : {df['campaign'].nunique()-1} klaster terkoordinasi")
    print(f"     Rentang waktu   : {df['timestamp'].min()}  ->  {df['timestamp'].max()}")


if __name__ == "__main__":
    main()
