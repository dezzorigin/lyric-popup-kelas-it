# PRD — Lyric Popup Kelas IT

## 1. Informasi Proyek

| Field | Nilai |
|---|---|
| Nama Proyek | Lyric Popup Kelas IT |
| Tech Stack | Python 3.10+ (tkinter bawaan, pygame opsional) + landing statis HTML/CSS/JS |
| Status | Proper — script jalan, landing live |
| Penanggung Jawab | Nabil Aulia Dika (dezzorigin) |
| Versi Dokumen | 2.0 (ditulis ulang 19 Nov 2026 — v1.0 adalah template generik yang tidak menggambarkan produk) |
| Tanggal | 2026-11-19 |

## 2. Latar Belakang

Demo kelas IT: memutar lagu dan menampilkan liriknya sebagai kotak-kotak
melayang di layar, seperti lyric video — tapi tiap baris lirik jadi
jendelanya sendiri yang bergerak. Dibuat untuk diputar di depan kelas:
satu perintah jalan, tanpa setup panggung.

## 3. Masalah yang Diselesaikan

Lyric video biasa tampil di satu jendela video yang diam. Di sini tiap
baris lirik muncul sebagai kotak tanpa title bar yang mengetik sendiri
lalu melayang memantul di layar — efek yang tidak bisa didapat dari
pemutar video biasa — dan tetap sinkron dengan musik lewat dua
konstanta kalibrasi (`SYNC_ADJUST`, `MUSIC_OFFSET`).

## 4. Tujuan & Sasaran

- Putar `lagu.mp3` dari detik 3:13 dan tampilkan 15 baris climax
  "the cure" (Olivia Rodrigo) 3:20–4:38 secara sinkron.
- Satu perintah (`python main.py`), kontrol demo minimal: ESC tutup
  semua, Spasi cek detik musik, klik kotak untuk menutupnya.
- Tetap jalan tanpa musik (tanpa pygame / tanpa file MP3): lirik
  tampil mengikuti jadwal.
- Landing web sebagai etalase + pemutar dengan jadwal yang sama persis.

## 5. Ruang Lingkup

### In Scope
- `main.py`: 15 baris `LYRICS`, `LyricBox` (typewriter + pantulan),
  `play_music()` (pygame, seek 193 detik), kontrol ESC/Spasi/klik.
- Landing statis: pemutar web `lagu.mp3`, panggung kotak melayang,
  setlist 15 baris, cara jalanin desktop.
- Docs, CI (py_compile + pytest jadwal + gate P0 + OSV + e2e),
  deploy Cloudflare Pages.

### Out of Scope
- Bukan pemutar lagu umum (satu lagu, satu segmen, lirik hardcode).
- Bukan distribusi musik: `lagu.mp3` adalah salinan demo pribadi;
  lagu resmi didengarkan via Spotify/YouTube (tautan di landing).
- Tidak ada sinkronisasi otomatis (tanpa analisis audio); kalibrasi
  manual lewat `SYNC_ADJUST` / `MUSIC_OFFSET`.

## 6. Fitur & Persyaratan Fungsional

| # | Fitur | Kriteria |
|---|---|---|
| F1 | Putar musik dari 3:13 | `play_music()` seek `MUSIC_OFFSET = 193`; gagal seek → main dari awal |
| F2 | 15 kotak lirik 3:20–4:38 | jadwal `jeda + SYNC_ADJUST`, baris 1 di 3:20, terakhir selesai 4:38 |
| F3 | Efek ketik | 25 ms/huruf (`TYPE_SPEED`) |
| F4 | Kotak melayang memantul | gerak 30 ms/frame (`GERAK_SPEED`), pantul di tepi layar |
| F5 | Kontrol demo | ESC tutup semua, Spasi cek detik, klik kotak tutup |
| F6 | Jalan tanpa musik | tanpa pygame/MP3, lirik tetap tampil 78 detik |
| F7 | Pemutar web | jadwal + konstanta sama dengan `main.py`; mode lirik-saja tanpa audio |
| F8 | Setlist | 15 baris + detik kemunculan; klik baris lompat ke detiknya |

## 7. Persyaratan Non-Fungsional

- **Performa:** 15 jendela ringan; gerak 30 ms/frame tanpa lag di laptop kelas.
- **Portabilitas:** Windows/macOS/Linux desktop dengan Python + tkinter.
  Tidak jalan di server headless (butuh layar) — batas yang didokumentasikan.
- **Maintainability:** satu file `main.py`; konstanta sinkron di satu tempat;
  `app.js` diuji identik dengan `main.py` oleh `tests/test_lyrics.py`.
- **Keamanan:** tidak ada secret; satu-satunya dependensi (pygame) di-sweep OSV.

## 8. Arsitektur & Tech Stack

Python + tkinter (GUI) + pygame (audio, opsional). Landing statis tanpa
build step. Detail: `docs/ARCHITECTURE.md`, diagram: `docs/diagrams.html`.

## 9. Milestone / Roadmap

| Fase | Status |
|---|---|
| Script desktop (15 lirik, popup, kalibrasi) | ✅ (awal) |
| Proper P1: docs + tes + CI + landing + deploy | ✅ 19 Nov 2026 |
| Screenshot README + video demo (browser live) | ⏳ follow-up |

## 10. Risiko & Mitigasi

| Risiko | Mitigasi |
|---|---|
| Lirik tidak sinkron dengan MP3 yang dipakai | `SYNC_ADJUST` / `MUSIC_OFFSET` + Spasi buat cek detik |
| tkinter tidak ada (Python minimal) | pesan error jelas; instalasi Python desktop biasa sudah membawa tkinter |
| `lagu.mp3` diganti lagu lain | jadwal lirik hardcode untuk "the cure" — ganti lagu = ganti `LYRICS` juga |
| File audio berhak cipta di repo publik | hanya salinan demo pribadi; landing menautkan kanal resmi |

## 11. Kriteria Keberhasilan

- `python main.py` jalan tanpa error di desktop; 15 kotak muncul berurutan.
- `py_compile` + 7 tes pytest hijau; CI penuh hijau.
- Landing live dengan pemutar web yang memakai jadwal sama; OG lengkap.
- Tidak ada klaim fitur yang tidak ada (dulu: README template menyebut
  `npm install` / `npm run dev` dan CHANGELOG menyebut Next.js — keduanya
  salah dan sudah dihapus 19 Nov 2026).

## 12. Lampiran

- Cara pakai: `docs/USAGE.md` · Pengujian: `docs/TESTING.md` ·
  Deploy: `docs/DEPLOY.md` · Desain: `docs/DESIGN.md`
- Lisensi: MIT (LICENSE)
