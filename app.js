// Lyric Popup Kelas IT — pemutar web.
// Cermin perilaku main.py (bukan produk baru): jadwal, offset, kecepatan
// ketik, dan pantulan kotak diambil langsung dari konstanta di main.py.
//
//   LYRICS        — 15 baris, (teks, jeda_ms_setelah_start, durasi_ms)
//   SYNC_ADJUST   — -500 ms (lirik dimajukan 0,5 detik)
//   MUSIC_OFFSET  — 193 detik (3:13): musik loncat ke sini saat play
//   SEGMENT_START — 200 detik (3:20): lirik pertama muncul
//   SEGMENT_END   — 278 detik (4:38): baris terakhir selesai
//   TYPE_SPEED    — 25 ms per huruf
//   GERAK_SPEED   — 30 ms per frame pantulan
"use strict";

// ── Data: salinan LYRICS dari main.py (jangan diubah sepihak —
//    tests/test_lyrics.py memastikan daftar ini identik dengan main.py).
const LYRICS = [
  ["OHH 'CAUSE BABY I'M UNRAVELED", 500, 5000],
  ["I'M UNRAVELED", 5500, 3500],
  ["WHY CAN'T YOU COME STITCH ME UP?", 9000, 5000],
  ["WHY CAN'T IT EVER BE ENOUGH?", 14500, 5000],
  ["WHY CAN'T YOU COME STITCH ME UP?", 20000, 5000],
  ["WHY CAN'T IT EVER BE ENOUGH?", 25500, 5000],
  ["IT'S NOT ENOUGH", 31000, 4000],
  ["MY HEAD IS FULL OF POISON", 35500, 4500],
  ["AND MY HEART IS FULL OF DOUBT", 40500, 4500],
  ["I GOT TOXINS IN MY BLOODSTREAM", 45500, 4500],
  ["YOU TRIED SO HARD TO SUCK OUT", 50500, 4500],
  ["AND IT FEELS LIKE MEDICATION", 55500, 4500],
  ["BUT IT DON'T MATTER HOW YOUR LOVE FEELS ANYMORE", 60500, 5000],
  ["IT'LL NEVER BE THE CURE", 66000, 6000],
  ["IT'LL NEVER BE THE CURE", 71000, 7000],
];

const SYNC_ADJUST = -500; // ms, sama seperti main.py
const MUSIC_OFFSET = 193; // detik (3:13), sama seperti main.py
const SEGMENT_START = 200; // detik (3:20)
const SEGMENT_END = 278; // detik (4:38)
const TYPE_SPEED = 25; // ms per huruf
const GERAK_SPEED = 30; // ms per frame

// Waktu lagu (detik) saat tiap baris muncul di pemutar web.
function lyricTime(i) {
  return SEGMENT_START + (LYRICS[i][1] + SYNC_ADJUST) / 1000;
}

function fmt(t) {
  const m = Math.floor(t / 60);
  const s = Math.floor(t % 60);
  return m + ":" + String(s).padStart(2, "0");
}

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const audio = document.getElementById("audio");
const stage = document.getElementById("stage");
const stageEmpty = document.getElementById("stage-empty");
const statusEl = document.getElementById("player-status");
const clockNow = document.getElementById("clock-now");
const btnPlay = document.getElementById("btn-play");
const btnPlayLabel = document.getElementById("btn-play-label");
const btnJump = document.getElementById("btn-jump");
const btnNoAudio = document.getElementById("btn-noaudio");
const wave = document.getElementById("wave");
const setlistEl = document.getElementById("setlist");

const boxes = []; // {el, x, y, dx, dy, timer, driftTimer, index}
let spawned = new Set();
let noAudioMode = false;
let noAudioT0 = 0;
let noAudioTimers = [];
let audioFailed = false;

// ── Setlist ───────────────────────────────────────────────────────────
LYRICS.forEach((row, i) => {
  const li = document.createElement("li");
  li.dataset.index = String(i);
  const num = document.createElement("span");
  num.className = "setlist-num";
  num.textContent = String(i + 1).padStart(2, "0");
  const time = document.createElement("span");
  time.className = "setlist-time";
  time.textContent = fmt(lyricTime(i));
  const text = document.createElement("span");
  text.className = "setlist-text";
  text.textContent = row[0];
  const dur = document.createElement("span");
  dur.className = "setlist-dur";
  dur.textContent = (row[2] / 1000).toFixed(1).replace(".", ",") + " dtk";
  li.append(num, time, text, dur);
  li.addEventListener("click", () => {
    seekTo(lyricTime(i));
    statusEl.textContent = "Lompat ke " + fmt(lyricTime(i)) + " — “" + row[0] + "”.";
  });
  setlistEl.appendChild(li);
});

