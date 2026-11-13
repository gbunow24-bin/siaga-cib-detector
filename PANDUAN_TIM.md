# PANDUAN MASTER TIM — MEMENANGKAN KARTIKA CYBER HACKATHON 2026
### Target: minimal 3 Besar · Strategi + Teori + Novelty + Rencana 4 Minggu + Walkthrough Kode

> Dokumen ini dirancang agar **seluruh anggota tim** — termasuk yang bukan ahli
> keamanan siber — bisa paham dari nol. Baca berurutan. Bagian ⭐ adalah yang
> paling menentukan kemenangan.

---

## DAFTAR ISI
1. Memahami medan lomba & cara juri menilai (rubrik)
2. Desain tools untuk **ke-4 kategori** (ringkas tapi lengkap)
3. ⭐ Rekomendasi: **1 kategori** untuk dibangun penuh + alasannya
4. ⭐ Teori keamanan siber dari **negara terkuat** + cara kita mengadopsinya
5. ⭐ Novelty / research gap + strategi lolos **plagiasi**
6. ⭐ Arsitektur SIAGA + **walkthrough kode tahap per tahap**
7. Rencana kerja **4 minggu** per peran (tim 3 orang)
8. Checklist submission dipetakan ke rubrik
9. Risiko, etika, legal, dan mitigasi
10. Skrip presentasi final (10 menit) yang memenangkan

---

## 1. MEMAHAMI MEDAN LOMBA & CARA JURI MENILAI

**Penyelenggara:** Pusat Siber Angkatan Darat (PUSSIBERAD) × CODEPOLITAN.
**Esensi:** karya terbaik **berpeluang diadopsi TNI AD** sebagai bagian sistem
pertahanan siber nasional. Jadi juri bukan hanya menilai "keren secara teknis",
tapi **"apakah ini benar-benar berguna & bisa dipakai satuan TNI AD"**.

**Format:** 2 babak. Babak 1 online 4 minggu (proposal + dokumentasi teknis +
video demo purwarupa). 10 tim lolos ke final offline (presentasi 10 menit) di
Jakarta, 24 November 2026. Deadline submission **15 November 2026**.

**Tim:** maksimal 3 orang. Submission: (a) link karya/project yang bisa diakses,
(b) video presentasi, (c) slide penjelasan.

### Rubrik penilaian (HAFALKAN — ini kompas kita)

| Bobot | Kriteria | Apa artinya buat kita |
|---|---|---|
| **25%** | Relevansi & Manfaat | Sesuai kebutuhan pengamanan **IT/OT TNI AD**. → Setiap fitur harus bisa dijawab: *"ini menyelesaikan masalah nyata satuan yang mana?"* |
| **25%** | Inovasi Teknis | Keaslian ide & pendekatan. → Butuh **novelty** yang jelas (Bagian 5). |
| **25%** | Fungsionalitas Purwarупа | **Bisa jalan & didemokan**. → Prototipe harus BENAR-BENAR berjalan. Ini alasan kita bangun kode yang teruji, bukan sekadar mockup. |
| **15%** | Kelayakan Implementasi | Mudah dikembangkan & diterapkan di satuan. → Arsitektur modular, ringan, dokumentasi jelas. |
| **10%** | Kualitas Dokumentasi | Proposal + dok teknis + video jelas. → Rapi, terstruktur, naratif. |

**Insight strategis:** 75% nilai ada di **Relevansi + Inovasi + Fungsionalitas**.
Banyak tim akan kuat di salah satu saja. **Kita menang dengan unggul di ketiganya
sekaligus** — ide yang relevan (menyelesaikan masalah TNI AD nyata), baru
(novelty terdokumentasi), DAN prototipenya benar-benar jalan mulus saat demo.

---

## 2. DESAIN TOOLS UNTUK KE-4 KATEGORI

Lomba punya 4 kategori. Berikut rancangan tool yang **layak** untuk masing-masing,
lengkap dengan risiko 4-minggunya. (Kita hanya akan **membangun penuh satu** —
lihat Bagian 3 — tapi tim harus paham keempatnya untuk memilih dengan sadar.)

