#!/usr/bin/env python3
"""Generate og-image.png 1200x630 untuk lyric-popup-kelas-it (PIL, lokal).

Desain mengikuti palet landing (docs/DESIGN.md): panggung #171310,
krem #F5F1E8, sorot #F0A500, ungu #6D4BD8. Kartu krem ber-border hitam
tebal + bayangan keras = kotak lirik melayang, detail khas repo ini.
Bukan screenshot — kartu preview yang digambar mengikuti palet landing.

Usage: python3 scripts/make-og-image.py  (tulis ke root repo)
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "og-image.png")

W, H = 1200, 630
PANGGUNG = (23, 19, 16)      # #171310
KREM = (245, 241, 232)       # #F5F1E8
SOROT = (240, 165, 0)        # #F0A500
UNGU = (109, 75, 216)        # #6D4BD8
TINTA = (20, 18, 16)         # #141210
MUTED = (201, 191, 169)      # #C9BFA9
GARIS = (58, 49, 40)         # #3A3128

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def main():
    img = Image.new("RGB", (W, H), PANGGUNG)
    d = ImageDraw.Draw(img)

    # garis sorot atas + bingkai dalam
    d.rectangle([0, 0, W, 10], fill=SOROT)
    d.rectangle([28, 28, W - 28, H - 28], outline=GARIS, width=2)

    # kicker
    f_kick = ImageFont.truetype(MONO_B, 28)
    d.text((72, 64), "KELAS IT  ·  SCRIPT DESKTOP PYTHON", font=f_kick, fill=UNGU)

    # judul poster
    f_title = ImageFont.truetype(SANS_B, 108)
    d.text((68, 116), "Lyric Popup", font=f_title, fill=KREM)
    d.text((68, 226), "Kelas IT", font=f_title, fill=SOROT)

    # kartu kotak lirik melayang (kanan): krem + border hitam + bayangan keras
    cx, cy, cw, ch = 700, 380, 428, 150
    d.rectangle([cx + 10, cy + 10, cx + cw + 10, cy + ch + 10], fill=(0, 0, 0))
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=KREM, outline=(0, 0, 0), width=6)
    f_lyric = ImageFont.truetype(SANS_B, 34)
    d.text((cx + 28, cy + 30), "IT'LL NEVER BE", font=f_lyric, fill=TINTA)
    d.text((cx + 28, cy + 76), "THE CURE", font=f_lyric, fill=TINTA)
    # garis sorot kecil di kartu
    d.rectangle([cx + 28, cy + ch - 22, cx + 120, cy + ch - 14], fill=SOROT)

    # sub + meta kiri bawah
    f_sub = ImageFont.truetype(SANS, 32)
    d.text((72, 380), "Olivia Rodrigo — “the cure”", font=f_sub, fill=KREM)
    d.text((72, 424), "3:20–4:38  ·  15 kotak lirik melayang", font=f_sub, fill=KREM)
    f_meta = ImageFont.truetype(MONO, 26)
    d.text((72, 500), "python main.py  ·  ESC tutup semua", font=f_meta, fill=MUTED)
    f_url = ImageFont.truetype(MONO_B, 28)
    d.text((72, 556), "lyric-popup-kelas-it.pages.dev", font=f_url, fill=SOROT)

    img.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
