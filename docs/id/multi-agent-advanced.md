# Modul 4: Multi-Agen & Lanjutan <span class="duration-badge">45 min</span>

> **Di mana agy melampaui sekadar asisten obrolan.** Modul ini mencakup fitur-fitur yang membedakan agy-cli dari setiap alat pengkodean AI lainnya: sub-agen paralel, pengarahan di tengah tugas dengan `/btw`, penjadwalan latar belakang, dan kelanjutan sesi.

---

## 4.0 — Model Agen agy <span class="duration-badge">5 menit</span>

agy-cli dapat memunculkan **sub-agen** — pelaksana tugas terisolasi yang beroperasi secara paralel, masing-masing dengan konteks ruang kerja mereka sendiri. Tidak seperti menjalankan beberapa tab terminal dengan sesi agy yang terpisah, sub-agen dikoordinasikan: mereka dapat berbagi ruang kerja, bekerja pada cabang yang terisolasi, atau beroperasi pada salinan hasil kloning.

Tiga mode ruang kerja:

| Mode | Arti | Kapan digunakan |
| :-- | :-- | :-- |
| `inherit` | Sub-agen berbagi ruang kerja yang sama | Tugas tambahan — tidak ada konflik yang diharapkan |
| `branch` | Sub-agen mendapatkan klon yang terisolasi | Perubahan paralel pada file yang sama |
| `share` | worktree git — cabang terisolasi, repo bersama | Pengembangan paralel yang sesungguhnya |

### Beralih Model

Gunakan `/model` untuk beralih model aktif di tengah sesi — berguna ketika Anda menginginkan penalaran yang lebih berat untuk tugas tertentu:

```bash
/model
```

Ini akan membuka pemilih model yang menunjukkan opsi yang tersedia (Gemini 3.5 Flash, Gemini 3.1 Pro, Claude Sonnet 4.6, dll.).

