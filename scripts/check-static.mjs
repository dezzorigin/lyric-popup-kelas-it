// Gate P0 anti-slop + kelengkapan tag OG/Twitter untuk landing lyric-popup.
// Dijalankan CI (npm run validate) — gagal = PR tidak merge.
// Aturan dari ~/workspace/github-actions/ui-anti-slop.md §2-3.
import { readFileSync, existsSync } from "node:fs";

const html = readFileSync("index.html", "utf8");
const css = readFileSync("styles.css", "utf8");
const js = readFileSync("app.js", "utf8");
const failures = [];

function check(cond, msg) {
  if (!cond) failures.push(msg);
}

// ── P0: gradient ──────────────────────────────────────────────────────────
check(!/linear-gradient|radial-gradient|conic-gradient/i.test(css + html),
  "P0: gradient terlarang di hero/background");
check(!/bg-clip-text|background-clip:\s*text/i.test(css + html),
  "P0: teks headline gradient terlarang");
// ── P0: font Inter / Roboto / system font untuk semuanya ──────────────────
check(!/\bInter\b/i.test(css), "P0: font Inter terlarang");
check(!/\bRoboto\b/i.test(css), "P0: font Roboto terlarang");
check(/Anton/.test(css) && /Space Grotesk/.test(css),
  "font harus Anton (display) + Space Grotesk (body/UI)");
// ── P0: emoji mentah sebagai ikon fungsi ──────────────────────────────────
const emojiRe = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u;
check(!emojiRe.test(html), "P0: emoji mentah sebagai ikon terlarang");
// ── P0: copy generik ──────────────────────────────────────────────────────
for (const phrase of ["Elevate your workflow", "Unlock the power", "Supercharge"]) {
  check(!html.toLowerCase().includes(phrase.toLowerCase()),
    `P0: copy generik terlarang: "${phrase}"`);
}
// ── P0: rounded-2xl shadow-lg di semua permukaan ──────────────────────────
check(!/rounded-2xl/.test(html) && !/border-radius:\s*(1rem|16px)/.test(css),
  "P0: rounded-2xl di semua permukaan terlarang");
// ── P0: statistik vanity tanpa sumber ─────────────────────────────────────
for (const phrase of ["99.9% uptime", "10x faster", "50k+ users", "10x lebih cepat"]) {
  check(!html.includes(phrase), `P0: statistik vanity tanpa sumber: "${phrase}"`);
}

// ── Orde-kedua ────────────────────────────────────────────────────────────
check(!/#39d353|#4af626|lime/i.test(css), "orde-kedua: lime fosfor terlarang");
check(!/terracotta|#e2725b/i.test(css + html), "orde-kedua: terracotta terlarang");
check(!/krem \+ terracotta/i.test(css + html), "orde-kedua: krim+terracotta");
// label mono all-caps di mana-mana: kicker boleh satu, selebihnya tidak
const allCapsLabels = (html.match(/class="kicker"/g) || []).length;
check(allCapsLabels <= 1, "orde-kedua: label mono all-caps di mana-mana");
// radius: kontrak 4px tajam, bukan 14px lembut repo #42
check(/--radius: 4px/.test(css), "radius harus 4px tajam sesuai DESIGN.md");

// ── Tag OG + Twitter wajib lengkap ────────────────────────────────────────
const ogRequired = [
  ["og:title", /<meta property="og:title" content="[^"]+"/],
  ["og:description", /<meta property="og:description" content="[^"]+"/],
  ["og:type", /<meta property="og:type" content="website"/],
  ["og:url", /<meta property="og:url" content="https:\/\/lyric-popup-kelas-it\.pages\.dev\/"/],
  ["og:image", /<meta property="og:image" content="https:\/\/lyric-popup-kelas-it\.pages\.dev\/og-image\.png"/],
  ["twitter:card", /<meta name="twitter:card" content="summary_large_image"/],
  ["twitter:title", /<meta name="twitter:title" content="[^"]+"/],
  ["twitter:description", /<meta name="twitter:description" content="[^"]+"/],
  ["twitter:image", /<meta name="twitter:image" content="https:\/\/lyric-popup-kelas-it\.pages\.dev\/og-image\.png"/],
];
for (const [name, re] of ogRequired) {
  check(re.test(html), `tag ${name} tidak ada / tidak absolut ke lyric-popup-kelas-it.pages.dev`);
}
check(existsSync("og-image.png"), "og-image.png tidak ada di root");
check(existsSync("favicon.svg"), "favicon.svg tidak ada di root");

// ── Kejujuran isi ─────────────────────────────────────────────────────────
check(/etalase/i.test(html) && /cermin/i.test(html),
  "landing harus jujur: ini etalase/cermin script desktop, bukan pengganti");
check(/the cure/i.test(html), "lagu 'the cure' harus disebut di landing");
check(/tanpa musik/i.test(html),
  "landing harus jujur: tanpa pygame lirik tetap jalan tanpa musik");

// ── Marker landing + logika ───────────────────────────────────────────────
check(html.includes("Lyric Popup") && html.includes("Kelas IT"),
  "marker 'Lyric Popup Kelas IT' tidak ada");
check(html.includes("3:20") && html.includes("4:38"),
  "rentang segmen 3:20–4:38 tidak ada di landing");
check(js.includes("MUSIC_OFFSET") && js.includes("SYNC_ADJUST"),
  "konstanta sinkron main.py tidak dicerminkan di app.js");
check(js.includes("IT'LL NEVER BE THE CURE"),
  "baris lirik terakhir tidak ada di app.js");

// ── A11y dasar ────────────────────────────────────────────────────────────
check(/aria-label=/.test(html), "tombol/region tanpa aria-label");
check(/<main/.test(html) && /<footer/.test(html), "tag semantik main/footer hilang");
check(/prefers-reduced-motion/.test(css), "reduced-motion tidak dihormati di CSS");

if (failures.length > 0) {
  console.error(`FAIL: ${failures.length} pelanggaran:\n- ${failures.join("\n- ")}`);
  process.exit(1);
}
console.log("OK: gate P0 + tag OG/Twitter + marker landing lolos");
