# Referensi: Pola DevOps & Otomatisasi

> **agy tanpa keterlibatan manusia.** Referensi mendalam untuk pipeline `--print` non-interaktif, integrasi CI/CD, ruang kerja multi-repositori, dan eksekusi sandbox. Perintah-perintah penting ditautkan dari [Lembar Contekan](cheatsheet.md).

---

## DevOps 1 — Mode Print: Inti Non-Interaktif <span class="duration-badge">5 min</span>

`--print` (singkatan: `-p`) adalah mode headless dari agy. Ini menjalankan satu prompt, mencetak respons, dan keluar. Tidak ada sesi interaktif, tidak ada prompt.

```bash
# Basic usage
agy --print "Summarize the top-level README of this project."

# Set a timeout (default: 5 minutes)
agy --print "Generate a full test suite for auth.js" --print-timeout 10m

# Short form
agy -p "What does this project do?"
```

Output dikirim ke stdout — lakukan pipe, alihkan, simpan.

```bash
# Pipe into a file
agy -p "Generate API documentation for all endpoints" > docs/api.md

# Pipe into another command
agy -p "List all TODO comments in this codebase as JSON" | jq '.[] | .file'
```

---

## DevOps 2 — Pipeline Shell <span class="duration-badge">10 menit</span>

> **Pola: agy sebagai perintah Unix** — gabungkan dengan alat shell standar.

### Pola: Pipe Kode ke agy

```bash
# Review a specific file
cat src/auth.js | agy -p "Review this file for security vulnerabilities."

# Review staged changes before commit
git diff --cached | agy -p "Review these changes. Flag bugs, security issues, or missing tests."

# Analyze a log file
tail -n 200 app.log | agy -p "Identify patterns in these errors. Group by root cause."
```

### Pola: Merangkai Panggilan agy

```bash
# Step 1: Generate a plan
agy -p "Create a migration plan for moving this project from CommonJS to ESM. Output as JSON with steps array." > migration-plan.json

# Step 2: Execute step by step
cat migration-plan.json | agy -p "Execute step 1 of this migration plan."
```

### Pola: Pemrosesan Batch

```bash
# Process multiple files
for f in src/**/*.js; do
  out="/tmp/review_$(basename $f .js).md"
  agy -p "Review $(basename $f) for issues" \
      --add-dir "$(dirname "$f")" \
      --print-timeout 2m > "$out"
  echo "=== $f ==="
  cat "$out"
done
```

---

## DevOps 3 — Ruang Kerja Multi-Direktori dengan --add-dir <span class="duration-badge">10 min</span>

> **Pola: Konteks Lintas-Repo** — memberikan agy visibilitas ke beberapa basis kode secara bersamaan.

Secara default, agy mengindeks repo git yang berisi direktori Anda saat ini. `--add-dir` memperluasnya ke direktori tambahan.

```bash
# Give agy access to both your app and its shared library
agy --add-dir ../shared-lib "How does the app use shared-lib? Identify any API mismatches."

# Add multiple directories
agy --add-dir ../api --add-dir ../frontend "Generate an integration test that covers the API-to-frontend data flow."

# Use in print mode
agy -p "Compare the error handling patterns in app/ vs api/" --add-dir ../api
```

### Kasus Penggunaan Dunia Nyata: Tinjauan Monorepo

```bash
# From the root of a monorepo, review cross-package dependencies
agy --add-dir packages/core --add-dir packages/api --add-dir packages/ui \
    -p "Map the dependency graph between these three packages and flag any circular dependencies."
```

!!! tip "Flag yang dapat diulang"
    `--add-dir` dapat diulang — tambahkan sebanyak mungkin direktori yang Anda butuhkan. agy mengindeks semuanya bersama repo git utama.

---

## DevOps 4 — Integrasi CI/CD <span class="duration-badge">10 min</span>

> **Pola: agy di dalam Pipeline** — tinjauan dan analisis kode otomatis pada setiap PR.

### Contoh GitHub Actions

```yaml
# .github/workflows/agy-review.yml
name: agy Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install agy-cli
        run: |
          curl -fsSL https://antigravity.google/cli/install.sh | bash

      - name: Review PR changes
        run: |
          git diff origin/main...HEAD | \
          agy --dangerously-skip-permissions \
              --print "Review these changes for: (1) correctness, (2) security, (3) missing tests. Output as markdown." \
              --print-timeout 5m > review.md

      - name: Post review as comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

!!! warning "--dangerously-skip-permissions di CI"
    Selalu gunakan `--dangerously-skip-permissions` di CI — tidak ada manusia yang akan mengklik "setujui". Pasangkan dengan mode sandbox untuk membatasi apa yang dapat diakses oleh agy.

### Hook Pre-Commit

```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "🤖 Running agy pre-commit review..."
git diff --cached | agy --dangerously-skip-permissions \
    -p "Flag any obvious bugs or security issues in these staged changes. If none, output 'LGTM'." \
    --print-timeout 60s

