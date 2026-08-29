#!/usr/bin/env bash
# PreToolUse hook: Inspects git context before file writes and replacements
# Matcher: write_to_file|replace_file_content|multi_replace_file_content
# Performance: <100ms — single git command
#
# PURPOSE: Checks recent git changes for the target file before modifying it.
# AGY CLI hook event: PreToolUse
# Register in: .agents/hooks.json under "PreToolUse"

input=$(cat)

# Extract target file path from toolCall arguments
filepath=$(echo "$input" | jq -r '
  .toolCall.args.TargetFile // 
  ""' 2>/dev/null)

# Verify if file exists and has git history
if [ -n "$filepath" ] && [ -f "$filepath" ]; then
    recent_changes=$(git log --oneline -3 -- "$filepath" 2>/dev/null | head -3)
    if [ -n "$recent_changes" ]; then
        echo "{\"decision\":\"allow\",\"reason\":\"Target file has recent commits: $recent_changes\"}"
    else
        echo '{"decision":"allow"}'
    fi
else
    echo '{"decision":"allow"}'
fi
