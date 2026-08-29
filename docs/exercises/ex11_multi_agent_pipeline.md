# Exercise 11: Multi-Agent Pipeline

> **Duration:** 45 min | **Module:** 3 — Building AGY Agents

---

## Objective

Build a **Write-then-Audit Pipeline** — a Technical Writer agent produces a privacy policy document, then a Compliance Analyst agent audits it for GDPR gaps. You'll wire them sequentially, add a parallel variant, implement session resume, and deploy to Cloud Run.

---

## Setup

```bash
# Create project directory
mkdir -p ~/agy-pipeline/skills/gdpr-expertise ~/agy-pipeline/tools

# Set up Python environment
cd ~/agy-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install google-antigravity pydantic
```

```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## Part 1: Build the Technical Writer Agent (10 min)

Create the GDPR skill that the writer will use. Create `skills/gdpr-expertise/SKILL.md`:

```text
---
name: gdpr-expertise
description: GDPR compliance requirements for technical documentation
---

## GDPR Documentation Requirements

When writing privacy-related documentation, ensure coverage of:

### Data Subject Rights (Articles 12-23)
- Right to access (Art. 15)
- Right to rectification (Art. 16)
- Right to erasure / "right to be forgotten" (Art. 17)
- Right to restrict processing (Art. 18)
- Right to data portability (Art. 20)
- Right to object (Art. 21)

### Lawful Basis for Processing (Article 6)
- Consent, contract, legal obligation, vital interests, public task, legitimate interests
- Each processing activity must cite its lawful basis

### Data Protection by Design (Article 25)
- Privacy by default
- Data minimisation
- Purpose limitation
- Storage limitation

### International Transfers (Chapter V)
- Adequacy decisions
- Standard contractual clauses (SCCs)
- Binding corporate rules

### Data Breach Notification (Articles 33-34)
- 72-hour notification to supervisory authority
- Communication to data subjects for high-risk breaches

### Data Protection Impact Assessment (Article 35)
- Required for high-risk processing
- Must be conducted before processing begins
```

Create `writer_agent.py`:

```python
from google.antigravity import LocalAgentConfig
from google.antigravity.hooks import policy

# Specify save_dir so trajectory history is persisted across sessions
SESSION_DIR = ".sessions"

writer_config = LocalAgentConfig(
    model="gemini-3.7-flash",
    save_dir=SESSION_DIR,
    skills_paths=["skills/"],
    system_instructions="""You are a Technical Writer specialising in privacy documentation.

Your job: produce a comprehensive privacy policy document for a SaaS application.

Requirements:
- Use the GDPR expertise skill for compliance requirements
- Structure the document with clear sections and headers
- Include specific data categories, retention periods, and legal bases
- Write in plain language accessible to non-lawyers
- Include placeholders marked [COMPANY_NAME] and [DPO_EMAIL] for customisation

Output a complete, ready-to-review privacy policy document.
""",
    tools=[],
    policies=[policy.allow_all()],
)
```

> **Key concept:** `skills_paths=["skills/"]` tells the SDK to auto-discover all `SKILL.md` files under that directory. The writer agent gets the GDPR skill injected automatically.

---

## Part 2: Build the Compliance Analyst Agent (10 min)

Create `analyst_agent.py`:

```python
import pydantic
from google.antigravity import LocalAgentConfig
from google.antigravity.hooks import policy


class GDPRGap(pydantic.BaseModel):
    article: str          # e.g. "Article 17"
    requirement: str      # What GDPR requires
    gap: str              # What's missing or incomplete
    severity: str         # 'critical', 'major', 'minor'
    recommendation: str   # How to fix it


class ComplianceReport(pydantic.BaseModel):
    overall_score: int           # 0-100
    overall_assessment: str      # 'compliant', 'needs-work', 'non-compliant'
    gaps: list[GDPRGap]
    strengths: list[str]
    summary: str


