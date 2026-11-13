// SIAGA — Deck Kartika Cyber Hackathon 2026
// Tema: cyber/militer gelap, aksen teal. 13 slide. Jalankan: node build_deck.js
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.author = "Tim SIAGA";
pres.title = "Proposal SIAGA — Kartika Cyber Hackathon 2026";

// ---- Palet ----
const BG = "0A0E13";       // navy near-black (selaras tema situs lomba)
const PANEL = "141C26";    // kartu di atas gelap
const PANEL2 = "1C2733";
const LINE = "27323F";
const INK = "0F1720";      // teks gelap di slide terang
const MUTED = "5B6B7A";    // teks redup di slide terang
const MUTED_D = "8FA1B2";  // teks redup di slide gelap
const PAPER = "FFFFFF";
const SOFT = "F3F6F8";     // kartu di slide terang
const LTINK = "E6EDF3";    // teks terang di slide gelap
const ACCENT = "2DD4BF";   // teal — teknologi/siaga
const AMBER = "F5A623";    // amber — peringatan
const DANGER = "E5484D";   // merah — ancaman
const HEAD = "Calibri";
const BODY = "Calibri";

const W = 13.33, H = 7.5, M = 0.6;

function darkBg(s, color) {
  s.background = { color: color || BG };
}
function lightBg(s) {
  s.background = { color: PAPER };
}
function kicker(s, text, color) {
  s.addText(text.toUpperCase(), {
    x: M, y: 0.42, w: W - 2 * M, h: 0.3, isTextBox: true, margin: 0,
    fontSize: 12, bold: true, color: color || ACCENT, fontFace: BODY, charSpacing: 2,
  });
}
function title(s, text, color) {
  s.addText(text, {
    x: M, y: 0.72, w: W - 2 * M, h: 1.0, isTextBox: true, margin: 0,
    fontSize: 32, bold: true, color: color || INK, fontFace: HEAD, align: "left", valign: "top",
  });
}
// Garis antar dua titik (pptxgen menggambar bounding-box; flipH untuk kemiringan negatif)
function netLine(s, p, q, col, w) {
  const x = Math.min(p[0], q[0]), y = Math.min(p[1], q[1]);
  const ww = Math.abs(q[0] - p[0]), hh = Math.abs(q[1] - p[1]);
  const flip = ((q[0] - p[0]) * (q[1] - p[1])) < 0;
  s.addShape(pres.ShapeType.line, { x, y, w: ww, h: hh, line: { color: col, width: w }, flipH: flip });
}
// Graf mini: dense=true -> semua titik saling terhubung (jaring rapat)
function miniNet(s, cx, cy, r, n, dense, lineCol, dotCol) {
  const pts = [];
  for (let i = 0; i < n; i++) { const a = Math.PI * 2 * i / n - Math.PI / 2; pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  if (dense) { for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) netLine(s, pts[i], pts[j], lineCol, 1); }
  else { [[0, 3], [2, 4]].forEach(p => netLine(s, pts[p[0]], pts[p[1]], lineCol, 1)); }
  pts.forEach(p => s.addShape(pres.ShapeType.ellipse, { x: p[0] - 0.07, y: p[1] - 0.07, w: 0.14, h: 0.14, fill: { color: dotCol }, line: { type: "none" } }));
}

// ====================================================================
// SLIDE 1 — COVER (gelap)
// ====================================================================
let s = pres.addSlide();
darkBg(s);
// titik-titik jaringan dekoratif (motif koordinasi)
const dots = [[11.2,1.1],[12.1,1.6],[11.6,2.4],[12.5,3.0],[10.8,2.0],[12.0,0.7],[11.0,3.1]];
dots.forEach(([x,y],i)=>{
  s.addShape(pres.ShapeType.ellipse,{x,y,w:0.16,h:0.16,fill:{color: i%3===0?ACCENT:MUTED_D},line:{type:"none"}});
});
s.addShape(pres.ShapeType.line,{x:11.28,y:1.18,w:0.82,h:0.42,line:{color:LINE,width:1}});
s.addShape(pres.ShapeType.line,{x:11.68,y:1.68,w:0.42,h:0.72,line:{color:LINE,width:1}});
s.addShape(pres.ShapeType.line,{x:11.08,y:2.08,w:0.92,h:0.3,line:{color:LINE,width:1}});
s.addText("KARTIKA CYBER HACKATHON 2026", { x: M, y: 1.5, w: 9, h: 0.4, isTextBox:true, margin:0, fontSize: 13, bold:true, color: ACCENT, fontFace: BODY, charSpacing: 3 });
s.addText("SIAGA", { x: M, y: 2.0, w: 9, h: 1.5, isTextBox:true, margin:0, fontSize: 96, bold:true, color: LTINK, fontFace: HEAD });
s.addText("Sistem Intelijen Analisis Gerakan siber-sosial Anomali", { x: M, y: 3.55, w: 9.5, h: 0.5, isTextBox:true, margin:0, fontSize: 20, color: MUTED_D, fontFace: BODY });
s.addText("Aplikasi analitik intelijen siber-sosial — deteksi dini berbahasa Indonesia", { x: M, y: 4.1, w: 10.5, h: 0.5, isTextBox:true, margin:0, fontSize: 16, italic:true, color: ACCENT, fontFace: BODY });
// chip kategori
s.addShape(pres.ShapeType.roundRect,{x:M,y:5.1,w:3.6,h:0.5,rectRadius:0.1,fill:{color:PANEL},line:{color:LINE,width:1}});
s.addText("Kategori 04 — Siber Sosial", { x:M, y:5.1, w:3.6, h:0.5, isTextBox:true, margin:0, align:"center", valign:"middle", fontSize:13, bold:true, color:LTINK, fontFace:BODY });
s.addText("Tim [NAMA TIM]  ·  [Anggota 1, Anggota 2, Anggota 3]", { x:M, y:6.5, w:11, h:0.4, isTextBox:true, margin:0, fontSize:13, color:MUTED_D, fontFace:BODY });
s.addNotes("Pembuka (1 menit). Ancaman siber tak mengenal seragam — perang hari ini juga perang narasi. Perkenalkan tim dan kategori Siber Sosial. SIAGA = sistem deteksi dini operasi informasi terkoordinasi.");

