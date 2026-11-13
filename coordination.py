"""
coordination.py — Inti ilmiah SIAGA: deteksi koordinasi antar-akun.

Ide pokok (dan sumber NOVELTY-nya):
    Alat lama (Botometer dkk.) menilai AKUN SATU PER SATU: "apakah akun ini bot?"
    Masalahnya, buzzer modern di Indonesia banyak yang DIOPERASIKAN MANUSIA,
    sehingga lolos deteksi per-akun. Yang membedakan operasi terkoordinasi
    BUKAN tiap akunnya, melainkan POLA KEBERSAMAAN mereka.

    SIAGA membalik pendekatannya: kami tidak bertanya "apakah akun X bot?",
    melainkan "akun mana saja yang BERGERAK BERSAMA secara tidak wajar?".

Kami membangun graf ko-aksi (co-action graph): simpul = akun, bobot sisi =
seberapa sering dua akun melakukan hal yang sama pada saat bersamaan. Tiga
saluran bukti digabung:
    (A) co-posting sinkron   : teks sangat mirip pada ember waktu yang sama
    (B) co-hashtag berbarengan: memakai hashtag yang sama dalam lonjakan
    (C) co-URL               : menyebar tautan identik
Lalu kami cari komunitas padat pada graf itu (klaster koordinasi), dan
beri setiap klaster sebuah COORDINATION SCORE yang bisa dijelaskan.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, List, Tuple

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .features import normalize_text, extract_hashtags, extract_urls, time_bucket


# ---------------------------------------------------------------------------
# Struktur hasil
# ---------------------------------------------------------------------------
@dataclass
class Cluster:
    cluster_id: int
    accounts: List[str]
    coordination_score: float          # 0..1, makin tinggi makin mencurigakan
    size: int
    synchrony: float                   # komponen waktu
    content_similarity: float          # komponen kemiripan isi
    top_hashtags: List[str]
    top_narratives: List[str]
    evidence: Dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Langkah 1 — Siapkan dataframe: normalisasi + fitur per post
# ---------------------------------------------------------------------------
def prepare(df: pd.DataFrame, bucket_minutes: int = 5) -> pd.DataFrame:
    """
    Terima dataframe dengan kolom minimal:
        account_id, timestamp, text
    Tambahkan kolom turunan yang dibutuhkan mesin koordinasi.
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["clean"] = df["text"].map(lambda t: normalize_text(t))
    df["hashtags"] = df["text"].map(extract_hashtags)
    df["urls"] = df["text"].map(extract_urls)
    df["tbucket"] = df["timestamp"].map(lambda t: time_bucket(t, bucket_minutes))
    return df


# ---------------------------------------------------------------------------
# Langkah 2 — Saluran bukti (A): co-posting SINKRON teks mirip
# ---------------------------------------------------------------------------
def _edges_from_text_synchrony(
    df: pd.DataFrame, sim_threshold: float = 0.80, bucket_col: str = "tbucket"
) -> Dict[Tuple[str, str], float]:
    """
    Untuk tiap ember waktu, bandingkan semua post di dalamnya. Pasangan akun
    yang teksnya mirip >= ambang pada ember yang sama -> bukti koordinasi.

    Memproses per-ember membuat perbandingan O(k^2) hanya di dalam ember kecil,
    bukan O(n^2) pada seluruh data — jauh lebih ringan & relevan (fokus ke
    kejadian yang benar-benar serempak).
    """
    weights: Dict[Tuple[str, str], float] = defaultdict(float)

    for _, grp in df.groupby(bucket_col):
        grp = grp[grp["clean"].str.len() > 0]
        if len(grp) < 2:
            continue
        # TF-IDF level karakter n-gram -> tahan terhadap sisipan kata/typo
        # yang sengaja dipakai buzzer untuk mengelabui filter kemiripan.
        try:
            vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
            mat = vec.fit_transform(grp["clean"].tolist())
        except ValueError:
            continue
        sim = cosine_similarity(mat)
        accounts = grp["account_id"].tolist()
        n = len(accounts)
        for i in range(n):
            for j in range(i + 1, n):
                if accounts[i] == accounts[j]:
                    continue
                s = sim[i, j]
                if s >= sim_threshold:
                    key = tuple(sorted((accounts[i], accounts[j])))
                    # akumulasi: makin sering serempak-mirip, makin kuat sisi
                    weights[key] += float(s)
    return weights


