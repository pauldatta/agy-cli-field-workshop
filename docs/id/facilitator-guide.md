# Panduan Fasilitator

> Panduan internal untuk fasilitator lokakarya. Jangan bagikan kepada peserta.

---

## Gambaran Umum

Ini adalah **workshop praktik langsung dengan 5 modul, ~7 jam** untuk Antigravity CLI. Ini dirancang untuk audiens pengembang: insinyur, pemimpin teknis, dan arsitek solusi yang sedang mengevaluasi atau mengadopsi Antigravity CLI.

!!! warning "Penghentian Gemini CLI: 18 Juni 2026"
    Gemini CLI mencapai akhir masa pakai pada **18 Juni 2026**. Ketika peserta bertanya tentang migrasi, arahkan mereka ke `agy plugin import gemini` — ini adalah jalur migrasi utama. Semua plugin Gemini CLI terbawa dalam satu perintah.

---

## Format Penyampaian

| Format | Modul | Durasi |
| :-- | :-- | :-- |
| ⚡ Kilat | Modul 1 + Sorotan Modul 2 | 1,5 jam |
| 📋 Setengah hari | Modul 1 + 2 | 2,5 jam |
| 📦 Sehari penuh | Modul 1–4 | ~5,5 jam |
| 🏗️ Diperpanjang | Semua 5 modul + lab terbuka | 7 jam |

---

## Daftar Periksa Pra-Lokakarya

- [ ] Peserta telah menginstal dan mengautentikasi Antigravity CLI *(lihat [setup.md](setup.md))*
- [ ] Detail autentikasi telah didistribusikan (khusus sesi — konfirmasikan dengan tim agy-cli)
- [ ] Peserta memiliki git dan basis kode demo yang sesuai
- [ ] Fasilitator telah menjalankan semua latihan dari awal hingga akhir pada versi agy-cli saat ini
- [ ] Berbagi layar / proyeksi telah diuji
- [ ] Untuk Modul 2: konfirmasikan bahwa peserta dapat menjalankan `dotnet` atau `mvn` (atau menggunakan kontainer yang disediakan)
- [ ] Untuk Modul 3: konfirmasikan bahwa `pip install google-antigravity` dan `gcloud auth application-default login` berfungsi
- [ ] Untuk Modul 5: konfirmasikan bahwa `uv` dan `agents-cli` telah diinstal (`uvx google-agents-cli setup`)

!!! warning "Autentikasi adalah titik kegagalan #1"
    Selalu jalankan pemeriksaan autentikasi pra-lokakarya 30 menit sebelum sesi:
    ```bash
    agy --print "Say READY" --print-timeout 30s
    ```
    Jika peserta tidak bisa mendapatkan respons, berhenti dan lakukan debug sebelum memulai.

---

## Catatan Penyampaian per Modul

### Modul 1 — Produktivitas SDLC (75 mnt)

**Pesan utama:** agy menggantikan beban mental dalam menavigasi basis kode yang tidak dikenal. Ini bukan pelengkapan otomatis — ini adalah insinyur senior yang dapat Anda tanyai apa saja.

- **Demo terlebih dahulu, latihan kemudian.** Lakukan demo langsung bagian 1.1 (pemahaman kode) pada basis kode Anda sendiri sebelum meminta peserta untuk mencoba basis kode mereka.
- **Gesekan umum:** peserta mencoba menulis prompt yang sempurna. Dorong penggunaan bahasa alami. "Beri tahu saya cara kerja autentikasi" lebih baik daripada "Tolong jelaskan arsitektur autentikasi dari basis kode ini."
- **Momen AGENTS.md:** bagian 1.5 adalah demo bernilai tinggi. Buat AGENTS.md secara langsung di layar dan tunjukkan bagaimana sesi berikutnya segera menjadi lebih pintar.
- **Demo impor plugin (bagian 1.7):** jalankan `agy plugin import gemini` secara langsung — output visualnya sangat menarik. Catatan: **tema kustom diabaikan secara diam-diam** selama impor dan tidak dapat dimigrasikan. Jika peserta bertanya mengapa tema mereka tidak terbawa, ini adalah perilaku yang diharapkan — tidak ada kesalahan, komponen tersebut hanya dilewati.

