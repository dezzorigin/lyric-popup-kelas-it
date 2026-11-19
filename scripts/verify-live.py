#!/usr/bin/env python3
"""Verifikasi live lyric-popup-kelas-it.pages.dev (UA browser).

Cek: root 200 + marker landing + semua tag og:/twitter: + og-image.png
200 dengan content-type image/* (bukan text/html — Pages fallback menipu).
"""
import sys
import urllib.request
import urllib.error

BASE = "https://lyric-popup-kelas-it.pages.dev"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    try:
        with urllib.request.build_opener().open(req, timeout=60) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read()


fails = []
st, ct, body = get("/")
print(f"root: {st} {ct} {len(body)} bytes")
if st != 200:
    fails.append(f"root HTTP {st}")
html = body.decode("utf-8", "replace")
for marker in ["Lyric Popup", "Kelas IT", "the cure", "3:20", "4:38",
               "Panggung kotak lirik", "Setlist 3:20"]:
    ok = marker in html
    print(f"marker {marker!r}: {'ADA' if ok else 'HILANG'}")
    if not ok:
        fails.append(f"marker hilang: {marker}")
for tag in ['property="og:title"', 'property="og:description"',
            'property="og:type"', 'property="og:url"',
            'property="og:image" content="https://lyric-popup-kelas-it.pages.dev/og-image.png"',
            'name="twitter:card" content="summary_large_image"',
            'name="twitter:title"', 'name="twitter:description"',
            'name="twitter:image" content="https://lyric-popup-kelas-it.pages.dev/og-image.png"']:
    ok = tag in html
    print(f"tag {tag[:44]}...: {'ADA' if ok else 'HILANG'}")
    if not ok:
        fails.append(f"tag hilang: {tag}")

st, ct, body = get("/og-image.png")
print(f"og-image.png: {st} {ct} {len(body)} bytes")
if st != 200:
    fails.append(f"og-image HTTP {st}")
if not ct.startswith("image/"):
    fails.append(f"og-image content-type bukan image/*: {ct}")
if len(body) < 10_000:
    fails.append(f"og-image terlalu kecil: {len(body)} byte")

st, ct, body = get("/lagu.mp3")
print(f"lagu.mp3: {st} {ct} {len(body)} bytes")
if st != 200:
    fails.append(f"lagu.mp3 HTTP {st}")
if len(body) < 1_000_000:
    fails.append(f"lagu.mp3 terlalu kecil: {len(body)} byte")

if fails:
    print(f"\nFAIL ({len(fails)}):")
    for f in fails:
        print(" - " + f)
    sys.exit(1)
print("\nOK: live terverifikasi penuh")
