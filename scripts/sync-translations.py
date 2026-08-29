#!/usr/bin/env python3
"""
sync-translations.py — Synchronize common fixes, code blocks, and paths to translated docs.
"""
import pathlib
import re

DOCS_DIR = pathlib.Path("docs")
LANGS = ["ko", "zh", "id"]

def replace_in_file(path: pathlib.Path, patterns: list[tuple[str, str]]):
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    original = text
    for target, replacement in patterns:
        text = text.replace(target, replacement)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  Updated: {path}")

def sync_all():
    print("🔄 Synchronizing fixes across translated docs...")
    
    # 1. Global state path replacement
    for lang in LANGS:
        for md_file in (DOCS_DIR / lang).rglob("*.md"):
            replace_in_file(md_file, [
                ("~/.gemini/antigravity/", "~/.gemini/antigravity-cli/"),
                ("~/.gemini/antigravity ", "~/.gemini/antigravity-cli "),
                (".agents/mcp.json", ".agents/mcp_config.json"),
                ("samples/configs/mcp.json", "samples/configs/mcp_config.json"),
                ("gemini-3.1-flash-lite-preview", "gemini-3.7-flash"),
                ("gemini-3-flash-preview", "gemini-3.7-flash"),
            ])
            
    # 2. SDK fixes in agy-sdk.md
    sdk_patterns = [
        ("success={tool_result.success}", "ok={tool_result.error is None}"),
        ("f\"[AUDIT] tool={tool_result.name} success={tool_result.success}\"", "f\"[AUDIT] tool={tool_result.name} ok={tool_result.error is None}\""),
        ("return HookResult(allow=False, message=f\"Blocked dangerous command: {cmd}\")", "return HookResult(allow=False)"),
        ("return HookResult(allow=False, message=", "return HookResult(allow=False)  # "),
    ]
    for lang in LANGS:
        replace_in_file(DOCS_DIR / lang / "agy-sdk.md", sdk_patterns)

    # 3. ex10 fixes
    ex10_patterns = [
        ('WRITE_TOOLS = {"write_to_file", "edit_file", "replace_file_content", "run_command"}',
         'WRITE_TOOLS = {BuiltinTools.CREATE_FILE, BuiltinTools.EDIT_FILE, BuiltinTools.RUN_COMMAND}'),
        ('return HookResult(allow=False, message="Modifying .git/ is prohibited")',
         'return HookResult(allow=False)'),
        ('from google.antigravity.agent import ToolContext',
         'from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig, ToolContext, BuiltinTools, types, hooks, triggers'),
    ]
    for lang in LANGS:
        replace_in_file(DOCS_DIR / lang / "exercises" / "ex10_first_agent.md", ex10_patterns)

    # 4. ex11 session dir
    ex11_patterns = [
        ('writer_config = LocalAgentConfig(\n    agent_name="doc-writer",\n    capabilities=CapabilitiesConfig(allow_subagents=False),\n    model="gemini-3.7-flash",\n)',
         'SESSION_DIR = pathlib.Path("./.sessions")\nwriter_config = LocalAgentConfig(\n    agent_name="doc-writer",\n    capabilities=CapabilitiesConfig(allow_subagents=False),\n    model="gemini-3.7-flash",\n    save_dir=SESSION_DIR,\n)'),
    ]
    for lang in LANGS:
        replace_in_file(DOCS_DIR / lang / "exercises" / "ex11_multi_agent_pipeline.md", ex11_patterns)

    # 5. Keybindings (Alt+J / alt+j)
    keybinding_patterns = [
        ("`ctrl+j`를 사용하여", "`alt+j`를 사용하여"),
        ("`ctrl+j`로 텔레포트", "`alt+j`로 텔레포트"),
        ("`ctrl+j` 进行传送", "`alt+j` 进行传送"),
        ("`ctrl+j` 用于传送", "`alt+j` 用于传送"),
        ("`ctrl+j` untuk teleport", "`alt+j` untuk teleport"),
        ("`ctrl+j` (subagent teleport)", "`alt+j` (subagent teleport)"),
        ("`ctrl+j` (하위 에이전트 텔레포트)", "`alt+j` (하위 에이전트 텔레포트)"),
        ("`ctrl+j`（子代理传送）", "`alt+j`（子代理传送）"),
    ]
    for lang in LANGS:
        for md_file in (DOCS_DIR / lang).rglob("*.md"):
            replace_in_file(md_file, keybinding_patterns)

if __name__ == "__main__":
    sync_all()