### Modul 2 — Modernisasi Basis Kode Legacy (90 mnt)

**Pesan utama:** mode ketat + orientasi mandiri mengubah migrasi selama seminggu menjadi sore yang terstruktur. Agen menulis konteksnya sendiri, lalu mengeksekusinya.

**Skrip demo langsung (disarankan):**

1. Kloning repo target .NET atau Java (dilakukan sebelumnya untuk menghemat waktu)
2. Masuk ke mode ketat: `/permissions strict`
3. Jalankan prompt investigasi — tunjukkan kepada peserta agen yang sedang membaca seluruh basis kode
4. Biarkan agen menghasilkan AGENTS.md — baca dengan lantang untuk menunjukkan bahwa agen tersebut menangkap konteks yang sebenarnya
5. `ctrl+g` — buka rencana yang dihasilkan di editor, buat satu editan yang terlihat untuk menunjukkan kendali manusia
6. Beralih ke `request-review`, eksekusi Fase 1 saja
7. Tunjukkan `/rewind` — kembalikan fase jika ada yang salah
8. Total demo: ~15 mnt, kemudian peserta melakukannya sendiri

- **Pertanyaan umum:** "Bisakah ini melakukan seluruh migrasi?" — Ya, tetapi nilainya ada pada peninjauan dan pengarahan, bukan sekadar melihatnya berjalan. Dorong mereka untuk mengedit rencana tersebut.
- **Catatan waktu Fasilitator:** Fase 0–1 bersama-sama memakan waktu ~20 mnt per peserta. Biarkan mereka mengerjakan Fase 2 sementara Anda berkeliling.

### Modul 3 — Membangun Agen AGY dengan SDK (90 mnt)

**Pesan utama:** CLI adalah untuk individu. Agen SDK adalah layanan spesialis yang dapat dipanggil oleh seluruh tim Anda.

- **Gerbang pengaturan:** pastikan semua orang telah menginstal `google-antigravity` dan autentikasi Vertex AI atau AI Studio berfungsi sebelum memulai. Ini adalah penghalang yang paling umum.
- **Momen `adk web .`:** setelah peserta menjalankan agen pertama mereka di UI browser, energinya berubah — mereka melihatnya merespons alat mereka.
- **Tabel pemilihan model:** tekankan Flash-lite untuk pembuatan, Pro untuk orkestrasi. Kesadaran akan biaya adalah sebuah fitur, bukan kompromi.
- **Latihan 11 (pipeline):** pola multi-agen `asyncio.gather` + `START_SUBAGENT` adalah wawasan arsitektur utama. Luangkan waktu 5 menit untuk menjelaskan bagaimana sub-agen menyusun sebelum mereka memulai.

### Modul 5 — Agen ADK dengan agents-cli (75 mnt)

**Pesan utama:** agents-cli mengubah agen pengkodean Anda menjadi pakar ADK. Siklus hidup 7 fase (scaffold → build → eval → deploy) adalah tempat agen beralih dari demo ke produksi.

- **Gerbang pengaturan:** pastikan `uv` dan `agents-cli` telah terinstal. Jalankan `agents-cli info` untuk memverifikasi.
- **Loop evaluasi adalah momen pembelajaran.** Luangkan waktu pada Fase 4 (evaluasi) — inilah yang membedakan mainan dari agen produksi. Biarkan peserta melihat skor gagal, lalu lakukan iterasi.
- **google-adk ≠ google-antigravity:** Modul 3 menggunakan `google-antigravity` (Antigravity SDK). Modul 5 menggunakan `google-adk` (ADK). Keduanya adalah paket yang berbeda. `agents-cli scaffold` mengelola dependensi yang tepat secara otomatis.
- **Kecepatan Latihan 12:** Bagian 1–2 berlangsung cepat (scaffold + build). Bagian 3–4 (loop eval + perbaikan) adalah tempat waktu dihabiskan. Tekankan bahwa 5–10 iterasi adalah hal yang normal.