# Optionally block commit if issues found
# (parse output for keywords)
```

---

## DevOps 5 — Mode Sandbox <span class="duration-badge">5 min</span>

> **Pola: Eksekusi Terbatas** — jalankan agy dengan isolasi terminal tingkat OS.

### Mengaktifkan Sandbox

Sandbox dikonfigurasi melalui `settings.json` (baik proyek `.agents/settings.json` atau pengguna `~/.gemini/antigravity-cli/settings.json`):

```json
{
  "enableTerminalSandbox": true
}
```

Saat diaktifkan, agy menggunakan **isolasi OS native** untuk membatasi eksekusi perintah terminal:

| OS | Teknologi Isolasi |
| :-- | :-- |
| **Linux** | nsjail |
| **macOS** | sandbox-exec |
| **Windows** | AppContainer |

### Bypass Per-Perintah

Dengan sandbox diaktifkan, agy akan **meminta persetujuan** ketika sebuah perintah perlu keluar dari sandbox. Anda akan melihat prompt bypass per-perintah — yang memungkinkan eksekusi selektif tanpa menonaktifkan seluruh sandbox.

### Kasus Penggunaan

- Menjalankan agy pada kode yang tidak tepercaya
- Mengaudit konten sensitif tanpa efek samping
- Lingkungan yang sensitif terhadap tata kelola di mana setiap eksekusi memerlukan persetujuan

### Menggabungkan dengan Izin

Untuk kontrol maksimum, pasangkan mode sandbox dengan model izin:

```json
{
  "enableTerminalSandbox": true,
  "permissions": {
    "allow": ["read_file", "command(git)"],
    "deny": ["command(rm)", "unsandboxed"]
  }
}
```

> 📖 Detail lengkap: [Dokumentasi Izin](https://www.antigravity.google/docs/permissions)

---

## DevOps 6 — Hook & Aturan <span class="duration-badge">5 min</span>

> **Pola: Pagar Pengaman & Otomatisasi** — menegakkan standar dan memicu tindakan pada titik-titik siklus hidup utama.

### Hook

Hook memungkinkan Anda menjalankan logika kustom pada 5 peristiwa siklus hidup:

| Peristiwa | Kapan ini terpicu |
| :-- | :-- |
| `PreToolUse` | Sebelum agy memanggil alat apa pun (membaca file, menjalankan perintah, dll.) |
| `PostToolUse` | Setelah pemanggilan alat selesai |
| `PreInvocation` | Sebelum agy mulai memproses prompt |
| `PostInvocation` | Setelah agy menyelesaikan respons |
| `Stop` | Saat sesi berakhir |

Konfigurasikan hook di `hooks.json` (di `.agents/` untuk proyek atau `~/.gemini/config/` untuk global). Skrip hook menerima JSON pada stdin dan mengembalikan JSON pada stdout.

#### Contoh Hook (di `samples/hooks/`)

| Skrip | Peristiwa | Tujuan |
| :-- | :-- | :-- |
| `secret-scanner.sh` | `PreToolUse` | Memblokir penulisan yang berisi kredensial yang di-hardcode |
| `git-context-injector.sh` | `PreToolUse` | Menyuntikkan riwayat git terbaru untuk file target sebelum penulisan |
| `test-nudge.sh` | `PostToolUse` | Mendorong agen untuk menjalankan pengujian setelah penulisan file |
| `session-context.sh` | `PreInvocation` | Menyuntikkan cabang, perubahan yang tertunda, dan dependensi pada awal sesi |

> 📖 Detail lengkap: [Dokumentasi Hook](https://www.antigravity.google/docs/hooks)

### Aturan

Aturan adalah file markdown yang disuntikkan ke dalam prompt sistem agy sebagai blok `RULE` — batasan keras yang harus diikuti oleh agy.

| Cakupan | Lokasi |
| :-- | :-- |
| **Proyek** | `.agents/rules.md` atau `.agents/rules/*.md` |
| **Global** | `~/.gemini/config/rules.md` atau `~/.gemini/config/rules/*.md` |

Contoh `.agents/rules.md`:

```markdown
- Never delete migration files
- Always use TypeScript strict mode
- Run `npm test` after any code change
- Do not modify files in the vendor/ directory
```

> 📖 Detail lengkap: [Dokumentasi Aturan & Alur Kerja](https://www.antigravity.google/docs/rules-workflows)

---

## Latihan

<div class="exercise-card" markdown>

### :material-file-document: Latihan 3: Pipeline --print

**Berkas:** [`ex03_print_mode_pipeline.md`](exercises/ex03_print_mode_pipeline.md)
**Durasi:** 20 menit
**Tujuan:** Membangun pipeline shell multi-langkah menggunakan agy --print. Meninjau perubahan yang di-stage, menghasilkan dokumentasi, dan mengonfigurasi alur kerja GitHub Actions.

</div>

---

## Modul Selanjutnya

→ **[Modul 4: Multi-Agen & Lanjutan](multi-agent-advanced.md)** — sub-agen, pengarahan di tengah tugas /btw, penjadwalan.