// ====================================================================
// SLIDE 2 — MASALAH (gelap)
// ====================================================================
s = pres.addSlide();
darkBg(s);
kicker(s, "Masalah", AMBER);
title(s, "Perang hari ini perang narasi", LTINK);
s.addText("Domain kognitif — perebutan persepsi publik lewat ruang siber sosial — kini jadi medan pertempuran nyata. Di Indonesia, “buzzer” dan disinformasi terkoordinasi sudah jadi pemandangan tetap sejak 2012.", { x:M, y:1.7, w:6.9, h:0.85, isTextBox:true, margin:0, fontSize:15, color:MUTED_D, fontFace:BODY, lineSpacingMultiple:1.15 });
// timeline kasus + badge data (nyata bila terdokumentasi, kualitatif bila tidak)
const cases2 = [
  ["2012","Fenomena buzzer mulai menonjol (Pilkada Jakarta)","Titik awal fenomena", MUTED_D],
  ["2019","Jaringan tak autentik dibersihkan jelang Pemilu","±234 akun, halaman & grup dihapus", ACCENT],
  ["2019+","Operasi informasi terkait isu Papua","Operasi lintas-platform", MUTED_D],
  ["2025","Amplifikasi tak autentik saat gelombang unjuk rasa","Skala terbesar yang terdokumentasi", AMBER],
];
let ry = 2.65;
cases2.forEach(([yr,desc,tag,tagc])=>{
  s.addShape(pres.ShapeType.roundRect,{x:M,y:ry,w:1.05,h:0.56,rectRadius:0.08,fill:{color:PANEL},line:{color:LINE,width:1}});
  s.addText(yr,{x:M,y:ry,w:1.05,h:0.56,isTextBox:true,margin:0,align:"center",valign:"middle",fontSize:14,bold:true,color:ACCENT,fontFace:BODY});
  s.addText(desc,{x:M+1.25,y:ry-0.04,w:5.4,h:0.4,isTextBox:true,margin:0,fontSize:13.5,color:LTINK,fontFace:BODY});
  s.addText(tag,{x:M+1.25,y:ry+0.3,w:5.4,h:0.35,isTextBox:true,margin:0,fontSize:12,bold:true,color:tagc,fontFace:BODY});
  ry += 0.88;
});
// panel data nyata 2025 (kanan)
s.addShape(pres.ShapeType.roundRect,{x:7.45,y:2.55,w:5.25,h:3.35,rectRadius:0.12,fill:{color:PANEL},line:{color:LINE,width:1}});
s.addText("SKALA GELOMBANG 2025", { x:7.75,y:2.8,w:4.7,h:0.3,isTextBox:true,margin:0,fontSize:12,bold:true,color:AMBER,fontFace:BODY,charSpacing:2 });
s.addText("±499 jt", { x:7.75,y:3.12,w:4.7,h:0.95,isTextBox:true,margin:0,fontSize:52,bold:true,color:LTINK,fontFace:HEAD });
s.addText("jangkauan potensial konten tak autentik", { x:7.75,y:4.12,w:4.7,h:0.4,isTextBox:true,margin:0,fontSize:14,color:MUTED_D,fontFace:BODY });
s.addShape(pres.ShapeType.line,{x:7.75,y:4.68,w:4.65,h:0,line:{color:LINE,width:1}});
s.addText("±8.500 post  ·  >350 rb interaksi", { x:7.75,y:4.82,w:4.7,h:0.35,isTextBox:true,margin:0,fontSize:14,bold:true,color:ACCENT,fontFace:BODY });
s.addText("Analisis Cyabra atas dinamika protes 2025", { x:7.75,y:5.22,w:4.7,h:0.4,isTextBox:true,margin:0,fontSize:12,italic:true,color:MUTED_D,fontFace:BODY });
// transisi ke solusi
s.addText("Namun operasi terkoordinasi selalu meninggalkan jejak — pola waktu, duplikasi pesan, struktur jaringan.", { x:M,y:6.12,w:12.1,h:0.4,isTextBox:true,margin:0,fontSize:13.5,italic:true,color:ACCENT,fontFace:BODY });
s.addText("Sumber: Facebook & DFRLab (2019); Cyabra (2025). Catatan: data 2012 & isu Papua terdokumentasi secara kualitatif.", { x:M,y:6.75,w:12.1,h:0.4,isTextBox:true,margin:0,fontSize:11,color:MUTED_D,fontFace:BODY });
s.addNotes("Masalah (1 menit). Judul: perang hari ini perang narasi. Eskalasi nyata: 2019 Facebook/DFRLab menghapus ±234 akun jelang Pemilu; 2025 analisis Cyabra ±8.500 post & ±499 juta jangkauan. 2012 & Papua kualitatif — sampaikan apa adanya. Tutup: operasi terkoordinasi selalu meninggalkan jejak, itulah yang SIAGA tangkap.");

