# Modul 1: Produktivitas SDLC <span class="duration-badge">75 menit</span>

> **Sesi Antigravity CLI nyata pertama Anda.** Modul ini mencakup alur kerja utama sehari-hari — memahami kode, melakukan refactoring, membuat pengujian, dan meninjau perubahan — ditambah cara memperluas CLI dengan plugin untuk toolchain tim Anda.

---

## 1.0 — Sesi Interaktif Pertama <span class="duration-badge">5 menit</span>

Luncurkan Antigravity CLI di direktori proyek lokakarya Anda:

```bash
cd agy-cli-field-workshop
agy
```

Anda akan masuk ke prompt interaktif. Coba:

```text
> What files are in this project and what does each one do?
```

Perhatikan bagaimana agy membaca ruang kerja Anda — ia mengindeks repositori git, membaca isi file, dan merespons dengan konteks. Ini **otomatis**: tidak ada konfigurasi, tidak ada prompt yang harus ditulis terlebih dahulu.

!!! tip "Folder .agents/"
    Setelah sesi pertama Anda, periksa `.agents/` — agy membuat file konfigurasi proyek yang melacak ruang kerja Anda. Ini adalah cara ia mengetahui apa yang harus diindeks pada proses selanjutnya.

---

## 1.1 — Pemahaman Kode <span class="duration-badge">10 menit</span>

> **Pola: Jelaskan Sebelum Anda Menyentuh** — pahami kode sebelum mengubahnya.

### Latihan: Memetakan Basis Kode yang Belum Dikenal

```bash
# -i seeds the session with an initial prompt and stays interactive
agy -i "Give me a high-level architecture overview of this project. What are the main components and how do they connect?"
```

Kemudian tindak lanjuti secara interaktif:

```text
> Which file handles the entry point?
> What external dependencies does this project have?
> Are there any obvious code smells or tech debt?
```

!!! tip "Gunakan -i untuk sesi dengan seed"
    `agy -i "<task>"` (singkatan dari `--prompt-interactive`) dimulai dengan sebuah prompt tetapi tetap interaktif. Sangat bagus untuk eksplorasi yang terarah — Anda menentukan arahnya, lalu mengarahkannya dengan tindak lanjut.

---

## 1.2 — Refactoring <span class="duration-badge">10 min</span>

> **Pola: Usulkan, Tinjau, Terapkan** — jangan pernah menerapkan perubahan yang belum Anda baca.

### Latihan: Refactoring Bertarget

```bash
agy
```

```text
> I want to refactor the error handling in this project. First, show me all the places where errors are currently caught or returned — don't change anything yet.
```

Tinjau temuan tersebut. Kemudian:

```text
> Now propose a refactored version of [specific function] using a consistent error handling pattern. Show me the diff before applying.
```

Terapkan hanya setelah Anda membaca perubahan yang diusulkan.

### Model Izin

agy memiliki **model izin 3 tingkat** yang mengontrol bagaimana ia menangani persetujuan alat:

| Tingkat | Perilaku |
| :-- | :-- |
| `request-review` | **Bawaan.** agy meminta persetujuan sebelum menulis file atau menjalankan perintah |
| `always-proceed` | Menyetujui otomatis semua panggilan alat — berguna untuk skrip tepercaya dan CI |
| `strict` | Menolak semua penggunaan alat kecuali diizinkan secara eksplisit — kontrol maksimum |

Gunakan perintah garis miring `/permissions` untuk melihat atau mengubah tingkat saat ini. Anda juga dapat menetapkan aturan terperinci di `settings.json`:

```json
{
  "permissions": {
    "allow": ["command(git)", "read_file"],
    "deny": ["command(rm -rf)"]
  }
}
```

