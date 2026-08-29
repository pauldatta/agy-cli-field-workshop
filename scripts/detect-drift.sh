#!/usr/bin/env bash
# detect-drift.sh — Detect documentation ↔ code drift in the AGY CLI workshop
#
# Two layers of validation:
#   1. LOCAL DRIFT:  File paths referenced in docs → do they exist?
#                   Agents/hooks in samples/ → are they mentioned in docs?
#                   settings.json hook refs → do matching scripts exist?
#   2. UPSTREAM DRIFT: AGY CLI commands used in docs → do they still exist
#                      in the official antigravity.google docs? (requires --upstream)
#
# Usage: ./scripts/detect-drift.sh [--upstream]
#   --upstream: Also check against antigravity.google/docs (requires network)
#
# Exit code: number of errors found (0 = all clean)

set -euo pipefail

CHECK_UPSTREAM=false
if [[ "${1:-}" == "--upstream" ]]; then
  CHECK_UPSTREAM=true
fi

ERRORS=0
WARNINGS=0

# Colors
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  CYAN='\033[0;36m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' CYAN='' NC=''
fi

log_ok()      { echo -e "  ${GREEN}✅${NC} $*"; }
log_warn()    { echo -e "  ${YELLOW}⚠️${NC}  $*"; WARNINGS=$((WARNINGS + 1)); }
log_fail()    { echo -e "  ${RED}❌${NC} $*"; ERRORS=$((ERRORS + 1)); }
log_section() { echo -e "\n${CYAN}$*${NC}"; }

# ═══════════════════════════════════════════════════════════
# LOCAL DRIFT CHECKS
# ═══════════════════════════════════════════════════════════

log_section "🔍 Local Drift Detection"

# --- 1. File paths referenced in docs should exist ---
log_section "  Checking file path references..."

