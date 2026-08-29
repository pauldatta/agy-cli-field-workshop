# Modul 3: Membangun Agen AGY dengan SDK

<div class="module-header" markdown>
**Durasi:** ~90 menit  
**Tujuan:** Membangun agen AGY siap produksi dari awal menggunakan pustaka Python `google-antigravity` — alat, hook, kebijakan, status sesi, orkestrasi multi-agen, dan keluaran terstruktur.  
**Latihan:** [Latihan 10: Agen Pertama Anda](exercises/ex10_first_agent.md) · [Latihan 11: Pipeline Multi-Agen](exercises/ex11_multi_agent_pipeline.md)
</div>

> 📖 Sumber: [Ringkasan SDK](https://antigravity.google/docs/sdk-overview) · [google-antigravity PyPI](https://pypi.org/project/google-antigravity/) · [Skill](https://antigravity.google/docs/skills)

---

## Mengapa Membangun Agen Daripada Hanya Menggunakan CLI?

CLI adalah **asisten serbaguna**. Sebuah agen yang Anda bangun dengan SDK adalah seorang **spesialis** — ia memiliki pekerjaan yang sempit, alat khusus domain, prompt sistem yang direkayasa dengan cermat, dan dapat di-deploy sebagai layanan yang dapat dipanggil oleh seluruh tim Anda.

| | Antigravity CLI | Agen SDK AGY |
| :-- | :-- | :-- |
| **Siapa yang menggunakannya** | Pengembang individu | Tim / konsumen API |
| **Kustomisasi** | AGENTS.md + plugin | Kontrol kode penuh |
| **Alat** | Alat CLI bawaan | Fungsi Python apa pun yang Anda tulis |
| **Kebijakan** | Prompt persetujuan interaktif | Aturan `policy.*` terprogram |
| **Deployment** | Sesi interaktif lokal | Layanan Cloud Run, dapat dipanggil melalui API |
| **Multi-agen** | Sub-agen dalam sesi CLI | `asyncio.gather` + `START_SUBAGENT` |

---

## 3.1 — Pengaturan SDK <span class="duration-badge">10 min</span>

### Prasyarat

- Python 3.11+
- Kunci API Gemini — tetapkan sebagai `GEMINI_API_KEY` atau teruskan melalui `api_key=` di konfigurasi

### Instalasi

```bash
python -m venv .venv
source .venv/bin/activate
pip install google-antigravity
```

### Verifikasi

```python
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy
print("google-antigravity installed ✅")
```

> **Kunci API vs Vertex AI:** Untuk pengembangan lokal yang cepat, gunakan `api_key="AIza..."` di
> `LocalAgentConfig`. Untuk produksi di GCP, autentikasi dengan
> `gcloud auth application-default login` — pustaka akan mengambil ADC secara otomatis.

---

## 3.2 — Primitif Inti: Agen, Konfigurasi, Alat <span class="duration-badge">20 mnt</span>

SDK `google-antigravity` memiliki tiga blok penyusun: `Agent`, `LocalAgentConfig`, dan alat (fungsi Python biasa). Pelajari ini dan Anda dapat membangun apa saja.

### Alat

Alat adalah **fungsi Python biasa**. Tanpa kelas pembungkus, tanpa dekorator. Agen memutuskan kapan harus memanggilnya berdasarkan docstring — itulah keseluruhan kontrak antarmuka.

```python
def get_file_contents(file_path: str) -> str:
    """Read and return the contents of a file at the given path.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        The file contents as a string, or an error message if not found.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
```

> **Aturan penting untuk alat:**
>
> - Gunakan anotasi tipe eksplisit — `str`, `int`, `bool`, `list[str]`. Jangan gunakan `typing.Optional`.
> - Gunakan nilai default `None` untuk parameter opsional: `param: str = None`
> - Docstring adalah skema alat — model membacanya untuk memutuskan kapan dan bagaimana memanggil alat tersebut. Tulis ini untuk model, bukan untuk manusia.
> - Jaga agar alat tetap sempit dan fokus. Satu pekerjaan per alat.

### Alat dengan Status Sesi

Untuk membaca/menulis **status sesi** di dalam alat, deklarasikan parameter dengan tipe `ToolContext`.
SDK mendeteksinya secara otomatis, menyuntikkannya pada saat pemanggilan, dan **menghapusnya dari skema yang ditampilkan ke model**:

```python
from google.antigravity.tools.tool_context import ToolContext

def record_finding(
    severity: str,
    message: str,
    ctx: ToolContext,
) -> dict:
    """Records a review finding into session state.

    Args:
        severity: One of 'critical', 'warning', 'info'.
        message: Description of the finding.

    Returns:
        Confirmation dict with the finding index.
    """
    findings = ctx.get_state("findings", [])
    findings.append({"severity": severity, "message": message})
    ctx.set_state("findings", findings)
    return {"status": "recorded", "index": len(findings) - 1}
```

### Agen + Konfigurasi

`Agent` adalah titik masuk tunggal. Semua konfigurasi masuk ke dalam `LocalAgentConfig`:

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

config = LocalAgentConfig(
    model="gemini-3.5-flash",
    system_instructions="""You are a code reviewer specialising in Python.
When given a file path, read the file and provide a structured review covering:
- Correctness and edge cases
- Code style and readability
- Security concerns
- Suggested improvements

Always read the file first before commenting. Be specific — cite line numbers.
""",
    tools=[get_file_contents, record_finding],
    policies=[policy.allow_all()],          # autonomous — no interactive prompts
    workspaces=["/path/to/project"],        # file ops scoped to this directory
)

async def main():
    async with Agent(config) as agent:
        response = await agent.chat("Review src/auth/login.py")
        print(await response.text())

asyncio.run(main())
```

> **`async with Agent(config) as agent:`** — selalu gunakan manajer konteks. Ini memulai jembatan runtime Go (`bin/localharness`) dan menghentikannya dengan bersih saat keluar.

### Pemilihan Model

Sesuaikan model dengan pekerjaannya. Kebijakan sadar biaya:

| Peran | Model | Alasan |
| :-- | :-- | :-- |
| Tugas umum, tinjauan kode | `gemini-3.5-flash` | Default SDK — hemat biaya, cepat |
| Orkestrasi, perutean, perencanaan | `gemini-3.1-pro-preview` | Penalaran kompleks, keputusan multi-langkah |
| Tugas pembuatan gambar | `gemini-3.1-flash-image-preview` | Default SDK untuk pembuatan gambar |
| Analisis berisiko tinggi | `gemini-3.1-pro-preview` dengan `ThinkingLevel.HIGH` | Penalaran mendalam untuk kepatuhan/keamanan |

> **Jangan pernah gunakan** `gemini-1.5-flash`, `gemini-1.5-pro`. Sudah usang.

### Skill

Skill adalah file `SKILL.md` yang dimuat pada saat runtime untuk menyuntikkan pengetahuan domain. Jaga agar prompt sistem Anda tetap ringkas — muat keahlian dari file:

```python
from pathlib import Path
import re

def load_skill(skill_name: str) -> str:
    """Load a SKILL.md and strip YAML frontmatter."""
    skill_path = Path("skills") / skill_name / "SKILL.md"
    if skill_path.exists():
        content = skill_path.read_text(encoding="utf-8")
        return re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL).strip()
    return ""

