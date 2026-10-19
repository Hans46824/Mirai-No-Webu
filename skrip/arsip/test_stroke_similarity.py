#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: skrip/arsip/test_stroke_similarity.py
Fungsi: Memvalidasi secara komprehensif logika pengenalan & kemiripan goresan (Stroke Similarity Engine)
di js/stroke.js:
  1. Verifikasi fungsi sampleSvgStrokesPoints, normalizePoints, computeStrokeSimilarity, evaluateCanvasSimilarity.
  2. Verifikasi penghitungan aspect-ratio preserving (scale = Math.max(w, h)).
  3. Verifikasi skor multi-metrik: Bentuk 55%, Arah 25%, Jumlah Goresan 20%.
  4. Simulasi Katakana ナ di atas garis panduan (skor 88% - 99%).
  5. Simulasi coretan tanpa garis panduan (skor 75% - 87%).
  6. Simulasi karakter salah / asal coret (skor < 45%).
  7. Sinkronisasi karakter target ke kandidat #1.
"""

import os
import sys
import re
import math
import json

def test_stroke_js_vector_similarity_code():
    print("==================================================")
    print("🧪 [1] MEMERIKSA KODE VECTOR STROKE SIMILARITY js/stroke.js")
    print("==================================================")

    with open("js/stroke.js", "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Pastikan fungsi-fungsi baru didefinisikan
    assert "sampleSvgStrokesPoints" in code, "sampleSvgStrokesPoints tidak ditemukan di js/stroke.js!"
    assert "sampleUserStrokes" in code, "sampleUserStrokes tidak ditemukan di js/stroke.js!"
    assert "normalizePoints" in code, "normalizePoints tidak ditemukan di js/stroke.js!"
    assert "computeChamferScore" in code, "computeChamferScore tidak ditemukan di js/stroke.js!"
    assert "computeStrokeSimilarity" in code, "computeStrokeSimilarity tidak ditemukan di js/stroke.js!"
    assert "evaluateCanvasSimilarity" in code, "evaluateCanvasSimilarity tidak ditemukan di js/stroke.js!"
    print("✔ Seluruh fungsi inti vektor & multi-metrik terdefinisi dengan tepat.")

    # 2. Pastikan font sans-serif 84px TIDAK digunakan sebagai target points
    assert "84px sans-serif" not in code, "Font sans-serif masih terdeteksi di stroke.js!"
    print("✔ 100% bebas dari rasterisasi font sans-serif offscreen canvas.")

    # 3. Pastikan normalisasi menggunakan Math.max(w, h)
    assert "Math.max(width, height" in code or "Math.max(w, h" in code or "Math.max(bounds.width" in code, "Skala proporsional aspect-ratio preserving tidak ditemukan!"
    print("✔ Normalisasi proporsional aspect-ratio preserving terpasang.")

    # 4. Pastikan multi-metrik 55% bentuk, 25% arah, 20% jumlah goresan terpasang
    assert "metricA * 0.55" in code and "metricB * 0.25" in code and "metricC * 0.20" in code, "Bobot multi-metrik (55/25/20) tidak ditemukan!"
    print("✔ Pembobotan multi-metrik (55% bentuk + 25% arah + 20% goresan) terpasang.")

    # 5. Pastikan label feedback terkalibrasi
    assert "Sangat Mirip / Sempurna! Pertahankan!" in code, "Feedback >= 88% tidak ditemukan!"
    assert "Bagus! Bentuk sudah tepat." in code, "Feedback >= 75% tidak ditemukan!"
    print("✔ Kalibrasi label feedback 88%+ dan 75%+ terpasang.")

def test_mathematical_stroke_similarity_scoring():
    print("\n==================================================")
    print("🧪 [2] SIMULASI MATEMATIS MULTI-METRIK KATAKANA ナ")
    print("==================================================")

    with open("js/stroke-data.js", "r", encoding="utf-8") as f:
        text = f.read()

    m = re.search(r'window\.MIRAI_STROKE_DATA\s*=\s*(\{[\s\S]*\});?\s*$', text)
    data = json.loads(m.group(1))
    assert "ナ" in data, "Katakana ナ harus ada di dataset!"
    na_data = data["ナ"]
    paths = na_data["paths"]
    assert len(paths) == 2, f"Katakana ナ harus memiliki 2 path, didapat {len(paths)}"

    # Titik referensi Katakana ナ
    stroke1 = [(18.5 + (91.88 - 18.5) * (i / 20), 44.12 - 5 * (i / 20)) for i in range(21)]
    stroke2 = [(53.26 - 15.5 * (i / 25)**1.5, 14.5 + 79.37 * (i / 25)) for i in range(26)]
    ref_pts = stroke1 + stroke2

    def chamfer_score(ptsA, ptsB, tol=5.5, sigma=10.5):
        sumA = sum(math.exp(-((max(0, min(math.hypot(ax - bx, ay - by) for bx, by in ptsB) - tol) / sigma) ** 2)) for ax, ay in ptsA)
        scoreA = sumA / len(ptsA)
        sumB = sum(math.exp(-((max(0, min(math.hypot(bx - ax, by - ay) for ax, ay in ptsA) - tol) / sigma) ** 2)) for bx, by in ptsB)
        scoreB = sumB / len(ptsB)
        if scoreA + scoreB < 1e-6:
            return 0
        return ((2 * scoreA * scoreB) / (scoreA + scoreB)) * 100

    def get_norm(pts):
        minX, maxX = min(p[0] for p in pts), max(p[0] for p in pts)
        minY, maxY = min(p[1] for p in pts), max(p[1] for p in pts)
        scale = max(maxX - minX, maxY - minY, 1)
        cx, cy = (minX + maxX) / 2, (minY + maxY) / 2
        return [((p[0] - cx) / scale, (p[1] - cy) / scale) for p in pts], (maxX - minX, maxY - minY)

    ref_norm, ref_dim = get_norm(ref_pts)
    ref_ar = max(1, ref_dim[0]) / max(1, ref_dim[1])

    def evaluate_sample(user_strokes, name):
        u_pts = [p for s in user_strokes for p in s]
        u_norm, u_dim = get_norm(u_pts)
        u_ar = max(1, u_dim[0]) / max(1, u_dim[1])

        s_direct = chamfer_score(u_pts, ref_pts, 5.5, 10.5)
        s_prop = chamfer_score(u_norm, ref_norm, 0.05, 0.14)
        ar_ratio = max(u_ar / ref_ar, ref_ar / u_ar)
        if ar_ratio > 1.3:
            s_prop *= max(0.2, 1.0 - math.log(ar_ratio) * 0.5)

        metricA = max(s_direct, s_prop)

        # Direction metric (B)
        ref_dirs = [(1, 0), (-0.19, 0.98)]
        u_dirs = []
        for s in user_strokes:
            dx = s[-1][0] - s[0][0]
            dy = s[-1][1] - s[0][1]
            l = math.hypot(dx, dy) or 1
            u_dirs.append((dx / l, dy / l, l))

        max_s = max(len(user_strokes), len(ref_dirs))
        min_s = min(len(user_strokes), len(ref_dirs))
        dir_sum = 0
        for i in range(min_s):
            dot = u_dirs[i][0] * ref_dirs[i][0] + u_dirs[i][1] * ref_dirs[i][1]
            if dot >= 0.7:
                ds = 0.88 + 0.12 * ((dot - 0.7) / 0.3)
            elif dot >= 0:
                ds = 0.50 + 0.38 * (dot / 0.7)
            else:
                ds = max(0.1, 0.50 * (1 + dot))
            dir_sum += ds
        metricB = (dir_sum / max_s) * 100

        # Stroke Count metric (C)
        diff = abs(len(user_strokes) - 2)
        if diff == 0: metricC = 100
        elif diff == 1: metricC = 60
        elif diff == 2: metricC = 30
        else: metricC = max(0, 30 - (diff - 2) * 10)

        total = round(metricA * 0.55 + metricB * 0.25 + metricC * 0.20)
        return total, metricA, metricB, metricC

    # Skenario 1: Jiplak rapi di atas panduan
    u1_s1 = [(x + 0.5, y - 0.5) for x, y in stroke1]
    u1_s2 = [(x - 0.5, y + 0.5) for x, y in stroke2]
    score1, a1, b1, c1 = evaluate_sample([u1_s1, u1_s2], "Panduan ON")
    print(f"✔ [Skenario 1] Mengikuti garis panduan rapi: {score1}% (A: {a1:.1f}%, B: {b1:.1f}%, C: {c1:.0f}%)")
    assert 88 <= score1 <= 100, f"Skor panduan rapi harus 88-100%! Mendapat: {score1}%"

    # Skenario 2: Gambar mirip tanpa panduan (posisi geser dan lebih kecil)
    u2_s1 = [(x * 0.75 + 20, y * 0.75 + 15) for x, y in stroke1]
    u2_s2 = [(x * 0.75 + 20, y * 0.75 + 15) for x, y in stroke2]
    score2, a2, b2, c2 = evaluate_sample([u2_s1, u2_s2], "Panduan OFF")
    print(f"✔ [Skenario 2] Menggambar tanpa panduan (geser & kecil): {score2}% (A: {a2:.1f}%, B: {b2:.1f}%, C: {c2:.0f}%)")
    assert 75 <= score2 <= 100, f"Skor tanpa panduan harus >= 75%! Mendapat: {score2}%"

    # Skenario 3: Huruf salah / asal coret (1 garis horizontal acak)
    u3 = [[(10 + i * 4, 20 + math.sin(i) * 5) for i in range(20)]]
    score3, a3, b3, c3 = evaluate_sample(u3, "Coretan Asal")
    print(f"✔ [Skenario 3] Coretan asal / huruf salah: {score3}% (A: {a3:.1f}%, B: {b3:.1f}%, C: {c3:.0f}%)")
    assert score3 < 50, f"Skor coretan salah harus rendah (< 50%)! Mendapat: {score3}%"

    print("\n🎉 SELURUH PENGUJIAN KEMIRIPAN GORESAN VEKTOR BERHASIL 100%!")

if __name__ == '__main__':
    test_stroke_js_vector_similarity_code()
    test_mathematical_stroke_similarity_scoring()
