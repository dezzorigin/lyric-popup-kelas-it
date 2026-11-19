# TESTING.md — Pengujian Lyric Popup Kelas IT

## Yang bisa diuji otomatis (CI)

| Job CI | Yang diuji | Bukti |
|---|---|---|
| `python-test` | `py_compile main.py` + 7 tes `tests/test_lyrics.py` | jadwal lirik, konstanta sinkron, `app.js` identik dengan `main.py`, `lagu.mp3` valid |
| `static-checks` | `html-validate index.html` + `npm run validate` (gate P0 + OG) | nol pelanggaran P0, 9 tag OG/Twitter lengkap |
| `advisory-sweep` | `scripts/advisory-sweep.py` (OSV, PyPI) | pygame 2.6.1 bersih dari HIGH/CRITICAL |
| `playwright-e2e` | `e2e/lyric.spec.ts` (desktop + mobile) | kotak muncul/mengetik/hilang, ESC, lompat setlist, salin perintah, tanpa overflow 390px |
| `smoke` | file deploy ada & tidak kosong | `index.html`, `styles.css`, `app.js`, `favicon.svg`, `og-image.png`, `lagu.mp3` |

## Tes Python — kenapa tanpa GUI/audio

`main.py` memakai tkinter (butuh layar) dan pygame (butuh audio).
Keduanya tidak ada di runner CI headless, jadi tes tidak mengimpor
`main.py` — ia mem-parse AST-nya:

- 15 baris lirik, teks persis seperti klaim (climax "the cure").
- Jadwal konsisten: jeda menaik, mulai ≥ 0 setelah `SYNC_ADJUST`,
  durasi 3–7 detik, total 78 detik (berakhir 4:38).
- Konstanta terkunci: `SYNC_ADJUST == -500`, `MUSIC_OFFSET == 193`.
- `LYRICS` di `app.js` identik dengan `main.py` (satu sumber kebenaran).
- `lagu.mp3` ada, > 1 MB, header MP3 asli (ID3/frame sync).
- `Tk()` hanya dipanggil di dalam `def main()`, bukan level modul.

Jalankan lokal:

```bash
python3 -m py_compile main.py
python3 -m pytest tests/ -q
```

## Tes E2E — hanya di CI

Chromium lokal tidak bisa start di sandbox VM dev (mmap memfd
ditolak EPERM), jadi `npm run e2e` hanya jalan di GitHub Actions.
Yang diuji: kotak pertama muncul ~7 detik setelah "Lirik saja"
(mode mulai dari 3:13, lirik pertama di 3:20), mengetik teks lengkap,
auto-tutup setelah 5 detik; ESC menutup semua kotak DAN menghentikan
pertunjukan (seperti desktop yang keluar — tidak ada kotak baru yang
muncul lagi); klik baris setlist
ke-8 melompat ke 3:55; tombol salin menyalin perintah `git clone …
&& python main.py`; mobile 390px tanpa scroll horizontal.

## Yang TIDAK bisa diuji otomatis (jujur)

- **Tampilan desktop asli** (jendela tkinter melayang di atas aplikasi
  lain): butuh layar + mata manusia. Verifikasi manual: jalankan
  `python main.py` di laptop, cek 15 kotak muncul berurutan, memantul,
  dan ESC menutup semua.
- **Sinkron telinga**: apakah lirik terasa pas dengan musik — kalibrasi
  manual pakai Spasi + `SYNC_ADJUST` (lihat `docs/USAGE.md`).
- **Screenshot README + video demo**: follow-up browser live, bukan
  gate merge (screenshot lokal mustahil di sandbox VM ini).