review_guidelines = load_skill("python-review")

config = LocalAgentConfig(
    model="gemini-3.5-flash",
    system_instructions=f"""You are a code reviewer.

## Review Guidelines
{review_guidelines}
""",
    tools=[get_file_contents],
    policies=[policy.allow_all()],
)
```

Skill juga dapat dimuat secara native melalui `LocalAgentConfig(skills_paths=["/path/to/skills/"])` — SDK menemukan file `SKILL.md` secara otomatis.

---

## 3.3 — Kebijakan dan Keamanan <span class="duration-badge">10 min</span>

**Kebijakan adalah hal pertama yang Anda konfigurasikan** — ini mengontrol apa yang diizinkan untuk dilakukan oleh agen tanpa persetujuan manusia. Setiap `LocalAgentConfig` membutuhkan daftar `policies=`:

```python
from google.antigravity.hooks import policy

# Fully autonomous — approve all tool calls (use for trusted, sandboxed agents)
policies=[policy.allow_all()]

# Default behaviour — ask user before running shell commands, allow everything else
policies=[policy.confirm_run_command()]

# Fine-grained rules (evaluated in order, first match wins)
async def approval_handler(tool_call) -> bool:
    answer = input(f"Allow {tool_call.name}? [y/N]: ")
    return answer.lower() == "y"

policies=[
    policy.deny("run_command"),                 # never run shell commands
    policy.allow("view_file"),                  # always allow reading
    policy.ask_user("edit_file", handler=approval_handler),  # ask before every write
    policy.allow("*"),                          # allow everything else
]

# Conditional deny — block dangerous patterns
policy.deny("run_command", when=lambda args: "rm -rf" in args.get("CommandLine", ""))

