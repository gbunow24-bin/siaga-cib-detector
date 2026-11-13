"""
connect_data.py — Adapter data NYATA ke format standar SIAGA.

Mesin SIAGA hanya butuh tiga kolom: account_id, timestamp, text. Tapi data
nyata (arsip operasi informasi, ekspor platform, hasil scraping resmi) datang
dengan nama kolom berbeda-beda. Script ini memetakannya ke format standar,
tanpa menyentuh mesin deteksi.

Contoh sumber nyata & nama kolomnya (verifikasi saat mengunduh):
    - Arsip Twitter/X Information Operations : userid, tweet_time, tweet_text
    - Ekspor generik                         : user, created_at, content
    - CSV buatan tim                          : account, time, message

Pakai:
    # pemetaan default mencoba nama-nama umum secara otomatis
    python connect_data.py --in arsip_nyata.csv --out data/real.csv

    # atau tentukan pemetaan secara eksplisit
    python connect_data.py --in arsip.csv --out data/real.csv \
        --account userid --timestamp tweet_time --text tweet_text

Lalu jalankan seperti biasa:
    python run_pipeline.py --in data/real.csv --outdir out_real

Catatan etis & legal: gunakan hanya data publik / arsip resmi, patuhi ToS
platform dan UU PDP (27/2022). Jangan unggah data pribadi ke repo publik.
"""

from __future__ import annotations

import argparse
import sys

import pandas as pd

# Kandidat nama kolom umum -> dicoba otomatis bila --account/--timestamp/--text
# tidak diberikan.
CANDIDATES = {
    "account_id": ["account_id", "userid", "user_id", "user", "account", "author", "screen_name"],
    "timestamp": ["timestamp", "tweet_time", "created_at", "time", "date", "datetime", "post_time"],
    "text": ["text", "tweet_text", "content", "message", "body", "full_text", "caption"],
}


def _auto(colnames, wanted):
    low = {c.lower(): c for c in colnames}
    for cand in CANDIDATES[wanted]:
        if cand in low:
            return low[cand]
    return None


def main():
    ap = argparse.ArgumentParser(description="Adapter data nyata -> format SIAGA")
    ap.add_argument("--in", dest="inp", required=True, help="CSV sumber (data nyata)")
    ap.add_argument("--out", default="data/real.csv", help="CSV keluaran format SIAGA")
    ap.add_argument("--account", help="nama kolom account (opsional, auto bila kosong)")
    ap.add_argument("--timestamp", help="nama kolom waktu (opsional)")
    ap.add_argument("--text", help="nama kolom teks (opsional)")
    ap.add_argument("--sep", default=",", help="pemisah CSV sumber (default koma)")
    args = ap.parse_args()

    df = pd.read_csv(args.inp, sep=args.sep)
    cols = list(df.columns)

    acc = args.account or _auto(cols, "account_id")
    ts = args.timestamp or _auto(cols, "timestamp")
    txt = args.text or _auto(cols, "text")

    missing = [name for name, v in [("account", acc), ("timestamp", ts), ("text", txt)] if v is None]
    if missing:
        print(f"[GAGAL] Tidak bisa menebak kolom: {', '.join(missing)}.")
        print(f"        Kolom tersedia: {cols}")
        print(f"        Tentukan manual, mis.: --account {CANDIDATES['account_id'][1]} "
              f"--timestamp {CANDIDATES['timestamp'][1]} --text {CANDIDATES['text'][1]}")
        sys.exit(1)

    out = pd.DataFrame({
        "account_id": df[acc].astype(str),
        "timestamp": pd.to_datetime(df[ts], errors="coerce"),
        "text": df[txt].astype(str),
    })
    before = len(out)
    out = out.dropna(subset=["timestamp"])          # buang baris tanpa waktu valid
    out = out[out["text"].str.strip() != ""]        # buang teks kosong
    out.to_csv(args.out, index=False)

    print(f"[OK] {len(out)} baris ditulis -> {args.out}  (dari {before}, "
          f"{before-len(out)} dibuang karena waktu/teks tidak valid)")
    print(f"     Pemetaan: account='{acc}'  timestamp='{ts}'  text='{txt}'")
    print(f"     Lanjutkan: python run_pipeline.py --in {args.out} --outdir out_real")


if __name__ == "__main__":
    main()
