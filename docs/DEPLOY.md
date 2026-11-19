# DEPLOY.md — Deploy Lyric Popup Kelas IT

## Yang di-deploy: landing statis

Script desktop `main.py` tidak di-deploy ke mana-mana — ia dijalankan
di laptop (`python main.py`). Yang di-deploy ke Cloudflare Pages adalah
etalase statis di root repo: `index.html`, `styles.css`, `app.js`,
`favicon.svg`, `og-image.png`, dan `lagu.mp3` (aset demo pemutar web).

- URL: https://lyric-popup-kelas-it.pages.dev/
- Proyek Pages: `lyric-popup-kelas-it`
- Cara deploy: `~/workspace/github-actions/cf_pages.py` (direct-upload,
  token via vault — jangan minta kredensial di chat):

```bash
python3 ~/workspace/github-actions/cf_pages.py deploy lyric-popup-kelas-it ~/workspace/lyric-popup-kelas-it
```

Deploy dilakukan dari branch `main` setelah PR merge (bukan dari branch
fitur). Verifikasi sesudah deploy:

```bash
python3 scripts/verify-live.py
```

Yang dicek: root 200 + 6 marker landing + 9 tag OG/Twitter +
`og-image.png` 200 dengan `content-type: image/*` +
`lagu.mp3` 200 dan > 1 MB.

## Nama proyek

Pilihan pertama `lyric-popup-kelas-it`. Kalau create mengembalikan nama
bersufiks (dipakai akun lain), pindah ke fallback `lyric-popup`, lalu
`lirik-popup-kelas-it` — dan perbarui URL di `index.html` (tag OG),
`scripts/check-static.mjs`, `scripts/verify-live.py`, `README.md`,
dan `docs/` sebelum merge.

## Homepage repo

Setelah live terverifikasi, set About → homepage repo ke URL Pages
(`gh_set_homepage.py` / PATCH homepage via GitHub API).