# Scope file operations to a specific directory
policy.workspace_only(["/path/to/project"])
```

> **Urutan prioritas:** `specific_deny` > `specific_ask` > `specific_allow` > `wildcard_deny` > `wildcard_ask` > `wildcard_allow`

---

## 3.4 — Hook: Observabilitas dan Kontrol <span class="duration-badge">10 min</span>

Hook memungkinkan Anda mencegat dan bereaksi terhadap setiap peristiwa dalam siklus hidup agen — untuk pencatatan, audit, pagar pengaman, atau alur persetujuan kustom:

```python
from google.antigravity.hooks import hooks
from google.antigravity.types import ToolCall, ToolResult, HookResult

# Block dangerous tool calls BEFORE they execute
@hooks.pre_tool_call_decide
async def security_guard(tool_call: ToolCall) -> HookResult:
    if tool_call.name == "run_command":
        cmd = tool_call.args.get("CommandLine", "")
        if any(danger in cmd for danger in ["rm -rf", "drop table", "DELETE FROM"]):
            return HookResult(allow=False)
    return HookResult(allow=True)

# Log all tool completions (non-blocking, read-only)
@hooks.post_tool_call
async def audit_logger(tool_result: ToolResult) -> None:
    print(f"[AUDIT] tool={tool_result.name} ok={tool_result.error is None}")

# Initialise state when a session begins
@hooks.on_session_start
async def initialise_state() -> None:
    print("[AGENT] Session started — ready.")

config = LocalAgentConfig(
    hooks=[security_guard, audit_logger, initialise_state],
    policies=[policy.allow_all()],
    model="gemini-3.5-flash",
    system_instructions="You are a code reviewer.",
    tools=[get_file_contents],
)
```

**Jenis-jenis hook:**

| Hook | Memblokir eksekusi | Memodifikasi data | Digunakan untuk |
| :-- | :-- | :-- | :-- |
| `@hooks.pre_tool_call_decide` | Ya | Tidak | Menyetujui/menolak pemanggilan alat |
| `@hooks.post_tool_call` | Tidak | Tidak | Pencatatan, metrik |
| `@hooks.pre_turn` | Tidak | Tidak | Pencatatan tingkat giliran |
| `@hooks.post_turn` | Tidak | Tidak | Pencatatan respons |
| `@hooks.on_session_start/end` | Tidak | Tidak | Pengaturan/pembongkaran |
| `@hooks.on_tool_error` | Ya | Ya | Pemulihan kesalahan |

---

## 3.5 — Orkestrasi Multi-Agen <span class="duration-badge">15 menit</span>

`google-antigravity` tidak memiliki kelas `SequentialAgent` atau `ParallelAgent`. Multi-agen dilakukan dengan dua cara: **digerakkan oleh model** (biarkan agen memunculkan sub-agen) atau **digerakkan oleh Python** (Anda mengorkestrasi instans `Agent` secara langsung).

### Pola A — Sub-agen Digerakkan oleh Model

Aktifkan `START_SUBAGENT` dalam kapabilitas. Model memanggilnya ketika memutuskan untuk mendelegasikan:

```python
from google.antigravity.types import BuiltinTools, CapabilitiesConfig

config = LocalAgentConfig(
    capabilities=CapabilitiesConfig(
        enable_subagents=True,
        enabled_tools=BuiltinTools.all_tools(),
    ),
    policies=[policy.allow_all()],
    model="gemini-3.1-pro-preview",
    system_instructions="""You are an engineering lead.
For complex tasks, spawn focused subagents to handle each part in parallel.
Synthesise their outputs into a final summary.""",
)
```

### Pola B — Pipeline Sekuensial (Digerakkan oleh Python)

Teruskan output dari satu agen sebagai input ke agen berikutnya:

```python
async def sequential_review(file_path: str):
    # Step 1 — read and summarise the file
    async with Agent(reader_config) as reader:
        r1 = await reader.chat(f"Read and summarise {file_path}")
        summary = await r1.text()

    # Step 2 — security audit using the summary
    async with Agent(security_config) as auditor:
        r2 = await auditor.chat(f"Security audit this code summary:\n\n{summary}")
        report = await r2.text()

    return report
```

### Pola C — Analisis Paralel

Jalankan agen independen secara bersamaan dengan `asyncio.gather`:

```python
async def parallel_analysis(file_path: str):
    async with (
        Agent(security_config) as security_agent,
        Agent(style_config)    as style_agent,
        Agent(perf_config)     as perf_agent,
    ):
        results = await asyncio.gather(
            security_agent.chat(f"Security review: {file_path}"),
            style_agent.chat(f"Style review: {file_path}"),
            perf_agent.chat(f"Performance review: {file_path}"),
        )
        texts = await asyncio.gather(*[r.text() for r in results])

    return {
        "security": texts[0],
        "style":    texts[1],
        "perf":     texts[2],
    }
