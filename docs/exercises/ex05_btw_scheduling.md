# Exercise 5: /btw & Scheduling

> **Duration:** 20 min (Fast: 15 min · Average: 20 min · Thorough: 25 min) | **Module:** 4 — Multi-Agent & Advanced

---

## Objective

Use `/btw` to steer a long-running task mid-flight without cancelling execution, resume disconnected sessions with `agy -c`, and schedule a recurring automated security scan.

---

## Part 1: /btw Mid-Task Steering (10 min)

Launch agy and kick off a substantial multi-phase analysis:

```bash
agy
```

```text
> I want to refactor the error handling across this entire project to use a consistent pattern. Start by analyzing all error handling in the codebase, then propose and implement a unified approach. This will touch multiple files — start with the analysis phase.
```

As agy starts working (while tool execution and streaming are active), inject an asynchronous constraint:

```text
/btw Only touch files in the backend/ directory for now. Leave frontend untouched.
```

Then add another note:

```text
/btw Use the Result<T, E> pattern if the language supports it. Otherwise use a custom Error class hierarchy.
```

Observe:

- The task continues executing without aborting or restarting
- agy incorporates both `/btw` notes into its active trajectory
- The resulting plan reflects your injected constraints

**Key insight:** `/btw` lets you course-correct without the cost of cancelling and restarting. This is the equivalent of tapping a developer on the shoulder mid-sprint.

---

## Part 2: Session Continuation (5 min)

End the session (`/exit` or Ctrl+C).

Resume the most recent session from where you left off:

```bash
agy -c
```

```text
> Remind me what we decided about the error handling refactor. What was the approach?
```

agy will have full conversational history. Now continue the work:

```text
> Let's implement step 1 of the plan we discussed.
```

---

## Part 3: Schedule a Recurring Report (5 min)

```bash
agy
```

```text
> Schedule a daily dependency check every weekday morning at 8am. It should:
> 1. Check for outdated dependencies with security advisories
> 2. List any new CVEs affecting our current dependency versions
> 3. Save the report to reports/deps-YYYY-MM-DD.md
>
> Create the reports/ directory if it doesn't exist.
```

Confirm the schedule was accepted:

```text
> What scheduled tasks are currently active?
```

---

## Pro Tips & Key Watchouts

!!! tip "Key Things to Watch For"
    1. **Timing `/btw`:** `/btw` is designed for in-flight steering. If the model has already completed generating its response and is idle, typing `/btw` will simply be processed as a standard new turn.
    2. **Session Resumption (`-c`):** Running `agy -c` connects to the most recently updated session in the current directory. If you want to resume a specific session across workspaces, provide the full session ID: `agy -c <conversation-id>`.
    3. **Background Daemon Persistence:** Scheduled jobs created via `/schedule` or sidecars run as background cron tasks managed by the CLI runtime. Ensure your machine does not enter deep sleep during scheduled execution windows.

---

## Completion Criteria

- [ ] Started a long-running task and used `/btw` at least twice during active execution
- [ ] Confirmed that `/btw` messages were incorporated into the output
- [ ] Used `agy -c` to resume a session and retrieved prior context
- [ ] Created and inspected a scheduled recurring task