### Kategori 01 — PENINDAKAN (Offensive Tech)
> *Solusi ofensif untuk menguji kerentanan / mendukung operasi siber aktif.*

**Rancangan tool: "PALAGAN" — Automated Attack-Surface & Exploit-Path Mapper.**
Diberi target (IP/domain milik sendiri / lab), tool memetakan permukaan serangan
(port, service, versi), mengkorelasikannya dengan basis data kerentanan (CVE),
lalu menyusun **"jalur serangan paling mungkin"** (attack path) secara otomatis
dan membuat laporan prioritas tambalan. Inti novelty: *AI-assisted attack-path
prioritization* (bukan sekadar scanner).

- **Tumpukan teknologi:** Python, `python-nmap`/`nmap`, API basis data CVE (NVD),
  graf serangan (networkx), laporan HTML.
- **Manfaat TNI AD:** red-team otomatis untuk menguji ketahanan aset satuan
  sebelum lawan menemukannya.
- ⚠️ **Risiko tinggi untuk 4 minggu:** (1) Dual-use/etis — juri militer akan
  sangat hati-hati pada "payload generator"/"exploit tool"; mudah tergelincir ke
  area berbahaya. (2) Banyak klon Metasploit/Nmap → **rawan dituduh plagiat /
  rendah novelty**. (3) Demo aman itu sulit (butuh lab terisolasi). **Tidak
  direkomendasikan sebagai pilihan utama** kecuali tim sudah ahli pentest.

### Kategori 02 — PENANGKALAN (Defensive Shield)
> *Deteksi, cegah, respons ancaman siber.*

**Rancangan tool: "BENTENG" — OT-Aware Anomaly Detector + LLM Triage Copilot.**
IDS ringan untuk jaringan **OT/ICS** (SCADA, PLC) yang mendeteksi anomali dari
perilaku proses fisik (bukan hanya signature), lalu sebuah **asisten LLM**
meringkas tiap alarm jadi bahasa yang dimengerti operator + rekomendasi tindakan
— mengurangi kelelahan analis (*alert fatigue*).

- **Tumpukan teknologi:** Python, dataset ICS publik (SWaT/WADI/HAI), scikit-learn
  (One-Class SVM/Isolation Forest/autoencoder), LLM untuk ringkasan alarm.
- **Manfaat TNI AD:** TNI AD secara eksplisit menyebut pengamanan **IT/OT**;
  infrastruktur militer & nasional (listrik, air, bahan bakar) adalah OT.
- ⚠️ **Risiko 4 minggu:** butuh data OT realistis & setup lebih berat; "IDS lagi"
  bisa dianggap kurang baru kecuali twist LLM-triage dieksekusi sangat rapi.
  **Kandidat kuat kedua.**

### Kategori 03 — DUKUNGAN TEKNOLOGI (Core Infra)
> *Infrastruktur / platform / tooling pendukung operasi siber satuan.*

**Rancangan tool: "KOMANDO" — Lightweight SIEM + Cyber Operation Dashboard.**
Pengumpul log terpusat (dari endpoint, firewall, server) yang ringan untuk
dijalankan di lapangan (edge), dengan dashboard situasi siber satuan: peta aset,
status ancaman, timeline insiden, dan *digital forensic triage* dasar.

- **Tumpukan teknologi:** Python/FastAPI + SQLite/ClickHouse ringan, parser log,
  dashboard web. Opsi: korelasi aturan + ringkasan AI.
- **Manfaat TNI AD:** "Cyber Operation Dashboard" & "SIEM Ringan" **disebut
  sebagai contoh resmi** di web lomba → relevansi sangat jelas.
- ⚠️ **Risiko 4 minggu:** sangat buildable & demoable, TAPI mudah terlihat
  "cuma dashboard" → **novelty harus diperkuat** (mis. SIEM yang jalan offline di
  edge dengan korelasi AI). **Kandidat kuat ketiga — paling aman secara teknis.**

### Kategori 04 — SIBER SOSIAL (Cognitive Domain) ⭐
> *Pemantauan ruang siber sosial: deteksi disinformasi, propaganda, buzzer, opini publik.*