```

> **Kapan menggunakan paralel:** Kapan pun Anda memiliki N analisis independen. Ini memangkas waktu nyata sebesar 60–80% dibandingkan dengan menjalankannya secara sekuensial.

---

## 3.6 — Streaming dan Output Terstruktur <span class="duration-badge">5 min</span>

### Respons Streaming

```python
async with Agent(config) as agent:
    response = await agent.chat("Write a detailed security report...")

    # Stream text deltas as they arrive
    async for delta in response:
        print(delta, end="", flush=True)

    # Stream reasoning/thinking (if thinking enabled)
    async for thought in response.thoughts:
        print(f"[thinking] {thought}")
```

### Output Terstruktur

Ikat output agen ke skema Pydantic:

```python
import asyncio
import pydantic
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

class ReviewResult(pydantic.BaseModel):
    issues: list[str]
    severity: str          # 'critical' | 'warning' | 'info'
    recommendation: str

config = LocalAgentConfig(
    response_schema=ReviewResult,
    system_instructions="Analyse the code and return structured output via the finish tool.",
    policies=[policy.allow_all()],
    model="gemini-3.5-flash",
    tools=[get_file_contents],
)

async def main():
    async with Agent(config) as agent:
        response = await agent.chat("Review src/auth/login.py")
        result = await response.structured_output()   # dict matching ReviewResult schema
        print(result["severity"], result["issues"])

asyncio.run(main())
```

---

## 3.7 — Melanjutkan Sesi dan Persistensi <span class="duration-badge">5 min</span>

```python
# First session — save the conversation ID
async with Agent(config) as agent:
    await agent.chat("Analyse this codebase and build a mental model.")
    conv_id = agent.conversation_id   # persist this

# Later session — resume exactly where you left off
resume_config = LocalAgentConfig(
    conversation_id=conv_id,
    save_dir="/path/where/first/session/was/saved",
    model="gemini-3.5-flash",
    policies=[policy.allow_all()],
)
async with Agent(resume_config) as agent:
    await agent.chat("Now suggest the top 3 refactoring priorities.")
```

---

## 3.8 — Pemicu: Agen Latar Belakang Otonom <span class="duration-badge">5 menit</span>

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy
from google.antigravity.triggers import every, on_file_change, TriggerContext

# Poll every 60 seconds
async def check_for_new_issues(ctx: TriggerContext) -> None:
    await ctx.send("Scan the repo for any new TODO comments added since last run.")

# React to file changes
async def on_code_change(ctx: TriggerContext, changes) -> None:
    paths = [c.path for c in changes]
    await ctx.send(f"Files changed: {paths}. Run quick security check.")

config = LocalAgentConfig(
    triggers=[
        every(60.0, check_for_new_issues),
        on_file_change("/path/to/src", on_code_change),
    ],
    policies=[policy.allow_all()],
    model="gemini-3.5-flash",
    system_instructions="You are a background code monitor.",
)

async def main():
    # The agent runs indefinitely, responding to triggers
    async with Agent(config) as agent:
        await asyncio.Event().wait()  # keep alive

asyncio.run(main())
```

---

## 3.9 — Konvensi Struktur Proyek <span class="duration-badge">5 min</span>

Strukturkan proyek agen Anda untuk kemudahan pemeliharaan:

```text
my_agent/
├── main.py                   # entry point — asyncio.run(main())
├── config.py                 # LocalAgentConfig construction
├── tools/
│   ├── __init__.py
│   ├── file_reader.py        # one tool per file
│   └── search_tool.py
├── hooks/
│   ├── __init__.py
│   └── security_guard.py     # pre_tool_call_decide hooks
├── skills/
│   └── domain-expertise/
│       └── SKILL.md          # portable skill packs
├── tests/
│   ├── test_file_reader.py
│   └── test_search_tool.py
├── requirements.txt          # google-antigravity + deps
└── README.md
```

### Penerapan ke Cloud Run

Terapkan sebagai aplikasi asinkronus Python standar:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
gcloud run deploy my-code-reviewer \
  --source . \
  --project $GOOGLE_CLOUD_PROJECT \
  --region $GOOGLE_CLOUD_REGION \
  --allow-unauthenticated