function markActive(i) {
  setlistEl.querySelectorAll("li").forEach((li) => {
    li.classList.toggle("active", Number(li.dataset.index) === i);
  });
  document.querySelectorAll(".lyric-box").forEach((b) => b.classList.remove("active"));
  const box = boxes.find((b) => b.index === i);
  if (box) box.el.classList.add("active");
}

// ── Waveform progress (48 batang, tinggi deterministik) ───────────────
const BAR_COUNT = 48;
const barHeights = [];
for (let i = 0; i < BAR_COUNT; i++) {
  // pola tetap (bukan acak tiap load): gabungan sinus supaya mirip gelombang
  const h = 22 + Math.round(58 * Math.abs(Math.sin(i * 0.9) * 0.7 + Math.sin(i * 0.23) * 0.3));
  barHeights.push(h);
  const bar = document.createElement("span");
  bar.style.height = h + "%";
  wave.appendChild(bar);
}
const bars = Array.from(wave.children);

function paintProgress(now) {
  const p = Math.max(0, Math.min(1, (now - MUSIC_OFFSET) / (SEGMENT_END - MUSIC_OFFSET)));
  const lit = Math.round(p * BAR_COUNT);
  bars.forEach((bar, i) => {
    bar.classList.toggle("on", i < lit);
    bar.classList.toggle("now", i === lit);
  });
  wave.setAttribute("aria-valuenow", String(Math.round(now)));
  clockNow.textContent = fmt(now);
}

// ── Kotak lirik: typewriter + pantulan DVD (mirip LyricBox) ───────────
function spawnBox(i) {
  if (spawned.has(i)) return;
  spawned.add(i);
  stageEmpty.style.display = "none";
  const [text, , duration] = LYRICS[i];

  const box = document.createElement("div");
  box.className = "lyric-box";
  box.setAttribute("role", "button");
  box.setAttribute("tabindex", "0");
  box.setAttribute("aria-label", "Tutup kotak lirik: " + text);
  const inner = document.createElement("div");
  inner.className = "lyric-box-inner";
  const p = document.createElement("p");
  p.className = "lyric-box-text";
  inner.appendChild(p);
  box.appendChild(inner);
  stage.appendChild(box);

  const bw = box.offsetWidth || 360;
  const bh = box.offsetHeight || 120;
  const maxX = Math.max(0, stage.clientWidth - bw);
  const maxY = Math.max(0, stage.clientHeight - bh);
  const state = {
    el: box, index: i,
    x: Math.floor(Math.random() * (maxX + 1)),
    y: Math.floor(Math.random() * (maxY + 1)),
    dx: [-2, -1, 1, 2][Math.floor(Math.random() * 4)],
    dy: [-1, 1][Math.floor(Math.random() * 2)],
    timer: 0, driftTimer: 0,
  };
  box.style.left = state.x + "px";
  box.style.top = state.y + "px";

  // Typewriter 25 ms/huruf — instan kalau reduced-motion.
  let n = 0;
  if (reduceMotion) {
    p.textContent = text;
  } else {
    state.timer = window.setInterval(() => {
      n += 1;
      p.textContent = text.slice(0, n);
      if (n >= text.length) window.clearInterval(state.timer);
    }, TYPE_SPEED);
  }

  // Pantulan tiap 30 ms — mati kalau reduced-motion.
  if (!reduceMotion) {
    state.driftTimer = window.setInterval(() => {
      state.x += state.dx;
      state.y += state.dy;
      const mx = Math.max(0, stage.clientWidth - box.offsetWidth);
      const my = Math.max(0, stage.clientHeight - box.offsetHeight);
      if (state.x <= 0 || state.x >= mx) state.dx = -state.dx;
      if (state.y <= 0 || state.y >= my) state.dy = -state.dy;
      state.x = Math.max(0, Math.min(mx, state.x));
      state.y = Math.max(0, Math.min(my, state.y));
      box.style.left = state.x + "px";
      box.style.top = state.y + "px";
    }, GERAK_SPEED);
  }

  const close = () => closeBox(state);
  box.addEventListener("click", close);
  box.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); close(); } });
  window.setTimeout(() => closeBox(state), duration);
  boxes.push(state);
  markActive(i);
}

function closeBox(state) {
  const idx = boxes.indexOf(state);
  if (idx === -1) return;
  boxes.splice(idx, 1);
  window.clearInterval(state.timer);
  window.clearInterval(state.driftTimer);
  state.el.remove();
  if (boxes.length === 0) {
    const last = Math.max(-1, ...Array.from(spawned));
    if (last >= LYRICS.length - 1) stageEmpty.style.display = "";
  }
  markActive(-1);
}

function closeAll() {
  Array.from(boxes).forEach(closeBox);
  statusEl.textContent = "Semua kotak ditutup (ESC).";
}

