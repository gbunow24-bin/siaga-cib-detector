"""
earlywarning.py — Deteksi dini narasi menanjak yang didorong klaster koordinasi.

Nilai tambah untuk TNI AD (kategori Siber Sosial) bukan sekadar "mendeteksi
buzzer setelah viral", melainkan MEMBERI PERINGATAN DINI: menandai sebuah
hashtag / narasi yang BARU mulai naik TAPI dorongan awalnya didominasi oleh
akun-akun yang sudah teridentifikasi terkoordinasi. Inilah jendela waktu
ketika operasi informasi masih bisa dinetralkan sebelum menyebar organik.

Skor risiko dini menggabungkan:
    - kecepatan (velocity)      : laju kemunculan hashtag naik tajam
    - dominasi koordinasi (cib_share): porsi dorongan awal dari akun klaster
    - konsentrasi akun (narrowness) : sedikit akun menghasilkan banyak post
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set

import numpy as np
import pandas as pd


@dataclass
class NarrativeAlert:
    hashtag: str
    risk_score: float          # 0..1
    velocity: float
    cib_share: float           # porsi post dari akun terkoordinasi
    n_posts: int
    n_accounts: int
    first_seen: str
    sample_texts: List[str]


def _velocity(times: pd.Series, window_minutes: int = 60) -> float:
    """
    Laju kemunculan: bandingkan kepadatan post di jendela TERAKHIR dengan
    rata-rata sebelumnya. Nilai tinggi = sedang melonjak (bukan topik lama
    yang stabil).
    """
    if len(times) < 3:
        return 0.0
    times = times.sort_values()
    span_min = max((times.iloc[-1] - times.iloc[0]).total_seconds() / 60.0, 1.0)
    last_cut = times.iloc[-1] - pd.Timedelta(minutes=window_minutes)
    recent = (times >= last_cut).sum()
    recent_rate = recent / min(window_minutes, span_min)
    overall_rate = len(times) / span_min
    return float(recent_rate / (overall_rate + 1e-9))


def detect_emerging_narratives(
    df: pd.DataFrame,
    coordinated_accounts: Set[str],
    min_posts: int = 5,
    top_k: int = 15,
) -> List[NarrativeAlert]:
    """
    df harus sudah melewati coordination.prepare() (punya kolom hashtags,
    timestamp). coordinated_accounts = gabungan semua akun dari klaster
    terdeteksi (lihat run_pipeline).
    """
    # ledakkan (explode) hashtag menjadi baris-baris
    rows = []
    for _, r in df.iterrows():
        for h in r["hashtags"]:
            rows.append((h, r["account_id"], r["timestamp"], r["text"]))
    if not rows:
        return []
    ht = pd.DataFrame(rows, columns=["hashtag", "account_id", "timestamp", "text"])

    alerts: List[NarrativeAlert] = []
    for tag, grp in ht.groupby("hashtag"):
        if len(grp) < min_posts:
            continue
        vel = _velocity(grp["timestamp"])
        n_acc = grp["account_id"].nunique()
        cib_posts = grp["account_id"].isin(coordinated_accounts).sum()
        cib_share = cib_posts / len(grp)
        # konsentrasi: sedikit akun -> banyak post = tidak organik
        narrowness = 1.0 - (n_acc / len(grp))

        # normalisasi velocity ke 0..1 secara lembut
        vel_norm = float(np.tanh(vel / 2.0))

        risk = 0.45 * cib_share + 0.35 * vel_norm + 0.20 * narrowness
        risk = float(min(max(risk, 0.0), 1.0))

        alerts.append(
            NarrativeAlert(
                hashtag=tag,
                risk_score=round(risk, 3),
                velocity=round(vel_norm, 3),
                cib_share=round(float(cib_share), 3),
                n_posts=int(len(grp)),
                n_accounts=int(n_acc),
                first_seen=str(grp["timestamp"].min()),
                sample_texts=grp["text"].drop_duplicates().head(3).tolist(),
            )
        )

    alerts.sort(key=lambda a: a.risk_score, reverse=True)
    return alerts[:top_k]
