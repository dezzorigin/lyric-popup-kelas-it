"""Uji jadwal lirik lyric-popup-kelas-it — TANPA GUI dan TANPA audio.

Alasan: main.py memakai tkinter (butuh layar) dan pygame (butuh audio).
Keduanya tidak ada di CI headless, jadi yang diuji di sini adalah
kontrak yang bisa dibuktikan tanpa jendela:

  1. LYRICS di main.py: 15 baris, teks + jeda + durasi persis seperti
     yang diklaim README (climax "the cure" 3:20-4:38).
  2. Jadwal konsisten: jeda menaik, tidak ada baris yang mulai sebelum
     detik 0 setelah SYNC_ADJUST, semua durasi positif, total 78 detik.
  3. Konstanta sinkron: SYNC_ADJUST == -500, MUSIC_OFFSET == 193 (3:13).
  4. Landing web memakai data yang sama: LYRICS di app.js identik
     dengan main.py (satu sumber kebenaran, dua presentasi).
  5. lagu.mp3 ada, berukuran wajar, dan header-nya MP3 asli.

Jalankan:  python3 -m pytest tests/ -q
"""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN_PY = ROOT / "main.py"
APP_JS = ROOT / "app.js"
LAGU = ROOT / "lagu.mp3"

EXPECTED_TEXTS = [
    "OHH 'CAUSE BABY I'M UNRAVELED",
    "I'M UNRAVELED",
    "WHY CAN'T YOU COME STITCH ME UP?",
    "WHY CAN'T IT EVER BE ENOUGH?",
    "WHY CAN'T YOU COME STITCH ME UP?",
    "WHY CAN'T IT EVER BE ENOUGH?",
    "IT'S NOT ENOUGH",
    "MY HEAD IS FULL OF POISON",
    "AND MY HEART IS FULL OF DOUBT",
    "I GOT TOXINS IN MY BLOODSTREAM",
    "YOU TRIED SO HARD TO SUCK OUT",
    "AND IT FEELS LIKE MEDICATION",
    "BUT IT DON'T MATTER HOW YOUR LOVE FEELS ANYMORE",
    "IT'LL NEVER BE THE CURE",
    "IT'LL NEVER BE THE CURE",
]


def eval_int_expr(node):
    """Evaluator aman untuk ekspresi integer sederhana (mis. 3 * 60 + 13)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -eval_int_expr(node.operand)
    if isinstance(node, ast.BinOp) and isinstance(
        node.op, (ast.Add, ast.Sub, ast.Mult, ast.FloorDiv)
    ):
        left = eval_int_expr(node.left)
        right = eval_int_expr(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        return left // right
    raise ValueError(f"ekspresi integer tak didukung: {ast.dump(node)}")


def load_main():
    """Parse main.py tanpa mengeksekusi tkinter/pygame."""
    tree = ast.parse(MAIN_PY.read_text(encoding="utf-8"))
    consts = {}
    lyrics = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = node.targets[0].id
            if name in ("SYNC_ADJUST", "MUSIC_OFFSET"):
                consts[name] = eval_int_expr(node.value)
            elif name == "LYRICS":
                lyrics = [tuple(ast.literal_eval(e)) for e in node.value.elts]
    assert lyrics is not None, "LYRICS tidak ditemukan di main.py"
    return lyrics, consts


def load_app_js_lyrics():
    """Ambil array LYRICS dari app.js (JSON setelah normalisasi kutip)."""
    src = APP_JS.read_text(encoding="utf-8")
    m = re.search(r"const LYRICS = (\[.*?\]);", src, re.S)
    assert m, "LYRICS tidak ditemukan di app.js"
    # app.js memakai double-quote JSON-valid untuk string lirik;
    # toleransi trailing comma di akhir array
    raw = re.sub(r",\s*\]", "]", m.group(1))
    return [tuple(row) for row in json.loads(raw)]


def test_lyrics_15_baris_teks_persis():
    lyrics, _ = load_main()
    assert len(lyrics) == 15, f"harus 15 baris, dapat {len(lyrics)}"
    assert [t for t, _, _ in lyrics] == EXPECTED_TEXTS


def test_jadwal_konsisten():
    lyrics, consts = load_main()
    sync = consts["SYNC_ADJUST"]
    starts = [jeda + sync for _, jeda, _ in lyrics]
    # jeda menaik (sesuai urutan lagu)
    assert starts == sorted(starts), "jeda lirik harus menaik"
    # tidak ada yang mulai sebelum detik 0
    assert min(starts) >= 0, f"ada lirik mulai sebelum 0: {min(starts)}ms"
    # semua durasi positif dan wajar (3-7 detik per kotak)
    for _, _, dur in lyrics:
        assert 3000 <= dur <= 7000, f"durasi di luar 3-7 dtk: {dur}"
    # total: baris terakhir muncul 71 dtk + tampil 7 dtk = 78 dtk
    total = max(jeda for _, jeda, _ in lyrics) + max(d for _, _, d in lyrics)
    assert total == 78000, f"total harus 78000ms, dapat {total}"
    # baris terakhir berakhir di 4:38 (200 dtk + 78 dtk)
    assert 200 + total / 1000 == 278


def test_konstanta_sinkron():
    _, consts = load_main()
    assert consts["SYNC_ADJUST"] == -500, "SYNC_ADJUST harus -500 (aman, tidak numpuk di detik 0)"
    assert consts["MUSIC_OFFSET"] == 193, "MUSIC_OFFSET harus 193 detik (3:13)"
    assert consts["SYNC_ADJUST"] >= -500, "SYNC_ADJUST tidak boleh < -500 (komentar main.py)"


def test_waktu_lagu_tiap_baris():
    """Waktu lagu tiap baris = 3:20 + (jeda + SYNC_ADJUST); baris 1 di 3:20."""
    lyrics, consts = load_main()
    sync = consts["SYNC_ADJUST"]
    times = [200 + (jeda + sync) / 1000 for _, jeda, _ in lyrics]
    assert times[0] == 200.0, "baris pertama harus di 3:20"
    assert times[-1] == 270.5, "baris terakhir harus di 4:30,5"
    assert times == sorted(times)


def test_app_js_lyrics_identik_dengan_main_py():
    lyrics, _ = load_main()
    web = load_app_js_lyrics()
    assert web == lyrics, "LYRICS app.js harus identik dengan main.py"


def test_lagu_mp3_ada_dan_valid():
    assert LAGU.exists(), "lagu.mp3 harus ada di repo"
    size = LAGU.stat().st_size
    assert size > 1_000_000, f"lagu.mp3 terlalu kecil: {size} byte"
    head = LAGU.open("rb").read(3)
    is_id3 = head == b"ID3"
    is_frame_sync = len(head) == 3 and head[0] == 0xFF and (head[1] & 0xE0) == 0xE0
    assert is_id3 or is_frame_sync, f"lagu.mp3 bukan MP3 (header: {head!r})"


def test_main_py_tanpa_gui_di_level_modul():
    """Tk() hanya boleh dipanggil di dalam def main(), bukan di level modul —
    supaya main.py aman di-import/di-compile tanpa layar."""
    tree = ast.parse(MAIN_PY.read_text(encoding="utf-8"))
    funcs = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {"main", "play_music"}.issubset(funcs)
    # tidak ada pemanggilan Tk()/mainloop() di statement level modul
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            callee = node.value.func
            name = getattr(callee, "attr", None) or getattr(callee, "id", None)
            assert name not in ("Tk", "mainloop", "main"), f"panggilan GUI di level modul: {name}"
