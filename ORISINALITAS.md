# Pernyataan Orisinalitas & Sumber

Dokumen ini menegaskan keaslian karya **SIAGA** untuk **Kartika Cyber Hackathon 2026**
(PUSSIBERAD × CODEPOLITAN), sekaligus mencantumkan sumber secara transparan.

## 1. Karya asli

- Seluruh **kode** (`siaga/`, `run_pipeline.py`, `generate_data.py`,
  `evaluate_robustness.py`, `api.py`, `dashboard.py`, `collect_youtube.py`,
  `connect_data.py`) dan **dokumentasi** disusun sendiri oleh tim dari nol.
- Yang bersifat orisinal adalah **metode & arsitektur**: fusi tiga saluran bukti
  (co-posting sinkron, co-hashtag ber-idf, co-URL) menjadi satu graf koordinasi,
  deteksi komunitas, **Coordination Score** yang transparan, normalisasi
  Bahasa Indonesia tahan-penyamaran (TF-IDF karakter *n*-gram), deteksi
  **multi-skala waktu** anti-evasion, dan modul **peringatan dini**.

## 2. Pustaka pihak ketiga (open-source, dipakai wajar)

| Pustaka | Lisensi | Peran |
|---|---|---|
| pandas, numpy | BSD | manipulasi data |
| scikit-learn | BSD | TF-IDF & cosine similarity |
| networkx | BSD | graf koordinasi + deteksi komunitas |
| streamlit, plotly | Apache-2.0 / MIT | dashboard (opsional) |
| fastapi, uvicorn | MIT / BSD | REST API (opsional) |
| certifi | MPL-2.0 | sertifikat SSL untuk collector (opsional) |

Penggunaan pustaka open-source adalah praktik standar dan **bukan plagiarisme**;
yang dinilai orisinal adalah cara kami merangkainya.

## 3. Konsep & teori yang dirujuk (dengan sitasi di proposal)

- *Coordinated Inauthentic Behavior* (CIB) dan *Social Network Analysis* (SNA).
- Prinsip doktrin: **Zero Trust / NIST SP 800-207** (AS), **Active Cyber Defense**
  (Israel/INCD), **Resiliensi & Tallinn Manual** (Estonia/NATO CCDCOE),
  **OT Masterplan** (Singapura/CSA).
- Kerangka respons operasi pengaruh: **DISARM** (padanan MITRE ATT&CK).

Konsep-konsep ini **dikutip dengan sitasi** di proposal — mengutip dengan sitasi
bukan plagiarisme; menyalin tanpa sitasi adalah plagiarisme.

## 4. Data

- Data demo (`data/demo_id.csv`) **100% sintetis** dan dihasilkan oleh
  `generate_data.py` — **tidak memuat data pribadi orang nyata**.
- Untuk data nyata: gunakan **hanya data publik**, patuhi **ToS platform** dan
  **UU PDP No. 27/2022**. Jangan pernah meng-commit data pribadi ke repo publik.

## 5. Etika

SIAGA menilai **pola perilaku terkoordinasi**, bukan benar/salah isi pendapat,
dan menerapkan prinsip **human-in-the-loop**: sistem memberi sinyal & bukti,
keputusan penindakan ada pada analis dan pihak berwenang.
