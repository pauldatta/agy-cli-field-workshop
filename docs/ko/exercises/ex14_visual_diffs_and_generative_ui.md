# Exercise 14: Visual Diffs & Generative UI Artifacts

> **Duration:** 20 min (Fast: 12 min · Average: 20 min · Thorough: 28 min) | **Module:** 1 — SDLC Productivity / Generative UI

---

## Objective

Leverage Antigravity's rich visual capabilities:
1. Render interactive **Generative UI** widgets, interactive charts, and system architecture diagrams directly in the artifact preview pane.
2. Review multi-file code modifications using the visual **`/diff`** viewer and **`Ctrl+R`** artifact review panel before approving disk writes.

---

## Part 1: Interactive Generative UI Widgets (8 min)

Launch `agy`:

```bash
agy
```

Prompt `agy` to generate a live, interactive data visualization:

```text
> Create an interactive latency & throughput benchmark dashboard widget for an API gateway handling 10,000 req/s. Include:
> 1. P50, P95, and P99 latency distribution sliders
> 2. An interactive SVG or Chart.js bar chart showing response time breakdown (DNS, TLS, backend processing)
> 3. An error budget calculator that recalculates live as sliders move
>
> Render this as an interactive HTML artifact.
```

Observe how `agy` creates the artifact:
* It writes an HTML/CSS/JS widget.
* The preview pane or web sidecar opens automatically to render the live interactive component.
* Move the sliders and click interactive controls to test live state recalculation.

Now request an architectural topology map:

```text
> Generate an interactive system architecture diagram showing a microservices mesh (Auth Service, Catalog, Checkout, Payment Gateway, Kafka Event Bus). Make service nodes clickable to reveal details in an info card.
```

---

## Part 2: Visual Diffs & Semantic Code Review (7 min)

Ask `agy` to make a multi-file refactor:

```text
> Refactor the project error handling: add an ApiError class with HTTP status codes and wrap all route handlers in try/catch blocks that return structured JSON error responses.
```

Before approving the file write tool calls:

1. Type **`/diff`** at the prompt to view a syntax-highlighted, side-by-side or unified semantic diff.
2. Press **`Ctrl+R`** to open the full-screen Artifact & Diff Review Panel (`prompt.open_review`).
3. Inspect line-by-line additions and deletions.
4. Press **`Escape`** or **`q`** to exit review mode and return to your prompt.
5. Approve or reject the changes based on the visual diff.

---

## Part 3: Image & Media Context via Clipboard (5 min)

Antigravity CLI allows pasting images, screenshots, and UI mockups directly into the terminal prompt.

1. Take a screenshot of any webpage or application diagram on your screen (copy to system clipboard: `Ctrl+C` / `Cmd+Ctrl+Shift+4`).
2. In the `agy` prompt, press **`Ctrl+V`** (`prompt.paste_media`).
3. Notice that `agy` converts the clipboard image into a temporary inline media asset reference.
4. Ask:

```text
> Analyze this architecture screenshot. What are the key bottlenecks in this design?
```

---

## ⚠️ Field Gotchas & Failure Modes

!!! warning "Common Workshop Gotchas"
    1. **Terminal Media Pasting:** Pasting images with `Ctrl+V` requires terminal graphics protocol support (e.g. iTerm2, Kitty, Ghostty, WezTerm, or VS Code integrated terminal). In basic terminals, `agy` will save the clipboard image to a local temporary path and reference it.
    2. **Local Port Proxies:** When running on remote cloud VMs, local dev server URLs (`http://localhost:3000`) cannot be reached from your local laptop browser. Use the provided hostname proxy format (`http://<hostname>.c.googlers.com:<PORT>`).
    3. **Artifact Directory Scoping:** HTML artifacts are generated in the session artifact directory (`~/.gemini/antigravity-cli/brain/<session-id>/`). They are isolated from your repository's working tree unless explicitly exported.

---

## Completion Criteria

- [ ] Generated an interactive Generative UI dashboard widget rendered in the artifact pane
- [ ] Rendered an interactive architectural diagram with clickable elements
- [ ] Used `/diff` and `Ctrl+R` to review semantic code changes before approving writes
- [ ] Pasted an image or inspected a visual asset in prompt context using `Ctrl+V`