analyst_config = LocalAgentConfig(
    model="gemini-3.7-flash",
    response_schema=ComplianceReport,
    system_instructions="""You are a GDPR Compliance Analyst.

Your job: audit a privacy policy document for GDPR compliance gaps.

Evaluation criteria:
1. Coverage of all Data Subject Rights (Articles 12-23)
2. Lawful basis specified for each processing activity (Article 6)
3. Data Protection by Design principles (Article 25)
4. International transfer safeguards (Chapter V)
5. Breach notification procedures (Articles 33-34)
6. DPIA provisions (Article 35)
7. DPO contact information (Article 37)
8. Clear, plain language (Article 12)

Severity classification:
- critical: Missing mandatory GDPR requirement, regulatory risk
- major: Incomplete coverage, ambiguous language on key rights
- minor: Style improvements, additional detail recommended

Be thorough and cite specific GDPR articles for every gap found.
Return your findings as structured output.
""",
    tools=[],
    policies=[policy.allow_all()],
)
```

---

## Part 3: Wire the Sequential Pipeline (10 min)

Create `main.py`:

```python
import asyncio
import json

from google.antigravity import Agent

from writer_agent import writer_config
from analyst_agent import analyst_config


async def sequential_pipeline():
    """Run writer → analyst in sequence. Output of writer feeds into analyst."""

    print("=" * 60)
    print("PHASE 1: Technical Writer — drafting privacy policy")
    print("=" * 60)

    # Step 1 — Writer produces the document
    async with Agent(writer_config) as writer:
        response = await writer.chat(
            "Write a comprehensive privacy policy for a B2B SaaS application "
            "that processes employee HR data, uses cloud infrastructure in the EU "
            "and US, and integrates with third-party payroll providers."
        )
        privacy_policy = await response.text()
        writer_conv_id = writer.conversation_id  # save for session resume

    print(privacy_policy[:500] + "...\n")

    print("=" * 60)
    print("PHASE 2: Compliance Analyst — auditing for GDPR gaps")
    print("=" * 60)

    # Step 2 — Analyst audits the writer's output
    async with Agent(analyst_config) as analyst:
        response = await analyst.chat(
            f"Audit the following privacy policy for GDPR compliance gaps:\n\n"
            f"{privacy_policy}"
        )
        report = await response.structured_output()

    # Print the structured report
    print(f"\nOverall Score: {report['overall_score']}/100")
    print(f"Assessment: {report['overall_assessment']}")
    print(f"\nStrengths ({len(report['strengths'])}):")
    for s in report["strengths"]:
        print(f"  ✅ {s}")

    print(f"\nGaps ({len(report['gaps'])}):")
    for gap in report["gaps"]:
        icon = {"critical": "🔴", "major": "🟡", "minor": "🔵"}.get(gap["severity"], "⚪")
        print(f"  {icon} [{gap['severity']}] {gap['article']}: {gap['gap']}")
        print(f"     → {gap['recommendation']}")

    print(f"\nSummary: {report['summary']}")

    return privacy_policy, report, writer_conv_id


if __name__ == "__main__":
    asyncio.run(sequential_pipeline())
```

### Run It

```bash
python main.py
```

---

## Part 4: Add a Parallel Variant (5 min)

Add a parallel analysis function to `main.py` that runs the writer and a legal reviewer simultaneously using `asyncio.gather`:

```python
from analyst_agent import analyst_config


