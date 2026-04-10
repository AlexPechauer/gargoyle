# Gargoyle — text trigger expansion

Type a short trigger (for example `/greet`) in any text field and the app replaces it with a longer phrase. A small listener runs in the terminal until you exit with **Esc**.

## Requirements

- **Python 3** with `venv` support (standard on current macOS, Linux, and Windows installs)

## First-time setup

1. **Get the code** (clone or unzip) and open a terminal in the **project root** (the folder that contains `requirements.txt` and `src/`).

2. **Start the app** (pick one):

   ```bash
   python3 src/main.py
   ```

   On Windows, if `python3` is not on your `PATH`, try:

   ```bash
   py src/main.py
   ```

3. **First run only**: the program creates a virtual environment at `./venv`, switches to it, and installs dependencies from `requirements.txt` (`pynput`, `python-dotenv`). Later runs reuse the same venv and only reinstall when `requirements.txt` changes.

You can also use a pre-made venv at `./.venv` instead of `./venv` — if either exists, the app prefers it.

## Everyday use

1. Leave the terminal window open while you work. You should see: `Listening for text triggers... (Press Esc to exit)`.
2. Focus a normal text field (browser, editor, chat, etc.) and type a **trigger** exactly as defined in `sentences.json` (see below). When the typed text **ends with** that trigger, it is erased and replaced by the configured sentence.
3. Press **Esc** in that terminal session to stop the listener, or close the terminal.

### Permissions (macOS)

`pynput` needs permission to observe keyboard input. If nothing happens when you type triggers, open **System Settings → Privacy & Security → Input Monitoring** (and/or **Accessibility**, depending on macOS version) and allow the app you are using to run Python (for example **Terminal**, **iTerm2**, or **Cursor**).

## Triggers and sentences

Triggers and replacement text live in:

`src/quicktext/sentences.json`

The file is a single JSON object: keys are triggers (strings you type), values are the text to insert.

**Example:**

```json
{
  "/rec": "This is the predefined text to autopopulate.",
  "/greet": "Hello! How can I assist you today?",
  "/sig": "— Alex"
}
```

**Rules:**

- Use valid JSON: double quotes for keys and string values, commas between entries, **no trailing comma** after the last property.
- Triggers are matched against what you have typed so far; the replacement runs when your buffer **ends with** the trigger string (so shorter triggers can overlap longer ones — order your keys with that in mind, or use unique prefixes).

After editing `sentences.json`, **restart** the program (Esc to quit, then run `python3 src/main.py` again) so changes load.

## Troubleshooting

- **Crash on startup or unexpected exit**: details may be written to `src/gargoyle_error.log` next to the running code.
- **JSON errors**: if `sentences.json` is invalid, Python will raise when loading; fix the file with a JSON-aware editor or validator.
- **Dependencies**: ensure `./venv` was created from this project’s root so `requirements.txt` is found; delete `venv` and run `python3 src/main.py` again for a clean install if needed.

## Project layout (short)

| Path | Role |
|------|------|
| `src/main.py` | Entry point: venv bootstrap, then starts the listener |
| `src/quicktext/sentences.json` | Trigger → replacement text |
| `src/quicktext/hotkey.py` | Loads JSON and listens for triggers |
| `requirements.txt` | Pip dependencies |
