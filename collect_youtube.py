"""
collect_youtube.py — Ambil komentar YouTube -> langsung format CSV SIAGA.

Skrip ini memakai YouTube Data API v3 (resmi, kuota gratis) untuk:
  1. mencari video berdasarkan kata kunci / tagar,
  2. menarik komentar dari video-video itu,
  3. menyimpannya sebagai CSV berkolom: account_id, timestamp, text
     (plus kolom tambahan video_id & author_name untuk referensi).

Keluarannya LANGSUNG bisa dipakai SIAGA tanpa konektor:
    python run_pipeline.py --in data/youtube.csv --outdir out_yt
atau buka dashboard dan isi path data/youtube.csv.

-------------------------------------------------------------------------------
CARA MENDAPATKAN API KEY (gratis, ~5 menit):
  1. Buka https://console.cloud.google.com  (login akun Google).
  2. Buat project baru (mis. "SIAGA-Monitor").
  3. APIs & Services -> Library -> cari "YouTube Data API v3" -> Enable.
  4. APIs & Services -> Credentials -> Create Credentials -> API key -> salin.
-------------------------------------------------------------------------------

CARA PAKAI:
    python collect_youtube.py --api-key KUNCI_ANDA --query "kata kunci" \
        --max-videos 20 --max-comments 100 --out data/youtube.csv

    # mencari tagar:
    python collect_youtube.py --api-key KUNCI --query "#pemilu2029" --out data/yt.csv

Hanya memakai pustaka standar Python (urllib) — tidak perlu pip install apa pun.

CATATAN ETIS/LEGAL: hanya data publik, patuhi ToS YouTube & UU PDP (27/2022).
Jangan unggah data pribadi nyata ke repo publik.
"""

from __future__ import annotations

import argparse
import csv
import json
import ssl
import sys
import urllib.parse
import urllib.request

API_BASE = "https://www.googleapis.com/youtube/v3"


def _ssl_context():
    """
    Konteks SSL yang tahan masalah sertifikat di macOS. Di macOS, Python sering
    tidak menemukan sertifikat sistem (CERTIFICATE_VERIFY_FAILED). Bila paket
    `certifi` ada, pakai bundel sertifikatnya; bila tidak, pakai bawaan sistem.
    """
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


_SSL_CTX = _ssl_context()


def _get(endpoint: str, params: dict) -> dict:
    """Panggil satu endpoint API dan kembalikan JSON (atau lempar error jelas)."""
    url = f"{API_BASE}/{endpoint}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=_SSL_CTX) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        # pesan ramah untuk kesalahan yang paling sering terjadi
        if e.code == 403 and "quota" in body.lower():
            raise SystemExit("[GAGAL] Kuota API habis untuk hari ini. Coba besok "
                             "atau kurangi --max-videos/--max-comments.")
        if e.code in (400, 403) and "api key" in body.lower():
            raise SystemExit("[GAGAL] API key tidak valid / API belum di-Enable. "
                             "Cek kembali langkah pembuatan API key.")
        raise SystemExit(f"[GAGAL] HTTP {e.code} dari YouTube API:\n{body[:500]}")
    except urllib.error.URLError as e:
        reason = str(e.reason)
        if "CERTIFICATE_VERIFY_FAILED" in reason or "certificate" in reason.lower():
            raise SystemExit(
                "[GAGAL] Verifikasi sertifikat SSL gagal (umum di macOS).\n"
                "        Solusi: pasang paket certifi lalu jalankan ulang:\n"
                "            pip3 install certifi\n"
                "        (Alternatif: jalankan 'Install Certificates.command' di folder "
                "Applications/Python 3.x Anda.)")
        raise SystemExit(f"[GAGAL] Tidak bisa menghubungi YouTube API: {reason}")


def search_videos(api_key: str, query: str, max_videos: int) -> list:
    """Kembalikan daftar video_id hasil pencarian kata kunci/tagar."""
    ids, token = [], None
    while len(ids) < max_videos:
        params = {
            "part": "snippet", "q": query, "type": "video",
            "maxResults": min(50, max_videos - len(ids)), "key": api_key,
        }
        if token:
            params["pageToken"] = token
        data = _get("search", params)
        for item in data.get("items", []):
            vid = item.get("id", {}).get("videoId")
            if vid:
                ids.append(vid)
        token = data.get("nextPageToken")
        if not token:
            break
    return ids[:max_videos]


def fetch_comments(api_key: str, video_id: str, max_comments: int) -> list:
    """
    Kembalikan daftar baris komentar untuk satu video, dalam bentuk dict:
        account_id, timestamp, text, video_id, author_name
    """
    rows, token = [], None
    while len(rows) < max_comments:
        params = {
            "part": "snippet", "videoId": video_id,
            "maxResults": min(100, max_comments - len(rows)),
            "textFormat": "plainText", "key": api_key,
        }
        if token:
            params["pageToken"] = token
        try:
            data = _get("commentThreads", params)
        except SystemExit:
            # komentar mungkin dinonaktifkan di video ini -> lewati diam-diam
            break
        for item in data.get("items", []):
            s = item["snippet"]["topLevelComment"]["snippet"]
            acc = s.get("authorChannelId", {}).get("value") or s.get("authorDisplayName", "unknown")
            rows.append({
                "account_id": acc,
                "timestamp": s.get("publishedAt", ""),
                "text": s.get("textOriginal", s.get("textDisplay", "")),
                "video_id": video_id,
                "author_name": s.get("authorDisplayName", ""),
            })
        token = data.get("nextPageToken")
        if not token:
            break
    return rows


def main():
    ap = argparse.ArgumentParser(description="Ambil komentar YouTube -> CSV SIAGA")
    ap.add_argument("--api-key", required=True, help="API key YouTube Data API v3")
    ap.add_argument("--query", required=True, help="kata kunci atau #tagar")
    ap.add_argument("--max-videos", type=int, default=20, help="jumlah video (default 20)")
    ap.add_argument("--max-comments", type=int, default=100,
                    help="komentar per video (default 100)")
    ap.add_argument("--out", default="data/youtube.csv", help="file CSV keluaran")
    args = ap.parse_args()

    print(f"[1/3] Mencari video untuk: {args.query!r} …")
    vids = search_videos(args.api_key, args.query, args.max_videos)
    if not vids:
        raise SystemExit("[GAGAL] Tidak ada video ditemukan. Coba kata kunci lain.")
    print(f"      {len(vids)} video ditemukan.")

    print(f"[2/3] Menarik komentar (maks {args.max_comments}/video) …")
    all_rows = []
    for i, vid in enumerate(vids, 1):
        rows = fetch_comments(args.api_key, vid, args.max_comments)
        all_rows.extend(rows)
        print(f"      [{i}/{len(vids)}] {vid}: {len(rows)} komentar "
              f"(total {len(all_rows)})")

    if not all_rows:
        raise SystemExit("[GAGAL] Tidak ada komentar terkumpul (mungkin komentar nonaktif).")

    import os
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["account_id", "timestamp", "text",
                                          "video_id", "author_name"])
        w.writeheader()
        w.writerows(all_rows)

    print(f"[3/3] [OK] {len(all_rows)} komentar disimpan -> {args.out}")
    print(f"      Lanjutkan: python run_pipeline.py --in {args.out} --outdir out_yt")


if __name__ == "__main__":
    main()
