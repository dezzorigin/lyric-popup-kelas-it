import { test, expect } from "@playwright/test";

// Landing lyric-popup-kelas-it adalah etalase script desktop Python:
// yang diuji adalah konten + interaksi halamannya (pemutar web, kotak
// lirik melayang, setlist, tombol salin). Script desktop-nya sendiri
// diuji di job python-test CI (py_compile + pytest jadwal lirik) —
// bukan di browser, karena tkinter butuh layar.

test("landing tampil: judul, pemutar, panggung, setlist 15 baris", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Lyric Popup Kelas IT/i);
  await expect(page.locator("text=Lyric Popup").first()).toBeVisible();
  await expect(page.locator("text=the cure").first()).toBeVisible();
  await expect(page.locator("text=3:20").first()).toBeVisible();
  await expect(page.locator("#setlist li")).toHaveCount(15);
  await expect(page.locator("text=IT'LL NEVER BE THE CURE").first()).toBeVisible();
  // kejujuran isi: ini etalase script desktop
  await expect(page.locator("text=etalase").first()).toBeVisible();
});

test("mode lirik saja: kotak muncul, mengetik, lalu hilang", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Lirik saja, tanpa audio" }).click();
  // Mode lirik saja mulai dari 3:13 (MUSIC_OFFSET) seperti main.py —
  // baris pertama muncul di 3:20, jadi ~7 detik setelah klik.
  const box = page.locator(".lyric-box").first();
  await expect(box).toBeVisible({ timeout: 12000 });
  await expect(box).toContainText("OHH 'CAUSE BABY I'M UNRAVELED");
  // baris pertama tampil 5 dtk lalu auto-tutup
  await expect(box).toBeHidden({ timeout: 8000 });
});

test("ESC menutup semua kotak", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Lirik saja, tanpa audio" }).click();
  await expect(page.locator(".lyric-box").first()).toBeVisible({ timeout: 12000 });
  await page.keyboard.press("Escape");
  await expect(page.locator(".lyric-box")).toHaveCount(0);
});

test("klik baris setlist melompat ke detiknya", async ({ page }) => {
  await page.goto("/");
  await page.locator("#setlist li").nth(7).click();
  await expect(page.locator("#player-status")).toContainText("3:55");
});

test("tombol salin perintah menyalin perintah jalankan", async ({ page }) => {
  await page.goto("/");
  await page.context().grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.getByRole("button", { name: "Salin perintah jalankan" }).click();
  const clip = await page.evaluate(() => navigator.clipboard.readText());
  expect(clip).toContain("git clone https://github.com/dezzorigin/lyric-popup-kelas-it.git");
  expect(clip).toContain("python main.py");
  await expect(page.getByRole("button", { name: "Salin perintah jalankan" })).toContainText("Tersalin");
});

test("mobile 390px: tanpa scroll horizontal", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow).toBe(0);
});
