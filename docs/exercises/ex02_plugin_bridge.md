# Exercise 2: Plugin Bridge

> **Duration:** 20 min (Fast: 12 min · Average: 18 min · Thorough: 25 min) | **Module:** 2 — Plugin Ecosystem

---

## Objective

Import an existing plugin library into Antigravity CLI, selectively enable/disable plugins, and validate and install custom workspace plugins.

---

## Part 1: Import Plugins (7 min)

```bash
# Check what's currently active in agy
agy plugin list

# Import everything from your Gemini CLI setup
agy plugin import gemini
```

Read the output carefully:

- Which plugins were imported?
- Which components did each plugin contribute (skills, commands, mcpServers, agents)?
- Were any skipped? Why?

```bash
# See the updated list formatted as JSON
agy plugin list | python3 -m json.tool
```

!!! tip "Fresh Machine Fallback"
    If you are running on a brand-new laptop without existing Gemini CLI plugins, `agy plugin import gemini` will report `0 plugins found`. To test the plugin workflow immediately, install the local sample plugin provided in this repository:
    ```bash
    agy plugin install ./samples/plugins/workshop-helpers/
    ```

---

## Part 2: Test an Imported Plugin (5 min)

Launch agy and try a command from one of the imported or installed plugins:

```bash
agy
```

If `code-review` was imported:

```text
> /code-review Review the main entry point of this project.
```

If `workshop-helpers` was installed:

```text
> What custom skills or helper commands are available from my installed plugins?
```

---

## Part 3: Disable and Re-enable (3 min)

```bash
# Disable a plugin you just imported/installed
agy plugin disable workshop-helpers   # or your imported plugin name

# Confirm it is marked inactive
agy plugin list | python3 -m json.tool

# Re-enable it
agy plugin enable workshop-helpers
```

---

## Part 4: Validate the Sample Plugin (5 min)

The workshop repository includes a pre-packaged sample plugin:

```bash
ls samples/plugins/workshop-helpers/

# Validate its plugin.json manifest and directory structure
agy plugin validate samples/plugins/workshop-helpers/
```

Now intentionally break the manifest to see how validation diagnostics work:

```bash
# Edit plugin.json (e.g. remove the "name" or "components" key)
# Then re-validate to see the schema error
agy plugin validate samples/plugins/workshop-helpers/

# Restore the original manifest
git checkout samples/plugins/workshop-helpers/plugin.json
```

---

## ⚠️ Field Gotchas & Failure Modes

!!! warning "Common Workshop Gotchas"
    1. **Fresh Machine False-Alarm:** `agy plugin import gemini` looks for `~/.gemini/extensions/`. If you've never used Gemini CLI on this machine, it reports 0 imported plugins. This is normal — use `agy plugin install ./samples/plugins/workshop-helpers/` to proceed.
    2. **Staged Paths:** Imported plugins are staged into `~/.gemini/antigravity-cli/plugins/`. If you modify a plugin source file afterwards, re-run `agy plugin validate` or reinstall to update the staged copy.
    3. **Name Collisions:** If two plugins export a command with the same name, the most recently installed plugin takes precedence. Use `agy plugin list` to inspect component mappings.

---

## Completion Criteria

- [ ] `agy plugin import` or `agy plugin install` ran successfully
- [ ] Tested at least one command/skill from an active plugin
- [ ] Successfully disabled and re-enabled a plugin
- [ ] `agy plugin validate` caught schema errors on a broken manifest and passed on a valid one