**Rancangan tool: "SIAGA" — Coordinated Inauthentic Behavior Early-Warning System.**
Mendeteksi **operasi informasi terkoordinasi** (pasukan buzzer/bot) berbahasa
Indonesia dengan menilai **pola kebersamaan** antar-akun — lalu memberi
**peringatan dini** saat sebuah narasi mulai didorong klaster terkoordinasi,
**sebelum** viral organik.

- **Tumpukan teknologi:** Python, pandas, scikit-learn, networkx (semua ringan).
- **Manfaat TNI AD:** domain kognitif/"perang narasi" adalah ancaman nyata &
  aktual di Indonesia (lihat Bagian 5). Inilah **yang kita bangun penuh.**
- ✅ **Risiko 4 minggu rendah:** data mudah (publik/sintetis), tidak ada dual-use
  berbahaya, sangat demoable, novelty kuat & terdokumentasi.

---

## 3. ⭐ REKOMENDASI: BANGUN KATEGORI **SIBER SOSIAL** (SIAGA)

**Keputusan: Fokus penuh ke Kategori 04 — Siber Sosial, produk `SIAGA`.**

Berikut alasannya, **dipetakan langsung ke rubrik** (inilah cara berpikir juri):

| Kriteria (bobot) | Mengapa SIAGA menang di sini |
|---|---|
| Relevansi & Manfaat (25%) | Buzzer & disinformasi adalah ancaman **aktif & terdokumentasi** di Indonesia (Pemilu 2019, isu Papua Barat, protes 2025, disinformasi pengadaan alutsista). Domain kognitif persis masuk mandat "Siber Sosial" TNI AD. |
| Inovasi Teknis (25%) | Novelty jelas & bisa dipertahankan: **deteksi koordinasi, bukan deteksi bot per-akun**, dan **berbahasa Indonesia** (celah riset yang terdokumentasi). Lihat Bagian 5. |
| Fungsionalitas Purwarupa (25%) | Prototipe **sudah jalan** (F1 1.0 pada data ber-ground-truth). Data sintetis membuat demo **selalu sukses & reproducible** di depan juri — tanpa risiko API mati/kuota habis. |
| Kelayakan Implementasi (15%) | Dependency ringan (pandas/sklearn/networkx), modular, bisa jalan di laptop/edge. Mudah dikembangkan jadi layanan nyata. |
| Kualitas Dokumentasi (10%) | Dokumen ini + README + laporan HTML/JSON otomatis = paket dokumentasi rapi siap submit. |

**Mengapa bukan yang lain (ringkas):**
- *Penindakan:* risiko etis + rawan plagiat + demo berbahaya. Buruk untuk 4 minggu.
- *Penangkalan (OT IDS):* kuat & relevan, tapi butuh data OT & setup berat;
  "IDS lagi" menuntut eksekusi sempurna untuk menonjol.
- *Dukungan Teknologi (SIEM):* paling aman teknis, tapi paling mudah terlihat
  generik → nilai Inovasi (25%) berisiko rendah.

> **Strategi lindung nilai (opsional, kalau tim kuat):** bangun SIAGA sebagai
> inti, lalu posisikan dashboard-nya sebagai bagian "Cyber Operation Dashboard"
> agar menyentuh relevansi Kategori 03 juga. Tapi **submit di satu kategori: 04.**

---

## 4. ⭐ TEORI KEAMANAN SIBER NEGARA TERKUAT — DAN CARA KITA MENGADOPSINYA

Permintaan: *teori handal & terbaru dari negara yang paling kuat sistem keamanan
sibernya, dengan contoh.* Tidak ada negara yang benar-benar "tak terkalahkan" —
tapi beberapa negara jadi **rujukan doktrin dunia**. Kita ambil prinsip terbaik
dari tiap negara dan **tanamkan ke SIAGA** supaya proposal kita berpijak pada
teori kelas dunia (menaikkan nilai Inovasi & Relevansi).