// ====================================================================
// SLIDE 3 — KENAPA ALAT LAMA GAGAL (terang, komparasi)
// ====================================================================
s = pres.addSlide();
lightBg(s);
kicker(s, "Celah", DANGER);
title(s, "Alat lama bertanya hal yang salah");
// kolom kiri (lama) vs kanan (siaga)
function compareCard(x, headColor, head, q, pts, dark) {
  s.addShape(pres.ShapeType.roundRect,{x,y:1.95,w:5.65,h:4.6,rectRadius:0.12,fill:{color:dark?INK:SOFT},line:{color:dark?INK:"E3E9ED",width:1}});
  s.addText(head,{x:x+0.35,y:2.2,w:5,h:0.4,isTextBox:true,margin:0,fontSize:13,bold:true,color:headColor,fontFace:BODY,charSpacing:1});
  s.addText(q,{x:x+0.35,y:2.65,w:4.95,h:1.0,isTextBox:true,margin:0,fontSize:22,bold:true,italic:true,color:dark?LTINK:INK,fontFace:HEAD,lineSpacingMultiple:1.05});
  s.addText(pts.map((t,i)=>({text:t, options:{bullet:{code:"2022"}, color:dark?MUTED_D:MUTED, fontSize:14.5, fontFace:BODY, breakLine:true, paraSpaceAfter:8}})),
    {x:x+0.35,y:3.95,w:4.95,h:2.3,isTextBox:true,margin:0,valign:"top"});
}
compareCard(M, MUTED, "PENDEKATAN LAMA", "“Apakah akun ini bot?”",
  ["Menilai akun satu per satu","Dirancang untuk akun otomatis, Inggris-sentris","Buzzer operasi-manusia tampak “wajar” dan lolos"], false);
compareCard(7.05, ACCENT, "PENDEKATAN SIAGA", "“Siapa bergerak bersama?”",
  ["Menilai pola kebersamaan antar-akun","Dioptimalkan untuk Bahasa Indonesia","Menangkap koordinasi, bukan sekadar otomatisasi"], true);
s.addNotes("Celah (1 menit). Inti pembeda kita. Alat lama = deteksi per-akun 'bot or not', gagal pada buzzer manusia. SIAGA membalik pertanyaannya menjadi 'siapa bergerak bersama'.");

// ====================================================================
// SLIDE 4 — SOLUSI / PERNYATAAN NOVELTY (gelap, besar)
// ====================================================================
s = pres.addSlide();
darkBg(s, "0C1218");
kicker(s, "Solusi", ACCENT);
s.addText([
  {text:"SIAGA mendeteksi ", options:{color:LTINK}},
  {text:"KOORDINASI", options:{color:ACCENT}},
  {text:",\nbukan ", options:{color:LTINK}},
  {text:"OTOMATISASI", options:{color:AMBER}},
  {text:".", options:{color:LTINK}},
], { x:M, y:2.3, w:11.5, h:2.4, isTextBox:true, margin:0, fontSize:52, bold:true, fontFace:HEAD, lineSpacingMultiple:1.05 });
s.addText("Sebuah aplikasi analitik intelijen yang memfusikan tiga saluran bukti — co-posting sinkron, co-hashtag berbobot kelangkaan, dan co-URL — menjadi satu graf koordinasi, di atas mesin deteksi yang modular.", { x:M, y:4.9, w:10.8, h:1.2, isTextBox:true, margin:0, fontSize:17, color:MUTED_D, fontFace:BODY, lineSpacingMultiple:1.2 });
s.addNotes("Solusi (45 detik). Kalimat inti novelty. SIAGA mendeteksi koordinasi, bukan otomatisasi — fusi 3 saluran bukti jadi graf koordinasi dengan skor transparan.");