```

> **Tips:** Tetapkan `GOOGLE_CLOUD_PROJECT` dan `GOOGLE_CLOUD_REGION` (misalnya `us-central1`) sebelum menjalankan.

---

## Latihan Praktik

<div class="exercise-card" markdown>

### :material-code-braces: Latihan 10: Agen AGY Pertama Anda

**Berkas:** [`ex10_first_agent.md`](exercises/ex10_first_agent.md)  
**Durasi:** 45 menit  
**Bangun:** Sebuah **Agen Tinjauan Kode** yang membaca berkas, mengidentifikasi masalah, dan menghasilkan laporan tinjauan terstruktur.

**Apa yang akan Anda implementasikan:**

1. Tentukan 3 alat: `read_file`, `list_directory`, `record_finding` (dengan `ToolContext`)
2. Tulis prompt sistem dengan rubrik tinjauan (dimuat dari sebuah `SKILL.md`)
3. Konfigurasikan `LocalAgentConfig` dengan `policy.allow_all()` dan `CapabilitiesConfig`
4. Tambahkan penjaga keamanan `@hooks.pre_tool_call_decide`
5. Jalankan dengan keluaran streaming dan skema Pydantic `ReviewResult` terstruktur

</div>

<div class="exercise-card" markdown>

### :material-graph: Latihan 11: Pipeline Multi-Agen

**Berkas:** [`ex11_multi_agent_pipeline.md`](exercises/ex11_multi_agent_pipeline.md)  
**Durasi:** 45 menit  
**Bangun:** Sebuah **Pipeline Tulis-lalu-Audit** — agen Penulis Teknis menghasilkan dokumen, kemudian Analis Kepatuhan mengauditnya untuk celah GDPR.

**Apa yang akan Anda implementasikan:**

1. Bangun agen `technical_writer` dengan SKILL.md GDPR yang dimuat melalui `skills_paths`
2. Bangun agen `compliance_analyst` dengan `response_schema=ComplianceReport`
3. Hubungkan secara berurutan: keluaran dari penulis diteruskan sebagai masukan ke analis
4. Tambahkan varian paralel menggunakan `asyncio.gather` untuk draf + pemeriksaan hukum secara bersamaan
5. Tambahkan pelanjutan sesi: analis membaca `conversation_id` penulis untuk memuat konteks
6. Terapkan ke Cloud Run sebagai `my-pipeline` menggunakan `gcloud run deploy`

</div>

---

## Ringkasan: Blok Pembangun SDK

| Primitif | Apa yang Dilakukannya | Kapan Digunakan |
| :-- | :-- | :-- |
| `Agent` | Agen LLM tunggal dengan alat, hook, kebijakan | Inti — setiap agen dimulai di sini |
| `LocalAgentConfig` | Semua konfigurasi di satu tempat (model, alat, kebijakan, hook) | Selalu |
| `tools=[fn]` | Callable Python biasa, docstring adalah skemanya | Operasi eksternal apa pun |
| `ToolContext` | Baca/tulis status yang disuntikkan ke dalam alat | Alat stateful dalam pipeline |
| `policy.allow_all()` | Menyetujui semua panggilan alat secara otonom | Agen yang tepercaya dan di-sandbox |
| `policy.deny("run_command")` | Memblokir jenis alat tertentu | Pagar pengaman keselamatan |
| `@hooks.pre_tool_call_decide` | Memblokir/menyetujui panggilan alat sebelum eksekusi | Penjaga keamanan |
| `@hooks.post_tool_call` | Mengamati panggilan alat yang selesai | Pencatatan audit |
| `response_schema=` | Mengikat output ke skema Pydantic | Ekstraksi data terstruktur |
| `async for delta in response:` | Melakukan streaming teks saat tiba | Pembuatan bentuk panjang |
| `asyncio.gather(...)` | Menjalankan agen secara paralel | Analisis independen |
| `every(60, handler)` | Memicu agen pada interval | Monitor latar belakang |
| `on_file_change(path, fn)` | Memicu agen pada peristiwa sistem file | Pengamat kode langsung |
| `skills_paths=[...]` | Memuat file SKILL.md pada saat runtime | Keahlian domain portabel |
| `conversation_id=` | Melanjutkan sesi sebelumnya | Alur kerja multi-sesi |

---

## Langkah Selanjutnya

→ Lanjutkan ke **[Modul 4: Multi-Agen & Pola Lanjutan](multi-agent-advanced.md)**

→ Referensi: **[Lembar Contekan](cheatsheet.md)** — semua perintah di satu tempat
