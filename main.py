"""
KELAS IT - Lyric Popup: Olivia Rodrigo - the cure
Cara run: python main.py
Tombol ESC untuk tutup semua.

+ Kalau ada file lagu.mp3 di folder yang sama -> otomatis diputar bareng liriknya.
  (taruh MP3 resmi yang kamu punya, rename jadi lagu.mp3)
  pip install pygame  # sekali aja biar ada suaranya
"""

import tkinter as tk
import random
import os
import sys

# ===== PENGATURAN =====
BG_COLOR = "#F5F1E8"      # krem / putih tulang kayak di video
FG_COLOR = "black"
FONT_JUDUL = ("Impact", 28, "bold")  # kalau di Linux Impact tidak ada, otomatis fallback
FONT_FALLBACK = ("Arial Black", 24, "bold")
BOX_W = 620
BOX_H = 180
TYPE_SPEED = 25  # ms per huruf, makin kecil makin cepat
GERAK_SPEED = 30  # ms per gerakan

# Lirik: Olivia Rodrigo - the cure (PART 3:20 - 4:35 aja, bagian climax/outro)
# format: (teks, jeda_muncul_ms_setelah_start, durasi_tampil_ms)
# 0 ms di code = 3:20 di lagu asli
LYRICS = [
    ("OHH 'CAUSE BABY I'M UNRAVELED", 500, 5000),
    ("I'M UNRAVELED", 5500, 3500),
    ("WHY CAN'T YOU COME STITCH ME UP?", 9000, 5000),
    ("WHY CAN'T IT EVER BE ENOUGH?", 14500, 5000),
    ("WHY CAN'T YOU COME STITCH ME UP?", 20000, 5000),
    ("WHY CAN'T IT EVER BE ENOUGH?", 25500, 5000),
    ("IT'S NOT ENOUGH", 31000, 4000),
    ("MY HEAD IS FULL OF POISON", 35500, 4500),
    ("AND MY HEART IS FULL OF DOUBT", 40500, 4500),
    ("I GOT TOXINS IN MY BLOODSTREAM", 45500, 4500),
    ("YOU TRIED SO HARD TO SUCK OUT", 50500, 4500),
    ("AND IT FEELS LIKE MEDICATION", 55500, 4500),
    ("BUT IT DON'T MATTER HOW YOUR LOVE FEELS ANYMORE", 60500, 5000),
    ("IT'LL NEVER BE THE CURE", 66000, 6000),
    ("IT'LL NEVER BE THE CURE", 71000, 7000),
]

# ===== SETTING SINKRON (gampang disetel biar PAS) =====
# Kalau lirik kecepatan -> tambah SYNC_ADJUST, kalau kelambatan -> kurangin
# Satuan ms. Contoh: 1500 = mundurin semua lirik 1.5 detik
# PENTING: jangan lebih negatif dari -500 biar ga numpuk di detik 0.
# Kalau masih telat, majuin MUSIC_OFFSET (kecilin angkanya) bukan SYNC.
SYNC_ADJUST = -500  # aman, ga bikin numpuk

# detik offset biar musik langsung loncat ke bagian 3:20
# file kamu 314 detik (lebih panjang 17 detik dari ori 297 detik)
# tadinya 200, dimajuin 7 detik jadi 193 (3:13) biar lirik ga telat 5 detik + ga numpuk
MUSIC_OFFSET = 3 * 60 + 13  # 193 detik

YOUTUBE_URL = "https://www.youtube.com/watch?v=B402rKl4bUg"
SPOTIFY_URL = "https://open.spotify.com/track/77JxSDvDcZVXNptwJOTX3m"


def play_music():
    """Coba putar lagu.mp3 langsung dari menit 3:20 kalau ada."""
    base = os.path.dirname(os.path.abspath(__file__))
    for nama in ["lagu.mp3", "the_cure.mp3", "music.mp3", "the cure.mp3"]:
        path = os.path.join(base, nama)
        if os.path.exists(path):
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(path)
                try:
                    # langsung loncat ke offset (3:13 biar pas)
                    pygame.mixer.music.play(0, MUSIC_OFFSET)
                    print(f"Playing dari {MUSIC_OFFSET:.0f}s (3:13): {nama}")
                except Exception:
                    pygame.mixer.music.play()
                    print(f"Playing dari awal (seek gagal): {nama}")
                    print("TIP: potong manual MP3 ke 3:20-4:35 biar pas.")
                return True
            except Exception as e:
                print(f"Gagal play {nama}: {e}")
                print("Install dulu: pip install pygame")
                return False
    print("\n[TIP MUSIK 3:20-4:35] Taruh file MP3 di folder class_it dengan nama 'lagu.mp3'")
    print("Nanti otomatis diputar mulai dari detik 3:20.")
    print(f"Official MV : {YOUTUBE_URL}")
    print(f"Spotify     : {SPOTIFY_URL}")
    print("Lirik tetap jalan tanpa musik kok (durasi 75 detik).\n")
    return False