### 4.1 Amerika Serikat — **Zero Trust** & **Defend Forward**
- **Zero Trust Architecture (ZTA):** prinsipnya *"never trust, always verify"* —
  tidak ada entitas yang otomatis dipercaya hanya karena ada "di dalam" jaringan;
  setiap akses diverifikasi terus-menerus. Dirumuskan formal di **NIST SP 800-207**
  dan diperkuat *Executive Order 14028* (2021) yang mewajibkan Zero Trust di
  lembaga federal AS. Lembaga operasionalnya: **CISA** (Cybersecurity and
  Infrastructure Security Agency).
- **Defend Forward / Persistent Engagement** (US Cyber Command, Doktrin 2018):
  pertahanan tidak menunggu di garis belakang, tapi **aktif memantau & mengganggu
  ancaman sedekat mungkin ke sumbernya**, terus-menerus.
- **Adopsi ke SIAGA:** (1) *Verifikasi berkelanjutan* → SIAGA tidak "percaya" akun
  hanya karena tampak manusiawi; ia terus menilai **perilaku**. (2) *Defend
  Forward* → filosofi **peringatan dini**: menindak narasi di hulu (saat mulai
  menanjak) bukan setelah telanjur viral.

### 4.2 Israel — **Active Cyber Defense** & ekosistem talenta (Unit 8200 → INCD)
- Israel membangun **Israel National Cyber Directorate (INCD)** (konsolidasi
  ~2017–2018) sebagai komando sipil-militer pertahanan siber nasional, dengan
  doktrin **active defense** (deteksi-respons cepat, berbagi intelijen real-time
  antar sektor) dan ekosistem talenta dari unit militer (mis. Unit 8200) yang
  mengalir ke industri. Pendekatannya: **kecepatan deteksi-ke-respons** dan
  **intelijen ancaman yang dibagikan**.
- **Adopsi ke SIAGA:** SIAGA dirancang sebagai **mesin intelijen** yang
  menghasilkan sinyal siap-bagi (laporan JSON/HTML) agar antar-satuan bisa
  bertindak cepat dan seragam — meniru prinsip *shared threat intelligence*.

### 4.3 Estonia — **Resiliensi** & **Data Embassy** (pelajaran 2007)
- Setelah serangan siber besar 2007, Estonia menjadi pelopor **resiliensi**
  (negara tetap berfungsi walau diserang). Estonia menjadi tuan rumah **NATO
  CCDCOE** (Cooperative Cyber Defence Centre of Excellence) di Tallinn — lahirnya
  *Tallinn Manual* soal hukum perang siber — dan menerapkan konsep **"data
  embassy"** (menyimpan salinan data negara di server berdaulat di luar negeri,
  mis. Luksemburg, agar fungsi negara bertahan).
- **Adopsi ke SIAGA:** fokus pada **ketahanan masyarakat terhadap disinformasi**
  (societal resilience), bukan hanya teknis. Output SIAGA bisa memberi masukan
  ke edukasi publik / *prebunking* — memperkuat "benteng kognitif" warga.

### 4.4 Singapura — **CSA** & **OT Cybersecurity Masterplan**
- **Cyber Security Agency (CSA)** Singapura (dibentuk 2015) menjalankan strategi
  nasional menyeluruh, termasuk **OT Cybersecurity Masterplan (2019)** yang
  memperlakukan infrastruktur kritis (OT) sebagai prioritas, dan program
  **SG Cyber Safe** untuk higiene siber. Kekuatannya: **koordinasi terpusat +
  kemitraan lintas sektor**.
- **Adopsi ke SIAGA:** arsitektur **modular & mudah diintegrasikan** ke pusat
  komando (dashboard terpusat), selaras dengan model koordinasi terpusat.

### 4.5 Benang merah untuk proposal
> "SIAGA menerjemahkan empat prinsip kelas dunia ke domain siber-sosial Indonesia:
> **verifikasi perilaku berkelanjutan** (Zero Trust, AS), **deteksi-ke-respons
> cepat yang bisa dibagi** (Active Defense, Israel), **resiliensi kognitif
> masyarakat** (Estonia), dan **koordinasi terpusat yang modular** (Singapura)."

Kalimat ini layak masuk slide & proposal — menunjukkan kita paham teori global,
bukan sekadar ngoding. (Catatan: saat menulis proposal, **verifikasi ulang detail
tahun/nama lembaga** dari sumber resmi masing-masing negara agar 100% akurat.)

