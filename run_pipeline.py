"""
run_pipeline.py — Menjalankan SIAGA ujung-ke-ujung & mengukur akurasinya.

Alur:
    1. baca CSV post (account_id, timestamp, text, [is_buzzer], [campaign])
    2. prepare -> fitur
    3. bangun graf koordinasi
    4. deteksi klaster + skor
    5. deteksi narasi menanjak (early warning)
    6. simpan laporan JSON + HTML, cetak ringkasan
    7. kalau ada kolom is_buzzer -> hitung precision/recall (evaluasi jujur)

Jalankan:
    python run_pipeline.py --in data/posts.csv --outdir out
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict

import pandas as pd

from siaga.coordination import (
    prepare,
    build_coordination_graph,
    detect_clusters,
)
from siaga.earlywarning import detect_emerging_narratives
from siaga.watchlist import export_watchlist


def evaluate(df: pd.DataFrame, flagged_accounts: set) -> dict:
    """
    Kalau dataset punya label is_buzzer, ukur seberapa baik SIAGA.
    Akun 'benar buzzer' = akun yang pernah mengirim post is_buzzer==1.
    """
    if "is_buzzer" not in df.columns:
        return {}
    truth = set(df[df["is_buzzer"] == 1]["account_id"].unique())
    all_acc = set(df["account_id"].unique())

    tp = len(flagged_accounts & truth)
    fp = len(flagged_accounts - truth)
    fn = len(truth - flagged_accounts)
    tn = len(all_acc - flagged_accounts - truth)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "true_negative": tn,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
    }


def render_html(clusters, alerts, metrics, outpath):
    """Laporan HTML statis sederhana — tidak butuh dependency tambahan."""
    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    rows_c = ""
    for c in clusters:
        rows_c += f"""<tr>
          <td>#{c.cluster_id}</td>
          <td><b>{c.coordination_score:.2f}</b></td>
          <td>{c.size}</td>
          <td>{c.content_similarity:.2f}</td>
          <td>{c.synchrony:.2f}</td>
          <td>{esc(', '.join('#'+h for h in c.top_hashtags))}</td>
          <td>{esc(c.top_narratives[0] if c.top_narratives else '')}</td>
        </tr>"""

    rows_a = ""
    for a in alerts:
        color = "#c0392b" if a.risk_score >= 0.6 else ("#e67e22" if a.risk_score >= 0.4 else "#7f8c8d")
        rows_a += f"""<tr>
          <td>#{esc(a.hashtag)}</td>
          <td style="color:{color}"><b>{a.risk_score:.2f}</b></td>
          <td>{a.cib_share:.2f}</td>
          <td>{a.velocity:.2f}</td>
          <td>{a.n_posts}</td>
          <td>{a.n_accounts}</td>
        </tr>"""

    m = metrics or {}
    met_html = ""
    if m:
        met_html = f"""<div class="metrics">
          <span>Precision: <b>{m['precision']}</b></span>
          <span>Recall: <b>{m['recall']}</b></span>
          <span>F1: <b>{m['f1']}</b></span>
          <span>TP {m['true_positive']} · FP {m['false_positive']} · FN {m['false_negative']}</span>
        </div>"""

    html = f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
    <title>Laporan SIAGA</title>
    <style>
      body{{font-family:system-ui,Segoe UI,sans-serif;margin:24px;background:#0f1419;color:#e6edf3}}
      h1{{color:#58a6ff}} h2{{color:#79c0ff;margin-top:28px}}
      table{{border-collapse:collapse;width:100%;margin-top:8px;font-size:14px}}
      th,td{{border:1px solid #30363d;padding:8px;text-align:left;vertical-align:top}}
      th{{background:#161b22}}
      .metrics span{{display:inline-block;margin-right:18px;background:#161b22;padding:6px 10px;border-radius:6px}}
      .sub{{color:#8b949e}}
    </style></head><body>
    <h1>SIAGA — Laporan Deteksi Koordinasi Siber-Sosial</h1>
    <p class="sub">Sistem Intelijen Analisis Gerakan siber-sosial Anomali · laporan otomatis</p>
    {met_html}
    <h2>Klaster Terkoordinasi Terdeteksi ({len(clusters)})</h2>
    <table><tr><th>ID</th><th>Skor</th><th>Akun</th><th>Kemiripan Isi</th>
    <th>Sinkronisasi</th><th>Hashtag Dominan</th><th>Narasi Inti</th></tr>{rows_c}</table>
    <h2>Peringatan Dini Narasi Menanjak ({len(alerts)})</h2>
    <table><tr><th>Hashtag</th><th>Risiko</th><th>Porsi CIB</th><th>Kecepatan</th>
    <th>Post</th><th>Akun</th></tr>{rows_a}</table>
    </body></html>"""
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    ap = argparse.ArgumentParser(description="Jalankan pipeline SIAGA")
    ap.add_argument("--in", dest="inp", default="data/posts.csv")
    ap.add_argument("--outdir", default="out")
    ap.add_argument("--bucket", type=int, default=5, help="ukuran ember waktu (menit)")
    ap.add_argument("--sim", type=float, default=0.80, help="ambang kemiripan teks")
    ap.add_argument("--min-size", type=int, default=3, help="ukuran klaster minimum")
    ap.add_argument("--min-score", type=float, default=0.25,
                    help="ambang coordination_score agar klaster ditandai sbg CIB")
    ap.add_argument("--min-edge", type=float, default=3.0,
                    help="ambang bobot sisi untuk pemangkasan ko-aksi lemah")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.inp)
    print(f"[1/5] Memuat {len(df)} post dari {args.inp}")

    df = prepare(df, bucket_minutes=args.bucket)
    print(f"[2/5] Normalisasi & ekstraksi fitur selesai")

    G = build_coordination_graph(df, sim_threshold=args.sim)
    print(f"[3/5] Graf koordinasi: {G.number_of_nodes()} simpul, {G.number_of_edges()} sisi")

    all_clusters = detect_clusters(df, G, min_cluster_size=args.min_size,
                                   min_edge_weight=args.min_edge)
    # Hanya klaster di atas ambang skor yang dianggap CIB terkonfirmasi.
    # Klaster di bawah ambang disimpan sebagai "pantauan" (watchlist), bukan alarm.
    clusters = [c for c in all_clusters if c.coordination_score >= args.min_score]
    watchlist = [c for c in all_clusters if c.coordination_score < args.min_score]
    flagged = set(a for c in clusters for a in c.accounts)
    print(f"[4/5] {len(clusters)} klaster CIB (skor>={args.min_score}) "
          f"+ {len(watchlist)} pantauan, {len(flagged)} akun ditandai")

    alerts = detect_emerging_narratives(df, flagged)
    print(f"[5/5] {len(alerts)} narasi menanjak dinilai")

    metrics = evaluate(df, flagged)

    # simpan JSON
    report = {
        "summary": {
            "n_posts": int(len(df)),
            "n_accounts": int(df["account_id"].nunique()),
            "n_clusters": len(clusters),
            "n_flagged_accounts": len(flagged),
        },
        "metrics": metrics,
        "clusters": [asdict(c) for c in clusters],
        "watchlist": [asdict(c) for c in watchlist],
        "alerts": [asdict(a) for a in alerts],
    }
    json_path = os.path.join(args.outdir, "report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    html_path = os.path.join(args.outdir, "report.html")
    render_html(clusters, alerts, metrics, html_path)

    # ekspor watchlist per-akun (operasional, siap ditindaklanjuti analis)
    wl_path = os.path.join(args.outdir, "watchlist.csv")
    n_wl = export_watchlist(df, clusters, wl_path)

    # ringkasan ke layar
    print("\n" + "=" * 60)
    print("RINGKASAN HASIL SIAGA")
    print("=" * 60)
    for c in clusters:
        print(f"  Klaster #{c.cluster_id} | skor {c.coordination_score:.2f} "
              f"| {c.size} akun | mirip {c.content_similarity:.2f} "
              f"| sinkron {c.synchrony:.2f}")
        if c.top_hashtags:
            print(f"      hashtag: {', '.join('#'+h for h in c.top_hashtags)}")
    if metrics:
        print("-" * 60)
        print(f"  EVALUASI (vs ground truth): "
              f"precision={metrics['precision']}  recall={metrics['recall']}  f1={metrics['f1']}")
    print("=" * 60)
    print(f"\nLaporan tersimpan:\n  {json_path}\n  {html_path}\n  {wl_path} ({n_wl} akun di watchlist)")


if __name__ == "__main__":
    main()