// ── Penjadwalan dari posisi lagu ───────────────────────────────────────
function tick(now) {
  paintProgress(now);
  LYRICS.forEach((row, i) => {
    if (!spawned.has(i) && now >= lyricTime(i)) spawnBox(i);
  });
  if (now >= SEGMENT_END && boxes.length === 0 && spawned.size === LYRICS.length) {
    statusEl.textContent = "Selesai — 15 baris tampil, 3:20–4:38. Putar lagi dari 3:13.";
  }
}

function currentPos() {
  if (noAudioMode) return MUSIC_OFFSET + (performance.now() - noAudioT0) / 1000;
  return audio.currentTime || MUSIC_OFFSET;
}

function seekTo(t) {
  // baris yang sudah lewat tidak dimunculkan ulang; baris ke depan dijadwalkan
  spawned = new Set();
  LYRICS.forEach((_, i) => { if (lyricTime(i) < t) spawned.add(i); });
  if (noAudioMode) {
    noAudioT0 = performance.now() - (t - MUSIC_OFFSET) * 1000;
  } else {
    audio.currentTime = t;
  }
  tick(t);
}

// ── Kontrol ───────────────────────────────────────────────────────────
function startPlayback() {
  if (audioFailed) { startNoAudio(); return; }
  if (audio.currentTime < MUSIC_OFFSET || audio.currentTime >= SEGMENT_END) {
    try { audio.currentTime = MUSIC_OFFSET; } catch (e) { /* seek gagal: main dari awal */ }
  }
  const playPromise = audio.play();
  if (playPromise) {
    playPromise.catch(() => {
      // Autoplay/dokumen diblokir atau file gagal: lirik tetap jalan.
      audioFailed = true;
      startNoAudio();
    });
  }
}

function startNoAudio() {
  noAudioMode = true;
  noAudioT0 = performance.now();
  spawned.clear();
  statusEl.textContent = "Mode lirik saja: tanpa audio, jadwal jalan dari 3:20 (seperti main.py tanpa pygame).";
  btnPlayLabel.textContent = "Jeda";
  btnPlay.disabled = true;
  btnJump.disabled = true;
  const step = () => {
    const now = MUSIC_OFFSET + (performance.now() - noAudioT0) / 1000;
    tick(now);
    if (now < SEGMENT_END + 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

btnPlay.addEventListener("click", () => {
  if (!audio.paused && !noAudioMode) {
    audio.pause();
    btnPlayLabel.textContent = "Lanjutkan";
    statusEl.textContent = "Dijeda di " + fmt(audio.currentTime) + ".";
    return;
  }
  btnPlayLabel.textContent = "Jeda";
  statusEl.textContent = "Memutar dari 3:13 — lirik pertama muncul di 3:20.";
  startPlayback();
});

btnJump.addEventListener("click", () => {
  seekTo(SEGMENT_START);
  if (audio.paused && !noAudioMode) startPlayback();
  statusEl.textContent = "Lompat ke 3:20 — lirik pertama.";
});

btnNoAudio.addEventListener("click", () => {
  closeAll();
  spawned.clear();
  startNoAudio();
});

audio.addEventListener("timeupdate", () => { if (!noAudioMode) tick(audio.currentTime); });
audio.addEventListener("error", () => {
  audioFailed = true;
  statusEl.textContent = "lagu.mp3 tidak bisa diputar di browser ini — pakai mode lirik saja, atau jalankan python main.py di desktop.";
});
audio.addEventListener("loadedmetadata", () => {
  if (audio.duration && audio.duration < SEGMENT_END) {
    statusEl.textContent = "Perhatian: lagu.mp3 ini lebih pendek (" + fmt(audio.duration) + ") dari segmen 3:20–4:38 — lirik terakhir mungkin tidak kebagian musik.";
  }
});

// Klik waveform = lompat; keyboard panah = geser 5 detik.
wave.addEventListener("click", (e) => {
  const rect = wave.getBoundingClientRect();
  const p = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
  seekTo(MUSIC_OFFSET + p * (SEGMENT_END - MUSIC_OFFSET));
});
wave.addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
    e.preventDefault();
    const d = e.key === "ArrowRight" ? 5 : -5;
    seekTo(Math.max(MUSIC_OFFSET, Math.min(SEGMENT_END, currentPos() + d)));
  }
});

// ESC tutup semua, Spasi cek detik — sama seperti main.py.
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") { closeAll(); }
  if (e.code === "Space" && !/BUTTON|A|INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
    e.preventDefault();
    const pos = currentPos();
    statusEl.textContent = "Musik di: " + fmt(pos) + " total (" + (pos - SEGMENT_START).toFixed(1) + " dtk sejak 3:20).";
  }
});

// Salin perintah jalankan.
document.querySelectorAll("[data-copy]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(btn.dataset.copy);
      btn.textContent = "Tersalin";
    } catch (e) {
      btn.textContent = "Gagal menyalin — blok perintah di atas";
    }
    window.setTimeout(() => { btn.textContent = "Salin perintah"; }, 2500);
  });
});

paintProgress(MUSIC_OFFSET);
