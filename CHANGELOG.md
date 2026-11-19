# Changelog

Semua perubahan penting proyek ini dicatat di sini.
Format mengikuti [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-11-19

### Added
- Landing statis (etalase + pemutar web): `index.html`, `styles.css`,
  `app.js`, `favicon.svg` — pemutar `lagu.mp3` dengan jadwal, kecepatan
  ketik, dan pantulan kotak yang sama persis dengan `main.py`, plus
  setlist 15 baris 3:20–4:38 dan mode "lirik saja, tanpa audio".
- `tests/test_lyrics.py`: 7 tes jadwal lirik tanpa GUI/audio (AST parse).
- CI (`.github/workflows/ci.yml`): py_compile + pytest, html-validate +
  gate P0 anti-slop + OG, advisory-sweep OSV (pygame), Playwright e2e,
  smoke file deploy.
- Docs: `docs/DESIGN.md` (kontrak desain + referensi Dribbble),
  `ARCHITECTURE.md`, `USAGE.md`, `TESTING.md`, `DEPLOY.md`,
  `diagrams.html` (HTML+SVG), `PRD.md` ditulis ulang (v2.0).
- `requirements.txt` (pygame==2.6.1, opsional), `package.json`
  (devDependencies html-validate + Playwright), `scripts/` (sweep,
  check-static, make-og-image, verify-live), `og-image.png` (PIL,
  1200×630, mengikuti palet landing).
- Deploy Cloudflare Pages: https://lyric-popup-kelas-it.pages.dev/

### Changed
- README ditulis ulang: cara jalan yang benar (`python main.py`,
  bukan `npm install` / `npm run dev` dari template lama).
- PRD ditulis ulang (v2.0): menggambarkan produk sebenarnya.
- CHANGELOG ini ditulis ulang: isi sebelumnya mengklaim setup Next.js,
  popup component, dan theme toggle yang tidak pernah ada di repo ini.

### Fixed
- Koreksi rentang segmen: komentar lama menulis 3:20–4:35, padahal
  jadwal berakhir 4:38 (baris terakhir 4:30,5 + tampil 7 detik).
  Angka 4:38 dipakai di landing, docs, dan tes.

## [1.0.0] - 2026-07-04

### Added
- `main.py`: script desktop tkinter — 15 kotak lirik melayang
  "the cure" (Olivia Rodrigo) 3:20–4:38, typewriter 25 ms/huruf,
  pantulan 30 ms/frame, ESC/Spasi/klik, pemutar `lagu.mp3` via pygame
  dari detik 3:13 (`MUSIC_OFFSET = 193`, `SYNC_ADJUST = -500`).
- `lagu.mp3`, `README.md`, `PRD.md` (v1.0, template), `LICENSE` (MIT),
  `.gitignore`.
