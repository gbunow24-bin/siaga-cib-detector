# SIAGA 🛡️
**Sistem Intelijen Analisis Gerakan siber-sosial Anomali**

Mesin deteksi *Coordinated Inauthentic Behavior* (CIB) berbahasa Indonesia untuk
kategori **Siber Sosial / Cognitive Domain** — Kartika Cyber Hackathon 2026
(PUSSIBERAD × CODEPOLITAN).

SIAGA tidak bertanya *"apakah akun ini bot?"* (pendekatan lama yang gagal
menangkap buzzer operasi-manusia). SIAGA bertanya *"akun mana saja yang
**bergerak bersama secara tidak wajar**?"* — mendeteksi **koordinasi**, bukan
sekadar otomatisasi.

---

## Cara kerja singkat

```
CSV post ─► features ─► coordination ─► earlywarning ─► laporan
(akun,     (normalisasi  (graf 3 saluran   (tagar          (HTML/JSON
 waktu,     teks ID,      bukti, deteksi    mencurigakan,    + watchlist
 teks)      ember waktu)  komunitas, skor)  skor risiko)     + dashboard)
```

**Tiga saluran bukti** yang difusikan menjadi satu graf koordinasi:
co-posting sinkron (TF-IDF karakter *n*-gram, tahan sisipan kata/typo),
co-hashtag (dibobot kelangkaan/idf), dan co-URL. Klaster padat ditemukan lewat
deteksi komunitas, lalu diberi **Coordination Score** transparan beserta buktinya:
`0.45·kemiripan isi + 0.35·sinkronisasi + 0.20·kepadatan jaringan`.

---

## Hasil uji (reproducible)

Pada dataset sintetis berbahasa Indonesia dengan *ground truth*
(3 kampanye buzzer di antara 120 akun organik), **konsisten lintas seed 42/7/123/999**:

```
Precision 1.00 · Recall 1.00 · F1 1.00
1.618 unggahan · 144 akun → 3 klaster CIB · 24 akun ditandai · 0 salah tangkap
```

**Tahan penyamaran (anti-evasion):** diuji terhadap sisip kata, ganti sinonim,
dan acak waktu. Pada skenario gabungan terburuk pun **presisi tetap 1,00**
(F1 0,70) berkat deteksi multi-skala waktu.

> Angka ini dari **data sintetis** untuk membuktikan mesin bekerja & bisa diukur
> jujur. Pada data nyata (lebih berisik) F1 akan lebih rendah — itu wajar dan
> justru harus dilaporkan apa adanya.

---

## Cara menjalankan (3 menit)

> Gunakan `python3`/`pip3` di macOS/Linux bila `python` tidak dikenal.

```bash
# 1. pasang dependency inti
pip install -r requirements.txt

# 2. jalankan pipeline pada dataset demo yang sudah disertakan
python run_pipeline.py --in data/demo_id.csv --outdir out
#    -> out/report.html   (buka di browser — laporan intelijen)
#    -> out/report.json   (untuk integrasi lanjutan)
#    -> out/watchlist.csv (daftar akun dicurigai, siap tindak lanjut)

# 3. (opsional) dashboard interaktif untuk demo ke juri
streamlit run dashboard.py

# 4. (opsional) buktikan ketahanan terhadap penyamaran
python evaluate_robustness.py
```

**Regenerasi data demo** (reproducible, tanpa API berbayar):
```bash
python generate_data.py --out data/demo_id.csv --seed 42
```

**Pakai data sendiri?** Siapkan CSV dengan kolom minimal
`account_id, timestamp, text`, lalu `python run_pipeline.py --in file_anda.csv`.
Untuk menarik data nyata YouTube: lihat `collect_youtube.py --help`
(butuh API key sendiri; hanya data publik, patuhi ToS & UU PDP).

**REST API** untuk integrasi pusat komando (opsional):
```bash
uvicorn api:app --reload      # lalu POST /analyze, GET /health
```

---

## Struktur proyek

```
siaga/
├── README.md                # berkas ini
├── ORISINALITAS.md          # pernyataan keaslian & sumber
├── LICENSE                  # MIT
├── requirements.txt         # dependency (inti ringan + opsional)
├── generate_data.py         # generator data sintetis + ground truth (Bahasa Indonesia)
├── run_pipeline.py          # pipeline CLI ujung-ke-ujung + evaluasi F1
├── evaluate_robustness.py   # uji ketahanan anti-penyamaran (evasion)
├── collect_youtube.py       # (opsional) tarik komentar YouTube publik -> CSV
├── connect_data.py          # (opsional) adaptor sumber data
├── api.py                   # (opsional) REST API (FastAPI): /health, /analyze
├── dashboard.py             # (opsional) dashboard analis (Streamlit)
├── PANDUAN_TIM.md           # panduan lengkap tim (arsitektur + walkthrough kode)
├── data/
│   └── demo_id.csv          # dataset demo siap pakai (sintetis)
├── out/                     # contoh keluaran (report.html / .json / watchlist.csv)
└── siaga/                   # paket inti
    ├── features.py          # normalisasi Bahasa Indonesia + fitur jejak
    ├── coordination.py      # ⭐ inti: graf koordinasi + skor klaster
    ├── earlywarning.py      # deteksi dini tagar/narasi menanjak
    ├── robustness.py        # logika uji penyamaran (dipakai dashboard & evaluasi)
    └── watchlist.py         # susun & ekspor daftar akun dicurigai
```

## Parameter yang bisa disetel

| Flag | Default | Arti |
|---|---|---|
| `--bucket` | 5 | ukuran ember waktu (menit) untuk menilai "serempak" |
| `--sim` | 0.80 | ambang kemiripan teks dua post dianggap duplikat terselubung |
| `--min-edge` | 3.0 | ambang bobot sisi — memangkas ko-aksi lemah (anti false-positive) |
| `--min-score` | 0.25 | ambang skor koordinasi agar klaster berstatus **alarm** CIB |

## Etika & legal

- Data demo **100% sintetis** — tidak ada data pribadi orang nyata.
- SIAGA mendeteksi **pola perilaku terkoordinasi**, bukan menilai benar/salah isi
  pendapat. Keputusan akhir ada pada analis manusia (*human-in-the-loop*).
- Untuk data nyata: gunakan hanya data publik, patuhi ToS platform & **UU PDP
  No. 27/2022**. Lihat `ORISINALITAS.md`.

---

*Dibuat untuk Kartika Cyber Hackathon 2026 — kategori 04, Siber Sosial.*