# ---------------------------------------------------------------------------
# Langkah 3 — Saluran bukti (B) & (C): co-hashtag & co-URL
# ---------------------------------------------------------------------------
def _edges_from_shared_tokens(
    df: pd.DataFrame, col: str, min_rarity: int = 2, bucket_col: str = "tbucket",
    max_global_accounts: int | None = None,
) -> Dict[Tuple[str, str], float]:
    """
    Dua akun yang berbagi hashtag/URL yang sama DI EMBER WAKTU yang sama
    mendapat bukti. Token yang dipakai banyak akun (sangat umum) diberi bobot
    kecil (idf-like), token langka yang tiba-tiba dipakai serempak diberi
    bobot besar — inilah ciri "flooding" hashtag oleh pasukan buzzer.

    `max_global_accounts`: bila diisi, token yang secara GLOBAL dipakai lebih
    dari sekian akun unik diabaikan. Dipakai pada lintasan ember kasar untuk
    membatasi diri hanya pada hashtag khas-kampanye (dipakai sedikit akun),
    sehingga hashtag populer organik tidak menimbulkan salah-tangkap.
    """
    weights: Dict[Tuple[str, str], float] = defaultdict(float)

    # frekuensi global token -> untuk bobot kelangkaan (makin langka makin berarti)
    global_freq: Dict[str, int] = defaultdict(int)
    global_accounts: Dict[str, set] = defaultdict(set)
    for _, row in df.iterrows():
        for t in set(row[col]):
            global_freq[t] += 1
            global_accounts[t].add(row["account_id"])

    for _, grp in df.groupby(bucket_col):
        token_to_accounts: Dict[str, set] = defaultdict(set)
        for _, row in grp.iterrows():
            for t in set(row[col]):
                token_to_accounts[t].add(row["account_id"])
        for t, accts in token_to_accounts.items():
            if len(accts) < min_rarity:
                continue
            if max_global_accounts is not None and len(global_accounts[t]) > max_global_accounts:
                continue
            # bobot kelangkaan: idf = log(N / df_token)
            idf = np.log(len(df) / (1 + global_freq[t]))
            w = max(idf, 0.1)
            for a, b in combinations(sorted(accts), 2):
                weights[(a, b)] += float(w)
    return weights


# ---------------------------------------------------------------------------
# Langkah 4 — Gabungkan saluran bukti -> satu graf koordinasi
# ---------------------------------------------------------------------------
def build_coordination_graph(
    df: pd.DataFrame,
    sim_threshold: float = 0.80,
    w_text: float = 1.0,
    w_hashtag: float = 0.6,
    w_url: float = 0.8,
    coarse_bucket_minutes: int = 60,
    w_coarse: float = 0.5,
) -> nx.Graph:
    """
    Bangun graf tak-berarah berbobot dari tiga saluran bukti, pada DUA SKALA
    WAKTU (multi-skala) agar tahan terhadap penyamaran "acak waktu":

      - Skala HALUS (ember `tbucket`, mis. 5 menit): keserempakan ketat,
        bukti terkuat. Bobot penuh.
      - Skala KASAR (ember `coarse_bucket_minutes`, mis. 60 menit): menangkap
        klaster yang sengaja menyebar waktunya agar tak terlihat serempak.
        Bobot lebih rendah (`w_coarse`) karena buktinya lebih lemah.

    Buzzer yang mengacak waktunya tetap menumpuk dalam jendela 60 menit yang
    sama saat membanjiri hashtag kampanye, sehingga tetap tertaut. Akun
    organik jarang berbagi hashtag langka, jadi skala kasar tidak menambah
    banyak salah-tangkap.
    """
    G = nx.Graph()
    G.add_nodes_from(df["account_id"].unique())

    def _add(edges, w):
        for (a, b), val in edges.items():
            if G.has_edge(a, b):
                G[a][b]["weight"] += w * val
            else:
                G.add_edge(a, b, weight=w * val)

    # --- Skala halus (ember yang sudah ada di df) ---
    _add(_edges_from_text_synchrony(df, sim_threshold), w_text)
    _add(_edges_from_shared_tokens(df, "hashtags"), w_hashtag)
    _add(_edges_from_shared_tokens(df, "urls"), w_url)

    # --- Skala kasar: HANYA hashtag/URL khas-kampanye (bukan teks) ---
    # Teks template organik bisa kebetulan sama dalam jendela 60 menit, jadi
    # kemiripan teks TIDAK dipakai di skala kasar. Yang dipakai hanya token
    # langka yang dipakai sedikit akun (ciri kampanye terkoordinasi), sehingga
    # buzzer yang mengacak waktu tetap tertaut tanpa menambah salah-tangkap.
    if coarse_bucket_minutes and w_coarse > 0:
        dfc = df.copy()
        dfc["cbucket"] = dfc["timestamp"].map(
            lambda t: time_bucket(t, coarse_bucket_minutes)
        )
        n_acc = dfc["account_id"].nunique()
        cap = max(2, int(0.15 * n_acc))  # token dipakai <=15% akun = khas-kampanye
        _add(_edges_from_shared_tokens(dfc, "hashtags", bucket_col="cbucket",
                                       max_global_accounts=cap), w_hashtag * w_coarse)
        _add(_edges_from_shared_tokens(dfc, "urls", bucket_col="cbucket",
                                       max_global_accounts=cap), w_url * w_coarse)

    return G