// ====================================================================
// SLIDE 5 — CARA KERJA / ARSITEKTUR (terang, pipeline)
// ====================================================================
s = pres.addSlide();
lightBg(s);
kicker(s, "Cara Kerja", ACCENT);
title(s, "Empat tahap, satu modul fusi");
const steps = [
  ["Data Post","CSV masukan"],
  ["Fitur","normalisasi ID"],
  ["Koordinasi","graf + skor"],
  ["Peringatan Dini","narasi menanjak"],
  ["Laporan","HTML · JSON"],
];
const bw = 2.18, bh = 1.15, gap = 0.34, startX = M, rowY = 2.2;
steps.forEach(([t,sub],i)=>{
  const x = startX + i*(bw+gap);
  const acc = i===2;
  s.addShape(pres.ShapeType.roundRect,{x,y:rowY,w:bw,h:bh,rectRadius:0.1,fill:{color:acc?ACCENT:SOFT},line:{color:acc?ACCENT:"E3E9ED",width:1}});
  s.addText(t,{x,y:rowY+0.16,w:bw,h:0.45,isTextBox:true,margin:0,align:"center",fontSize:15,bold:true,color:acc?"0A2E2A":INK,fontFace:BODY});
  s.addText(sub,{x,y:rowY+0.62,w:bw,h:0.4,isTextBox:true,margin:0,align:"center",fontSize:12,color:acc?"0A3E39":MUTED,fontFace:BODY});
  if(i<steps.length-1){
    s.addText("→",{x:x+bw-0.02,y:rowY,w:gap+0.04,h:bh,isTextBox:true,margin:0,align:"center",valign:"middle",fontSize:20,bold:true,color:MUTED});
  }
});
// kotak 3 saluran bukti di bawah Koordinasi
const evX = startX + 2*(bw+gap) - 1.0, evY = 4.1;
s.addShape(pres.ShapeType.line,{x:evX+2.1,y:3.95,w:0,h:-0.6,line:{color:MUTED,width:1.5,endArrowType:"triangle"}});
s.addShape(pres.ShapeType.roundRect,{x:evX,y:evY,w:4.2,h:2.15,rectRadius:0.1,fill:{color:PAPER},line:{color:ACCENT,width:1.5}});
s.addText("3 Saluran bukti yang difusikan",{x:evX+0.3,y:evY+0.2,w:3.6,h:0.4,isTextBox:true,margin:0,fontSize:15,bold:true,color:INK,fontFace:BODY});
s.addText([
  {text:"Co-posting sinkron — teks mirip, waktu sama",options:{bullet:{code:"2022"},breakLine:true,paraSpaceAfter:6}},
  {text:"Co-hashtag — dibobot kelangkaan (idf)",options:{bullet:{code:"2022"},breakLine:true,paraSpaceAfter:6}},
  {text:"Co-URL — tautan identik",options:{bullet:{code:"2022"}}},
],{x:evX+0.3,y:evY+0.7,w:3.7,h:1.3,isTextBox:true,margin:0,fontSize:13.5,color:MUTED,fontFace:BODY});
// panel "kepadatan jaringan" (visual: jaring rapat vs renggang) di sisi kanan
s.addShape(pres.ShapeType.roundRect,{x:9.0,y:evY,w:3.7,h:2.15,rectRadius:0.1,fill:{color:PAPER},line:{color:ACCENT,width:1.5}});
s.addText("Kepadatan jaringan",{x:9.25,y:evY+0.18,w:3.3,h:0.35,isTextBox:true,margin:0,fontSize:14,bold:true,color:INK,fontFace:BODY});
miniNet(s, 10.0, evY+1.15, 0.42, 6, true, ACCENT, ACCENT);
miniNet(s, 11.7, evY+1.15, 0.42, 6, false, MUTED, MUTED);
s.addText("Terkoordinasi",{x:9.2,y:evY+1.72,w:1.6,h:0.3,isTextBox:true,margin:0,align:"center",fontSize:10.5,bold:true,color:ACCENT,fontFace:BODY});
s.addText("Organik",{x:10.9,y:evY+1.72,w:1.6,h:0.3,isTextBox:true,margin:0,align:"center",fontSize:10.5,color:MUTED,fontFace:BODY});
// catatan bawah (lebar penuh, di bawah kotak bukti)
s.addText("Klaster padat ditemukan lewat deteksi komunitas, lalu diberi Coordination Score yang bisa dijelaskan: kemiripan isi + sinkronisasi + kepadatan jaringan. Modul peringatan dini menilai narasi menanjak yang dorongan awalnya didominasi akun terkoordinasi.", {x:M,y:6.45,w:12.1,h:0.8,isTextBox:true,margin:0,fontSize:14,color:MUTED,fontFace:BODY,lineSpacingMultiple:1.15});
s.addNotes("Cara kerja (1.5 menit). Pipeline 4 tahap. Jantungnya modul Koordinasi yang memfusikan 3 saluran bukti jadi graf, lalu skor transparan. Di sini lakukan DEMO LANGSUNG bila memungkinkan.");

// ====================================================================
// SLIDE 6 — NOVELTY & RESEARCH GAP (terang, 3 baris)
// ====================================================================
s = pres.addSlide();
lightBg(s);
kicker(s, "Novelty & Research Gap", ACCENT);
title(s, "Mengisi celah yang nyata");
const gaps = [
  ["Per-akun → koordinasi","Alat dominan menilai “seberapa bot” satu akun; SIAGA menilai pola gerak bersama."],
  ["Inggris-sentris → Bahasa Indonesia","Normalisasi tahan-penyamaran: pemanjangan huruf, slang, stopword ID; TF-IDF karakter n-gram."],
  ["Kotak hitam → transparan","Setiap skor disertai bukti (isi, waktu, jaringan) — layak untuk akuntabilitas militer/hukum."],
];
let gy = 2.15;
gaps.forEach(([h,d],i)=>{
  s.addShape(pres.ShapeType.ellipse,{x:M,y:gy,w:0.6,h:0.6,fill:{color:ACCENT},line:{type:"none"}});
  s.addText(String(i+1),{x:M,y:gy,w:0.6,h:0.6,isTextBox:true,margin:0,align:"center",valign:"middle",fontSize:20,bold:true,color:"0A2E2A",fontFace:HEAD});
  s.addText(h,{x:M+0.9,y:gy-0.05,w:11,h:0.5,isTextBox:true,margin:0,fontSize:19,bold:true,color:INK,fontFace:HEAD});
  s.addText(d,{x:M+0.9,y:gy+0.45,w:11.2,h:0.7,isTextBox:true,margin:0,fontSize:14.5,color:MUTED,fontFace:BODY,lineSpacingMultiple:1.1});
  gy += 1.45;
});
s.addText("Orisinal: kode & dokumen disusun dari nol, semua sumber disitasi, rekam jejak commit terdokumentasi.", {x:M,y:6.55,w:12,h:0.5,isTextBox:true,margin:0,fontSize:13,italic:true,color:ACCENT,fontFace:BODY});
s.addNotes("Novelty (1 menit). Tiga celah yang kita isi. Tekankan: fusi 3 saluran + skor transparan + Bahasa Indonesia + anti-penyamaran. Dan jaminan orisinalitas untuk lolos plagiasi.");