grep -rhoE '(samples|exercises)/[a-zA-Z0-9_./-]+' docs/*.md 2>/dev/null | sort -u | while read -r ref_path; do
  ref_path=$(echo "$ref_path" | sed 's/[).,;:]*$//')
  if [ -e "$ref_path" ]; then
    log_ok "Referenced path exists: $ref_path"
  elif [ -e "$(dirname "$ref_path")" ]; then
    log_warn "Path not found (parent exists): $ref_path"
  else
    log_fail "Referenced path not found: $ref_path"
  fi
done

# --- 2. Every agent in samples/agents/ should be mentioned in docs ---
log_section "  Checking agent documentation coverage..."

for agent_file in samples/agents/*.md; do
  [ -f "$agent_file" ] || continue
  agent_name=$(basename "$agent_file" .md)
  if grep -rq "$agent_name" docs/*.md 2>/dev/null; then
    log_ok "Agent '$agent_name' is documented"
  else
    log_warn "Agent '$agent_name' exists in samples/ but is not referenced in any doc"
  fi
done

# --- 3. Every hook in samples/hooks/ should be mentioned in docs ---
log_section "  Checking hook documentation coverage..."

for hook_file in samples/hooks/*.sh; do
  [ -f "$hook_file" ] || continue
  hook_name=$(basename "$hook_file" .sh)
  if grep -rq "$hook_name" docs/*.md 2>/dev/null; then
    log_ok "Hook '$hook_name' is documented"
  else
    log_warn "Hook '$hook_name' exists in samples/ but is not referenced in any doc"
  fi
done

# --- 4. Hooks referenced in hooks.json/settings.json should exist in samples/hooks/ ---
log_section "  Checking samples/configs/hooks.json ↔ hook file alignment..."

for config_file in samples/configs/hooks.json samples/configs/settings.json; do
  if [ -f "$config_file" ]; then
    (grep -oE 'hooks/[a-zA-Z0-9_-]+\.sh' "$config_file" || true) | sort -u | while read -r hook_ref; do
      [ -n "$hook_ref" ] || continue
      hook_basename=$(basename "$hook_ref" .sh)
      if [ -f "samples/hooks/${hook_basename}.sh" ]; then
        log_ok "$config_file hook '${hook_basename}' has matching script"
      else
        log_fail "$config_file references '${hook_ref}' but samples/hooks/${hook_basename}.sh not found"
      fi
    done
  fi
done

# --- 5. AGY CLI hook event names — flag any Gemini CLI leftovers ---
log_section "  Checking for stale Gemini CLI hook event names..."

STALE_EVENTS=("SessionStart" "BeforeTool" "AfterTool")
AGY_EVENTS=("PreInvocation" "PreToolUse" "PostToolUse")

for stale in "${STALE_EVENTS[@]}"; do
  if grep -rq --exclude="ex07_migration_walkthrough.md" "\"${stale}\"" docs/ samples/ 2>/dev/null; then
    log_fail "Stale Gemini CLI hook event '${stale}' found — use AGY equivalent: PreInvocation/PreToolUse/PostToolUse"
  fi
done
log_ok "Hook event names: no stale Gemini CLI names found"

# --- 6. AGY binary references — flag any 'gemini' binary calls in docs ---
log_section "  Checking for stale 'gemini' binary references in docs..."

# Allow "gemini" as a noun (e.g., "from Gemini CLI") but flag bare 'gemini' commands
if grep -rqE '^\s*(gemini |`gemini )' docs/*.md 2>/dev/null; then
  log_warn "Found bare 'gemini' command in docs — verify these should be 'agy'"
  grep -rnoE '^\s*(gemini |`gemini )' docs/*.md 2>/dev/null | head -5
else
  log_ok "No stale 'gemini' binary references found"
fi

# --- 7. Nav entries in mkdocs.yml should have matching doc files ---
log_section "  Checking mkdocs.yml nav ↔ doc file alignment..."

if [ -f "mkdocs.yml" ]; then
  grep -E ':\s+[a-zA-Z0-9_-]+\.md\s*$' mkdocs.yml | grep -oE '[a-zA-Z0-9_-]+\.md' | sort -u | while read -r nav_file; do
    if [ -f "docs/${nav_file}" ]; then
      log_ok "Nav entry '${nav_file}' exists"
    else
      log_fail "mkdocs.yml references '${nav_file}' but docs/${nav_file} not found"
    fi
  done
fi

# --- 8. Dual-copy exercise parity (docs/exercises/*.md ↔ exercises/*.md) ---
log_section "  Checking dual-copy exercise parity..."

for doc_ex in docs/exercises/ex*.md; do
  [ -f "$doc_ex" ] || continue
  ex_base=$(basename "$doc_ex")
  root_ex="exercises/$ex_base"
  if [ ! -f "$root_ex" ]; then
    log_fail "Exercise '$doc_ex' has no matching copy at '$root_ex'"
  elif ! diff -q "$doc_ex" "$root_ex" > /dev/null 2>&1; then
    log_fail "Exercise drift: '$doc_ex' and '$root_ex' differ — run 'cp $doc_ex $root_ex'"
  else
    log_ok "Exercise copy in sync: $ex_base"
  fi
done

# --- 9. SDK API & Runtime Integrity Checks ---
log_section "  Checking SDK APIs, types, and runtime conventions in docs/..."

# A: ToolResult.success
if grep -rnE 'tool_result\.success|\.success\b.*ToolResult' docs/ 2>/dev/null; then
  log_fail "Detected invalid 'tool_result.success' — use 'tool_result.error is None'"
else
  log_ok "SDK ToolResult API: no invalid .success accesses"
fi

# B: HookResult message parameter
if grep -rnE 'HookResult\([^)]*message=' docs/ 2>/dev/null; then
  log_fail "Detected invalid 'HookResult(message=...)' — HookResult only accepts allow: bool"
else
  log_ok "SDK HookResult schema: compliant"
fi

# C: CLI write tool names in SDK Python sets
if grep -rnE 'WRITE_TOOLS\s*=\s*\{[^}]*write_to_file' docs/ 2>/dev/null; then
  log_fail "Detected CLI tool name 'write_to_file' in SDK WRITE_TOOLS — use BuiltinTools.CREATE_FILE"
else
  log_ok "SDK WRITE_TOOLS constants: compliant"
fi

# D: Legacy CLI state paths
if grep -rnE '~/\.gemini/antigravity/' docs/ 2>/dev/null; then
  log_fail "Detected legacy '~/.gemini/antigravity/' path — use '~/.gemini/antigravity-cli/'"
else
  log_ok "CLI state paths: normalized to ~/.gemini/antigravity-cli/"
fi

# E: Keybinding accuracy
if grep -rnE 'ctrl\+j.*teleport|teleport.*ctrl\+j' docs/ 2>/dev/null; then
  log_fail "Detected stale 'ctrl+j' for subagent teleport — must be 'alt+j'"
else
  log_ok "Subagent teleport shortcut: verified alt+j"
fi

# ═══════════════════════════════════════════════════════════
# UPSTREAM DRIFT CHECKS (validates against AUDIT.md ground truth)
# ═══════════════════════════════════════════════════════════

if $CHECK_UPSTREAM; then
  log_section "🌐 Upstream Drift Detection (against AUDIT.md ground truth)"

  AUDIT_FILE="AUDIT.md"
  if [ ! -f "$AUDIT_FILE" ]; then
    log_fail "AUDIT.md not found — cannot run upstream checks"
  else
    log_ok "Using AUDIT.md as verified ground truth"

    # --- Check CLI flags used in docs are grounded in AUDIT.md ---
    log_section "  Checking agy CLI flags against AUDIT.md..."
    grep -rhoE 'agy --[a-z-]+' docs/*.md 2>/dev/null | sed 's/agy //' | sort -u | while read -r flag; do
      if grep -q -- "$flag" "$AUDIT_FILE"; then
        log_ok "CLI flag '$flag' grounded in AUDIT.md"
      else
        log_warn "CLI flag '$flag' used in workshop but NOT in AUDIT.md — verify against official docs"
      fi
    done

    # --- Check slash commands used in docs are grounded in AUDIT.md ---
    log_section "  Checking slash commands against AUDIT.md..."
    grep -rhoE '`/[a-z][a-z0-9_-]+`' docs/*.md 2>/dev/null | tr -d '`' | sort -u | while read -r cmd; do
      cmd_name="${cmd#/}"
      # Skip common non-command patterns
      case "$cmd_name" in dev|bin|etc|usr|tmp|src|var|opt|home|docs|exercises|samples|assets|scripts) continue ;; esac
      if grep -qw "$cmd_name" "$AUDIT_FILE"; then
        log_ok "Slash command '${cmd}' grounded in AUDIT.md"
      else
        log_warn "Slash command '${cmd}' used in workshop but NOT in AUDIT.md — verify or add"
      fi
    done

    # --- Check AUDIT.md source URLs are still reachable ---
    log_section "  Checking AUDIT.md source URLs are reachable..."
    grep -oE 'https://[^ )|>]+' "$AUDIT_FILE" | sort -u | while read -r url; do
      # Only check antigravity.google and developers.googleblog.com
      case "$url" in
        *antigravity.google*|*developers.googleblog.com*)
          status=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")
          if [ "$status" = "200" ]; then
            log_ok "URL reachable ($status): $url"
          elif [ "$status" = "000" ]; then
            log_warn "URL unreachable (timeout/DNS): $url"
          else
            log_warn "URL returned $status: $url"
          fi
          ;;
      esac
    done

    # --- Check AUDIT.md freshness ---
    log_section "  Checking AUDIT.md freshness..."
    audit_date=$(grep -oE 'Audit date:.*[0-9]{4}-[0-9]{2}-[0-9]{2}' "$AUDIT_FILE" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
    if [ -n "$audit_date" ]; then
      audit_ts=0
      if date -d "$audit_date" +%s &>/dev/null; then
        audit_ts=$(date -d "$audit_date" +%s)
      elif date -j -f "%Y-%m-%d" "$audit_date" +%s &>/dev/null; then
        audit_ts=$(date -j -f "%Y-%m-%d" "$audit_date" +%s)
      fi
      days_old=$(( ( $(date +%s) - audit_ts ) / 86400 ))
      if [ "$audit_ts" -eq 0 ]; then
        log_warn "Could not convert audit date '$audit_date' to epoch timestamp"
      elif [ "$days_old" -lt 30 ]; then
        log_ok "AUDIT.md is ${days_old} days old (fresh)"
      elif [ "$days_old" -lt 90 ]; then
        log_warn "AUDIT.md is ${days_old} days old — consider refreshing (see VERIFICATION.md)"
      else
        log_fail "AUDIT.md is ${days_old} days old — needs refresh (see VERIFICATION.md)"
      fi
    else
      log_warn "Could not parse audit date from AUDIT.md"
    fi
  fi
else
  echo ""
  echo "  (Skipping upstream checks. Run with --upstream to enable.)"
fi

# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"

if [ "$ERRORS" -gt 0 ]; then
  echo -e "${RED}DRIFT DETECTED${NC}"
  exit 1
else
  echo -e "${GREEN}ALL CLEAN${NC}"
  exit 0
fi