async def parallel_pipeline():
    """Run writer and a parallel legal pre-check simultaneously."""

    # Create a second analyst config for a different perspective
    legal_config = analyst_config.model_copy(
        update={
            "system_instructions": """You are an EU Data Protection Lawyer.
Review the prompt describing a SaaS application and produce a pre-check
compliance report listing what a privacy policy MUST contain for this
specific use case. Return structured output.""",
        }
    )

    prompt = (
        "B2B SaaS application processing employee HR data, "
        "cloud infrastructure in EU and US, "
        "third-party payroll provider integrations."
    )

    print("Running writer + legal pre-check in parallel...\n")

    async with (
        Agent(writer_config) as writer,
        Agent(legal_config) as lawyer,
    ):
        writer_task = writer.chat(f"Write a privacy policy for: {prompt}")
        lawyer_task = lawyer.chat(f"What must a privacy policy contain for: {prompt}")

        results = await asyncio.gather(writer_task, lawyer_task)
        texts = await asyncio.gather(*[r.text() for r in results])

    privacy_policy, legal_checklist = texts
    print(f"Writer produced {len(privacy_policy)} chars")
    print(f"Lawyer produced {len(legal_checklist)} chars")

    # Now run the compliance analyst on the writer's output
    async with Agent(analyst_config) as analyst:
        response = await analyst.chat(
            f"Audit this privacy policy:\n\n{privacy_policy}\n\n"
            f"Also consider this legal pre-check:\n\n{legal_checklist}"
        )
        report = await response.structured_output()

    print(f"\nFinal Score: {report['overall_score']}/100")
    return report
```

> **When to use parallel:** Any time you have N independent analyses. Running the writer and legal pre-check simultaneously cuts wall-clock time by ~50%.

---

## Part 5: Add Session Resume (5 min)

Add a resume function to `main.py` that lets the analyst read the writer's prior conversation:

```python
async def resume_and_refine(writer_conv_id: str, original_report: dict):
    """Resume the writer's session and ask it to fix the gaps found by the analyst."""

    # Resume the writer's conversation — it remembers the full context
    resume_config = writer_config.model_copy(
        update={
            "conversation_id": writer_conv_id,
            "save_dir": SESSION_DIR,
        }
    )

    critical_gaps = [g for g in original_report["gaps"] if g["severity"] == "critical"]
    if not critical_gaps:
        print("No critical gaps found — no revision needed!")
        return

    gap_descriptions = "\n".join(
        f"- {g['article']}: {g['gap']} → {g['recommendation']}"
        for g in critical_gaps
    )

    print(f"\nResuming writer session to fix {len(critical_gaps)} critical gaps...")

    async with Agent(resume_config) as writer:
        response = await writer.chat(
            f"The compliance analyst found these critical GDPR gaps in your "
            f"privacy policy. Please revise the document to address them:\n\n"
            f"{gap_descriptions}"
        )
        revised_policy = await response.text()

    print("Revised policy generated. Running final audit...")

    # Re-audit the revised version
    async with Agent(analyst_config) as analyst:
        response = await analyst.chat(
            f"Audit this REVISED privacy policy for GDPR compliance:\n\n"
            f"{revised_policy}"
        )
        final_report = await response.structured_output()

    print(f"Revised Score: {final_report['overall_score']}/100 "
          f"(was {original_report['overall_score']}/100)")
```

Update the `__main__` block:

```python
if __name__ == "__main__":
    policy_text, report, conv_id = asyncio.run(sequential_pipeline())
    asyncio.run(resume_and_refine(conv_id, report))
```

---

## Part 6: Deploy to Cloud Run (5 min)

Create `requirements.txt`:

```text
google-antigravity
pydantic
```

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Deploy:

```bash
gcloud run deploy my-pipeline \
  --source . \
  --project $GOOGLE_CLOUD_PROJECT \
  --region $GOOGLE_CLOUD_REGION \
  --allow-unauthenticated
```

> **Tip:** Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_REGION` (e.g. `us-central1`) before deploying. For production, remove `--allow-unauthenticated` and add proper IAM controls.

---

## Completion Criteria

- [ ] GDPR `SKILL.md` created and loaded by the writer agent via `skills_paths`
- [ ] `ComplianceReport` Pydantic schema defined with `GDPRGap` sub-model
- [ ] Sequential pipeline runs: writer output feeds into analyst input
- [ ] Analyst returns structured `ComplianceReport` with gaps, strengths, and score
- [ ] Parallel variant runs writer + legal pre-check simultaneously with `asyncio.gather`
- [ ] Session resume works: writer conversation resumed by `conversation_id` to fix gaps
- [ ] `Dockerfile` and `gcloud run deploy` command prepared for Cloud Run deployment
