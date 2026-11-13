"""
features.py — Normalisasi teks Bahasa Indonesia & ekstraksi fitur jejak.

Tujuan modul ini: mengubah teks mentah (post / cuitan) menjadi bentuk yang
BISA DIBANDINGKAN antar-akun. Deteksi koordinasi bertumpu pada kemiripan;
kalau normalisasi teksnya lemah, "copy-paste terselubung" milik buzzer akan
lolos. Maka langkah ini adalah fondasi akurasi SIAGA.

Semua fungsi di sini MURNI (tanpa efek samping) agar mudah diuji satu per satu.
"""

from __future__ import annotations

import re
import unicodedata
from typing import List

# ---------------------------------------------------------------------------
# 1. Daftar pendek stopword Bahasa Indonesia.
#    Bukan daftar lengkap — cukup untuk menurunkan "berisik" kata sambung yang
#    muncul di hampir semua kalimat sehingga tidak mengaburkan sidik teks.
#    Tim bisa memperluas ini di Minggu 3 (lihat panduan master, bagian Roadmap).
# ---------------------------------------------------------------------------
STOPWORDS_ID = {
    "yang", "untuk", "dengan", "dari", "dan", "di", "ke", "ini", "itu", "pada",
    "adalah", "akan", "atau", "juga", "karena", "sudah", "saya", "kita", "kami",
    "mereka", "dia", "nya", "para", "oleh", "agar", "dalam", "tidak", "ada",
    "bisa", "harus", "lebih", "sangat", "saja", "kalau", "jika", "maka", "ya",
    "sih", "deh", "nih", "gak", "ga", "nggak", "banget", "aja", "kok", "tuh",
}

# Pola regex yang sering dipakai (dikompilasi sekali agar cepat pada data besar)
_RE_URL = re.compile(r"https?://\S+|www\.\S+")
_RE_MENTION = re.compile(r"@\w+")
_RE_HASHTAG = re.compile(r"#\w+")
_RE_NONWORD = re.compile(r"[^a-z0-9\s]")
_RE_SPACE = re.compile(r"\s+")
# Memanjangkan huruf untuk penekanan, mis. "baguuuus" -> "bagus"
_RE_ELONG = re.compile(r"(.)\1{2,}")


def extract_hashtags(text: str) -> List[str]:
    """Kembalikan daftar hashtag (lowercase, tanpa tanda #)."""
    return [h[1:].lower() for h in _RE_HASHTAG.findall(text or "")]


def extract_urls(text: str) -> List[str]:
    """Kembalikan daftar URL mentah yang muncul di teks."""
    return _RE_URL.findall(text or "")


def extract_mentions(text: str) -> List[str]:
    """Kembalikan daftar akun yang di-mention (lowercase, tanpa @)."""
    return [m[1:].lower() for m in _RE_MENTION.findall(text or "")]


def normalize_text(text: str, drop_stopwords: bool = True) -> str:
    """
    Normalisasi agresif supaya variasi 'copy-paste yang disamarkan' tetap
    terlihat mirip. Langkah:
      1. ke huruf kecil + normalisasi unicode (hapus aksen/emoji aneh)
      2. buang URL, mention, hashtag  (ditangani sebagai fitur terpisah)
      3. ringkas huruf berulang  (baguuus -> bagus)
      4. buang tanda baca & simbol
      5. buang stopword  (opsional)
      6. rapikan spasi
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")  # buang emoji/aksen
    text = text.lower()
    text = _RE_URL.sub(" ", text)
    text = _RE_MENTION.sub(" ", text)
    text = _RE_HASHTAG.sub(" ", text)
    text = _RE_ELONG.sub(r"\1", text)
    text = _RE_NONWORD.sub(" ", text)
    tokens = _RE_SPACE.sub(" ", text).strip().split()
    if drop_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS_ID and len(t) > 1]
    return " ".join(tokens)


def time_bucket(ts, minutes: int = 5) -> int:
    """
    Petakan timestamp ke 'ember waktu' (bucket) berukuran `minutes` menit.
    Dua akun yang memposting dalam ember yang sama dianggap SINKRON.
    Sinkronisasi waktu adalah salah satu sidik koordinasi terkuat: manusia
    organik tidak serempak memposting pesan yang sama di menit yang sama.
    """
    import pandas as pd

    ts = pd.Timestamp(ts)
    epoch_min = int(ts.value // 60_000_000_000)  # nanodetik -> menit
    return epoch_min // minutes
