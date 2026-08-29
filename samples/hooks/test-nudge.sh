#!/usr/bin/env bash
# PostToolUse hook: Telemetry & audit logging after tool execution
# Matcher: write_to_file|replace_file_content|run_command
# Performance: <10ms — writes diagnostic trace if error occurs
#
# PURPOSE: Logs failed tool executions or changes for offline auditing.
# AGY CLI hook event: PostToolUse
# Register in: .agents/hooks.json under "PostToolUse"

input=$(cat)

tool_name=$(echo "$input" | jq -r '.toolCall.name // ""' 2>/dev/null)
step_idx=$(echo "$input" | jq -r '.stepIdx // 0' 2>/dev/null)
tool_error=$(echo "$input" | jq -r '.error // ""' 2>/dev/null)

# If tool execution produced an error, record telemetry to audit log
if [ -n "$tool_error" ]; then
    mkdir -p .agents/logs
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Step $step_idx ($tool_name) failed: $tool_error" >> .agents/logs/tool_audit.log
fi

# PostToolUse output contract is strictly an empty JSON object
echo '{}'
