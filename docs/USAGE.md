# USAGE.md — Cara Pakai Lyric Popup Kelas IT

## Yang asli: script desktop

```bash
git clone https://github.com/dezzorigin/lyric-popup-kelas-it.git
cd lyric-popup-kelas-it
pip install -r requirements.txt   # pygame saja; boleh dilewati
python main.py
```

- Butuh Python 3.10+ dan tkinter (bawaan di kebanyakan instalasi Python
  desktop Windows/macOS/Linux).
- `lagu.mp3` sudah ada di repo. Mau ganti lagu? Taruh MP3 yang kamu punya
  dengan nama `lagu.mp3` (atau `the_cure.mp3` / `music.mp3`).
- Tanpa pygame, lirik tetap jalan — cuma tanpa musik. Script mencetak
  tautan YouTube/Spotify resmi kalau tidak ada file musik.

### Kontrol saat jalan

| Tombol | Fungsi |
|---|---|
| `ESC` | tutup semua kotak, keluar |
| `SPASI` | cek detik musik sekarang (kalibrasi) |
| Klik kotak | tutup kotak itu saja |

### Kalibrasi sinkron

Kalau lirik terasa kecepatan, tambah `SYNC_ADJUST` di `main.py`
(mis. `-500` → `0` memundurkan semua lirik 0,5 detik). Kalau
kelambatan, kurangi — tapi jangan di bawah `-500`, nanti lirik
numpuk di detik 0. Kalau masih telat, majukan `MUSIC_OFFSET`
(kecilkan angkanya), bukan `SYNC`.

Lirik yang dipakai: climax "the cure" Olivia Rodrigo, 3:20–4:38,
15 baris. Daftar lengkapnya ada di setlist landing
(https://lyric-popup-kelas-it.pages.dev/) dan di `LYRICS` `main.py`.

## Pemutar web (etalase)

Buka https://lyric-popup-kelas-it.pages.dev/ — tidak perlu install
apa pun:

- **Putar dari 3:13**: memutar `lagu.mp3` dari `MUSIC_OFFSET`, kotak
  lirik muncul mengikuti jadwal yang sama dengan desktop.
- **Lirik saja, tanpa audio**: kalau browser memblokir audio atau
  `lagu.mp3` gagal dimuat, jadwal tetap jalan dari jam dinding.
- **Lompat ke 3:20**: langsung ke lirik pertama.
- Klik baris setlist untuk lompat ke detik baris itu; klik kotak lirik
  untuk menutupnya; ESC menutup semua; Spasi menampilkan posisi lagu.

## Batas yang jujur

- Script desktop butuh layar: di server headless / CI tanpa display,
  `main.py` tidak bisa membuka jendela. Itu batas platform, bukan bug.
  Verifikasi otomatis di CI hanya `py_compile` + uji jadwal tanpa GUI
  (lihat `docs/TESTING.md`).
- Audio web memakai `lagu.mp3` dari repo — file demo pribadi, bukan
  distribusi resmi. Dengarkan lagu resminya di Spotify/YouTube
  (tautan ada di landing).
