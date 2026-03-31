# Repository Guidelines

## Project Structure & Module Organization
This repository is a small Streamlit-based Python app.

- `cyberstate.py`: main app for letter-frequency analysis and visualization.
- `app.py`: simple Streamlit demo entry point.
- `UI.md`: UI notes and design ideas.
- `test.txt`: sample text input for manual checks.
- `cyberstate - 副本.py`: backup copy; treat `cyberstate.py` as the canonical source.

Keep new app logic in focused Python modules if the codebase grows. Put reusable helpers near the main app or under a future `utils/` directory instead of duplicating logic.

## Build, Test, and Development Commands
- `streamlit run cyberstate.py`: run the main application locally.
- `streamlit run app.py`: run the demo app.
- `python -m py_compile app.py cyberstate.py`: quick syntax check before submitting changes.

Install missing dependencies with your preferred environment manager before running the app. Current imports indicate `streamlit`, `plotly`, and standard-library modules; `app.py` also uses `pandas` and `numpy`.

## Coding Style & Naming Conventions
Use 4-space indentation and follow PEP 8 for Python.

- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Files: lowercase names without spaces when creating new modules

Prefer small, single-purpose functions such as `letter_frequency(text)`. Keep Streamlit UI code readable by grouping related widgets inside clearly labeled sections.

## Testing Guidelines
There is no formal test suite yet. For now, rely on lightweight checks:

- Run `python -m py_compile app.py cyberstate.py`
- Start the app with `streamlit run cyberstate.py`
- Verify text input, `.txt` upload, chart rendering, and empty-input warnings

If you add tests, use `pytest`, place them under `tests/`, and name files `test_*.py`.

## Commit & Pull Request Guidelines
Git history is not available in this workspace, so no existing commit convention can be inferred. Use short, imperative commit messages such as `feat: add csv download` or `fix: handle empty uploads`.

Pull requests should include a clear summary, the user-facing impact, manual test steps, and screenshots for UI changes.

## Configuration Notes
Assume uploaded text files are UTF-8 unless the app is updated to support other encodings. Avoid committing local IDE files or temporary backup copies.