// ====================================================================
// SLIDE 7 — LANDASAN TEORI (terang, 2x2)
// ====================================================================
s = pres.addSlide();
lightBg(s);
kicker(s, "Landasan Teori", ACCENT);
title(s, "Prinsip kelas dunia, diadopsi ke ranah kita");
const theory = [
  ["Amerika Serikat","Zero Trust & Defend Forward","Verifikasi perilaku berkelanjutan; tindak narasi di hulu saat baru menanjak."],
  ["Israel","Active Cyber Defense (INCD)","Deteksi-ke-respons cepat; intelijen siap-bagi antar-satuan."],
  ["Estonia","Resiliensi & Data Embassy","Ketahanan kognitif masyarakat; masukan untuk edukasi publik & prebunking."],
  ["Singapura","CSA & OT Masterplan","Koordinasi terpusat; arsitektur modular siap integrasi pusat komando."],
];
const cardW = 5.7, cardH = 2.1, gx = 0.35, gyy = 0.3, ox = M, oy = 2.05;
theory.forEach((t,i)=>{
  const col = i%2, row = Math.floor(i/2);
  const x = ox + col*(cardW+gx), y = oy + row*(cardH+gyy);
  s.addShape(pres.ShapeType.roundRect,{x,y,w:cardW,h:cardH,rectRadius:0.1,fill:{color:SOFT},line:{color:"E3E9ED",width:1}});
  s.addText(t[0].toUpperCase(),{x:x+0.35,y:y+0.25,w:cardW-0.7,h:0.3,isTextBox:true,margin:0,fontSize:12,bold:true,color:ACCENT,fontFace:BODY,charSpacing:1});
  s.addText(t[1],{x:x+0.35,y:y+0.58,w:cardW-0.7,h:0.5,isTextBox:true,margin:0,fontSize:18,bold:true,color:INK,fontFace:HEAD});
  s.addText(t[2],{x:x+0.35,y:y+1.1,w:cardW-0.7,h:0.85,isTextBox:true,margin:0,fontSize:13.5,color:MUTED,fontFace:BODY,lineSpacingMultiple:1.1});
});
s.addNotes("Teori (1 menit). Empat negara rujukan doktrin dunia. SIAGA menerjemahkan prinsip mereka ke ranah siber-sosial Indonesia. Catatan: verifikasi detail tahun/lembaga saat finalisasi.");

// ====================================================================
// SLIDE 8 — HASIL & EVALUASI (gelap, stat besar)
// ====================================================================
s = pres.addSlide();
darkBg(s);
kicker(s, "Hasil & Evaluasi", ACCENT);
title(s, "Purwarupa sudah berjalan dan terukur", LTINK);
const stats = [
  ["1.00","Precision","Ketepatan — 0 akun biasa salah dituduh"],
  ["1.00","Recall","Kelengkapan — 0 pelaku lolos tangkap"],
  ["1.00","F1-score","Gabungan — 1,00 = nilai sempurna (terbaik)"],
];
stats.forEach((st,i)=>{
  const x = M + i*3.9;
  s.addShape(pres.ShapeType.roundRect,{x,y:2.1,w:3.5,h:2.3,rectRadius:0.12,fill:{color:PANEL},line:{color:LINE,width:1}});
  s.addText(st[0],{x,y:2.22,w:3.5,h:1.1,isTextBox:true,margin:0,align:"center",fontSize:58,bold:true,color:ACCENT,fontFace:HEAD});
  s.addText(st[1],{x,y:3.34,w:3.5,h:0.4,isTextBox:true,margin:0,align:"center",fontSize:16,bold:true,color:LTINK,fontFace:BODY});
  s.addText(st[2],{x:x+0.22,y:3.78,w:3.06,h:0.55,isTextBox:true,margin:0,align:"center",fontSize:11.5,color:MUTED_D,fontFace:BODY,lineSpacingMultiple:1.03});
});
s.addText("Pada dataset sintetis ber-ground-truth (3 kampanye buzzer di antara 120 akun organik): 24 akun buzzer tertangkap, 0 salah tangkap — konsisten lintas seed 42, 7, 123, 999.", {x:M,y:4.75,w:12,h:0.9,isTextBox:true,margin:0,fontSize:15,color:MUTED_D,fontFace:BODY,lineSpacingMultiple:1.15});
s.addShape(pres.ShapeType.roundRect,{x:M,y:5.8,w:12.1,h:0.85,rectRadius:0.08,fill:{color:"1A1410"},line:{color:AMBER,width:1}});
s.addText([{text:"Jujur: ",options:{bold:true,color:AMBER}},{text:"angka ini dari data sintetis untuk membuktikan metode valid & terukur. Pada data nyata F1 akan lebih rendah — validasi data nyata adalah prioritas berikutnya.",options:{color:MUTED_D}}], {x:M+0.3,y:5.8,w:11.5,h:0.85,isTextBox:true,margin:0,valign:"middle",fontSize:13.5,fontFace:BODY});
s.addNotes("Hasil (1 menit). Tunjukkan metrik. PENTING: sampaikan kejujuran soal data sintetis — ini menambah kredibilitas di mata juri berpengalaman. Jangan over-claim.");

