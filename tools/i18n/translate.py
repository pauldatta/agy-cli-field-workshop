# /// script
# dependencies = [
#     "google-genai>=1.0.0",
#     "pyyaml>=6.0",
# ]
# ///
"""
translate.py — Antigravity Field Workshop Translation Pipeline.

Translates workshop markdown files using Google GenAI SDK (Gemini models)
while strictly preserving:
  1. YAML frontmatter
  2. Fenced code blocks and their code tags
  3. Admonitions, inline HTML tags, and markdown tables
  4. Relative file paths and URL links

Usage:
    uv run tools/i18n/translate.py docs/setup.md --lang ko
    uv run tools/i18n/translate.py --all --lang ko
    uv run tools/i18n/translate.py --all --langs ko,zh,id
"""

import argparse
import os
import pathlib
import re
import sys
import time
from typing import Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

LANG_MAP = {
    "ko": "Korean (한국어)",
    "zh": "Chinese (Simplified / 简体中文)",
    "id": "Indonesian (Bahasa Indonesia)",
    "ja": "Japanese (日本語)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
}

SYSTEM_INSTRUCTION = """\
You are an expert technical translator specializing in software developer documentation and cloud architecture.
Translate the provided markdown document accurately into the target language.

STRICT TRANSLATION RULES:
1. Maintain all markdown formatting, tables, headings, lists, and indentation.
2. DO NOT translate code blocks (```...```), terminal commands, command flags, or JSON/YAML contents.
3. DO NOT translate brand names, product names, or CLI commands: 'agy', 'gemini', 'Antigravity CLI', 'Gemini CLI', 'ADK', 'agents-cli', 'Vertex AI', 'Cloud Run', 'GCP', 'GitHub', 'Google Cloud'.
4. DO NOT translate slash commands (e.g., `/resume`, `/rewind`, `/diff`, `/btw`, `/goal`, `/schedule`, `/browser`, `/fast`).
5. DO NOT translate key combinations (e.g., `alt+j`, `ctrl+k`, `ctrl+o`, `shift+enter`).
6. DO NOT translate file paths (e.g., `~/.gemini/antigravity-cli/settings.json`, `.agents/mcp_config.json`, `docs/setup.md`).
7. Keep HTML tags, MkDocs admonitions (e.g. `> [!NOTE]`, `<div class="exercise-card">`), and mermaid diagrams intact.
8. Output ONLY the translated markdown content. Do NOT wrap the entire response in extra outer markdown code fences or add meta commentary.
"""

def get_client() -> Optional["genai.Client"]:
    if genai is None:
        return None
    # Support Vertex AI or Google AI Studio
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    if project:
        return genai.Client(vertexai=True, project=project, location=location)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    return None

def translate_content(client: "genai.Client", text: str, target_lang_name: str, model: str = "gemini-3.7-flash") -> str:
    prompt = f"Translate the following documentation into {target_lang_name}:\n\n{text}"
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
        ),
    )
    return response.text.strip()

def translate_file(src_path: pathlib.Path, lang: str, model: str = "gemini-3.7-flash", client: Optional["genai.Client"] = None):
    target_lang_name = LANG_MAP.get(lang, lang)
    repo_root = pathlib.Path.cwd()
    
    rel_path = src_path.relative_to(repo_root / "docs") if src_path.is_relative_to(repo_root / "docs") else src_path
    dest_path = repo_root / "docs" / lang / rel_path
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"📖 Translating {src_path} → docs/{lang}/{rel_path} ({target_lang_name})...")
    
    if client is None:
        print("  ⚠️  Google GenAI client not available (check GCP project or GEMINI_API_KEY)")
        return
        
    text = src_path.read_text(encoding="utf-8")
    try:
        translated = translate_content(client, text, target_lang_name, model=model)
        # Strip extraneous markdown wrap if model added it
        if translated.startswith("```markdown\n") and translated.endswith("\n```"):
            translated = translated[12:-4]
        dest_path.write_text(translated + "\n", encoding="utf-8")
        print(f"  ✅ Saved docs/{lang}/{rel_path}")
    except Exception as e:
        print(f"  ❌ Failed to translate {src_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Translate workshop markdown files.")
    parser.add_argument("file", nargs="?", help="Specific markdown file to translate")
    parser.add_argument("--all", action="store_true", help="Translate all docs")
    parser.add_argument("--lang", default="ko", help="Target language (ko, zh, id, etc.)")
    parser.add_argument("--langs", help="Comma-separated list of target languages")
    parser.add_argument("--model", default="gemini-3.7-flash", help="Gemini model to use")
    parser.add_argument("--parallel", type=int, default=4, help="Worker parallelism")
    parser.add_argument("--file-parallel", type=int, default=2, help="File parallelism")
    
    args = parser.parse_args()
    
    client = get_client()
    if client is None:
        print("⚠️  Warning: No Vertex AI or Gemini API credentials configured.")
        print("   Set GOOGLE_CLOUD_PROJECT or GEMINI_API_KEY before translating.")
    
    langs = [l.strip() for l in args.langs.split(",")] if args.langs else [args.lang]
    
    docs_dir = pathlib.Path("docs")
    if args.file:
        src_files = [pathlib.Path(args.file)]
    elif args.all:
        src_files = sorted([f for f in docs_dir.glob("*.md") if f.is_file()])
        # Also include exercises
        src_files.extend(sorted((docs_dir / "exercises").glob("*.md")))
    else:
        parser.print_help()
        sys.exit(1)
        
    for lang in langs:
        print(f"\n🌐 Starting translation for language: {lang}")
        for src in src_files:
            translate_file(src, lang, model=args.model, client=client)

if __name__ == "__main__":
    main()