> 📖 Detail lengkap: [Dokumentasi Izin](https://www.antigravity.google/docs/permissions) · [Dokumentasi Mode Ketat](https://www.antigravity.google/docs/strict-mode)

---

## 1.3 — Pembuatan Pengujian <span class="duration-badge">10 min</span>

> **Pola: Uji Apa yang Ada** — buat pengujian untuk kode nyata, bukan hipotetis.

### Latihan: Buat Pengujian Unit

```bash
agy
```

```text
> Look at [specific function or file]. Generate a comprehensive unit test suite for it. Include happy path, edge cases, and error conditions. Use the testing framework already in this project.
```

Kemudian:

```text
> Run the tests and fix any that fail.
```

!!! tip "Biarkan agy menjalankan pengujian"
    agy dapat mengeksekusi perintah shell. Ini akan menjalankan rangkaian pengujian Anda dan melakukan iterasi pada kegagalan tanpa Anda harus menyalin-tempel pesan kesalahan. Perhatikan ia mengoreksi diri.

---

## 1.4 — Tinjauan Kode <span class="duration-badge">10 min</span>

> **Pola: Tinjauan Pra-Komit** — gunakan agy sebagai peninjau senior sebelum setiap push.

### Latihan: Tinjau Perubahan Anda

```bash
# Stage some changes (or use an existing branch)
git add -p

# Start agy and review what's staged
agy
```

```text
> Review my staged changes for: (1) correctness, (2) security issues, (3) missing test coverage, (4) anything that would block a PR. Be direct — don't soften findings.
```

### Varian Headless (untuk pembuatan skrip)

```bash
# Review changes non-interactively — useful in pre-commit hooks or CI
git diff --cached | agy --print "Review these changes. Flag any bugs, security issues, or missing tests. Output as markdown."
```

---

## 1.5 — Konteks Proyek dengan AGENTS.md <span class="duration-badge">5 menit</span>

> **Pola: Konteks Persisten** — beri tahu agy sekali, ia akan mengingatnya di setiap sesi.

agy membaca file konteks saat sesi dimulai. Buat satu di root proyek:

```bash
cat > AGENTS.md << 'EOF'
# Project Context

This is a Node.js REST API built with Express and TypeScript.

## Key Conventions
- Language: TypeScript (strict mode, no `any`)
- Testing: Jest with 80% coverage minimum; run `npm test` to validate
- Style: ESLint + Prettier; run `npm run lint` before committing
- DO NOT modify `src/db/migrations/` — those are append-only
- DO NOT use `console.log` in production code; use the `logger` utility

## Architecture
Three-layer: `routes/` → `services/` → `repositories/`. All DB access goes through the repository layer. External HTTP calls go through `src/clients/`.

## Common Commands
- `npm run dev` — start local dev server on :3000
- `npm test` — run full test suite
- `npm run db:migrate` — apply pending DB migrations
EOF
```

Sekarang mulai sesi baru:

```bash
agy --print "What do you know about this project?"
```

agy akan memasukkan AGENTS.md Anda ke dalam setiap sesi berikutnya secara otomatis.

!!! info "Hierarki konteks"
    agy membaca AGENTS.md dari: direktori saat ini → direktori induk → direktori beranda. Konteks yang lebih spesifik menimpa konteks yang lebih luas.

### Sumber Konteks Tambahan

Selain AGENTS.md, agy juga memuat:

- **`.agents/rules.md`** (atau `.agents/rules/*.md`) — aturan tingkat proyek yang disuntikkan sebagai arahan prompt sistem. Gunakan ini untuk persyaratan mutlak seperti "jangan pernah menghapus file migrasi" atau "selalu gunakan mode ketat TypeScript."
- **`.gemini/`** — untuk kompatibilitas Gemini CLI, agy membaca direktori `.gemini/` bersama dengan `.agents/`.
- **`~/.gemini/config/rules.md`** — aturan global yang diterapkan ke semua sesi.

> 📖 Detail lengkap: [Dokumentasi Aturan & Alur Kerja](https://www.antigravity.google/docs/rules-workflows)

### Contoh Definisi Agen (di `samples/agents/`)

| Agen | Model | Tujuan |
| :-- | :-- | :-- |
| `doc-writer.md` | `gemini-3.5-flash` | Menghasilkan dokumentasi API, bagian README, dan komentar sebaris dari sumber |
| `pr-reviewer.md` | `gemini-3.5-flash` | Meninjau perubahan kode untuk kualitas, bug, dan pelanggaran gaya |
| `migration-validator.md` | `gemini-3.5-flash` | Memvalidasi kelengkapan migrasi Gemini CLI → Antigravity CLI |

---

## 1.6 — Navigasi Interaktif <span class="duration-badge">5 min</span>

> **Pola: Kelancaran Terminal** — ketahui pintasan yang membuat sesi agy menjadi cepat.
> 📖 Referensi lengkap: [Menggunakan Antigravity CLI](https://www.antigravity.google/docs/cli-using)

### Perintah Slash Utama

| Perintah | Fungsinya |
| :-- | :-- |
| `/rewind` (atau `/undo`) | Mengembalikan riwayat percakapan ke checkpoint sebelumnya |
| `/resume` (atau `/switch`) | Membuka pemilih percakapan untuk melanjutkan atau beralih sesi |
| `/rename <name>` | Mengganti nama utas percakapan aktif |
| `/config` (atau `/settings`) | Membuka overlay pengaturan layar penuh |
| `/permissions` | Mengatur tingkat otonomi agen (`request-review`, `always-proceed`, `strict`) |
| `/model` | Memilih model penalaran (bertahan di seluruh sesi) |
| `/tasks` | Memantau, melihat log untuk, atau menghentikan tugas latar belakang |
| `/agents` | Melihat, mengelola, dan menyetujui tindakan sub-agen |
| `/open <path>` | Membuka file di editor eksternal pilihan Anda |
| `/usage` | Membuka manual bantuan interaktif sebaris |
| `/skills` | Menelusuri skill agen lokal dan global |
| `/mcp` | Mengonfigurasi dan mengelola server MCP |

> 📖 Referensi lengkap perintah slash: [Fitur CLI](https://antigravity.google/docs/cli-features)

### Tips Cepat

| Pintasan | Fungsinya |
| :-- | :-- |
| `@` | Pelengkapan otomatis jalur file — ketik `@` untuk memicu saran jalur |
| `!` | Menjalankan perintah terminal secara langsung tanpa meninggalkan agy |
| `esc esc` | Menghapus input prompt saat ini (ketika tidak ada streaming yang aktif) |
| `?` | Mendapatkan bantuan dan membuat daftar semua perintah slash |
| `alt+enter` / `ctrl+j` / `shift+enter` | Menyisipkan baris baru di prompt Anda (input multi-baris) |
| `ctrl+g` | Mengedit prompt di dalam editor shell default Anda |
| `ctrl+l` | Membersihkan layar TUI |
| `ctrl+d` | Keluar dari CLI |

> 📖 Referensi lengkap keybinding: [Menggunakan Antigravity CLI](https://antigravity.google/docs/cli-using)

---

## 1.7 — Perluas dengan Plugin <span class="duration-badge">15 menit</span> {: #17-extend-with-plugins-15-min }

> **Pola: Bawa Toolchain Anda** — plugin menambahkan skill, server MCP, agen, dan aturan ke agy. Instal sekali, tersedia di setiap sesi.

Sistem plugin Antigravity CLI melakukan sesuatu yang unik: sistem ini dapat **mengimpor plugin yang telah Anda instal di Gemini CLI** — tanpa perlu menginstal ulang atau mengonfigurasi ulang. Investasi Anda yang sudah ada akan terbawa.

### Lihat Apa yang Aktif

```bash
agy plugin list
```

Menampilkan nama setiap plugin, sumber, tanggal impor, dan komponen (skill, perintah, mcpServers, agen).

### Impor dari Gemini CLI

```bash
agy plugin import gemini
```

agy memindai instalasi Gemini CLI lokal Anda, menemukan semua plugin yang terinstal, dan menyiapkan komponennya ke dalam `~/.gemini/antigravity-cli/`. Output:

```text
  [ok]    code-review
          ✔ skills      : 3 processed
          ✔ commands    : 2 processed
          - mcpServers  : skipped (not found)
  [ok]    gemini-deep-research
          ✔ commands    : 1 processed
          ✔ mcpServers  : 1 processed
  [skip]  superpowers (already imported)
```

!!! warning "Tema kustom diabaikan secara diam-diam"
    Komponen tema kustom tidak dapat dimigrasikan 1:1 ke model agy dan dilewati tanpa kesalahan selama impor. Periksa plugin aktif Anda setelah impor jika tema penting untuk alur kerja Anda.

!!! tip "Impor ulang setelah pembaruan plugin"
    Plugin yang sudah diimpor akan dilewati secara default. Paksa impor ulang:
    ```bash
    agy plugin import gemini --force
    ```

### What Gets Imported

| Component | What it means |
| :-- | :-- |
| `skills` | SKILL.md files — injected as domain expertise into agy sessions |
| `commands` | Slash commands available inside agy sessions |
| `mcpServers` | MCP tool servers (GitHub, gcloud, Workspace, etc.) |
| `agents` | Custom subagent definitions |
| `rules` | Rules files injected as system prompt directives |
| `hooks` | Staged but not auto-executed — agy handles lifecycle differently |

### Enable / Disable Per-Project

Not every plugin is appropriate for every codebase:

```bash
# Nonaktifkan untuk proyek ini
agy plugin disable gemini-deep-research

# Aktifkan kembali
agy plugin enable gemini-deep-research
```

### Plugin Locations

| Scope | Path |
| :-- | :-- |
| **Global** | `~/.gemini/antigravity-cli/plugins/` |
| **Project** | `.agents/plugins/` |

### Building a Custom Plugin

A valid agy plugin needs a `plugin.json` manifest:

```text
my-plugin/
├── plugin.json          ← wajib
├── mcp_config.json      ← definisi server MCP (opsional)
├── hooks.json           ← penangan peristiwa hook (opsional)
├── skills/              ← berkas SKILL.md (opsional)
│   └── my-skill/
│       └── SKILL.md
├── agents/              ← definisi sub-agen (opsional)
└── rules/               ← berkas aturan (opsional)
    └── my-rules.md
```

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin agy kustom saya",
  "components": ["skills"]
}
```

Validate it before shipping:

```bash
agy plugin validate ./my-plugin
# ✔ Manifes plugin valid
```

> 📖 Referensi lengkap: [Plugin](https://www.antigravity.google/docs/plugins) · [Panduan Migrasi](https://www.antigravity.google/docs/gcli-migration)

---

## Latihan Modul 1

<div class="exercise-card" markdown>

### :material-file-document: Latihan 1: Sesi Pertama

**Berkas:** [`ex01_first_session.md`](exercises/ex01_first_session.md)  
**Durasi:** 15 menit  
**Tujuan:** Meluncurkan agy, menjelajahi basis kode, menghasilkan AGENTS.md.

</div>

<div class="exercise-card" markdown>

### :material-puzzle: Latihan 2: Jembatan Plugin

**Berkas:** [`ex02_plugin_bridge.md`](exercises/ex02_plugin_bridge.md)  
**Durasi:** 20 menit  
**Tujuan:** Mengimpor plugin dari Gemini CLI, mengaktifkan/menonaktifkan secara selektif, memvalidasi plugin kustom.

</div>

---

## Modul Selanjutnya

→ **[Modul 2: Modernisasi Basis Kode Legacy](legacy-modernization.md)** — mode ketat, orientasi mandiri agen, sub-agen, dan `/rewind` sebagai jaring pengaman Anda.
