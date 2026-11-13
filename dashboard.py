"""
dashboard.py — Dashboard analis SIAGA (Streamlit), versi ramah-awam.

Ini "wajah" produk. Dirancang agar orang awam (bukan ahli keamanan siber) pun
langsung paham: ada vonis ringkas berbahasa sederhana, label tingkat bahaya,
dan penjelasan singkat di tiap bagian. Detail teknis disembunyikan di bagian
"untuk analis" agar tidak membuat bingung.

Menjalankan:
    pip install streamlit plotly
    streamlit run dashboard.py

Kalau belum punya data:
    python generate_data.py --out data/posts.csv
"""

from __future__ import annotations

import os

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from siaga.coordination import prepare, build_coordination_graph, detect_clusters
from siaga.earlywarning import detect_emerging_narratives
from siaga.watchlist import build_watchlist

st.set_page_config(page_title="SIAGA — Deteksi Koordinasi Siber-Sosial",
                   page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.verdict-danger{background:#3a1215;border:1px solid #c0392b;border-radius:10px;
  padding:18px 22px;margin:4px 0 8px 0}
.verdict-safe{background:#12331f;border:1px solid #27ae60;border-radius:10px;
  padding:18px 22px;margin:4px 0 8px 0}
.verdict-title{font-size:22px;font-weight:700;margin:0}
.verdict-sub{font-size:15px;opacity:.85;margin-top:6px}
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-weight:700;
  font-size:13px;color:#fff}
.b-high{background:#c0392b}.b-med{background:#e67e22}.b-low{background:#27ae60}
.pill{background:#1c2733;border:1px solid #30363d;border-radius:10px;padding:12px 14px;
  margin-bottom:10px}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ SIAGA")
st.caption("Sistem Intelijen Analisis Gerakan siber-sosial Anomali · "
           "mendeteksi akun yang bergerak terkoordinasi (buzzer) di media sosial")

# Panduan singkat untuk orang awam
with st.expander("❓ Apa ini & cara membacanya (baca dulu bila baru pertama kali)"):
    st.markdown(
        "**Apa yang dilakukan SIAGA?** Membaca ribuan unggahan media sosial, lalu "
        "mencari **kelompok akun yang bergerak bersama secara tidak wajar** — ciri "
        "pasukan *buzzer* atau kampanye disinformasi.\n\n"
        "**Cara pakai:** tekan tombol **Jalankan Analisis** di kiri. Lalu baca dari atas:\n"
        "1. **Vonis** — kesimpulan ringkas: aman atau ada yang mencurigakan.\n"
        "2. **Angka ringkas** — berapa akun dipantau & berapa yang dicurigai.\n"
        "3. **Peringatan dini** — topik/tagar yang sedang didorong kelompok mencurigakan.\n"
        "4. **Peta jaringan** — gambaran siapa terhubung dengan siapa.\n"
        "5. **Daftar akun dicurigai** — bisa diunduh untuk ditindaklanjuti.\n\n"
        "Keputusan akhir selalu di tangan manusia — SIAGA hanya memberi petunjuk & bukti."
    )

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("1. Sumber Data")
    default_path = "data/posts.csv"
    path = st.text_input("File data (CSV)", default_path)
    st.caption("Isi minimal: siapa (account_id), kapan (timestamp), apa (text).")

    st.header("2. Tingkat Kepekaan")
    st.caption("Biarkan apa adanya bila ragu — nilai bawaan sudah optimal.")
    with st.expander("Setelan lanjutan (opsional)"):
        bucket = st.slider("Jendela waktu 'serempak' (menit)", 1, 30, 5,
                           help="Dua akun yang memposting dalam rentang ini dianggap serempak.")
        sim = st.slider("Ambang kemiripan teks", 0.5, 0.95, 0.80, 0.05,
                        help="Seberapa mirip teks dianggap 'sama'. 0,80 = 80% mirip.")
        min_edge = st.slider("Pemangkasan hubungan lemah", 1.0, 6.0, 3.0, 0.5,
                             help="Makin tinggi = makin ketat, makin sedikit salah tangkap.")
        min_score = st.slider("Ambang alarm", 0.1, 0.8, 0.25, 0.05,
                              help="Batas sebuah kelompok dianggap mencurigakan.")
    st.write("")
    run = st.button("🔎 Jalankan Analisis", type="primary", use_container_width=True)


@st.cache_data(show_spinner=False)
def _load(path):
    return pd.read_csv(path)


def _risk_badge(score: float) -> str:
    if score >= 0.6:
        return "<span class='badge b-high'>BAHAYA TINGGI</span>"
    if score >= 0.4:
        return "<span class='badge b-med'>BAHAYA SEDANG</span>"
    return "<span class='badge b-low'>RENDAH</span>"


def _graph_figure(G: nx.Graph, clusters):
    if G.number_of_edges() == 0:
        return None
    H = G.subgraph([n for n in G.nodes if G.degree(n) > 0])
    pos = nx.spring_layout(H, seed=1, k=0.5)
    acc_to_cluster = {}
    for c in clusters:
        for a in c.accounts:
            acc_to_cluster[a] = c.cluster_id
    edge_x, edge_y = [], []
    for a, b in H.edges():
        edge_x += [pos[a][0], pos[b][0], None]
        edge_y += [pos[a][1], pos[b][1], None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines",
                            line=dict(width=0.5, color="#888"), hoverinfo="none")
    node_x = [pos[n][0] for n in H.nodes()]
    node_y = [pos[n][1] for n in H.nodes()]
    colors = [acc_to_cluster.get(n, -1) for n in H.nodes()]
    texts = [f"{n}<br>kelompok: {acc_to_cluster.get(n,'(tidak terkoordinasi)')}"
             for n in H.nodes()]
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers", hoverinfo="text", text=texts,
        marker=dict(size=10, color=colors, colorscale="Turbo", line_width=1))
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
                      height=460, xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig


if run or os.path.exists(path):
    if not os.path.exists(path):
        st.warning(f"File tidak ditemukan: {path}. "
                   f"Buat dulu dengan: python generate_data.py --out {path}")
        st.stop()

    raw = _load(path)
    df = prepare(raw, bucket_minutes=bucket)
    G = build_coordination_graph(df, sim_threshold=sim)
    _min_edge = min_edge
    _min_score = min_score
    all_clusters = detect_clusters(df, G, min_edge_weight=_min_edge)
    clusters = [c for c in all_clusters if c.coordination_score >= _min_score]
    flagged = set(a for c in clusters for a in c.accounts)
    alerts = detect_emerging_narratives(df, flagged)

    n_acc = df["account_id"].nunique()
    pct = (len(flagged) / n_acc * 100) if n_acc else 0

    # ============ VONIS RINGKAS (bahasa awam) ============
    if clusters:
        st.markdown(
            f"<div class='verdict-danger'>"
            f"<p class='verdict-title'>⚠️ Terdeteksi aktivitas terkoordinasi mencurigakan</p>"
            f"<p class='verdict-sub'>Ditemukan <b>{len(clusters)} kelompok akun</b> yang "
            f"bergerak bersama secara tidak wajar, melibatkan <b>{len(flagged)} akun</b> "
            f"(sekitar {pct:.0f}% dari {n_acc} akun yang dipantau). "
            f"Perlu ditelaah analis.</p></div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div class='verdict-safe'>"
            f"<p class='verdict-title'>✅ Tidak ada pola koordinasi mencurigakan</p>"
            f"<p class='verdict-sub'>Dari {n_acc} akun yang dipantau, tidak ditemukan "
            f"kelompok yang bergerak terkoordinasi pada tingkat kepekaan saat ini.</p></div>",
            unsafe_allow_html=True)

    # ============ ANGKA RINGKAS ============
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Unggahan Diperiksa", f"{len(df):,}",
              help="Total unggahan yang dibaca sistem.")
    c2.metric("Akun Dipantau", f"{n_acc:,}",
              help="Semua akun yang muncul di data. Semua dinilai.")
    c3.metric("Kelompok Mencurigakan", len(clusters),
              help="Kelompok akun yang bergerak terkoordinasi (istilah teknis: klaster CIB).")
    c4.metric("Akun Dicurigai", f"{len(flagged)}",
              help="Akun di dalam kelompok mencurigakan — yang perlu ditelaah.")

    if "is_buzzer" in raw.columns:
        truth = set(raw[raw["is_buzzer"] == 1]["account_id"].unique())
        tp = len(flagged & truth); fp = len(flagged - truth); fn = len(truth - flagged)
        p = tp/(tp+fp) if tp+fp else 0; r = tp/(tp+fn) if tp+fn else 0
        f1 = 2*p*r/(p+r) if p+r else 0
        st.caption(f"✔️ Uji akurasi (data berlabel): tepat sasaran {p:.0%} · "
                   f"tertangkap {r:.0%} · nilai-F {f1:.2f}")

    st.divider()

    # ============ PERINGATAN DINI (plain) ============
    st.subheader("🚨 Peringatan Dini: Topik yang Sedang Didorong")
    st.caption("Tagar/topik yang dinilai berisiko karena dorongannya didominasi akun mencurigakan.")
    if not alerts:
        st.info("Belum ada topik berisiko pada data ini.")
    for a in alerts[:6]:
        st.markdown(
            f"<div class='pill'>{_risk_badge(a.risk_score)} &nbsp; "
            f"<b>#{a.hashtag}</b> &nbsp;·&nbsp; skor risiko {a.risk_score:.2f}<br>"
            f"<span style='opacity:.8;font-size:13px'>"
            f"{a.cib_share:.0%} dorongannya dari akun mencurigakan · "
            f"muncul di {a.n_posts} unggahan dari hanya {a.n_accounts} akun</span></div>",
            unsafe_allow_html=True)

    st.divider()

    # ============ PETA JARINGAN ============
    st.subheader("🕸️ Peta Jaringan Akun")
    st.caption("Tiap titik = satu akun. **Titik berwarna yang menggerombol = kelompok "
               "mencurigakan.** Titik ungu yang menyebar = akun normal. "
               "Arahkan kursor ke titik untuk melihat detail.")
    fig = _graph_figure(G, clusters)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada hubungan koordinasi yang terdeteksi pada data ini.")

    st.divider()

    # ============ DAFTAR AKUN DICURIGAI (watchlist) ============
    st.subheader("📋 Daftar Akun Dicurigai (bisa diunduh)")
    st.caption("Daftar siap ditindaklanjuti: tiap baris satu akun, lengkap dengan buktinya.")
    wl = build_watchlist(df, clusters)
    if wl.empty:
        st.info("Tidak ada akun yang dicurigai pada tingkat kepekaan ini.")
    else:
        wl_show = wl.rename(columns={
            "account_id": "Akun", "cluster_id": "Kelompok", "risk_score": "Skor Risiko",
            "n_posts": "Jml Unggahan", "top_hashtags": "Tagar Utama",
            "contoh_narasi": "Contoh Pesan", "first_seen": "Pertama", "last_seen": "Terakhir",
            "alasan": "Alasan Ditandai"})
        st.dataframe(wl_show, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Unduh daftar ini (CSV)",
            data=wl.to_csv(index=False).encode("utf-8"),
            file_name="daftar_akun_dicurigai.csv", mime="text/csv", type="primary")

    # ============ DETAIL TEKNIS (untuk analis) ============
    with st.expander("🔬 Detail teknis per kelompok (untuk analis)"):
        if not clusters:
            st.write("Tidak ada kelompok terdeteksi.")
        for c in clusters:
            st.markdown(f"**Kelompok #{c.cluster_id}** — {c.size} akun — "
                        f"{', '.join('#'+h for h in c.top_hashtags[:3])}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Kemiripan Isi", f"{c.content_similarity:.2f}",
                      help="Seberapa seragam teks dalam kelompok (0–1).")
            m2.metric("Keserempakan", f"{c.synchrony:.2f}",
                      help="Seberapa menumpuk waktu posting (0–1).")
            m3.metric("Kepadatan", f"{c.evidence.get('cohesion',0):.2f}",
                      help="Seberapa rapat akun saling terhubung (0–1).")
            st.caption("Narasi inti yang diulang:")
            for t in c.top_narratives:
                st.write(f"- {t}")
            st.divider()

    # ============ KETAHANAN ANTI-PENYAMARAN (v2) ============
    with st.expander("🛡️ Uji ketahanan: apakah SIAGA bisa dikelabui? (v2)"):
        st.markdown(
            "SIAGA memeriksa pada **dua skala waktu** sekaligus, jadi buzzer yang sengaja "
            "mengacak waktunya tetap tertangkap. Uji langsung di bawah ini — SIAGA akan "
            "'berpura-pura' menjadi buzzer yang mencoba mengelabui, lalu mengukur hasilnya."
        )
        if "is_buzzer" not in raw.columns:
            st.info("Uji ini butuh data berlabel (ada kolom `is_buzzer`). Pakai data demo.")
        elif st.button("▶️ Jalankan uji ketahanan sekarang"):
            with st.spinner("Mensimulasikan buzzer yang mencoba mengelabui…"):
                from siaga.robustness import run_scenarios
                res = run_scenarios(raw, bucket=bucket, sim=sim,
                                    min_edge=_min_edge, min_score=_min_score)
            res_show = res.rename(columns={
                "Precision": "Tepat Sasaran", "Recall": "Tertangkap", "F1": "Nilai-F"})
            st.table(res_show)
            worst = res.iloc[-1]
            st.caption(
                f"Bahkan saat buzzer memakai SEMUA trik sekaligus, SIAGA tetap "
                f"tepat sasaran {worst['Precision']:.0%} (tidak menuduh akun tak bersalah) "
                f"dan menangkap {worst['Recall']:.0%} dari mereka.")
        else:
            st.caption("Klik tombol untuk menghitung ketahanan langsung (perlu beberapa detik).")
else:
    st.info("👈 Tekan **Jalankan Analisis** di kiri untuk memulai. "
            "Belum punya data? Jalankan dulu: `python generate_data.py --out data/posts.csv`")
