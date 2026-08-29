# Modul 2: Modernisasi Basis Kode Legacy

<div class="module-header" markdown>
**Durasi:** ~75 menit  
**Tujuan:** Memigrasikan aplikasi legacy dengan aman menggunakan primitif Antigravity CLI — pembatasan izin yang ketat, self-onboarding agen, analisis sub-agen paralel, hook sebagai pagar pengaman, dan `/rewind` sebagai jaring pengaman Anda.  
**PRD Latihan:** [Modernisasi .NET](exercises/ex08_dotnet_modernization.md) · [Pembaruan Java](exercises/ex09_java_upgrade.md)
</div>

> 📖 Sumber: [Izin](https://antigravity.google/docs/permissions) · [Mode Ketat](https://antigravity.google/docs/strict-mode) · [Sub-agen](https://antigravity.google/docs/subagents) · [Skill](https://antigravity.google/docs/skills) · [Hook](https://antigravity.google/docs/hooks) · [cli-features](https://antigravity.google/docs/cli-features) · [cli-using](https://antigravity.google/docs/cli-using)

---

## Mengapa Modernisasi Legacy Itu Sulit

Risiko dalam migrasi besar bukanlah perubahan kode — melainkan **hal-hal yang tidak diketahui**. Anda tidak tahu apa yang akan Anda rusak sampai hal itu benar-benar rusak. Tiga mode kegagalan tersebut adalah:

1. **Pelebaran ruang lingkup** — agen memfaktorkan ulang hal-hal yang tidak Anda minta untuk disentuh
2. **Keruntuhan konteks** — setelah sesi yang panjang, agen kehilangan jejak batasan migrasi Anda
3. **Tidak ada rollback** — perubahan yang salah merambat sebelum Anda dapat menghentikannya

Primitif AGY mengatasi ketiganya secara langsung.

---

## 2.1 — Izin Ketat: Baca Sebelum Anda Menulis <span class="duration-badge">15 min</span>

Padanan AGY untuk "Mode Perencanaan" adalah **izin ketat** — sebuah gerbang keras yang menolak semua penulisan file dan perintah shell sampai Anda secara eksplisit mengizinkannya.

### Kunci Sebelum Anda Menjelajah

```bash
/permissions
```

Atur level ke `strict`:

```bash
# In the permissions dialog, select: strict
# Or set directly in settings.json:
```

```json
{
  "permissions": {
    "mode": "strict"
  }
}
```

Dalam mode `strict`, agen dapat membaca file, mencari di web, dan menalar — tetapi **tidak dapat menulis, menghapus, atau mengeksekusi apa pun**. Ini adalah dinding keras, bukan prompt lunak.

> 📖 Sumber: [Mode Ketat](https://antigravity.google/docs/strict-mode) · [Izin](https://antigravity.google/docs/permissions)

### Sekarang Selidiki dengan Bebas

Dengan penulisan terkunci, beri agen mandat membaca tanpa batas:

```text
Analyze this entire codebase for a migration. Map:
1. Framework versions and dependency tree (check package.json / pom.xml / .csproj)
2. Architectural patterns in use (MVC, layered, hexagonal)
3. All deprecated API usage (javax.* imports, legacy auth patterns, XML config)
4. Configuration files and external property sources
5. Test frameworks and coverage gaps
6. Migration risks ordered by severity
```

> **Apa yang terjadi:** Agen membaca setiap file yang dibutuhkannya, melacak impor dan rantai panggilan, dan membangun model mental — semuanya dengan nol risiko modifikasi. Ini adalah fase pengintaian Anda.

### Tinjau Rencana di Editor Anda

Setelah agen menghasilkan rencana migrasi, buka di editor Anda untuk menyempurnakannya:

```text
ctrl+g
```

Ini akan membawa Anda ke `$EDITOR` dengan output agen saat ini. Edit batasan, tambahkan persyaratan khusus tim, coret ruang lingkup yang tidak Anda inginkan. Agen akan menggabungkan hasil edit Anda saat Anda menyimpan dan keluar.

> 📖 Sumber: [cli-using — Keybindings](https://antigravity.google/docs/cli-using) — uid 3_276–3_280: "Edit prompt di dalam editor shell default Anda"

### Buka Kunci Penulisan — Tetapi Hanya untuk Apa yang Anda Setujui

Setelah rencana disetujui, pulihkan akses tulis secara selektif:

```bash
/permissions
# Select: request-review
```

Dalam mode `request-review`, agen meminta persetujuan sebelum setiap penulisan atau perintah shell. Anda melihat dengan tepat apa yang ingin dilakukannya sebelum ia melakukannya.

> **Alurnya:** `strict` (selidiki) → setujui rencana → `request-review` (eksekusi dengan pengawasan) → `always-proceed` hanya untuk langkah akhir yang tepercaya dan teruji dengan baik.

---

## 2.2 — AGENTS.md: Mengodekan Standar Migrasi <span class="duration-badge">10 min</span>

Konteks menghilang selama sesi yang panjang. AGENTS.md adalah cara Anda mencegahnya — ini disuntikkan ke setiap sesi secara otomatis, tidak peduli seberapa lama percakapan berlangsung.

### Orientasi Mandiri Agen

Pola yang paling kuat adalah meminta agen **menulis AGENTS.md-nya sendiri** dari apa yang ditemukannya selama investigasi. Ini mengodekan apa yang dipelajarinya sebagai pagar pengaman untuk pekerjaannya sendiri selanjutnya.

```text
Based on your codebase analysis, write an AGENTS.md that:
1. Documents current state (Spring Boot 2.6, Java 8, javax.* namespaces)
2. Defines target state (Spring Boot 3.3, Java 21, jakarta.* namespaces)
3. Sets migration rules:
   - Migrate one module at a time — never touch more than one bounded context per session
   - Every migrated class must have a passing test before moving on
   - Preserve all existing API contracts — no breaking changes to callers
   - Commit after each completed phase with a structured message
4. Flags the specific risks you identified in your analysis
5. Lists files that are off-limits in this phase

Write this to AGENTS.md in the project root.
```

> **Mengapa orientasi mandiri berfungsi:** Agen menulis instruksi untuk dirinya sendiri. Setiap keputusan migrasi yang dibuatnya dari titik ini ke depan diperiksa terhadap batasan yang ditulisnya. Ini adalah loop yang memperkuat dirinya sendiri — konteks yang lebih baik menghasilkan perubahan yang lebih baik, yang memunculkan lebih banyak pola, yang meningkatkan konteks.

### Konteks Modular dengan Impor @file

Untuk proyek besar, jaga agar AGENTS.md tetap ringkas dan impor spesifikasi terperinci:

```markdown
# AGENTS.md

@./docs/migration/architecture-target.md
@./docs/migration/api-contracts.md
@./docs/migration/phase-1-checklist.md
```

> 📖 Sumber: [cli-using](https://antigravity.google/docs/cli-using) — sintaks impor AGENTS.md

### Berkas Aturan untuk Batasan Ketat

Untuk persyaratan yang tidak dapat dinegosiasikan, gunakan `.agents/rules.md` — ini disuntikkan sebagai arahan prompt sistem, bukan hanya konteks:

```markdown
# .agents/rules.md

- NEVER delete migration files (MIGRATION.md, phase-*.md)
- NEVER modify files outside the current migration module's directory
- ALWAYS run the test suite before declaring a phase complete
- ALWAYS commit with message format: "migrate(phase-N): <description>"
```

> 📖 Sumber: [cli-using](https://antigravity.google/docs/cli-using) — arahan prompt sistem `.agents/rules.md`

---

## 2.3 — Sub-agen: Tim Analisis Paralel <span class="duration-badge">15 min</span>

Migrasi besar memiliki beberapa masalah independen — keamanan, performa, kontrak API, cakupan pengujian. Menjalankannya secara berurutan akan lambat dan membuang jendela konteks agen. Gunakan sub-agen untuk memparalelkannya.

### Membuat Tim Analisis Paralel

```text
I need three parallel analyses before we start migrating. Please spawn:

1. A security-analysis subagent: scan every auth and session-handling class
   for OWASP Top 10 issues. Read-only. Report back with file paths and line numbers.

2. A dependency-map subagent: trace all inter-module dependencies and identify
   which modules can be migrated independently vs which have shared state.
   Produce a migration-order recommendation.

3. A test-coverage subagent: list every public method in the auth module with
   no test coverage. Produce a test-gap report.

Run all three concurrently. I'll review the reports before we start Phase 1.
```

### Memantau dari Panel Sub-agen

```bash
/agents
```

Panel ini menunjukkan semua sub-agen yang sedang berjalan dengan status: `running`, `done`, `killed`. Perhatikan ketiganya selesai secara bersamaan.

```text
ctrl+j
```

Menteleportasi Anda ke sub-agen berikutnya yang menunggu persetujuan Anda — berguna jika salah satunya mencapai batas izin dan membutuhkan persetujuan.

```text
ctrl+k
```

Menyetujui dengan cepat permintaan izin sub-agen dari percakapan utama tanpa meninggalkan konteks Anda saat ini.

> 📖 Sumber: [cli-features — Sub-agen](https://antigravity.google/docs/cli-features) — uid 5_278–5_316

### Definisi Sub-agen Kustom

Buat pemindai keamanan read-only di `.agents/agents/security-scanner.md`:

```markdown
---
model: gemini-3.7-flash
tools:
  allow:
    - read_file
    - list_directory
    - grep_search
# No write_file, no run_command — this agent is read-only
---

You are a security analyst specializing in migration risk assessment.
Your job is to identify vulnerabilities in legacy code that could be
amplified during a modernization effort.

Focus on:
- Authentication and session management anti-patterns
- SQL injection vectors in legacy data access layers
- Hardcoded credentials or secrets in configuration files
- Deprecated cryptographic primitives (MD5, SHA-1, DES)
- Unvalidated redirects or file path traversal risks

Always report: file path, line number, severity (HIGH/MEDIUM/LOW), and remediation.
Never modify any file. Never execute any command.
```

> 📖 Sumber: [Sub-agen](https://antigravity.google/docs/subagents) · [cli-features](https://antigravity.google/docs/cli-features) — uid 5_274: format JSON izin terperinci

---

## 2.4 — Skill: Keahlian Migrasi yang Dapat Digunakan Kembali <span class="duration-badge">10 min</span>

Skill adalah kumpulan instruksi yang dibaca dan diaktifkan oleh agen saat relevan. Untuk migrasi yang berulang (Java 8→21, .NET Framework→.NET 8, Express→Fastify), enkodekan pola tersebut sekali sebagai sebuah skill.

### Telusuri Skill yang Tersedia

```bash
/skills
```

### Buat Skill Migrasi

```bash
mkdir -p ~/.gemini/antigravity-cli/skills/java-migration
```

Buat `~/.gemini/antigravity-cli/skills/java-migration/SKILL.md`:

```markdown
---
name: java-migration
description: >
  Guides Java 8 to Java 21 + Spring Boot 3.x migration. Activates when
  the user mentions javax.*, Spring Boot 2.x, or Java upgrade. Provides
  phase-by-phase migration steps, jakarta.* namespace rules, and
  mandatory test-gate requirements between phases.
---

## Java 8 → 21 Migration Protocol

### Phase 0 — Inventory (always first)
- Run: grep -r "javax\." src/ | grep -v test | sort | uniq -c | sort -rn
- Identify all Spring Boot starter versions in pom.xml
- Check for removed APIs: sun.misc.*, com.sun.*, internal packages

### Phase 1 — Dependency Upgrade
- Update Spring Boot parent to 3.3.x
- Replace javax.* with jakarta.* (use: sed -i 's/javax\./jakarta\./g')
- Update Hibernate to 6.x — @Entity annotation semantics changed
- Gate: mvn clean verify must pass before Phase 2

### Phase 2 — Configuration Migration

**Goal:** Migrate XML/property-file config to type-safe structured config.

**Steps:**
1. Identify all config sources (XML, .properties, environment variables)
2. Map to typed configuration classes
3. Replace with framework-native config (Spring Boot `@ConfigurationProperties`, .NET `IOptions<T>`)
4. Add validation annotations
5. Remove legacy config loading code

**Validation:** All tests pass with new config loading path.
```

> 📖 Sumber: [Skill](https://antigravity.google/docs/skills) · [cli-features — /skills](https://antigravity.google/docs/cli-features) — uid 5_251–5_253

---

## 2.5 — Hook: Pagar Pengaman Otomatis <span class="duration-badge">10 min</span>

Untuk migrasi enterprise, Anda menginginkan gerbang otomatis — bukan hanya peninjauan manual. Hook terpicu pada peristiwa CLI dan dapat memblokir, memperingatkan, atau mencatat penggunaan alat sebelum itu terjadi.

### Hook Pra-Alat: Blokir Penulisan di Luar Cakupan Migrasi

Buat `.agents/hooks/scope-guard.sh`:

```bash
#!/bin/bash
# AGY CLI hook event: PreToolUse
# Blocks writes to files outside the current migration module

TOOL_NAME="$1"
FILE_PATH="$2"
MIGRATION_MODULE="${MIGRATION_MODULE:-src/auth}"  # Set before starting each phase

if [[ "$TOOL_NAME" == "write_file" || "$TOOL_NAME" == "edit" ]]; then
  if [[ "$FILE_PATH" != *"$MIGRATION_MODULE"* ]]; then
    echo "BLOCK: Write to $FILE_PATH is outside migration scope ($MIGRATION_MODULE)" >&2
    exit 1  # Non-zero exit blocks the tool call
  fi
fi
```

Daftarkan di `settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "write_file|edit",
        "command": ".agents/hooks/scope-guard.sh"
      }
    ]
  }
}
```

### Hook Pasca-Alat: Jalankan Otomatis Pengujian Setelah Setiap Penulisan Berkas

```bash
#!/bin/bash
# AGY CLI hook event: PostToolUse
# Runs tests automatically after every source file write

TOOL_NAME="$1"
FILE_PATH="$2"

if [[ "$TOOL_NAME" == "write_file" && "$FILE_PATH" == *".java" ]]; then
  echo "Running test gate after $FILE_PATH was modified..."
  mvn test -pl "$(dirname $FILE_PATH | sed 's|src/main/java||')" -q 2>&1
  if [[ $? -ne 0 ]]; then
    echo "⚠️  Tests failed after writing $FILE_PATH — consider /rewind"
  fi
fi
```

> 📖 Sumber: [Hook](https://antigravity.google/docs/hooks)

---

## 2.6 — /rewind dan /fork: Jaring Pengaman Anda <span class="duration-badge">5 min</span>

### /rewind — Memutar Kembali Percakapan

Jika agen keluar jalur, Anda tidak perlu memulai dari awal. `/rewind` memutar kembali riwayat percakapan:

```bash
/rewind
```

Ini akan membuka pemilih riwayat. Pilih giliran untuk dikembalikan. Pemahaman agen tentang basis kode akan diatur ulang ke titik tersebut — berguna jika ia telah mengumpulkan asumsi yang salah selama sesi yang panjang.

> 📖 Sumber: [cli-features](https://antigravity.google/docs/cli-features) — uid 5_220–5_226: "`/rewind` (alias `/undo`) — memutar kembali riwayat percakapan"

### /fork — Eksplorasi Tanpa Risiko

Sebelum mencoba langkah migrasi yang berisiko, fork percakapan tersebut:

```bash
/fork
```

Ini akan membuat ruang kerja paralel. Anda dapat mencoba pendekatan berisiko di dalam fork tersebut. Jika berhasil, bagus. Jika tidak, tutup fork dan lanjutkan dari percakapan utama — yang tidak pernah berubah.

> 📖 Sumber: [cli-using](https://antigravity.google/docs/cli-using) — uid 3_219–3_224: "`/fork` untuk membuat ruang kerja terpisah"

### /resume — Melanjutkan Migrasi Panjang

Migrasi besar memakan waktu berhari-hari. Saat Anda kembali:

```bash
/resume
```

Ini akan membuka pemilih sesi yang menampilkan sesi migrasi Anda sebelumnya dengan stempel waktu dan nama percakapan. Pilih sesi yang tepat untuk melanjutkan tepat di tempat Anda tinggalkan.

> 📖 Sumber: [cli-features](https://antigravity.google/docs/cli-features) — uid 5_213–5_219

Ganti nama sesi untuk menjaga agar migrasi tetap teratur:

```bash
/rename "Java 21 Migration — Phase 2: Jakarta namespace"
```

---

## 2.7 — Mode Cetak: Pipeline Migrasi Non-Interaktif <span class="duration-badge">5 min</span>

Untuk gerbang CI/CD atau eksekusi migrasi semalaman, gunakan mode cetak untuk menyalurkan tugas migrasi tanpa interaksi:

```bash
# Dry-run: analyze and report issues — no writes
agy -p "Review the migration changes in the last commit. \
  Check for: javax.* references that weren't updated, \
  missing jakarta.* imports, and test files that weren't \
  updated to match renamed packages. \
  Output a structured report with file paths and line numbers."
```

```bash
# Chain: analyze → generate migration report → save
agy -p "Scan src/auth/ for javax.persistence.* usage" | \
  agy -p "Convert this javax.persistence usage report into \
  a step-by-step migration plan with exact sed commands" > migration-plan.md
```

> 📖 Sumber: [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — `agy --help`: "-p: Alias pendek untuk --print"

---

## Latihan Praktik

<div class="exercise-card" markdown>

### :material-file-document: Latihan 8: Modernisasi Legacy

**Berkas:** [`ex08_dotnet_modernization.md`](exercises/ex08_dotnet_modernization.md) · [`ex09_java_upgrade.md`](exercises/ex09_java_upgrade.md)  
**Durasi:** 45 menit  
**Tujuan:** Melakukan migrasi penuh menggunakan primitif AGY dari modul ini.

**Pilih jalur Anda:**

#### Jalur A: Utamakan Rencana (Ketat → Investigasi → Eksekusi)

1. Atur `/permissions` ke `strict` — kunci semua penulisan
2. Berikan agen mandat investigasi penuh (Bagian 2.1)
3. Gunakan `ctrl+g` untuk membuka rencana di editor Anda dan tambahkan batasan tim
4. Tulis AGENTS.md yang mengodekan aturan migrasi (atau minta agen untuk menulisnya)
5. Tambahkan `.agents/rules.md` dengan hal-hal mutlak yang tidak dapat dinegosiasikan
6. Beralih ke `request-review` — mulai Fase 1 dengan pengawasan
7. Gunakan `/rewind` jika agen menyimpang di luar lingkup
8. Ganti nama sesi: `/rename "Migrasi — Fase 1 selesai"`

#### Jalur B: Utamakan Sub-agen (Analisis Paralel → Konteks → Eksekusi)

1. Buat tiga sub-agen paralel: pemindaian keamanan, peta dependensi, cakupan pengujian
2. Pantau melalui `/agents` — gunakan `ctrl+j` dan `ctrl+k` untuk persetujuan
3. Gabungkan laporan mereka ke dalam AGENTS.md (minta agen untuk menyintesisnya)
4. Instal skill `java-migration` (Bagian 2.4)
5. Gunakan `/fork` sebelum langkah paling berisiko — coba di sana terlebih dahulu
6. Gunakan mode cetak untuk menghasilkan laporan pasca-fase

</div>

---

## Ringkasan: Primitif AGY untuk Modernisasi Legacy

| Primitif | Apa yang Dilakukannya | Kapan Digunakan |
| :-- | :-- | :-- |
| `/permissions strict` | Gerbang read-only yang ketat — tidak ada penulisan atau perintah | Fase investigasi |
| `/permissions request-review` | Agen bertanya sebelum setiap penulisan | Eksekusi terkontrol |
| `ctrl+g` | Buka rencana di `$EDITOR` untuk pengeditan kolaboratif | Penyempurnaan rencana |
| **AGENTS.md** | Standar migrasi persisten di seluruh sesi | Selalu — menyandikan batasan |
| `.agents/rules.md` | Arahan system-prompt yang ketat | Pagar pengaman yang tidak dapat dinegosiasikan |
| **Sub-agen** | Tim analisis paralel | Investigasi multi-perhatian |
| `/agents` + `ctrl+j` + `ctrl+k` | Pantau dan setujui pekerjaan sub-agen | Selama eksekusi paralel |
| **Hooks** (PreToolUse) | Blokir penulisan di luar lingkup migrasi | Pagar pengaman otomatis |
| **Hooks** (PostToolUse) | Jalankan pengujian otomatis setelah setiap perubahan | Otomatisasi gerbang pengujian |
| `/rewind` | Kembalikan percakapan jika agen menyimpang | Koreksi arah pertengahan sesi |
| `/fork` | Coba langkah berisiko di cabang yang terisolasi | Sebelum perubahan berisiko tinggi |
| `/resume` | Lanjutkan migrasi multi-hari | Kembali ke sesi |
| `/rename` | Beri label sesi berdasarkan fase | Manajemen sesi |
| `agy -p` | Pipeline migrasi non-interaktif | Gerbang CI, eksekusi semalaman |
| **Skills** | Playbook migrasi yang dapat digunakan kembali | Pola migrasi yang dapat diulang |

---

## Langkah Selanjutnya

→ Lanjutkan ke **[Modul 3: Membangun Agen AGY dengan SDK](agy-sdk.md)**

→ **[Lembar Contekan](cheatsheet.md)** — semua perintah di satu tempat