// ====================================================================
// SLIDE 8B — KETAHANAN ANTI-PENYAMARAN (gelap, pembeda v2)
// ====================================================================
s = pres.addSlide();
darkBg(s);
kicker(s, "Ketahanan (v2)", ACCENT);
title(s, "Tetap menangkap walau buzzer mencoba mengelabui", LTINK);
s.addText("Operator buzzer beradaptasi. SIAGA diuji terhadap upaya pengelabuan — dan tetap bertahan berkat deteksi dua skala waktu.", {x:M,y:1.75,w:11.5,h:0.7,isTextBox:true,margin:0,fontSize:16,color:MUTED_D,fontFace:BODY,lineSpacingMultiple:1.15});
// tabel ketahanan sederhana (baris manual agar konsisten tema gelap)
const robRows = [
  ["Skenario penyamaran","Presisi","Recall","F1"],
  ["Tanpa penyamaran","1,00","1,00","1,00"],
  ["Sisip kata netral","1,00","1,00","1,00"],
  ["Ganti sinonim","1,00","0,96","0,98"],
  ["Acak waktu posting","1,00","0,92","0,96"],
  ["Gabungan (terburuk)","1,00","0,54","0,70"],
];
const rtX=M, rtY=2.75, rtW=7.6, rh=0.56, cW=[3.4,1.4,1.4,1.4];
robRows.forEach((row,ri)=>{
  const y=rtY+ri*rh, head=ri===0, worst=ri===robRows.length-1;
  s.addShape(pres.ShapeType.rect,{x:rtX,y,w:rtW,h:rh,fill:{color:head?PANEL2:(worst?"1A1410":PANEL)},line:{color:LINE,width:0.5}});
  let cx=rtX;
  row.forEach((cell,ci)=>{
    const col = head?LTINK:(ci===0?LTINK:(worst&&ci>0?AMBER:ACCENT));
    s.addText(cell,{x:cx+0.15,y,w:cW[ci]-0.2,h:rh,isTextBox:true,margin:0,valign:"middle",align:ci===0?"left":"center",fontSize:13.5,bold:head||worst,color:head?MUTED_D:col,fontFace:BODY});
    cx+=cW[ci];
  });
});
// kesimpulan kanan
s.addShape(pres.ShapeType.roundRect,{x:8.5,y:2.75,w:4.2,h:3.36,rectRadius:0.12,fill:{color:PANEL},line:{color:ACCENT,width:1.5}});
s.addText("Presisi tetap 1,00", {x:8.8,y:3.05,w:3.6,h:0.8,isTextBox:true,margin:0,fontSize:26,bold:true,color:ACCENT,fontFace:HEAD});
s.addText("Bahkan saat buzzer memakai SEMUA trik sekaligus, tidak ada akun tak bersalah yang dituduh.", {x:8.8,y:3.95,w:3.6,h:1.0,isTextBox:true,margin:0,fontSize:14,color:LTINK,fontFace:BODY,lineSpacingMultiple:1.15});
s.addText("Naik dari gagal total (F1 0,0) sebelum deteksi multi-skala.", {x:8.8,y:5.15,w:3.6,h:0.8,isTextBox:true,margin:0,fontSize:13,italic:true,color:MUTED_D,fontFace:BODY,lineSpacingMultiple:1.1});
s.addText("Diuji langsung dengan: python evaluate_robustness.py", {x:M,y:6.4,w:12,h:0.4,isTextBox:true,margin:0,fontSize:12,italic:true,color:MUTED_D,fontFace:BODY});
s.addNotes("Ketahanan v2 (1 menit) — PEMBEDA UTAMA. Jawab pertanyaan juri 'bagaimana kalau dikelabui?'. Serangan normal nyaris tak berpengaruh; gabungan terburuk presisi tetap 1,00. Sebaiknya jalankan evaluate_robustness.py LANGSUNG saat demo.");

// ====================================================================
// SLIDE 9 — MANFAAT TNI AD (terang, 4 kartu)
// ====================================================================
s = pres.addSlide();
lightBg(s);
kicker(s, "Manfaat bagi TNI AD", ACCENT);
title(s, "Dari ribuan unggahan ke keputusan");
// --- Funnel penyaringan (angka nyata dari demo) ---
const funnel = [
  ["1.618","unggahan masuk","F3F6F8", INK, MUTED],
  ["144","akun dipantau","DDF4EF", INK, MUTED],
  ["3","klaster CIB","A9E6DC", INK, "0A3E39"],
  ["24","akun ditandai","2DD4BF", "0A2E2A", "0A3E39"],
];
const fw=2.7, fgap=0.4, fbase=3.55;
const fheights=[1.35,1.1,0.9,0.9];
funnel.forEach((st,i)=>{
  const fx=0.67+i*(fw+fgap), h=fheights[i], y=fbase-h;
  s.addShape(pres.ShapeType.roundRect,{x:fx,y,w:fw,h,rectRadius:0.1,fill:{color:st[2]},line:{color:i===3?ACCENT:"E3E9ED",width:1}});
  s.addText(st[0],{x:fx,y,w:fw,h,isTextBox:true,margin:0,align:"center",valign:"middle",fontSize:30,bold:true,color:st[3],fontFace:HEAD});
  s.addText(st[1],{x:fx,y:fbase+0.1,w:fw,h:0.35,isTextBox:true,margin:0,align:"center",fontSize:12.5,color:MUTED,fontFace:BODY});
  if(i<3) s.addText("→",{x:fx+fw-0.03,y:2.95,w:fgap+0.06,h:0.5,isTextBox:true,margin:0,align:"center",valign:"middle",fontSize:20,bold:true,color:MUTED});
});
// --- 4 kartu statistik (angka nyata per poin) ---
const stat4 = [
  ["0,94","Kesadaran dini","skor risiko narasi — terdeteksi sebelum viral"],
  ["17%","Efisiensi analis","akun yang perlu ditelaah (24 dari 144)"],
  ["100%","Akuntabel","presisi · 0 salah tangkap"],
  ["3","Fondasi","modul inti · ringan, siap integrasi"],
];
const cw=2.85, cg=0.23, cy9=4.0, ch9=2.15;
stat4.forEach((c,i)=>{
  const x=0.62+i*(cw+cg);
  s.addShape(pres.ShapeType.roundRect,{x,y:cy9,w:cw,h:ch9,rectRadius:0.1,fill:{color:SOFT},line:{color:"E3E9ED",width:1}});
  s.addText(c[0],{x,y:cy9+0.22,w:cw,h:0.85,isTextBox:true,margin:0,align:"center",fontSize:40,bold:true,color:ACCENT,fontFace:HEAD});
  s.addText(c[1],{x,y:cy9+1.12,w:cw,h:0.4,isTextBox:true,margin:0,align:"center",fontSize:16,bold:true,color:INK,fontFace:HEAD});
  s.addText(c[2],{x:x+0.2,y:cy9+1.52,w:cw-0.4,h:0.55,isTextBox:true,margin:0,align:"center",fontSize:12,color:MUTED,fontFace:BODY,lineSpacingMultiple:1.05});
});
s.addText("*Angka dari hasil demo (data sintetis, 1.618 unggahan ber-ground-truth); kinerja pada data nyata akan divalidasi.", {x:M,y:6.45,w:12.1,h:0.5,isTextBox:true,margin:0,fontSize:12,italic:true,color:MUTED,fontFace:BODY});
s.addNotes("Manfaat (45 detik). Funnel menunjukkan alur nyata: 1.618 unggahan disaring jadi 3 klaster & 24 akun ditandai (0 salah tangkap). Tegaskan angka = hasil demo data sintetis, bukan klaim produksi.");

