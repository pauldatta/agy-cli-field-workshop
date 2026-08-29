# Exercise 15: Browser Automation & DevTools MCP

> **Duration:** 25 min (Fast: 15 min · Average: 25 min · Thorough: 35 min) | **Module:** 4 — Multi-Agent & Advanced Workflows / MCP

---

## Objective

Connect Antigravity CLI to the **Chrome DevTools MCP** server to automate browser interactions, inspect running web applications, capture console errors and network requests, and fix frontend bugs directly from browser evidence.

---

## Setup

Create a sample web app workspace:

```bash
mkdir -p ~/agy-browser-lab/public ~/agy-browser-lab/.agents
cd ~/agy-browser-lab
git init
```

Create a sample webpage with an intentional JavaScript bug in `public/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Customer Portal</title>
  <style>
    body { font-family: sans-serif; padding: 2rem; }
    .card { border: 1px solid #ccc; padding: 1.5rem; border-radius: 8px; max-width: 400px; }
    button { background: #4285F4; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
    .error { color: red; margin-top: 1rem; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Customer Lookup</h2>
    <input type="text" id="customerId" placeholder="Enter Customer ID (e.g. 101)">
    <button id="lookupBtn">Search</button>
    <div id="result"></div>
  </div>

  <script>
    document.getElementById('lookupBtn').addEventListener('click', () => {
      const id = document.getElementById('customerId').value;
      // INTENTIONAL BUG: ReferenceError on undefined helper
      const formattedId = formatCustomerId(id);
      document.getElementById('result').innerText = "Customer record loaded for: " + formattedId;
    });
  </script>
</body>
</html>
```

Start a lightweight HTTP server:

```bash
# In a separate terminal or background job:
python3 -m http.server 8080 --directory public &
```

---

## Part 1: Configure Chrome DevTools MCP (5 min)

Configure the Chrome DevTools MCP server in `.agents/mcp_config.json`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

Verify that the MCP server is recognized:

```bash
agy
```

At the prompt, verify active MCP tools:

```text
> /mcp
```

Confirm that browser automation tools (`navigate`, `click`, `fill`, `evaluate_script`, `take_screenshot`) are active.

---

## Part 2: Browser Navigation & Automated Interaction (10 min)

Use the `/browser` command or direct browser tools to navigate to your test page:

```text
> /browser Navigate to http://localhost:8080. Inspect the page layout and take a snapshot of the DOM.
```

Now automate user interaction:

```text
> In the browser, type '101' into the #customerId input field, then click the #lookupBtn button.
```

Inspect the browser's console output:

```text
> What console messages or errors were logged when clicking the search button?
```

Notice that `agy` retrieves the browser console log:
`Uncaught ReferenceError: formatCustomerId is not defined`

---

## Part 3: Automated Bug Remediation from Browser Evidence (10 min)

Ask `agy` to fix the source code based on what the browser observed:

```text
> Based on the browser console ReferenceError you just observed, fix public/index.html so that formatCustomerId is properly defined and returns `CUST-${id}`.
```

After `agy` updates `public/index.html`:

```text
> Reload http://localhost:8080 in the browser, type '101', click the Search button again, and confirm that the result displays "Customer record loaded for: CUST-101" with 0 console errors.
```

---

## Catatan Lapangan & Hal Penting

!!! tip "Hal yang Perlu Diperhatikan"
    1. **Puppeteer / Chromium Dependencies:** The `@modelcontextprotocol/server-puppeteer` package downloads Chromium automatically. On headless Linux systems, ensure standard system libraries (e.g. `libnss3`, `libatk-bridge2.0-0`) are available, or configure Chrome DevTools MCP with `--headless`.
    2. **Port Conflicts:** Ensure the local test server port (`8080` or `3000`) is not already bound by another service before starting `python3 -m http.server`.
    3. **Tool Approval Prompting:** Browser interaction tools (`click`, `fill`, `navigate`) are external actions. You can use `/permissions request-review` or `/permissions auto-tool` to adjust interaction prompting.

---

## Completion Criteria

- [ ] Configured Chrome DevTools / Puppeteer MCP in `.agents/mcp_config.json`
- [ ] Verified active MCP tools with `/mcp`
- [ ] Navigated to a local web page and automated input filling and clicking with `/browser`
- [ ] Captured a browser console error and remediated the source code bug
- [ ] Verified the bug fix in the running browser with zero console errors
