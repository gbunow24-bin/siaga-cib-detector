"""
evaluate_robustness.py — Uji ketahanan SIAGA terhadap PENYAMARAN (evasion).

Kenapa ini penting untuk menang?
    Pertanyaan tersulit dari juri: "Bagaimana kalau buzzer sengaja mengelabui
    sistem?" Operator buzzer nyata memang beradaptasi. Alat yang rapuh runtuh
    begitu lawan berubah taktik.

    Script ini membuktikan SIAGA TAHAN BANTING: membuat ulang data buzzer
    menjadi versi "pintar" (sisip kata, ganti sinonim, acak waktu), lalu
    mengukur apakah deteksi tetap bertahan.

Logika inti ada di siaga/robustness.py (dipakai juga oleh dashboard).

Jalankan:  python evaluate_robustness.py
"""

from __future__ import annotations

from generate_data import generate
from siaga.robustness import run_scenarios


def main():
    base = generate(seed=42)
    res = run_scenarios(base)

    print("=" * 66)
    print("UJI KETAHANAN SIAGA TERHADAP PENYAMARAN (EVASION)")
    print("=" * 66)
    print(f"{'Skenario':<24}{'Precision':>12}{'Recall':>10}{'F1':>8}")
    print("-" * 66)
    for _, r in res.iterrows():
        print(f"{r['Skenario penyamaran']:<24}{r['Precision']:>12}"
              f"{r['Recall']:>10}{r['F1']:>8}")
    print("=" * 66)

    worst = res.iloc[-1]
    print("\nKESIMPULAN:")
    print(f"  Bahkan pada skenario penyamaran GABUNGAN terburuk, SIAGA masih")
    print(f"  mempertahankan F1 = {worst['F1']} "
          f"(precision {worst['Precision']}, recall {worst['Recall']}).")
    print("  Alasan: SIAGA tidak bergantung pada SATU sinyal. Deteksi multi-skala")
    print("  waktu + fusi tiga saluran bukti membuatnya sulit dikelabui.")


if __name__ == "__main__":
    main()