// ====================================================================
// SLIDE 9B — REKOMENDASI TINDAK LANJUT (terang, playbook berjenjang)
// ====================================================================
s = pres.addSlide();
lightBg(s);
kicker(s, "Tindak Lanjut", ACCENT);
title(s, "Rekomendasi: dari deteksi ke aksi");
const rcList = [
  [DANGER, "Risiko tinggi", "SKOR ≥ 0,60", [
    "Verifikasi analis (human-in-the-loop)",
    "Lestarikan bukti — ekspor + stempel waktu (chain of custody)",
    "Lapor ke platform via kanal CIB (Meta/X/TikTok)",
    "Peringatan dini ke pimpinan/satuan",
  ]],
  [AMBER, "Risiko sedang", "0,40–0,59", [
    "Pantau intensif di watchlist aktif",
    "Telusuri keterkaitan antar-klaster",
    "Siapkan kontra-narasi faktual (penerangan resmi)",
  ]],
  [MUTED_D, "Risiko rendah", "< 0,40", [
    "Arsipkan untuk deteksi kebangkitan (resurgence)",
    "Amati berkala — tanpa tindakan",
  ]],
];
const rcW = 3.95, rcG = 0.22, rcY = 2.15, rcH = 3.05;
rcList.forEach((c, i) => {
  const x = 0.62 + i * (rcW + rcG);
  s.addShape(pres.ShapeType.roundRect, { x, y: rcY, w: rcW, h: rcH, rectRadius: 0.1, fill: { color: SOFT }, line: { color: "E3E9ED", width: 1 } });
  s.addShape(pres.ShapeType.roundRect, { x, y: rcY, w: rcW, h: 0.12, rectRadius: 0.05, fill: { color: c[0] }, line: { color: c[0], width: 1 } });
  s.addText(c[1], { x: x + 0.28, y: rcY + 0.3, w: rcW - 1.6, h: 0.4, isTextBox: true, margin: 0, fontSize: 17, bold: true, color: INK, fontFace: HEAD });
  s.addText(c[2], { x: x + rcW - 1.5, y: rcY + 0.32, w: 1.25, h: 0.36, isTextBox: true, margin: 0, align: "right", valign: "middle", fontSize: 12, bold: true, color: c[0], fontFace: BODY });
  s.addText(c[3].map((t) => ({ text: t, options: { bullet: { code: "2022" }, color: MUTED, fontSize: 12.5, fontFace: BODY, breakLine: true, paraSpaceAfter: 7 } })),
    { x: x + 0.3, y: rcY + 0.9, w: rcW - 0.55, h: rcH - 1.1, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.03 });
});
s.addShape(pres.ShapeType.roundRect, { x: 0.62, y: 5.45, w: 12.09, h: 1.0, rectRadius: 0.1, fill: { color: "0C1218" }, line: { color: "0C1218", width: 1 } });
s.addText([
  { text: "Alur: ", options: { bold: true, color: ACCENT } },
  { text: "Verifikasi → Bukti → Lapor platform → Peringatan dini", options: { color: LTINK } },
], { x: 0.95, y: 5.58, w: 7.1, h: 0.74, isTextBox: true, margin: 0, valign: "middle", fontSize: 14, fontFace: BODY });
s.addText([
  { text: "Dipetakan ke kerangka DISARM. ", options: { bold: true, color: ACCENT } },
  { text: "SIAGA merekomendasikan; eksekusi oleh pihak berwenang.", options: { color: MUTED_D } },
], { x: 8.15, y: 5.58, w: 4.35, h: 0.74, isTextBox: true, margin: 0, valign: "middle", fontSize: 11.5, fontFace: BODY, lineSpacingMultiple: 1.05 });
s.addNotes("Rekomendasi tindak lanjut (45 detik). Ini jawaban untuk pertanyaan juri 'lalu apa?'. Tindakan berjenjang menurut skor risiko: tinggi = eskalasi (verifikasi, bukti, lapor platform, peringatan dini); sedang = pantau & kontra-narasi; rendah = arsip. Tegaskan guardrail: perilaku bukan identitas, tanpa takedown otomatis, patuh UU PDP 27/2022, defensif (bukan hack-back), terpetakan ke DISARM (padanan MITRE ATT&CK operasi pengaruh). SIAGA berhenti di rekomendasi & bukti; penindakan oleh manusia/lembaga berwenang.");

