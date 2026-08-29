# Latihan 7 — Penelusuran Migrasi

> **Modul:** Lampiran — Panduan Migrasi
> **Waktu:** 20 menit
> **Format:** Individu atau berpasangan

---

## Tujuan

Telusuri direktori proyek Gemini CLI yang sebenarnya dan migrasikan ke AGY CLI. Anda akan memperbarui lokasi file konfigurasi, definisi server MCP, nama peristiwa hook, dan konten AGENTS.md — kemudian memvalidasinya menggunakan sub-agen `migration-validator`.

---

## Latar Belakang

Saat tim melakukan migrasi dari Gemini CLI ke AGY CLI, terdapat empat titik kerusakan umum:

| Apa yang rusak | Mengapa |
| :-- | :-- |
| Peristiwa hook `SessionStart`, `BeforeTool`, `AfterTool` | Diubah namanya menjadi `PreInvocation`, `PreToolUse`, `PostToolUse` |
| Kunci `url` MCP di `settings.json` | AGY menggunakan `serverUrl` dalam `mcp.json` yang terpisah |
| Direktori konfigurasi proyek `.gemini/` | AGY menggunakan `.agents/` |
| Berkas biner `gemini` dalam skrip | Harus diperbarui menjadi `agy` |

---

## Pengaturan

Anda memerlukan contoh proyek Gemini CLI untuk dimigrasikan. Buat starter:

```bash
mkdir ~/gemini-migration-lab && cd ~/gemini-migration-lab

# Create a legacy Gemini CLI settings.json
mkdir -p .gemini/hooks
cat > .gemini/settings.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
    }
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{
          "name": "session-context",
          "type": "command",
          "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/session-context.sh",
          "timeout": 3000
        }]
      }
    ],
    "BeforeTool": [
      {
        "matcher": "write_file|replace_in_file",
        "hooks": [{
          "name": "secret-scanner",
          "type": "command",
          "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/secret-scanner.sh",
          "timeout": 2000
        }]
      }
    ]
  }
}
EOF

# Create a legacy GEMINI.md
cat > .gemini/GEMINI.md << 'EOF'
# Project Context

This is a Node.js API service. Always run `npm test` after changes.
Use gemini for code reviews before merging PRs.
EOF

# Create a CI script that calls the old binary
mkdir -p .github/workflows
cat > scripts/review.sh << 'EOF'
#!/usr/bin/env bash
gemini -p "Review the diff: $(git diff HEAD~1)" > review.md
EOF
```

---

## Bagian 1 — Migrasi Manual (10 menit)

Migrasikan proyek ini sendiri:

### Langkah 1: Pindahkan konfigurasi ke direktori AGY

```bash
mkdir -p .agents/hooks
# AGY reads .agents/ instead of .gemini/ for project config
cp .gemini/GEMINI.md .agents/AGENTS.md
cp .gemini/settings.json .agents/settings.json
```

### Langkah 2: Pisahkan konfigurasi MCP

```bash
# AGY uses mcp.json, not mcpServers in settings.json
cat > .agents/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
    }
  }
}
EOF
```

### Langkah 3: Tulis ulang nama peristiwa hook di settings.json

```json
{
  "hooks": {
    "PreInvocation": [
      {
        "hooks": [{
          "name": "session-context",
          "type": "command",
          "command": "$AGY_PROJECT_DIR/.agents/hooks/session-context.sh",
          "timeout": 3000
        }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "write_file|edit",
        "hooks": [{
          "name": "secret-scanner",
          "type": "command",
          "command": "$AGY_PROJECT_DIR/.agents/hooks/secret-scanner.sh",
          "timeout": 2000
        }]
      }
    ]
  }
}
```

### Langkah 4: Perbarui referensi berkas biner

```bash
sed -i 's/\bgemini\b/agy/g' scripts/review.sh
```

---

## Bagian 2 — Validasi dengan Agen Validator Migrasi (5 menit)

Mulai AGY CLI dan luncurkan validator migrasi:

```bash
cd ~/gemini-migration-lab
agy
```

Di dalam REPL AGY:

```text
Use the migration-validator agent to check this project directory for any remaining Gemini CLI configuration.
```

Sub-agen `migration-validator` akan memeriksa:

- [ ] Nama peristiwa hook (tidak ada `SessionStart`, `BeforeTool`, `AfterTool`)
- [ ] Format MCP (`serverUrl` untuk SSE, bidang `type` ada)
- [ ] Referensi berkas biner (`agy` bukan `gemini` dalam skrip)
- [ ] Jalur konfigurasi (`.agents/` bukan `.gemini/`)

---

## Bagian 3 — Diskusi (5 menit)

**Pertanyaan refleksi:**

1. Apa yang akan rusak pertama kali di CI jika Anda lupa memperbarui nama peristiwa hook?
2. Mengapa AGY memisahkan konfigurasi MCP ke dalam `mcp.json` alih-alih menggabungkannya di `settings.json`?
3. Jika Anda memiliki monorepo dengan 10 proyek, seperti apa bentuk skrip migrasi Anda?

---

## Tantangan Bonus

Tambahkan sebuah hook `PreToolUse` ke proyek yang dimigrasikan yang memblokir agen agar tidak memanggil `git push` tanpa konfirmasi. Gunakan pola hook `decision: deny`.

Lihat [`samples/hooks/secret-scanner.sh`](https://github.com/pauldatta/agy-cli-field-workshop/blob/main/samples/hooks/secret-scanner.sh) sebagai templat untuk pola keputusan tersebut.

---

## Poin Penting

| Gemini CLI | AGY CLI |
| :-- | :-- |
| `SessionStart` | `PreInvocation` |
| `BeforeTool` | `PreToolUse` |
| `AfterTool` | `PostToolUse` |
| alat `replace_in_file` | alat `edit` |
| direktori proyek `.gemini/` | direktori proyek `.agents/` |
| `GEMINI.md` | `AGENTS.md` |
| blok MCP `settings.json` | `mcp.json` dengan `serverUrl` |
| `url:` untuk SSE | `serverUrl:` untuk SSE |
| berkas biner `gemini` | berkas biner `agy` |
