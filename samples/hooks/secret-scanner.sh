#!/usr/bin/env bash
# PreToolUse hook: Lightweight secret detection in file writes and command executions
# Matcher: write_to_file|replace_file_content|multi_replace_file_content|run_command
# Performance: <50ms — simple regex over stdin JSON
#
# PURPOSE: Enforces enterprise security policy by blocking hardcoded credentials.
# AGY CLI hook event: PreToolUse
# Register in: .agents/hooks.json under "PreToolUse"

input=$(cat)

# Extract content from write_to_file, replace_file_content, or run_command
content=$(echo "$input" | jq -r '
  .toolCall.args.CodeContent // 
  .toolCall.args.ReplacementContent // 
  (.toolCall.args.ReplacementChunks[]?.ReplacementContent) // 
  .toolCall.args.CommandLine // 
  ""' 2>/dev/null)

# Quick regex scan for API keys, tokens, and hardcoded passwords
if echo "$content" | grep -qEi '(AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}|sk-[a-zA-Z0-9]{48}|password\s*[:=]\s*["'"'"'][^\s"]{8,})'; then
    echo '{"decision":"deny","reason":"Hardcoded credential detected. Store secrets in environment variables or .env (gitignored) and access them via process.env or os.environ."}'
else
    echo '{"decision":"allow"}'
fi