// ====================================================================
// SLIDE 10 — ETIKA & HUMAN-IN-THE-LOOP (gelap)
// ====================================================================
s = pres.addSlide();
darkBg(s,"0C1218");
kicker(s, "Etika & Tata Kelola", ACCENT);
title(s, "Deteksi perilaku, bukan sensor opini", LTINK);
const eth = [
  ["Human-in-the-loop","Sistem memberi sinyal; keputusan akhir di tangan analis manusia."],
  ["Berbasis perilaku","Menilai pola koordinasi (waktu, duplikasi, jaringan) — bukan benar-salah isi."],
  ["Patuh hukum","Hanya data publik; mematuhi ToS platform & UU PDP (27/2022)."],
];
let ey2 = 2.15;
eth.forEach(([h,d])=>{
  s.addShape(pres.ShapeType.roundRect,{x:M,y:ey2,w:12.1,h:1.2,rectRadius:0.1,fill:{color:PANEL},line:{color:LINE,width:1}});
  s.addText(h,{x:M+0.4,y:ey2+0.2,w:3.6,h:0.8,isTextBox:true,margin:0,valign:"middle",fontSize:18,bold:true,color:ACCENT,fontFace:HEAD});
  s.addText(d,{x:M+4.1,y:ey2+0.2,w:8,h:0.8,isTextBox:true,margin:0,valign:"middle",fontSize:15,color:MUTED_D,fontFace:BODY,lineSpacingMultiple:1.1});
  ey2 += 1.42;
});
s.addNotes("Etika (45 detik). Krusial di konteks militer. Tegaskan: alat intelijen yang akuntabel, bukan alat pembungkaman. Human-in-the-loop, berbasis perilaku, patuh hukum.");

// ====================================================================
// SLIDE 11 — RENCANA 4 MINGGU (terang, timeline)
// ====================================================================
s = pres.addSlide();
lightBg(s);
kicker(s, "Rencana Kerja", ACCENT);
title(s, "Empat minggu menuju submission");
const weeks = [
  ["M1","19–25 Okt","Kuasai purwarupa; kerangka proposal & novelty"],
  ["M2","26 Okt–1 Nov","Uji data nyata; akurasi semantik; dashboard"],
  ["M3","2–8 Nov","Uji ketahanan; rekam video; dokumentasi 100%"],
  ["M4","9–15 Nov","Cek plagiasi; poles; submit H-2 (13 Nov)"],
];
const tw = 2.95, tgap = 0.18, ty2 = 2.3;
weeks.forEach((w,i)=>{
  const x=M+i*(tw+tgap);
  s.addShape(pres.ShapeType.roundRect,{x,y:ty2,w:tw,h:2.9,rectRadius:0.1,fill:{color:i===3?ACCENT:SOFT},line:{color:i===3?ACCENT:"E3E9ED",width:1}});
  s.addText(w[0],{x,y:ty2+0.25,w:tw,h:0.6,isTextBox:true,margin:0,align:"center",fontSize:30,bold:true,color:i===3?"0A2E2A":ACCENT,fontFace:HEAD});
  s.addText(w[1],{x,y:ty2+0.95,w:tw,h:0.4,isTextBox:true,margin:0,align:"center",fontSize:13,bold:true,color:i===3?"0A3E39":INK,fontFace:BODY});
  s.addText(w[2],{x:x+0.25,y:ty2+1.45,w:tw-0.5,h:1.2,isTextBox:true,margin:0,align:"center",fontSize:13,color:i===3?"0A3E39":MUTED,fontFace:BODY,lineSpacingMultiple:1.15});
});
s.addText("Milestone: 15 Nov deadline  ·  20 Nov pengumuman finalis  ·  24 Nov final + closing (Hotel Aston Kartika, Jakarta)", {x:M,y:5.6,w:12.1,h:0.5,isTextBox:true,margin:0,fontSize:13,italic:true,color:MUTED,fontFace:BODY});
s.addNotes("Rencana (45 detik). Tim 3 orang, 4 minggu, target submit H-2. Tunjukkan kita punya eksekusi yang realistis, bukan cuma ide.");

// ====================================================================
// SLIDE 12 — PENUTUP (gelap)
// ====================================================================
s = pres.addSlide();
darkBg(s);
s.addText("SIAGA", { x:M, y:2.3, w:11, h:1.4, isTextBox:true, margin:0, fontSize:84, bold:true, color:LTINK, fontFace:HEAD });
s.addText("Mendeteksi koordinasi. Memberi peringatan dini. Menjaga ruang siber sosial Indonesia.", { x:M, y:3.8, w:11, h:1.0, isTextBox:true, margin:0, fontSize:22, color:MUTED_D, fontFace:BODY, lineSpacingMultiple:1.2 });
s.addText("Purwarupa terbukti jalan  ·  novelty dapat dipertahankan  ·  siap dikembangkan untuk TNI AD", { x:M, y:5.0, w:11, h:0.5, isTextBox:true, margin:0, fontSize:15, color:ACCENT, fontFace:BODY });
s.addShape(pres.ShapeType.roundRect,{x:M,y:5.8,w:2.2,h:0.55,rectRadius:0.1,fill:{type:"none"},line:{color:ACCENT,width:1.5}});
s.addText("Terima kasih", { x:M, y:5.8, w:2.2, h:0.55, isTextBox:true, margin:0, align:"center", valign:"middle", fontSize:14, bold:true, color:ACCENT, fontFace:BODY });
s.addNotes("Penutup (30 detik). Tutup dengan kuat: SIAGA menjaga ruang siber sosial Indonesia. Prinsip emas presentasi: tunjukkan yang jalan, jangan hanya ceritakan. Siap untuk tanya-jawab.");

pres.writeFile({ fileName: "SIAGA_Deck_Kartika_2026.pptx" }).then(f => console.log("OK:", f));