class LyricBox:
    """Satu kotak lirik melayang."""

    def __init__(self, master, full_text, duration=4000):
        self.full_text = full_text
        self.typewriter_index = 0

        self.win = tk.Toplevel(master)
        self.win.overrideredirect(True)  # hilangin title bar, kayak di video
        self.win.attributes("-topmost", True)  # selalu di depan
        self.win.configure(bg=BG_COLOR)

        # posisi acak biar kayak di screenshot (numpuk-numpuk)
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.x = random.randint(50, max(60, sw - BOX_W - 50))
        self.y = random.randint(50, max(60, sh - BOX_H - 100))
        # kecepatan melayang
        self.dx = random.choice([-2, -1, 1, 2])
        self.dy = random.choice([-1, 1])

        self.win.geometry(f"{BOX_W}x{BOX_H}+{self.x}+{int(self.y)}")

        # border hitam tipis biar tegas
        border = tk.Frame(self.win, bg="black", padx=3, pady=3)
        border.pack(fill="both", expand=True)
        inner = tk.Frame(border, bg=BG_COLOR)
        inner.pack(fill="both", expand=True)

        try:
            font = FONT_JUDUL
            self.label = tk.Label(
                inner, text="", bg=BG_COLOR, fg=FG_COLOR,
                font=font, wraplength=BOX_W - 60, justify="center"
            )
        except Exception:
            self.label = tk.Label(
                inner, text="", bg=BG_COLOR, fg=FG_COLOR,
                font=FONT_FALLBACK, wraplength=BOX_W - 60, justify="center"
            )
        self.label.pack(expand=True)

        # klik kotak untuk tutup manual
        self.win.bind("<Button-1>", lambda e: self.close())
        self.label.bind("<Button-1>", lambda e: self.close())

        self.typewriter()   # mulai efek ketik
        self.melayang()     # mulai gerak
        # auto tutup
        self.win.after(duration, self.close)

    def typewriter(self):
        """Efek huruf muncul satu-satu."""
        if self.typewriter_index <= len(self.full_text):
            self.label.config(text=self.full_text[:self.typewriter_index])
            self.typewriter_index += 1
            self.win.after(TYPE_SPEED, self.typewriter)

    def melayang(self):
        """Gerakin window mantul kayak screensaver DVD."""
        try:
            self.x += self.dx
            self.y += self.dy

            sw = self.win.winfo_screenwidth()
            sh = self.win.winfo_screenheight()

            if self.x <= 0 or self.x + BOX_W >= sw:
                self.dx = -self.dx
            if self.y <= 0 or self.y + BOX_H >= sh:
                self.dy = -self.dy

            self.win.geometry(f"{BOX_W}x{BOX_H}+{self.x}+{int(self.y)}")
            self.win.after(GERAK_SPEED, self.melayang)
        except Exception:
            pass  # window sudah ditutup

    def is_offscreen(self):
        return self.y > self.win.winfo_screenheight() + 50

    def close(self):
        try:
            self.win.destroy()
        except Exception:
            pass


def main():
    import time
    t0 = time.time()
    has_music = play_music()  # putar lagu.mp3 kalau ada
    root = tk.Tk()
    root.withdraw()  # sembunyikan window utama, cuma popup yang tampil
    root.attributes("-topmost", True)

    boxes = []

    def spawn(i):
        if i < len(LYRICS):
            teks, _, durasi = LYRICS[i]
            import time as _t
            print(f"[{_t.time()-t0:5.1f}s] {teks}")
            boxes.append(LyricBox(root, teks, duration=durasi))

    # jadwalkan tiap lirik muncul sesuai timing + SYNC_ADJUST
    for i, (teks, jeda, durasi) in enumerate(LYRICS):
        root.after(max(0, jeda + SYNC_ADJUST), lambda i=i: spawn(i))

    # total waktu + buffer, lalu keluar otomatis
    total = max(j for _, j, _ in LYRICS) + 7000 if LYRICS else 5000
    #тики root.after(total, root.destroy)

    # ESC = tutup semua (penting buat demo di kelas)
    def tutup_semua(e=None):
        for b in boxes:
            b.close()
        root.destroy()

    root.bind("<Escape>", tutup_semua)
    root.after(total, tutup_semua)

    # SPASI = cek posisi musik sekarang (buat kalibrasi biar pas)
    def cek_posisi(e=None):
        try:
            import pygame
            pos = pygame.mixer.music.get_pos() / 1000.0  # detik sejak play
            print(f"Musik di: {MUSIC_OFFSET + pos:.1f}s total ({pos:.1f}s sejak 3:20)")
        except Exception as ex:
            print(f"cek gagal: {ex}")
    root.bind("<space>", cek_posisi)

    print("=== LYRIC VIDEO BERJALAN (3:20-4:35) ===")
    print("ESC = tutup | SPASI = cek detik musik buat kalibrasi")
    print(f"SYNC_ADJUST sekarang: {SYNC_ADJUST}ms")
    root.mainloop()


if __name__ == "__main__":
    main()
