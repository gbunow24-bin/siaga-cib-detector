"""
watchlist.py — Daftar pantau (watchlist) per-akun yang dapat ditindaklanjuti.

Keluaran mesin (klaster) berguna untuk analisis, tapi satuan di lapangan butuh
sesuatu yang OPERASIONAL: daftar akun konkret, risikonya, dan BUKTI kenapa
ditandai — dalam format yang bisa diekspor, dibagikan, dan ditindaklanjuti.

Modul ini mengubah klaster terdeteksi menjadi tabel per-akun berisi:
    account_id, cluster_id, risk_score, n_posts, top_hashtags,
    contoh_narasi, first_seen, last_seen, alasan

Lalu mengekspornya ke CSV (siap dibuka di Excel / masuk ke sistem lain).
"""

from __future__ import annotations

from typing import List

import pandas as pd

from .coordination import Cluster


def build_watchlist(df: pd.DataFrame, clusters: List[Cluster]) -> pd.DataFrame:
    """
    Bangun tabel watchlist per-akun dari klaster yang terdeteksi.

    df harus sudah melewati coordination.prepare() (punya kolom hashtags,
    timestamp, text). Setiap akun dalam klaster menjadi satu baris, mewarisi
    skor koordinasi klasternya sebagai risk_score, dilengkapi bukti ringkas.
    """
    rows = []
    for c in clusters:
        for acc in c.accounts:
            sub = df[df["account_id"] == acc]
            tags = [t for tags in sub["hashtags"] for t in tags]
            top_tags = (
                pd.Series(tags).value_counts().head(3).index.tolist() if tags else []
            )
            sample = sub["text"].iloc[0] if len(sub) else ""
            rows.append({
                "account_id": acc,
                "cluster_id": c.cluster_id,
                "risk_score": c.coordination_score,
                "n_posts": int(len(sub)),
                "top_hashtags": " ".join("#" + t for t in top_tags),
                "contoh_narasi": sample[:120],
                "first_seen": str(sub["timestamp"].min()) if len(sub) else "",
                "last_seen": str(sub["timestamp"].max()) if len(sub) else "",
                "alasan": (
                    f"anggota klaster #{c.cluster_id}: kemiripan isi "
                    f"{c.content_similarity}, sinkronisasi {c.synchrony}"
                ),
            })
    wl = pd.DataFrame(rows)
    if not wl.empty:
        wl = wl.sort_values(["risk_score", "cluster_id"], ascending=[False, True])
        wl = wl.reset_index(drop=True)
    return wl


def export_watchlist(df: pd.DataFrame, clusters: List[Cluster], path: str) -> int:
    """Tulis watchlist ke CSV. Kembalikan jumlah akun yang diekspor."""
    wl = build_watchlist(df, clusters)
    wl.to_csv(path, index=False)
    return len(wl)
