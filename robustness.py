"""
robustness.py — Logika uji ketahanan anti-penyamaran (dipakai bersama).

Modul ini berisi inti uji ketahanan agar bisa dipakai oleh:
    - evaluate_robustness.py  (CLI, cetak tabel ke terminal)
    - dashboard.py            (tombol "Jalankan uji ketahanan" interaktif)

Taktik penyamaran yang disimulasikan HANYA pada post buzzer (is_buzzer==1):
    sisip     : menyelipkan kata netral agar teks tampak berbeda
    sinonim   : mengganti sebagian kata dengan sinonim
    acak_waktu: menyebar waktu posting agar tak terlihat serempak
"""

from __future__ import annotations

import random
from typing import Dict, List

import pandas as pd

from .coordination import prepare, build_coordination_graph, detect_clusters

_FILLER = [
    "menurut saya", "sebenarnya", "jujur saja", "btw", "oh ya", "ngomong-ngomong",
    "yang jelas", "intinya", "nah", "gini loh", "serius", "fyi", "pokoknya",
]
_SYNONYMS = {
    "gagal": "tidak berhasil", "total": "sepenuhnya", "membuang": "memboroskan",
    "anggaran": "dana", "negara": "pemerintah", "dukung": "sokong",
    "kebijakan": "aturan", "masa depan": "hari esok", "bangsa": "rakyat",
    "lebih baik": "makin bagus", "awas": "hati-hati", "berita": "kabar",
    "percaya": "yakin", "sebarkan": "bagikan", "benar": "tepat",
}

SCENARIOS = [
    ("Tanpa penyamaran", []),
    ("Sisip kata", ["sisip"]),
    ("Ganti sinonim", ["sinonim"]),
    ("Acak waktu", ["acak_waktu"]),
    ("Gabungan (terburuk)", ["sisip", "sinonim", "acak_waktu"]),
]


def _insert_filler(text: str, rng: random.Random) -> str:
    words = text.split()
    for _ in range(rng.randint(1, 3)):
        words.insert(rng.randint(0, len(words)), rng.choice(_FILLER))
    return " ".join(words)


def _swap_synonyms(text: str, rng: random.Random) -> str:
    out = text
    for word, syn in _SYNONYMS.items():
        if word in out and rng.random() < 0.7:
            out = out.replace(word, syn)
    return out


def harden(df: pd.DataFrame, tactics: List[str], seed: int = 7) -> pd.DataFrame:
    """Terapkan taktik penyamaran pada post buzzer saja (butuh kolom is_buzzer)."""
    rng = random.Random(seed)
    df = df.copy()
    mask = df["is_buzzer"] == 1
    if "sisip" in tactics:
        df.loc[mask, "text"] = df.loc[mask, "text"].map(lambda t: _insert_filler(t, rng))
    if "sinonim" in tactics:
        df.loc[mask, "text"] = df.loc[mask, "text"].map(lambda t: _swap_synonyms(t, rng))
    if "acak_waktu" in tactics:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        jitter = df.loc[mask].apply(
            lambda _: pd.Timedelta(minutes=rng.randint(0, 90)), axis=1)
        df.loc[mask, "timestamp"] = df.loc[mask, "timestamp"] + jitter
    return df


def _evaluate(df: pd.DataFrame, bucket: int, sim: float,
              min_edge: float, min_score: float) -> Dict[str, float]:
    truth = set(df[df["is_buzzer"] == 1]["account_id"].unique())
    dfx = prepare(df, bucket_minutes=bucket)
    G = build_coordination_graph(dfx, sim_threshold=sim)
    clusters = detect_clusters(dfx, G, min_edge_weight=min_edge)
    flagged = set(a for c in clusters for a in c.accounts
                  if c.coordination_score >= min_score)
    tp = len(flagged & truth); fp = len(flagged - truth); fn = len(truth - flagged)
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return {"precision": round(p, 2), "recall": round(r, 2), "f1": round(f1, 2)}


def run_scenarios(df: pd.DataFrame, bucket: int = 5, sim: float = 0.80,
                  min_edge: float = 3.0, min_score: float = 0.25) -> pd.DataFrame:
    """
    Jalankan semua skenario penyamaran pada `df` (harus punya kolom is_buzzer)
    dan kembalikan DataFrame hasil (Skenario, Precision, Recall, F1).
    """
    rows = []
    for name, tactics in SCENARIOS:
        d = df if not tactics else harden(df, tactics)
        m = _evaluate(d, bucket, sim, min_edge, min_score)
        rows.append({"Skenario penyamaran": name, "Precision": m["precision"],
                     "Recall": m["recall"], "F1": m["f1"]})
    return pd.DataFrame(rows)
