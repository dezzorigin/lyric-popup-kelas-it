# Lyric Popup Kelas IT

Script desktop Python yang memutar lagu dan menelurkan **15 kotak lirik
melayang** — Olivia Rodrigo, **"the cure"**, bagian climax 3:20–4:38.
Tiap baris lirik jadi satu jendela tanpa title bar yang mengetik sendiri
lalu melayang memantul seperti screensaver DVD, sinkron dengan musik.

> **Live:** https://lyric-popup-kelas-it.pages.dev/ — etalase + pemutar
> web dengan jadwal yang sama persis (tanpa install apa pun).
> Screenshot README + video demo: follow-up browser live (lihat
> `docs/TESTING.md`).

## Cara jalan (desktop)

```bash
git clone https://github.com/dezzorigin/lyric-popup-kelas-it.git
cd lyric-popup-kelas-it
pip install -r requirements.txt   # pygame saja; boleh dilewati
python main.py
```

- Butuh Python 3.10+ dan tkinter (bawaan di kebanyakan instalasi Python
  desktop). Tidak jalan di server headless — butuh layar.
- `lagu.mp3` sudah ada di repo. Mau ganti lagu? Taruh MP3 yang kamu
  punya dengan nama `lagu.mp3`.
- Tanpa pygame, lirik tetap jalan — cuma tanpa musik.

| Tombol | Fungsi |
|---|---|
| `ESC` | tutup semua kotak, keluar |
| `SPASI` | cek detik musik sekarang (kalibrasi) |
| Klik kotak | tutup kotak itu saja |

Kalibrasi sinkron ada di `main.py`: `SYNC_ADJUST = -500` (majukan lirik
0,5 detik; jangan di bawah −500) dan `MUSIC_OFFSET = 193` (musik loncat
ke 3:13, lirik pertama muncul 3:20). Detail: `docs/USAGE.md`.

## Setlist 3:20–4:38

15 baris dari `LYRICS` di `main.py` — dibuka `OHH 'CAUSE BABY I'M
UNRAVELED` di 3:20, ditutup `IT'LL NEVER BE THE CURE` yang muncul dua
kali (4:25,5 dan 4:30,5) dan selesai 4:38. Daftar lengkap + detik tiap
baris ada di landing dan `docs/USAGE.md`.

> Catatan jujur: komentar lama di `main.py` menulis 3:20–4:35, padahal
> jadwalnya berakhir 4:38. Angka 4:38 yang dipakai di mana-mana, karena
> jadwal adalah sumber kebenaran.

## Tech stack

- **Desktop:** Python + tkinter (GUI) + pygame (audio, opsional).
- **Landing:** HTML/CSS/JS statis tanpa build step; `app.js` mencerminkan
  `main.py` — tes memastikan keduanya identik.
- **CI:** py_compile + pytest jadwal lirik, html-validate + gate P0
  anti-slop + tag OG, advisory-sweep OSV, Playwright e2e, smoke.

## Struktur proyek

```
main.py                  script desktop (produk asli)
lagu.mp3                 audio demo (7,8 MB)
requirements.txt         pygame==2.6.1 (opsional)
index.html / styles.css / app.js / favicon.svg / og-image.png
                         landing statis (etalase + pemutar web)
tests/test_lyrics.py     7 tes jadwal (tanpa GUI/audio)
scripts/                 advisory-sweep.py, check-static.mjs,
                         make-og-image.py, verify-live.py
e2e/lyric.spec.ts        Playwright (HANYA di CI)
docs/                    DESIGN, ARCHITECTURE, USAGE, TESTING,
                         DEPLOY, diagrams.html
PRD.md / CHANGELOG.md    spesifikasi + riwayat (root)
```

## Docs

- Desain landing (kontrak + referensi): `docs/DESIGN.md`
- Arsitektur: `docs/ARCHITECTURE.md` · Cara pakai: `docs/USAGE.md`
- Pengujian: `docs/TESTING.md` · Deploy: `docs/DEPLOY.md`
- Diagram: `docs/diagrams.html` · PRD: `PRD.md`

## Lirik & audio

Lirik © Olivia Rodrigo — "the cure", ditampilkan sebagai kutipan demo
sinkronisasi. `lagu.mp3` adalah salinan demo pribadi pemilik repo;
dengarkan lagu resminya di
[Spotify](https://open.spotify.com/track/77JxSDvDcZVXNptwJOTX3m) atau
[YouTube](https://www.youtube.com/watch?v=B402rKl4bUg).

## Lisensi

MIT — lihat [LICENSE](./LICENSE).

---
Dikembangkan oleh **dezzorigin** (Nabil Aulia Dika).
