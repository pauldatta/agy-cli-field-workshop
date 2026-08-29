#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Pre-commit structural checks — mirrors CI (workshop-structural.yml)
# Run: bash scripts/precommit-checks.sh   or   make precommit
# ─────────────────────────────────────────────────────────────
set -euo pipefail

# Color helpers
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; NC='\033[0m'
pass() { echo -e "  ${GREEN}✅ $1${NC}"; }
fail() { echo -e "  ${RED}❌ $1${NC}"; }
warn() { echo -e "  ${YELLOW}⚠️  $1${NC}"; }

errors=0

# ─────────────────────────────────────────────────────────────
# 1. Required files
# ─────────────────────────────────────────────────────────────
echo "📋 Checking required files..."
for f in README.md mkdocs.yml docs/index.md \
         samples/configs/settings.json samples/configs/mcp.json \
         AUDIT.md CHANGELOG.md; do
  if [ -f "$f" ]; then
    pass "$f"
  else
    fail "Missing: $f"
    errors=$((errors + 1))
  fi
done

# ─────────────────────────────────────────────────────────────
# 2. JSON validation
# ─────────────────────────────────────────────────────────────
echo "📋 Validating JSON configs..."
for f in samples/configs/*.json; do
  if jq . "$f" > /dev/null 2>&1; then
    pass "$f — valid"
  else
    fail "$f — invalid JSON"
    errors=$((errors + 1))
  fi
done

# ─────────────────────────────────────────────────────────────
# 3. Shell script syntax
# ─────────────────────────────────────────────────────────────
echo "📋 Checking shell scripts..."
for f in scripts/*.sh samples/hooks/*.sh; do
  [ -f "$f" ] || continue
  if bash -n "$f" 2>/dev/null; then
    pass "$f"
  else
    fail "$f — syntax error"
    errors=$((errors + 1))
  fi
done

# ─────────────────────────────────────────────────────────────
# 4. Agent frontmatter
# ─────────────────────────────────────────────────────────────
echo "📋 Checking agent definitions..."
for f in samples/agents/*.md; do
  [ -f "$f" ] || continue
  if head -1 "$f" | grep -q '^---'; then
    pass "$f — frontmatter OK"
  else
    fail "$f — missing YAML frontmatter"
    errors=$((errors + 1))
  fi
done

# ─────────────────────────────────────────────────────────────
# 5. Stale 'gemini' binary references
# ─────────────────────────────────────────────────────────────
echo "📋 Checking for stale 'gemini' binary references..."
if grep -rqE '^\s*(gemini |`gemini )' docs/*.md 2>/dev/null; then
  fail "Found bare 'gemini' command calls — should be 'agy'"
  grep -rnoE '^\s*(gemini |`gemini )' docs/*.md | head -5
  errors=$((errors + 1))
else
  pass "No stale 'gemini' binary references"
fi

# ─────────────────────────────────────────────────────────────
# 6. Stale Gemini CLI hook event names
#    Excludes ex07 (migration walkthrough — intentional legacy content)
# ─────────────────────────────────────────────────────────────
echo "📋 Checking for stale hook event names..."
for stale in SessionStart BeforeTool AfterTool; do
  if grep -rq --exclude="ex07_migration_walkthrough.md" "\"${stale}\"" docs/ samples/ 2>/dev/null; then
    fail "Stale hook event '${stale}' found — use PreInvocation/PreToolUse/PostToolUse"
    grep -rn --exclude="ex07_migration_walkthrough.md" "\"${stale}\"" docs/ samples/ | head -5
    errors=$((errors + 1))
  fi
done
if [ "$errors" -eq 0 ] 2>/dev/null; then
  pass "All hook event names are AGY-correct"
fi

# ─────────────────────────────────────────────────────────────
# 7. Internal project references (must never appear in public docs)
# ─────────────────────────────────────────────────────────────
echo "📋 Checking for internal project references..."
PATTERNS="gpu-launchpad|paul-sdlc|googleplex|corp\.google|buganizer|google3|critique\.corp|piper\/"
if grep -rqE --exclude="precommit-checks.sh" "$PATTERNS" docs/ samples/ scripts/ *.md 2>/dev/null; then
  fail "Internal reference found — replace with generic placeholder"
  grep -rnoE --exclude="precommit-checks.sh" "$PATTERNS" docs/ samples/ scripts/ *.md 2>/dev/null | head -10
  errors=$((errors + 1))
else
  pass "No internal project references"
fi

# ─────────────────────────────────────────────────────────────
# 8. Markdown lint (if npx available)
# ─────────────────────────────────────────────────────────────
echo "📋 Running markdown lint..."
if command -v npx >/dev/null 2>&1; then
  if npx markdownlint-cli2 "docs/**/*.md" "README.md" 2>&1 | tail -3; then
    pass "Markdown lint passed"
  else
    fail "Markdown lint errors found"
    errors=$((errors + 1))
  fi