> 📖 Daftar model lengkap: [Dokumentasi model](https://www.antigravity.google/docs/models)

---

## 4.1 — Memunculkan Sub-agen <span class="duration-badge">15 min</span>

> **Pola: Eksekusi Paralel** — mengirimkan beberapa agen untuk bekerja secara bersamaan.
> 📖 Referensi lengkap: [Dokumentasi sub-agen](https://www.antigravity.google/docs/subagents)

### Dari Sesi Interaktif

```text
> Spawn a subagent to write unit tests for the auth module while I work on the API refactor.
```

agy akan memunculkan sub-agen, melaporkan ID-nya, dan melanjutkan sesi utama Anda. Sub-agen bekerja secara independen.

```text
> What's the status of the test-writing subagent?
```

```text
> Show me what the test subagent produced.
```

### Mengelola Sub-agen dengan /agents

Gunakan panel `/agents` untuk melihat semua sub-agen yang aktif, statusnya, dan outputnya:

```bash
/agents
```

Pintasan utama dari percakapan utama:

| Pintasan | Aksi |
| :-- | :-- |
| `Ctrl+J` | Teleportasi ke sub-agen yang menunggu persetujuan — lompat langsung untuk meninjau permintaannya |
| `Ctrl+K` | Persetujuan cepat dari percakapan utama — menyetujui tindakan sub-agen yang tertunda tanpa berpindah |

Siklus hidup sub-agen: **Berjalan → Menganggur → Dimatikan**

### Batasan dan Tipe Bawaan

- **Kedalaman maksimum:** 10 (sub-agen dapat memunculkan sub-agen mereka sendiri, hingga 10 tingkat)
- **Tipe bawaan:** `research` (riset web), `browser` (otomatisasi peramban), `self` (tujuan umum)

### Pola Audit Paralel

```text
> Spawn three subagents in parallel:
> 1. Security audit — scan for hardcoded credentials, injection risks, and insecure dependencies
> 2. Performance audit — find N+1 queries, unindexed lookups, and memory leaks
> 3. Coverage audit — identify untested functions and missing integration tests
>
> Use branch workspace mode for each. Report back when all three complete.
```

Saksikan tiga analisis independen berjalan secara bersamaan. Saat mereka selesai, agy menyintesis hasilnya.

!!! tip "Momen Wow"
    Tiga agen khusus berjalan secara paralel pada basis kode Anda, masing-masing dengan konteks penuh, masing-masing menghasilkan temuan independen. Ini adalah pola yang membuat agy secara kualitatif berbeda dari asisten berbasis obrolan.

### Pola Tinjauan Adversarial

```text
> Spawn a subagent to act as an adversarial reviewer for the changes in this branch.
> Its only job: find reasons why this code should NOT be merged.
> It should challenge every assumption and look for edge cases the implementer missed.
```

Pola peninjau adversarial sangat kuat untuk perubahan yang sensitif terhadap keamanan, modifikasi infrastruktur, atau PR apa pun di mana "terlihat bagus bagi saya" saja tidak cukup.

---

## 4.2 — /btw: Pengarahan di Tengah Tugas <span class="duration-badge">10 min</span>

> **Pola: Mengarahkan Tanpa Menginterupsi** — menyuntikkan konteks ke dalam tugas yang sedang berjalan tanpa menghentikannya.

`/btw` adalah salah satu fitur agy yang paling khas. Saat agy berada di tengah tugas, Anda dapat mengiriminya pesan tanpa membatalkan operasi saat ini.

### Cara Kerjanya

```text
> Refactor the entire authentication module to use JWT instead of sessions. This will touch multiple files. Start with the backend.
```

*agy mulai bekerja... saat sedang berjalan:*

```bash
/btw Actually, keep backward compatibility with sessions for 30 days — implement a dual-mode auth.
```

agy menggabungkan catatan Anda ke dalam tugas yang sedang berlangsung tanpa berhenti. Ini seperti meninggalkan catatan tempel untuk seorang pengembang di tengah-tengah sprint — mereka melihatnya dan menyesuaikan.

### Kasus Penggunaan untuk /btw

```bash
/btw The API rate limit is 100 req/min, factor that into any retry logic you add.
```

```bash
/btw The team uses conventional commits — make sure any commit messages follow that format.
```

```bash
/btw Skip the frontend changes for now, just focus on the backend API.
```

!!! info "Kontras dengan menginterupsi"
    Tanpa `/btw`, mengarahkan tugas yang berjalan lama berarti membatalkannya, menyesuaikan prompt Anda, dan memulai ulang — kehilangan semua kemajuan. `/btw` memungkinkan Anda mengoreksi arah tanpa biaya tersebut.

---

## 4.3 — Eksekusi Latar Belakang & Penjadwalan <span class="duration-badge">10 min</span>

> **Pola: Async Agy** — memulai tugas yang berjalan lama dan dapatkan pemberitahuan saat tugas tersebut selesai.

### Tugas Latar Belakang

agy mendukung eksekusi asinkronus — Anda dapat memulai suatu tugas dan terus bekerja. agy memberi tahu Anda saat tugas tersebut selesai.

```text
> In the background, do a comprehensive security audit of this entire codebase. Take as long as you need. Notify me when done.
```

agy menjalankan audit tanpa memblokir terminal Anda. Saat selesai, Anda menerima pemberitahuan beserta hasilnya.

### Tugas Terjadwal

agy mendukung penjadwalan bergaya cron untuk analisis berulang:

```text
> Schedule a nightly code quality report every day at 2am. It should check for new TODOs, failing tests, and dependency updates. Save the report to reports/nightly-YYYY-MM-DD.md.
```

Ekspresi cron (hingga 5 bidang) didukung:

```bash
# Run at 2am daily
0 2 * * *

# Run every Monday at 9am
0 9 * * 1

# Run every 15 minutes
*/15 * * * *
```

!!! warning "Penjadwalan bersifat persisten dalam sesi"
    Tugas terjadwal tetap ada di seluruh sesi selama agy berjalan. Periksa `/tasks` untuk melihat dan mengelola tugas terjadwal.

---

## 4.4 — Melanjutkan Sesi <span class="duration-badge">5 menit</span>

> **Pola: Pekerjaan Berjalan Lama** — lanjutkan tepat di tempat Anda berhenti.
> 📖 Referensi lengkap: [Menggunakan Antigravity CLI](https://www.antigravity.google/docs/cli-using)

### Melanjutkan Sesi Terbaru

Dari dalam agy, gunakan perintah garis miring `/resume`:

```bash
/resume
```

Ini akan membuka pemilih sesi yang menampilkan percakapan terbaru Anda. Pilih salah satu untuk dilanjutkan.

### Menjelajahi dan Beralih Sesi

```bash
/switch
```

Sama seperti `/resume` — kedua perintah membuka pemilih sesi.

### Lanjutkan Otomatis saat Keluar

Saat Anda keluar dari sesi agy, agy mencetak perintah yang tepat untuk melanjutkannya:

```bash
Session saved. Resume with: agy --conversation <conversation-id>
```

Anda dapat menggunakan perintah ini langsung dari terminal untuk kembali masuk.

### Kasus Penggunaan: Pekerjaan Fitur Multi-Hari

```bash
# Day 1: Start a feature
agy -i "I'm building a payment integration feature. Let's start with the backend API design."

# Day 2: Resume from terminal
agy --conversation <conversation-id>

# Or from inside agy:
# /resume
```

```text
> What was the last thing we decided about the payment API schema?
```

agy akan memiliki konteks lengkap, termasuk kode yang ditulis, keputusan yang dibuat, dan pertanyaan yang terbuka.

---

## 4.5 — Lanjutan: Menggabungkan Pola <span class="duration-badge">Opsional</span>

> **Kekuatan penuh stack:** sub-agen + /btw + latar belakang + penjadwalan + kelanjutan percakapan.

### Respons Insiden enterprise

```text
> I'm starting an incident response for a production issue. Spawn:
> 1. A log-analyzer subagent (branch mode) — read the last 1000 lines of app.log and identify the root cause
> 2. A config-checker subagent (branch mode) — review all environment configs and recent deploys for anomalies
>
> Report back when both complete. I'll be monitoring in the meantime.
```

Saat mereka berjalan:

```bash
/btw The incident started at 14:32 UTC. Focus analysis on that window.
```

Ini adalah triase insiden multi-agen — dua investigasi paralel, yang dapat diarahkan di tengah jalan.

---

## Latihan Modul 4

<div class="exercise-card" markdown>

### :material-file-document: Latihan 4: Sub-agen

**Berkas:** [`ex04_subagents.md`](exercises/ex04_subagents.md)
**Durasi:** 20 menit
**Tujuan:** Memunculkan tim audit paralel. Mempraktikkan pola peninjau adversarial.

</div>

<div class="exercise-card" markdown>

### :material-file-document: Latihan 5: /btw & Penjadwalan

**Berkas:** [`ex05_btw_scheduling.md`](exercises/ex05_btw_scheduling.md)
**Durasi:** 20 menit
**Tujuan:** Menggunakan /btw untuk mengarahkan tugas yang berjalan lama. Menjadwalkan laporan kualitas kode berulang.

</div>

<div class="exercise-card" markdown>

### :material-file-document: Latihan 6: Tata Kelola Sandbox

**Berkas:** [`ex06_sandbox_governance.md`](exercises/ex06_sandbox_governance.md)  
**Durasi:** 15 menit  
**Tujuan:** Mengonfigurasi mode sandbox di settings.json dan mengujinya dengan model izin.

</div>

---

## Anda Telah Selesai

→ **[Lembar Contekan](cheatsheet.md)** — setiap perintah dari keempat modul di satu tempat

→ **[Referensi: Pola DevOps](devops-automation.md)** — pipeline `--print`, CI/CD, pembahasan mendalam sandbox

→ **[Referensi: Ekosistem Plugin](plugin-ecosystem.md)** — referensi lengkap siklus hidup plugin