---

## 5. ⭐ NOVELTY / RESEARCH GAP + STRATEGI ANTI-PLAGIASI

### 5.1 Masalahnya nyata (ini memperkuat Relevansi 25%)
Fenomena **"buzzer"** (pasukan siber bayaran yang menggiring opini) adalah
fixture politik Indonesia sejak Pilkada Jakarta 2012. Terdokumentasi: jaringan
*coordinated inauthentic behavior* dibersihkan platform jelang Pemilu 2019;
operasi informasi soal Papua Barat; serta jaringan tidak autentik yang memperkuat
polarisasi saat gelombang protes 2025 dan disinformasi seputar pengadaan alutsista.
Industri buzzer bahkan beroperasi dengan model bisnis klien-penyedia, memakai
**bahasa sandi/slang & metafora lokal** untuk mengelabui filter otomatis.

### 5.2 Celah riset (research gap) yang kita isi
Berdasarkan literatur terkini:
1. **Alat dominan bersifat per-akun & Inggris-sentris.** Botometer dkk. menilai
   "seberapa bot sebuah akun". Buzzer Indonesia banyak **dioperasikan manusia** →
   lolos deteksi per-akun.
2. **Akun sering diperlakukan sebagai "kendaraan", bukan "infrastruktur
   terkoordinasi".** Literatur akademik Indonesia terkini secara eksplisit
   menyebut kebutuhan memperlakukan jaringan akun sebagai **infrastruktur
   strategis** — justru koordinasinya yang penting.
3. **Minim alat berbahasa Indonesia** yang menggabungkan sinyal **waktu + isi +
   jaringan** sekaligus, dan **tahan terhadap penyamaran** (sisipan kata, slang).

### 5.3 Klaim novelty SIAGA (tulis persis ini di proposal)
> **SIAGA mendeteksi KOORDINASI, bukan OTOMATISASI.** Alih-alih bertanya "apakah
> akun X bot?", SIAGA memfusikan tiga saluran bukti — **co-posting sinkron**
> (teks mirip pada ember waktu sama), **co-hashtag berbarengan** (dibobot
> kelangkaan/idf), dan **co-URL** — menjadi satu **graf koordinasi**, menemukan
> klaster padat via deteksi komunitas, lalu memberinya **Coordination Score yang
> dapat dijelaskan** (kemiripan isi + sinkronisasi + kepadatan). Dioptimalkan
> untuk **Bahasa Indonesia** (normalisasi tahan-penyamaran: pemanjangan huruf,
> slang, stopword ID) dan dilengkapi **modul peringatan dini** yang menandai
> narasi menanjak yang dorongan awalnya didominasi akun terkoordinasi.

Yang membuat ini **baru & dapat dipertahankan**:
- **Fusi 3-saluran + skor yang transparan** (bukan kotak hitam) → cocok untuk
  pertanggungjawaban militer/hukum.
- **Fokus Bahasa Indonesia & anti-penyamaran** (char n-gram, bukan kata utuh).
- **Early-warning dini** (bukan forensik pasca-viral).

### 5.4 Strategi lolos cek plagiasi (penting!)
1. **Tulis kode & dokumen dari nol** (repo ini original). Jangan salin-tempel repo
   GitHub orang. Pakai ini sebagai basis dan kembangkan sendiri.
2. **Sitasi semua sumber** di proposal (konsep Zero Trust/NIST, CIB, dll.) —
   mengutip dengan sitasi ≠ plagiat; **menyalin tanpa sitasi = plagiat**.
3. **Library open-source itu wajar** (pandas, sklearn) — sebutkan di dokumentasi;
   yang dinilai orisinal adalah **metode & arsitektur** kita.
4. **Jalankan cek similarity** pada dokumen proposal (mis. Turnitin kampus /
   layanan gratis) sebelum submit; targetkan similarity rendah & parafrase penuh.
5. **Rekam jejak pengembangan** (commit Git bertahap) sebagai bukti karya asli.

---

## 6. ⭐ ARSITEKTUR SIAGA + WALKTHROUGH KODE TAHAP PER TAHAP

