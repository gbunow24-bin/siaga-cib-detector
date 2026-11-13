"""
api.py — REST API SIAGA (FastAPI) untuk integrasi ke pusat komando.

Kenapa penting untuk "bisa dipakai TNI Siber"?
    Dashboard bagus untuk analis, tapi sistem komando butuh ANTARMUKA MESIN:
    kirim sekumpulan unggahan, terima kembali klaster + watchlist + peringatan
    dalam format JSON yang bisa ditelan sistem lain. API ini menjadikan SIAGA
    sebuah komponen yang dapat ditanam (embeddable), bukan sekadar aplikasi
    berdiri sendiri.

Menjalankan server:
    pip install fastapi uvicorn
    uvicorn api:app --host 0.0.0.0 --port 8000
    lalu buka dokumentasi interaktif di  http://localhost:8000/docs

Endpoint:
    GET  /health            -> cek sistem hidup
    POST /analyze           -> kirim daftar post, terima hasil deteksi lengkap

Contoh body POST /analyze:
    {
      "posts": [
        {"account_id":"u1","timestamp":"2026-10-18T08:00:00","text":"halo #promo"},
        ...
      ],
      "min_score": 0.25
    }
"""

from __future__ import annotations

from typing import List, Optional
from dataclasses import asdict

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from siaga.coordination import prepare, build_coordination_graph, detect_clusters
from siaga.earlywarning import detect_emerging_narratives
from siaga.watchlist import build_watchlist
from siaga import __version__

app = FastAPI(
    title="SIAGA API",
    description="Deteksi Coordinated Inauthentic Behavior berbahasa Indonesia",
    version=__version__,
)


class Post(BaseModel):
    account_id: str
    timestamp: str
    text: str


class AnalyzeRequest(BaseModel):
    posts: List[Post] = Field(..., min_length=1)
    bucket_minutes: int = 5
    sim_threshold: float = 0.80
    min_edge_weight: float = 3.0
    min_score: float = 0.25


class ClusterOut(BaseModel):
    cluster_id: int
    accounts: List[str]
    coordination_score: float
    size: int
    top_hashtags: List[str]


class AnalyzeResponse(BaseModel):
    n_posts: int
    n_accounts: int
    n_clusters: int
    n_flagged_accounts: int
    clusters: List[ClusterOut]
    alerts: list
    watchlist: list


@app.get("/health")
def health():
    """Cek sederhana bahwa layanan hidup."""
    return {"status": "ok", "service": "SIAGA", "version": __version__}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    """
    Jalankan deteksi koordinasi penuh pada sekumpulan post.
    Mengembalikan klaster terdeteksi, peringatan dini, dan watchlist per-akun.
    """
    df = pd.DataFrame([p.model_dump() for p in req.posts])
    df = prepare(df, bucket_minutes=req.bucket_minutes)
    G = build_coordination_graph(df, sim_threshold=req.sim_threshold)
    all_clusters = detect_clusters(df, G, min_edge_weight=req.min_edge_weight)
    clusters = [c for c in all_clusters if c.coordination_score >= req.min_score]
    flagged = set(a for c in clusters for a in c.accounts)
    alerts = detect_emerging_narratives(df, flagged)
    wl = build_watchlist(df, clusters)

    return AnalyzeResponse(
        n_posts=int(len(df)),
        n_accounts=int(df["account_id"].nunique()),
        n_clusters=len(clusters),
        n_flagged_accounts=len(flagged),
        clusters=[
            ClusterOut(
                cluster_id=c.cluster_id,
                accounts=c.accounts,
                coordination_score=c.coordination_score,
                size=c.size,
                top_hashtags=c.top_hashtags,
            )
            for c in clusters
        ],
        alerts=[asdict(a) for a in alerts],
        watchlist=wl.to_dict(orient="records"),
    )