else
  warn "npx not found — skipping markdown lint"
fi

# ─────────────────────────────────────────────────────────────
# 9. Code block validation (if script exists)
# ─────────────────────────────────────────────────────────────
echo "📋 Validating code blocks..."
if [ -f scripts/validate-code-blocks.sh ]; then
  if bash scripts/validate-code-blocks.sh docs/ 2>&1 | tail -3; then
    pass "Code block validation passed"
  else
    fail "Code block validation errors"
    errors=$((errors + 1))
  fi
else
  warn "scripts/validate-code-blocks.sh not found — skipping"
fi

# ─────────────────────────────────────────────────────────────
# 10. Dual-copy exercise parity (docs/exercises/*.md ↔ exercises/*.md)
# ─────────────────────────────────────────────────────────────
echo "📋 Checking dual-copy exercise parity..."
dual_copy_errors=0
for doc_ex in docs/exercises/ex*.md; do
  [ -f "$doc_ex" ] || continue
  ex_base=$(basename "$doc_ex")
  root_ex="exercises/$ex_base"
  if [ ! -f "$root_ex" ]; then
    fail "Exercise '$doc_ex' has no matching copy at '$root_ex'"
    dual_copy_errors=$((dual_copy_errors + 1))
  elif ! diff -q "$doc_ex" "$root_ex" > /dev/null 2>&1; then
    fail "Exercise drift: '$doc_ex' and '$root_ex' differ"
    dual_copy_errors=$((dual_copy_errors + 1))
  fi
done
if [ "$dual_copy_errors" -eq 0 ]; then
  pass "All exercises in docs/exercises/ match root exercises/"
else
  errors=$((errors + dual_copy_errors))
fi

# ─────────────────────────────────────────────────────────────
# 11. SDK API & Runtime Integrity
# ─────────────────────────────────────────────────────────────
echo "📋 Checking SDK APIs and types..."
sdk_errors=0
if grep -rnE 'tool_result\.success|\.success\b.*ToolResult' docs/ 2>/dev/null; then
  fail "Detected invalid 'tool_result.success' — use 'tool_result.error is None'"
  sdk_errors=$((sdk_errors + 1))
fi
if grep -rnE 'HookResult\([^)]*message=' docs/ 2>/dev/null; then
  fail "Detected invalid 'HookResult(message=...)' — HookResult only accepts allow: bool"
  sdk_errors=$((sdk_errors + 1))
fi
if grep -rnE 'WRITE_TOOLS\s*=\s*\{[^}]*write_to_file' docs/ 2>/dev/null; then
  fail "Detected CLI tool name 'write_to_file' in SDK WRITE_TOOLS — use BuiltinTools.CREATE_FILE"
  sdk_errors=$((sdk_errors + 1))
fi
if [ "$sdk_errors" -eq 0 ]; then
  pass "SDK APIs, types, and constants compliant"
else
  errors=$((errors + sdk_errors))
fi

# ─────────────────────────────────────────────────────────────
# 12. CLI state directory paths
# ─────────────────────────────────────────────────────────────
echo "📋 Checking CLI state paths..."
if grep -rnE --exclude-dir="id" --exclude-dir="ko" --exclude-dir="zh" '~/\.gemini/antigravity/' docs/ 2>/dev/null; then
  fail "Detected legacy '~/.gemini/antigravity/' path in docs/ — use '~/.gemini/antigravity-cli/'"
  errors=$((errors + 1))
else
  pass "All CLI state directory paths use ~/.gemini/antigravity-cli/"
fi

# ─────────────────────────────────────────────────────────────
# 13. Keybinding integrity
# ─────────────────────────────────────────────────────────────
echo "📋 Checking keybindings..."
if grep -rnE 'ctrl\+j.*teleport|teleport.*ctrl\+j' docs/ 2>/dev/null; then
  fail "Detected stale 'ctrl+j' for subagent teleport — must be 'alt+j'"
  errors=$((errors + 1))
else
  pass "Subagent teleport keybinding verified as alt+j"
fi

# ─────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────
echo ""
if [ "$errors" -gt 0 ]; then
  echo -e "${RED}💥 $errors check(s) failed — fix before committing${NC}"
  exit 1
else
  echo -e "${GREEN}🎉 All pre-commit checks passed${NC}"
fi