### 6.1 Peta alur (pipeline)
```
CSV post  ─►  features.py        ─►  coordination.py       ─►  earlywarning.py  ─►  laporan
(akun,     (normalisasi teks ID,   (graf ko-aksi 3 saluran,   (narasi menanjak     (HTML/JSON
 waktu,     hashtag, url, ember     deteksi komunitas,         + skor risiko)       + dashboard)
 teks)      waktu)                  Coordination Score)
```

### 6.2 `siaga/features.py` — fondasi akurasi
**Tugas:** membuat teks **bisa dibandingkan** antar-akun.
- `normalize_text()` — huruf kecil, buang emoji/aksen, buang URL/mention/hashtag
  (ditangani terpisah), **ringkas huruf berulang** (`baguuus`→`bagus`), buang
  tanda baca & stopword Indonesia. Ini kunci menangkap "copy-paste disamarkan".
- `time_bucket()` — memetakan waktu ke "ember" 5-menit. Dua akun yang posting di
  ember yang sama = **sinkron** (sidik koordinasi terkuat).
- **Pelajari:** coba `normalize_text("Baguuus bangeet!!! #promo @akun")` di Python,
  lihat hasilnya. Ubah daftar `STOPWORDS_ID`, amati pengaruhnya.

### 6.3 `siaga/coordination.py` — ⭐ otak sistem
**Tugas:** dari post → **klaster akun yang bergerak bersama**.
1. `prepare()` — tambah kolom turunan (clean, hashtags, urls, tbucket).
2. `_edges_from_text_synchrony()` — **per ember waktu**, bandingkan semua post
   dengan **TF-IDF char n-gram (3–5)** + cosine. Pakai char n-gram (bukan kata)
   supaya **tahan sisipan kata/typo** yang dipakai buzzer. Pasangan ≥ ambang
   (0.80) pada ember yang sama → sisi (edge) koordinasi.
   *Mengapa per-ember?* Supaya perbandingan hanya O(k²) di dalam ember kecil
   (ringan) **dan** hanya menghitung kejadian yang benar-benar serempak (relevan).
3. `_edges_from_shared_tokens()` — co-hashtag & co-URL. Token langka yang tiba-tiba
   dipakai serempak diberi **bobot besar (idf)**; token umum diberi bobot kecil.
   Inilah cara menangkap **flooding hashtag** tanpa terjebak hashtag populer biasa.
4. `build_coordination_graph()` — gabung 3 saluran jadi **satu graf berbobot**.
5. `detect_clusters()` — **pangkas sisi lemah** (`min_edge_weight`), lalu
   **greedy modularity communities** (networkx) menemukan klaster padat, lalu skor:
   `score = 0.45·kemiripan_isi + 0.35·sinkronisasi + 0.20·kepadatan`.
   Semua komponen **ditampilkan** ke analis sebagai **bukti** (bukan kotak hitam).
- **Pelajari:** di `run_pipeline.py`, naik-turunkan `--min-edge` & `--sim`, amati
  jumlah klaster. Ini melatih intuisi *precision vs recall*.

### 6.4 `siaga/earlywarning.py` — nilai tambah untuk TNI AD
**Tugas:** peringatan **dini**. Untuk tiap hashtag: hitung **kecepatan**
(sedang melonjak?), **porsi dorongan dari akun terkoordinasi** (cib_share), dan
**konsentrasi akun** (sedikit akun → banyak post). Gabung jadi `risk_score`.
Hashtag dengan risiko tinggi = **operasi informasi yang sedang dirakit** →
jendela emas untuk dinetralkan sebelum viral organik.

### 6.5 `generate_data.py` — demo yang selalu sukses
Membuat data sintetis: ~120 akun organik (teks beragam, waktu acak) + 3 kampanye
buzzer (pesan nyaris identik, serempak dalam "gelombang", membanjiri hashtag).
Menyimpan label `is_buzzer` **hanya untuk evaluasi** (mesin tidak melihatnya).
Ini memberi **ground truth** → kita bisa klaim F1 secara jujur di depan juri.

### 6.6 `run_pipeline.py` & `dashboard.py` — keluaran
- `run_pipeline.py`: jalankan semua, hitung **precision/recall/F1**, simpan
  `out/report.html` (dibuka tanpa dependency) + `out/report.json`.
