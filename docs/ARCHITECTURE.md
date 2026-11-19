# ARCHITECTURE.md — Lyric Popup Kelas IT

## Gambaran

Repo ini punya DUA presentasi dari SATU sumber kebenaran — daftar lirik
`LYRICS` di `main.py`:

1. **Script desktop** (`main.py`, tkinter + pygame opsional): produk aslinya.
   Satu `LyricBox` = satu jendela `Toplevel` tanpa title bar yang mengetik
   lirik huruf demi huruf lalu melayang memantul sampai durasinya habis.
2. **Landing statis** (`index.html` + `styles.css` + `app.js`): etalase yang
   di-deploy ke Cloudflare Pages. Pemutar web memutar `lagu.mp3` yang sama
   dan menelurkan kotak lirik dengan jadwal, kecepatan ketik, dan pantulan
   yang sama. `tests/test_lyrics.py` memastikan `LYRICS` di `app.js`
   identik dengan `main.py`.

Tidak ada backend, tidak ada database, tidak ada akun. Satu-satunya
dependensi produksi adalah pygame — dan itu pun opsional.

## Alur desktop (`main.py`)

```
pengguna menjalankan `python main.py`
  └─ play_music() ── ada lagu.mp3? ── ya ──► pygame: play(0, 193)
                        │                      (loncat ke 3:13)
                        └─ tidak ──► lirik tetap jalan tanpa musik
  └─ root.after(jeda + SYNC_ADJUST) untuk tiap baris LYRICS
        └─ LyricBox(root, teks, durasi)
              ├─ typewriter(): 25 ms/huruf
              ├─ melayang(): geser tiap 30 ms, pantul di tepi layar
              ├─ klik kotak → tutup | ESC → tutup semua
              └─ auto-tutup setelah durasi (3,5–7 dtk)
  └─ SPASI → cek posisi musik (kalibrasi), total 78 dtk lalu keluar
```

Konstanta sinkron (jangan diubah sepihak — tes menguncinya):

| Konstanta | Nilai | Arti |
|---|---|---|
| `SYNC_ADJUST` | `-500` ms | lirik dimajukan 0,5 dtk; jangan < −500 (numpuk di detik 0) |
| `MUSIC_OFFSET` | `193` dtk (3:13) | musik loncat ke sini; lirik pertama di 3:20 |
| `TYPE_SPEED` | `25` ms/huruf | kecepatan ketik |
| `GERAK_SPEED` | `30` ms/frame | kecepatan pantulan |
| `BOX_W` × `BOX_H` | `620` × `180` | ukuran kotak lirik |

Segmen yang dicover: 3:20–4:38 (78 detik, 15 baris). Komentar asli di
`main.py` menulis "3:20–4:35", tapi jadwalnya berakhir 4:38 — baris
terakhir muncul 4:30,5 dan tampil 7 detik. Angka 4:38 yang dipakai di
landing dan tes, karena jadwal adalah sumber kebenaran.

## Alur web (`app.js`)

```
pengguna tekan Putar
  └─ audio.currentTime = 193 (MUSIC_OFFSET) → audio.play()
  └─ timeupdate → tick(now): tiap baris yang waktunya tiba → spawnBox(i)
        └─ spawnBox: typewriter 25 ms/huruf + drift pantul 30 ms/frame
           di dalam .stage, klik → tutup, auto-tutup setelah durasi
  └─ ESC → tutup semua · SPASI → tampilkan posisi · klik baris setlist → lompat
  └─ tombol "Lirik saja, tanpa audio": jadwal jalan dari jam dinding
     (cermin perilaku desktop tanpa pygame)
```

`lagu.mp3` (7,8 MB) di-deploy sebagai aset statis Pages supaya pemutar
web benar-benar berbunyi. File ini sudah publik di repo; landing
mencantumkan tautan Spotify/YouTube resmi dan menyatakan lirik sebagai
kutipan demo.

## File

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
docs/                    PRD, DESIGN, ARCHITECTURE, USAGE, TESTING,
                         DEPLOY, diagrams.html
```

Lihat `docs/diagrams.html` untuk diagram modul dan alur (HTML+SVG).