### Modul 4 — Multi-Agen & Lanjutan (60 mnt)

**Pesan utama:** sub-agen + `/btw` adalah lompatan kualitatif. Di sinilah agy menjadi orkestrator, bukan sekadar chatbot.

- **Demo sub-agen adalah momen yang memukau.** Munculkan dua agen secara langsung, tunjukkan keduanya berjalan secara bersamaan.
- **Demo /btw:** mulai tugas yang agak panjang (memfaktorkan ulang file), lalu gunakan `/btw` di tengah tugas. Tunjukkan kepada peserta bahwa kursor terus bergerak sementara catatan yang disuntikkan digabungkan.
- **Penjadwalan:** jelaskan polanya secara konseptual, jangan didemokan secara langsung (latensi membuatnya canggung dalam lokakarya).

---

## Pertanyaan Umum Peserta

| Pertanyaan | Jawaban |
| :-- | :-- |
| "Model apa yang digunakan agy?" | Gunakan `/model` untuk melihat dan beralih. Lihat [Dokumentasi model](https://www.antigravity.google/docs/models). |
| "Apa bedanya ini dengan Gemini CLI?" | agy menjembatani plugin dari Gemini CLI dan Claude, memiliki orkestrasi sub-agen bawaan, dan pengarahan di tengah tugas `/btw`. Gemini CLI mencapai EOL pada 18 Juni 2026. |
| "Bisakah saya menggunakan kunci API saya sendiri?" | agy menggunakan Google Sign-In berbasis peramban. Pengguna enterprise menghubungkan proyek GCP. Lihat [Dokumentasi enterprise](https://www.antigravity.google/docs/enterprise). |
| "Apakah kode dikirim ke Google?" | Lihat [FAQ](https://www.antigravity.google/docs/faq) untuk detail penanganan data. |
| "Bagaimana dengan hook?" | agy-cli mendukung hook melalui `hooks.json`. Lihat [Dokumentasi hook](https://www.antigravity.google/docs/hooks). |
| "Di mana log percakapan disimpan?" | `~/.gemini/antigravity-cli/conversations/` |
| "Tema Gemini CLI saya tidak terimpor." | Sudah diduga — tema kustom diabaikan secara diam-diam selama `agy plugin import gemini`. Skill, server MCP, dan agen tetap terbawa. |
| "Bisakah saya men-deploy agen SDK ke Cloud Run?" | Ya — `adk deploy cloud_run`. Lihat Modul 3 bagian 3.6. |

---

## Pemecahan Masalah Selama Lokakarya

| Gejala | Solusi |
| :-- | :-- |
| `agy: command not found` | Periksa PATH. Jalankan `which agy` atau `which agy-cli`. |
| Kesalahan Autentikasi / 401 | Kredensial sesi mungkin telah kedaluwarsa. Distribusikan ulang autentikasi. |
| Kesalahan `agy plugin list` | Periksa apakah `~/.gemini/antigravity-cli/` ada |
| Respons lambat | Periksa jaringan. Proses pertama setelah diam mungkin lebih lambat karena pengindeksan ruang kerja. |
| Sub-agen tidak muncul | Pastikan peserta berada dalam mode interaktif (bukan `--print`) |
| Kesalahan impor `google-adk` (M3) | Pastikan venv diaktifkan: `source .venv/bin/activate` |
| Vertex AI 403 (M3) | Jalankan `gcloud auth application-default login` dan pastikan `GOOGLE_CLOUD_PROJECT` telah diatur |

---

## Pasca-Lokakarya

1. Kumpulkan umpan balik menggunakan formulir umpan balik lokakarya standar
2. Catat setiap bug agy-cli atau perilaku tak terduga yang diamati — laporkan ke tim agy-cli
3. Setiap latihan yang memerlukan solusi alternatif harus ditandai untuk pembaruan dokumen di `CONTRIBUTING.md`