- `dashboard.py` (Streamlit): graf interaktif + daftar klaster + peringatan dini —
  untuk **demo visual** ke juri. Opsional; kalau juri tak mau pasang Streamlit,
  laporan HTML sudah cukup.

### 6.7 Cara melatih diri (untuk seluruh tim)
1. Jalankan 4 perintah di README. Buka `out/report.html`.
2. Buka `generate_data.py`, ubah jumlah akun buzzer / variasi teks, jalankan lagi,
   amati apakah SIAGA tetap menangkapnya.
3. Baca `coordination.py` baris demi baris sambil mencocokkan dengan Bagian 6.3.
4. Rusak sistem dengan sengaja (mis. set `--sim 0.99`) → lihat recall turun →
   pahami *kenapa*. Ini bahan **tanya-jawab juri** yang mematikan kalau dikuasai.

---

## 7. RENCANA KERJA 4 MINGGU (TIM 3 ORANG)

Asumsi peran (sesuaikan): **A = Lead/ML**, **B = Data/Backend**, **C = Produk/Dokumentasi/Demo**.
Periode efektif: 19 Okt → 15 Nov 2026 (deadline). Final 24 Nov.

### Minggu 1 (19–25 Okt) — Fondasi & bukti konsep
- **Semua:** daftar tim di CODEPOLITAN; ikut Webinar Pembekalan 1 (19 Okt) &
  catat kebutuhan IT/OT yang disebut TNI AD. Kunci kategori: **Siber Sosial**.
- **A:** jalankan & kuasai repo SIAGA ini; pastikan F1 1.0 reproduce di laptop tim.
- **B:** siapkan **data nyata skala kecil** (dataset publik CIB / ekspor manual
  dari platform sesuai ToS) untuk uji di luar sintetis.
- **C:** buat kerangka proposal + slide (pakai struktur Bagian 8); tulis bagian
  Latar Belakang & Novelty (Bagian 5).
- **Milestone:** purwarupa jalan + proposal draf 30%.

### Minggu 2 (26 Okt–1 Nov) — Perkuat mesin & data
- **A:** tingkatkan deteksi: tambah fitur (usia akun, rasio duplikat), uji
  parameter; opsional integrasi embedding semantik Bahasa Indonesia (IndoBERT /
  sentence-transformers) sebagai pengganti/pelengkap TF-IDF untuk kemiripan makna.
- **B:** pipeline ingest data nyata → format CSV standar SIAGA; ukur F1 pada data
  nyata & **laporkan apa adanya** (kejujuran metrik menambah kredibilitas).
- **C:** ikut Webinar Pembekalan 2 (27 Okt); rapikan dashboard untuk demo;
  proposal draf 70%.
- **Milestone:** SIAGA jalan pada ≥1 dataset nyata; dashboard siap demo.

### Minggu 3 (2–8 Nov) — Validasi, dokumentasi, video
- **A+B:** uji ketahanan (robustness) — variasikan data, stress-test, perbaiki
  false positive; bekukan versi stabil (tag Git).
- **C:** **rekam video demo** (3–5 menit): masalah → solusi → demo langsung
  (klaster terdeteksi + peringatan dini) → dampak untuk TNI AD. Selesaikan
  dokumentasi teknis & proposal 100%.
- **Milestone:** video + dokumen + kode **siap submit** (jangan nunggu mepet).

### Minggu 4 (9–15 Nov) — Poles & submit lebih awal
- **Semua:** cek plagiasi dokumen (Bagian 5.4); rapikan README & repo publik;
  uji ulang "clone → install → run" di mesin bersih (buktikan **jalan mulus**).
- **Submit H-2** (13 Nov), bukan 15 Nov — hindari risiko server padat.
- **Milestone:** **SUBMITTED.**

### Pasca-submit (16–24 Nov) — Siapkan final
- Latihan presentasi 10 menit (Bagian 10); siapkan jawaban tanya-jawab teknis;
  siapkan **plan B demo** (video cadangan + screenshot) jika internet venue buruk.

---

