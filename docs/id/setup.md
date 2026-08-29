# Pengaturan Lingkungan

> Selesaikan ini sebelum memulai modul apa pun. Membutuhkan waktu sekitar 15 menit.

---

## Persyaratan Sistem

| Komponen | Minimum | Catatan |
| :-- | :-- | :-- |
| **agy** | Terbaru | Instruksi instalasi di bawah ini |
| **Git** | v2.30+ | Untuk repositori latihan |
| **Terminal** | Apa saja | iTerm2, Terminal macOS, atau terintegrasi dengan VS Code |
| **jq** | Opsional | Berguna untuk mengurai keluaran JSON `--print` |

---

## Langkah 1: Instal agy

> 📖 Instruksi lengkap: [Dokumentasi Memulai](https://www.antigravity.google/docs/cli-getting-started)

### macOS / Linux

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

### Windows

```powershell
# PowerShell
irm https://antigravity.google/cli/install.ps1 | iex

# Or via WSL (recommended)
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

Setelah instalasi, verifikasi bahwa berkas biner tersedia:

```bash
# Verify the binary is in your PATH
which agy

# Confirm the version
agy --version
```

---

## Langkah 2: Autentikasi

agy menggunakan **Google Sign-In berbasis browser**. Pada saat pertama kali dijalankan, ini akan:

- **Mesin lokal:** Secara otomatis membuka browser default Anda untuk masuk.
- **Sesi SSH / jarak jauh:** Mencetak URL untuk ditempelkan ke browser apa pun, lalu tempelkan kembali kode autentikasi ke dalam terminal.

```bash
# Start agy — auth will trigger automatically on first run
agy
```

Untuk keluar:

```text
# Run this inside an agy interactive session (not in your terminal):
/logout
```

> 📖 Untuk autentikasi enterprise melalui proyek GCP, lihat [Dokumentasi enterprise](https://www.antigravity.google/docs/enterprise).

Setelah autentikasi dikonfigurasi, jalankan pengujian cepat:

```bash
agy --print "Say 'Workshop ready!' in exactly two words." --print-timeout 30s
```

Output yang diharapkan: `Workshop ready!`

---

## Langkah 3: Inisialisasi Ruang Kerja Proyek Anda

agy secara otomatis menemukan konfigurasi proyek dengan menelusuri ke atas dari direktori Anda saat ini, mencari folder `.agents/`. Buat satu untuk lokakarya ini:

```bash
# Clone the workshop exercises repo
git clone https://github.com/pauldatta/agy-cli-field-workshop.git
cd agy-cli-field-workshop

# agy will create .agents/ on first run
agy --print "List the files in the current directory."
```

Anda akan melihat folder `.agents/` dibuat dengan file konfigurasi proyek (settings.json, mcp.json, dll.).

!!! info "Kompatibilitas .gemini/"
    agy juga membaca direktori `.gemini/` — berguna jika Anda sudah memiliki pengaturan proyek Gemini CLI. Kedua lokasi konfigurasi tersebut dihormati.

---

## Langkah 4: Verifikasi Semuanya

```bash
# Check agy is accessible
agy --help

# List installed plugins (output is JSON)
agy plugin list

# Pretty-print the plugin list (works once plugins are installed in Module 2)
# agy plugin list | python3 -m json.tool

# Quick print-mode smoke test
agy --print "What is 2 + 2?" --print-timeout 30s
```

Daftar periksa sebelum lokakarya dimulai:

- [ ] `agy --help` menampilkan flag dan subperintah
- [ ] `agy plugin list` berhasil dijalankan
- [ ] `agy --print "..."` mengembalikan respons

---

## Pemecahan Masalah

| Masalah | Solusi |
| :-- | :-- |
| `agy: command not found` | Periksa apakah berkas biner ada di PATH Anda. Jalankan `echo $PATH` dan pastikan direktori instalasi disertakan. Jalankan ulang skrip instalasi jika diperlukan |
| Kesalahan autentikasi / browser tidak terbuka | Untuk sesi SSH, salin URL yang dicetak secara manual. Untuk lokal, periksa pengaturan browser bawaan. Jalankan `/logout` dan coba lagi |
| `agy plugin list` mengembalikan `No imported plugins.` | Diharapkan pada instalasi baru (bukan JSON). Anda akan mengisi plugin pada Modul 2 |
| Respons pertama lambat | Proses pertama mungkin lebih lambat karena agy mengindeks ruang kerja Anda |
| Konfigurasi tidak dimuat | Periksa `~/.gemini/antigravity-cli/settings.json` (pengaturan pengguna) dan `.agents/` (pengaturan proyek) |

---

## Langkah Selanjutnya

→ Mulai dengan **[Modul 1: Produktivitas SDLC](sdlc-productivity.md)**
