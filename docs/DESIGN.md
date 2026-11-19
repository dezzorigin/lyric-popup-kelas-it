# DESIGN.md — Lyric Popup Kelas IT

Kontrak arah desain landing (ditulis SEBELUM coding, mengikuti
`~/workspace/github-actions/ui-anti-slop.md` §4). Landing ini etalase untuk
script desktop Python `main.py`, bukan app web pengganti: pemutar web di
halaman ini memutar `lagu.mp3` yang sama dan menelurkan kotak lirik yang
sama — cermin perilaku desktop, bukan produk baru.

## Referensi (tour dulu, baru bangun)

Kebutuhan + keyword: pemutar lagu dengan lirik tersinkron, nuansa panggung /
lyric-video, dipakai mahasiswa kelas IT untuk demo di kelas.

Kandidat yang ditour:

1. **Dribbble — "Music Player UI — Dark Immersive Concept" oleh Sujita Sunam**
   (https://dribbble.com/shots/27504330-Music-Player-UI-Dark-Immersive-Concept)
   — pemutar gelap yang imersif, ungu solid diambil dari sampul album,
   progress berbentuk waveform, kontrol minimal yang mengutamakan musik.
2. **Karakara — Modern MIDI & Karaoke Player** (https://karakara.dev/)
   — lirik karaoke di jendela terpisah yang bisa dilepas dan disusun bebas
   di banyak layar; konsep "satu lirik = satu jendela melayang" ini persis
   perilaku `main.py` (satu `LyricBox` = satu `Toplevel` tanpa title bar).
3. Dribbble dark player generik lain — ditolak: terlalu mirip template
   streaming (cover besar di tengah + kontrol di bawah), tidak ada ruang
   untuk kotak lirik melayang.

**Pemenang: #1 (Dribbble Sujita Sunam)**, struktur yang dicloning: panggung
gelap satu kolom, pemutar besar dengan progress waveform di tengah, kontrol
minimal, warna aksen diambil dari "album" (di sini: era GUTS Olivia
Rodrigo). Yang diubah: cover album diganti **panggung kotak lirik** —
area tempat kotak lirik melayang muncul dan memantul seperti screensaver
DVD (perilaku asli `LyricBox.melayang()`), karena kotak lirik itulah produk
script ini, bukan cover art. Warna ungu dipakai solid sebagai aksen saja,
bukan gradient. Ditambah setlist bernomor 3:20–4:35 dari Karakara (#2):
satu baris = satu popup, lengkap dengan detik kemunculan.

## Palet (6 warna bernama, tiap warna punya tugas)

| Nama | Hex | Peran |
|---|---|---|
| Panggung | `#171310` | latar halaman — panggung gelap yang hangat, bukan slate biru |
| Krem | `#F5F1E8` | kartu kotak lirik — warna `BG_COLOR` asli `main.py`, jujur ke script |
| Sorot | `#F0A500` | lampu sorot amber — CTA utama, baris lirik aktif, progress |
| Ungu | `#6D4BD8` | aksen solid era GUTS — kicker, nomor setlist, fokus |
| Tinta | `#141210` | teks di atas krem |
| Garis | `#3A3128` | garis pemisah / border di atas panggung |

Tidak ada gradient di mana pun. Ungu dan amber tidak pernah dicampur
menjadi gradient — keduanya tampil sebagai bidang solid.

## Tipografi (2 keluarga)

- **Anton** (display, condensed, all-caps) — judul poster, teks kotak lirik,
  angka waktu besar. Rasa poster konser, bukan serif editorial.
- **Space Grotesk** (body/UI) — penjelasan, setlist, tombol, label waktu.
  Angka waktu memakai `font-variant-numeric: tabular-nums`.

## Layout (satu kalimat)

Panggung gelap satu kolom: header poster → pemutar besar dengan progress
waveform → panggung kotak lirik melayang → setlist 15 baris 3:20–4:35 →
cara jalanin script desktop → footer satu baris.

## Satu detail khas

**Kotak lirik melayang**: tiap baris lirik muncul sebagai kartu krem
ber-border hitam 3px dengan bayangan keras, mengetik huruf demi huruf
(typewriter 25 ms/huruf, sama seperti `TYPE_SPEED`), lalu melayang
memantul di dalam panggung seperti screensaver DVD (sama seperti
`LyricBox.melayang()`); klik kartu menutupnya, ESC menutup semua —
semua perilaku ini diwarisi langsung dari `main.py`, bukan hiasan.

## Geometri

Radius 4px tajam di semua permukaan (bukan 14px lembut), border solid
3px hitam pada kartu krem, bayangan keras offset `6px 6px 0` tanpa blur.
Grid 8pt; padding kartu minimal 16px; radius dalam = radius luar − padding.

## Beda dari repo sebelumnya (#42 dao-student-marketplace)

Minimal 3 dari 5 sumbu, di sini 5 dari 5:

| Sumbu | #42 DAOS | #43 ini |
|---|---|---|
| Palet | kertas `#F4F1ED` + merah denyut `#C0392B` | panggung gelap `#171310` + amber sorot + ungu solid |
| Tipografi | Fraunces + IBM Plex Mono | Anton + Space Grotesk |
| Layout | papan triase dua kolom | panggung satu kolom + setlist vertikal |
| Radius/spacing | 14px lembut | 4px tajam + border 3px + bayangan keras |
| Detail khas | kartu kantong darah | kotak lirik melayang DVD-bounce + typewriter |

## Larangan P0 (dicek `scripts/check-static.mjs`)

Nol gradient, nol headline gradient, bukan Inter/Roboto, bukan hero tengah
+ 3 kartu identik, ikon SVG satu bobot (stroke 1.5–2px) bukan emoji,
nol statistik vanity, nol copy generik, nol `rounded-2xl shadow-lg`,
footer satu baris (bukan 4 kolom). Orde-kedua: bukan krim+terracotta,
bukan near-black+lime, label mono all-caps hanya satu kicker, tanpa
hiasan 01/02/03, palet multi-hue (bukan satu hue), bukan dark blue/slate.

## Gate 7 sumbu (nilai sendiri sebelum merge, tiap sumbu minimal 4/5)

1. anti-slop purity — 5: nol P0 + nol orde-kedua (gate otomatis).
2. UX speed & 1-to-3 — 5: satu aksi utama per viewport (Putar), sekunder
   maks 3 (popup, lompat ke 3:20, salin perintah).
3. Tipografi — 5: 2 font, tabular-nums di semua waktu, body ≤75ch.
4. Spacing & geometri — 5: grid 8pt, radius 4px, padding kartu ≥16px.
5. Motion — 4: transisi <200ms ease-out, drift kotak 30 ms/frame seperti
   `GERAK_SPEED`, `prefers-reduced-motion` mematikan drift + typewriter
   jadi instan.
6. A11y — 5: focus ring amber, aria-label di semua tombol ikon,
   tag semantik, kontras AA (krem di panggung, tinta di krem).
7. Mobile — 5: stack vertikal, panggung jadi satu kolom, tanpa scroll
   horizontal di 390px (diuji e2e).

## Tes siluet

Thumbnail hitam-putih landing harus tetap terbaca sebagai "pemutar lagu
dengan kotak lirik melayang", bukan halaman produk generik: blok pemutar
besar + kartu-kartu krem yang menumpuk + garis waktu 3:20–4:35 adalah
siluetnya. Kalau siluetnya bisa jadi landing SaaS apa pun, revisi.