## 8. CHECKLIST SUBMISSION DIPETAKAN KE RUBRIK

**(a) Link karya/project** — repo Git publik rapi + README + `report.html` contoh.
*(menyasar Fungsionalitas 25% + Kelayakan 15%)*

**(b) Proposal solusi** — struktur disarankan:
1. Latar belakang & masalah (buzzer/disinformasi di Indonesia) *(Relevansi 25%)*
2. Solusi & cara kerja (arsitektur SIAGA, Bagian 6) *(Inovasi 25%)*
3. **Novelty & research gap** eksplisit (Bagian 5) *(Inovasi 25%)*
4. Landasan teori (Bagian 4, dengan sitasi) *(Inovasi + Relevansi)*
5. Hasil & evaluasi (metrik F1, tangkapan layar) *(Fungsionalitas 25%)*
6. Rencana implementasi & pengembangan di satuan *(Kelayakan 15%)*
7. Etika, legal, batasan *(kredibilitas)*
8. Daftar pustaka.

**(c) Video + slide** — jelas, naratif, tunjukkan demo nyata. *(Dokumentasi 10%)*

---

## 9. RISIKO, ETIKA, LEGAL & MITIGASI

- **Etika deteksi:** SIAGA menilai **pola perilaku terkoordinasi**, bukan
  benar/salah isi pendapat. Selalu **human-in-the-loop** — sistem memberi sinyal,
  manusia memutuskan. Tegaskan ini di proposal (menghindari kesan alat sensor).
- **Legal data:** gunakan **hanya data publik**, patuhi **ToS platform** & **UU
  PDP (UU 27/2022)**. Untuk demo, **pakai data sintetis** repo ini (aman).
- **Bias & false positive:** akun aktivis sah bisa "tampak" terkoordinasi.
  Mitigasi: ambang skor + verifikasi manusia + transparansi bukti.
- **Risiko teknis demo:** mitigasi dengan data sintetis (tak butuh internet) +
  video cadangan.
- **Over-claim:** jangan klaim "100% akurat di dunia nyata". Klaim yang jujur &
  terukur lebih meyakinkan juri berpengalaman.

---

## 10. SKRIP PRESENTASI FINAL (10 MENIT) YANG MEMENANGKAN

1. **(1 mnt) Kaitkan ke misi:** "Ancaman siber tak mengenal seragam. Perang
   hari ini juga perang **narasi**." Tunjukkan 1 contoh kasus Indonesia.
2. **(1 mnt) Masalah & gap:** alat lama tanya "bot atau bukan" → gagal pada
   buzzer manusia. Kita tanya **"siapa bergerak bersama?"**.
3. **(3 mnt) DEMO LANGSUNG:** jalankan pipeline → dashboard: klaster terdeteksi,
   bukti (kemiripan+sinkron+jaringan), **peringatan dini** hashtag naik.
4. **(2 mnt) Novelty & teori:** fusi 3-saluran + skor transparan + Bahasa
   Indonesia; sandarkan ke prinsip Zero Trust/Active Defense/Resiliensi.
5. **(1,5 mnt) Manfaat & implementasi TNI AD:** ringan, modular, edge-ready,
   human-in-the-loop, roadmap pengembangan.
6. **(0,5 mnt) Etika:** deteksi perilaku, bukan sensor opini.
7. **(1 mnt) Tanya-jawab:** kuasai "kenapa char n-gram?", "bagaimana hindari
   false positive aktivis?", "skala ke jutaan post?" (jawab: pemrosesan per-ember
   + indeks + batch).

**Prinsip emas:** *tunjukkan yang jalan, jangan hanya ceritakan.* Fungsionalitas
25% + demo mulus adalah pembeda utama dari tim yang "cuma punya slide".

---

### Penutup
Repo SIAGA ini adalah **titik awal yang sudah terbukti jalan (F1 1.0, reproducible)**,
punya **novelty yang bisa dipertahankan**, **relevansi tinggi untuk TNI AD**, dan
**ringan untuk 4 minggu**. Tugas tim: kuasai kodenya, uji pada data nyata, poles
dokumentasi & demo, dan submit lebih awal. Selamat bertanding — *Siaga!* 🛡️
