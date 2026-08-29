#!/usr/bin/env bash
# PreInvocation hook: Injects project state into the session context
# Performance: <200ms — reads git status & node version
#
# PURPOSE: Before model invocation, gives the agent a summary of project state
# AGY CLI hook event: PreInvocation
# Register in: .agents/hooks.json under "PreInvocation"

input=$(cat)

# Extract primary workspace root directory from stdin metadata
workspace=$(echo "$input" | jq -r '.workspacePaths[0] // "."' 2>/dev/null)

# Gather lightweight project state
branch=$(git -C "$workspace" branch --show-current 2>/dev/null || echo "main")
dirty_count=$(git -C "$workspace" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
node_version=$(node --version 2>/dev/null || echo "unknown")

context="[Session Context] Workspace: $workspace | Branch: $branch | Uncommitted Files: $dirty_count | Node: $node_version"

# Return injectSteps with ephemeralMessage per official Antigravity schema
echo "{\"injectSteps\":[{\"ephemeralMessage\":\"$context\"}]}"