# ---------------------------------------------------------------------------
# Langkah 5 — Temukan klaster & beri skor yang BISA DIJELASKAN
# ---------------------------------------------------------------------------
def _synchrony_score(df_sub: pd.DataFrame) -> float:
    """
    Seberapa serempak klaster memposting? Diukur dari konsentrasi post pada
    sedikit ember waktu. 1.0 = semua post menumpuk di satu-dua ember (sangat
    tidak organik); mendekati 0 = tersebar merata (wajar).
    """
    counts = df_sub["tbucket"].value_counts(normalize=True).values
    if len(counts) == 0:
        return 0.0
    # indeks Herfindahl (konsentrasi) sebagai proksi sinkronisasi
    return float(np.sum(counts ** 2))


def _content_similarity_score(df_sub: pd.DataFrame) -> float:
    """Rata-rata kemiripan isi di dalam klaster (0..1)."""
    texts = [t for t in df_sub["clean"].tolist() if t]
    if len(texts) < 2:
        return 0.0
    try:
        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
        mat = vec.fit_transform(texts)
    except ValueError:
        return 0.0
    sim = cosine_similarity(mat)
    n = sim.shape[0]
    iu = np.triu_indices(n, k=1)
    return float(np.mean(sim[iu])) if len(iu[0]) else 0.0


def detect_clusters(
    df: pd.DataFrame,
    G: nx.Graph,
    min_cluster_size: int = 3,
    min_edge_weight: float = 3.0,
) -> List[Cluster]:
    """
    1. Buang sisi lemah (di bawah ambang) -> sisakan ko-aksi yang berarti.
    2. Deteksi komunitas (greedy modularity) pada graf tersisa.
    3. Skor tiap komunitas menjadi coordination_score.

    coordination_score = rata-rata tertimbang dari:
        - content_similarity (isi seragam)
        - synchrony          (waktu serempak)
        - cohesion           (kepadatan sisi internal klaster)
    Ketiganya adalah BUKTI yang bisa ditunjukkan ke analis — bukan kotak hitam.
    """
    H = nx.Graph()
    H.add_nodes_from(G.nodes())
    for a, b, d in G.edges(data=True):
        if d["weight"] >= min_edge_weight:
            H.add_edge(a, b, weight=d["weight"])

    H.remove_nodes_from(list(nx.isolates(H)))
    if H.number_of_edges() == 0:
        return []

    communities = nx.community.greedy_modularity_communities(H, weight="weight")

    clusters: List[Cluster] = []
    cid = 0
    for comm in communities:
        accounts = sorted(comm)
        if len(accounts) < min_cluster_size:
            continue
        sub = df[df["account_id"].isin(accounts)]

        content = _content_similarity_score(sub)
        synchrony = _synchrony_score(sub)

        # kepadatan internal: rata-rata bobot sisi dalam komunitas, dinormalisasi
        sg = H.subgraph(accounts)
        if sg.number_of_nodes() > 1:
            possible = sg.number_of_nodes() * (sg.number_of_nodes() - 1) / 2
            cohesion = sg.number_of_edges() / possible
        else:
            cohesion = 0.0

        score = 0.45 * content + 0.35 * synchrony + 0.20 * cohesion
        score = float(min(max(score, 0.0), 1.0))

        # bukti ringkas untuk analis
        all_tags = [t for tags in sub["hashtags"] for t in tags]
        top_tags = pd.Series(all_tags).value_counts().head(5).index.tolist() if all_tags else []
        top_texts = (
            sub["text"].value_counts().head(3).index.tolist()
        )

        clusters.append(
            Cluster(
                cluster_id=cid,
                accounts=accounts,
                coordination_score=round(score, 3),
                size=len(accounts),
                synchrony=round(synchrony, 3),
                content_similarity=round(content, 3),
                top_hashtags=top_tags,
                top_narratives=top_texts,
                evidence={
                    "cohesion": round(cohesion, 3),
                    "n_posts": int(len(sub)),
                    "peak_bucket_share": round(float(sub["tbucket"].value_counts(normalize=True).max()), 3),
                },
            )
        )
        cid += 1

    clusters.sort(key=lambda c: c.coordination_score, reverse=True)
    return clusters
