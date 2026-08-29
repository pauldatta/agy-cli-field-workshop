# Lembar Contekan agy-cli

> Referensi cepat untuk semua yang dibahas dalam lokakarya ini.
> Semua perintah telah diverifikasi berdasarkan [antigravity.google/docs](https://antigravity.google/docs/cli-overview).

---

## Instalasi & Versi

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
agy --help         # Show all flags and subcommands
agy changelog      # Show release notes
agy update         # Self-update
agy install        # Configure PATH and shell aliases
```

---

## Mode Peluncuran

| Mode | Perintah | Kapan digunakan |
| :-- | :-- | :-- |
| **Interaktif** | `agy` | Bawaan — sesi percakapan penuh |
| **Interaktif dengan awalan** | `agy -i "<prompt>"` | Mulai dengan arahan, lanjutkan secara percakapan |
| **Cetak (headless)** | `agy -p "<prompt>"` | Satu kali eksekusi, teruskan ke stdout |
| **Lanjutkan terakhir** | `agy -c` | Lanjutkan sesi paling baru |
| **Lanjutkan berdasarkan ID** | `agy --conversation <id>` | Lanjutkan sesi masa lalu tertentu |
| **Lanjutkan dalam sesi** | `/resume` atau `/switch` | Beralih percakapan tanpa meninggalkan agy |

---

## Flag Utama

> Sumber: [`agy --help`](https://antigravity.google/docs/cli-getting-started) · [cli-using](https://antigravity.google/docs/cli-using)

| Flag | Singkatan | Deskripsi |
| :-- | :-- | :-- |
| `--print "<prompt>"` | `-p` | Prompt tunggal non-interaktif |
| `--prompt-interactive "<prompt>"` | `-i` | Sesi interaktif dengan seed |
| `--continue` | `-c` | Melanjutkan percakapan terbaru |
| `--conversation <id>` | — | Melanjutkan berdasarkan ID percakapan |
| `--add-dir <path>` | — | Menambahkan direktori ke ruang kerja (dapat diulang) |
| `--sandbox` | — | Mengaktifkan pembatasan sandbox terminal |
| `--dangerously-skip-permissions` | — | Menyetujui otomatis semua permintaan alat (hanya CI) |
| `--print-timeout <duration>` | — | Batas waktu untuk mode cetak (bawaan: 5m) |
| `--log-file <path>` | — | Menimpa jalur keluaran log |

> **Catatan:** Pemilihan model dan mode ketat diatur melalui perintah garis miring `/model` dan `/permissions`, bukan flag CLI. Lihat [Dokumentasi fitur](https://antigravity.google/docs/cli-features).

---

## Perintah Slash (Mode Interaktif)

> Sumber: [Fitur CLI — Perintah Slash Inti](https://antigravity.google/docs/cli-features) · [Menggunakan Antigravity CLI](https://antigravity.google/docs/cli-using)

| Perintah | Kategori | Tujuan |
| :-- | :-- | :-- |
| `/resume` (`/switch`) | Percakapan | Buka pemilih percakapan untuk melanjutkan atau beralih sesi |
| `/rewind` (`/undo`) | Percakapan | Kembalikan riwayat percakapan ke checkpoint sebelumnya |
| `/fork` | Percakapan | Cabangkan percakapan saat ini ke ruang kerja terisolasi paralel — uji coba langkah berisiko tanpa memengaruhi yang asli |
| `/rename <name>` | Percakapan | Ganti nama utas percakapan aktif |
| `/permissions` | Konfigurasi | Atur tingkat otonomi: `request-review`, `always-proceed`, `strict` |
| `/model` | Konfigurasi | Pilih model penalaran default (bertahan di seluruh sesi) |
| `/config` (`/settings`) | Konfigurasi | Buka overlay pengaturan layar penuh |
| `/keybindings` | Konfigurasi | Buka editor pintasan keyboard interaktif |
| `/statusline` | Konfigurasi | Sesuaikan indikator bilah status CLI waktu nyata |
| `/tasks` | Pemantauan | Pantau, lihat log untuk, atau hentikan tugas latar belakang |
| `/skills` | Pemantauan | Telusuri skill agen lokal dan global |
| `/mcp` | Pemantauan | Konfigurasi dan kelola server MCP |
| `/agents` | Pemantauan | Lihat, kelola, dan setujui tindakan sub-agen |
| `/open <path>` | Utilitas | Buka file di editor eksternal pilihan Anda |
| `/usage` | Utilitas | Buka manual bantuan interaktif sebaris |
| `/logout` | Akun | Keluar dan bersihkan kredensial dalam cache |

---

## Tips Cepat

> Sumber: [Menggunakan Antigravity CLI — Tips Cepat & Pintasan Keyboard](https://antigravity.google/docs/cli-using)

| Pintasan / Tips | Aksi |
| :-- | :-- |
| `@` | Pelengkapan otomatis jalur file (ketik `@` untuk memicu saran jalur) |
| `!` | Jalankan perintah terminal langsung dari prompt |
| `esc esc` | Bersihkan kotak prompt Anda (saat tidak ada streaming yang aktif) |
| `?` | Dapatkan bantuan dan tampilkan semua perintah garis miring |
| `alt+enter` / `shift+enter` | Sisipkan baris baru tanpa mengirimkan |
| `ctrl+g` | Edit prompt di dalam editor shell default Anda |
| `ctrl+l` | Bersihkan layar TUI |
| `ctrl+d` | Keluar dari sesi CLI |
| `ctrl+z` | Tangguhkan CLI ke latar belakang terminal |
| `ctrl+j` (di `/agents`) | Teleportasi ke persetujuan sub-agen tertunda berikutnya |
| `ctrl+k` | Setujui cepat izin sub-agen yang tertunda dari percakapan utama |

---

## Perintah Plugin

```bash
# List all active plugins (JSON)
agy plugin list

# Import from Gemini CLI
agy plugin import gemini

# Import from Claude Code
agy plugin import claude

# Force re-import (after plugin updates)
agy plugin import gemini --force

# Install a plugin
agy plugin install <name>
agy plugin install <name>@<version>

# Enable / disable
agy plugin enable <name>
agy plugin disable <name>

# Validate a plugin directory
agy plugin validate ./my-plugin

# Generate marketplace link
agy plugin link <marketplace> <target>
```

---

## Sidecars

> Proses latar belakang yang dikelola AGY untuk Anda — meluncurkan, memulai ulang, dan berjalan secara independen dari percakapan apa pun. Sumber: [antigravity.google/docs/sidecars](https://antigravity.google/docs/sidecars)

```bash
# Config locations:
~/.gemini/config/sidecars/<name>/sidecar.json                         # global
~/.gemini/config/plugins/<plugin>/sidecars/<name>/sidecar.json        # plugin-scoped

# Enable (disabled by default) — edit ~/.gemini/config/config.json:
#   { "sidecars": { "<name>": { "enabled": true } } }

# Check logs:
ls ~/.gemini/antigravity-cli/sidecar_data/<name>/logs/

# agentapi (auto-available inside sidecars):
agentapi new-conversation "<prompt>"
agentapi send-message <conversation_id> "<prompt>"
```

Minimal `sidecar.json` — skrip latar belakang:

```json
{ "command": "python3", "args": ["worker.py"], "restart_policy": "on-failure" }
```

Minimal `sidecar.json` — tugas berulang terjadwal:

```json
{
  "builtin": "schedule",
  "args": ["0 9 * * 1-5", "agentapi", "new-conversation", "Summarise open PRs."]
}
```

---

## Ruang Kerja & Konteks

```bash
# Project config directory:
.agents/                    # settings.json, mcp.json, hooks.json, rules.md, skills/, plugins/

# Global config directory:
~/.gemini/config/           # settings.json, mcp.json, hooks.json, rules.md, skills/, plugins/

# User settings:
~/.gemini/antigravity-cli/settings.json

# Context file (hierarchical: cwd → parent → home):
AGENTS.md

# agy also reads:
.gemini/                    # Gemini CLI config (compatible)
```

### Pola AGENTS.md

```markdown
# Project Context

Brief description of what this project is.

## Conventions
- Language: TypeScript, Node 20
- Testing: Jest + Supertest
- DO NOT run database migrations without explicit approval
```

---

## Pola Berguna

```bash
# Review staged changes before commit
git diff --cached | agy -p "Review for bugs, security issues, missing tests."

# Generate docs for a file
cat src/api.ts | agy -p "Generate OpenAPI documentation for all exported functions."

# Analyze logs
tail -n 500 app.log | agy -p "Group these errors by root cause. Output as JSON."

# Multi-dir cross-repo analysis
agy --add-dir ../api --add-dir ../frontend \
    -p "Map data flow from frontend form submission to database write."

# Full headless CI audit (safe)
agy --sandbox --dangerously-skip-permissions \
    -p "Audit for hardcoded secrets and insecure patterns." \
    --print-timeout 5m > audit.md

# Schedule a recurring task (in interactive mode)
# > Schedule a daily code quality report at 9am weekdays.
```

---

## Pola Multi-Agen

```text
# Spawn parallel subagents (in interactive mode)
> Spawn a security auditor and a performance auditor in parallel (branch mode).

# Adversarial review
> Spawn an adversarial reviewer subagent — its job is to find reasons to NOT merge this PR.

# Steer mid-task
/btw Focus only on the authentication module, skip the frontend.

# Background task
> In the background, audit all dependencies for known CVEs. Notify me when done.
```

---

## Contoh Pipeline Mode Cetak

```bash
# Step 1: plan
agy -p "Create a refactoring plan for moving from callbacks to async/await. JSON output." \
  > plan.json

# Step 2: execute
cat plan.json | agy -p "Execute step 1 of this plan."

# Batch: process multiple files
for f in src/*.ts; do
  agy --add-dir "$(dirname $f)" \
      -p "Add JSDoc to all exported functions in $(basename $f)."
done
```

---

## Dokumentasi Resmi

| Topik | Tautan |
| :-- | :-- |
| Gambaran Umum CLI | [antigravity.google/docs/cli-overview](https://antigravity.google/docs/cli-overview) |
| Memulai | [antigravity.google/docs/cli-getting-started](https://antigravity.google/docs/cli-getting-started) |
| Menggunakan Antigravity CLI (pengaturan, kiat, pintasan keyboard) | [antigravity.google/docs/cli-using](https://antigravity.google/docs/cli-using) |
| Fitur (plugin, sandbox, perintah garis miring, sub-agen) | [antigravity.google/docs/cli-features](https://antigravity.google/docs/cli-features) |
| Migrasi dari Gemini CLI | [antigravity.google/docs/gcli-migration](https://antigravity.google/docs/gcli-migration) |
| Izin | [antigravity.google/docs/permissions](https://antigravity.google/docs/permissions) |
| Mode Ketat | [antigravity.google/docs/strict-mode](https://antigravity.google/docs/strict-mode) |
| Plugin | [antigravity.google/docs/plugins](https://antigravity.google/docs/plugins) |
| MCP | [antigravity.google/docs/mcp](https://antigravity.google/docs/mcp) |
| Skill | [antigravity.google/docs/skills](https://antigravity.google/docs/skills) |
| Aturan | [antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows) |
| Hook | [antigravity.google/docs/hooks](https://antigravity.google/docs/hooks) |
| Sidecar | [antigravity.google/docs/sidecars](https://antigravity.google/docs/sidecars) |
| Sub-agen | [antigravity.google/docs/subagents](https://antigravity.google/docs/subagents) |
| Enterprise | [antigravity.google/docs/enterprise](https://antigravity.google/docs/enterprise) |
