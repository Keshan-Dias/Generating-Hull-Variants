# Hull Variants

Hull Variants is a Streamlit-based desktop tool for preliminary general cargo vessel analysis. It combines Holtrop-Mennen resistance and power estimation, carrying-capacity calculations, hull-variant generation, and export workflows into a single application.

This branch packages the app as a standalone Windows desktop window using `pywebview` and PyInstaller. The frontend behavior remains the same as the current Streamlit UI, but the user can launch it from a native `.exe` instead of a browser tab.

## Current Scope

- Streamlit UI in `app.py`
- Core resistance and power formulas in `holtrop_core.py`
- Native desktop launcher in `run_native.py`
- One-file Windows build via `Hull_Variants.spec`
- Export output written to `exports/`

## Main Features

- Resistance and power prediction across a speed range
- Design-speed resistance breakdown
- Carrying-capacity and hydrostatic summary values
- Hull-form dataset generation around a baseline design
- Export to MATLAB `.mat`
- Export to Word `.docx`
- Export to Excel `.xlsx`

## Repository Layout

- `app.py`: main Streamlit application
- `holtrop_core.py`: calculation core
- `run_native.py`: native desktop launcher for the app window
- `Hull_Variants.spec`: PyInstaller build spec for the standalone executable
- `build_windows.bat`: Windows build script
- `assets/hull_variants.ico`: app icon
- `exports/`: generated output files
- `docs/`: design and packaging notes

## Requirements

- Windows 64-bit
- Existing project virtual environment at `venv/`
- Python dependencies from `requirements.txt`

## Run Locally

Run the native desktop window:

```bat
venv\Scripts\python.exe run_native.py
```

Run the original browser-based Streamlit app:

```bat
venv\Scripts\python.exe -m streamlit run app.py
```

## Build the Standalone EXE

From Windows Command Prompt in the project root:

```bat
build_windows.bat
```

This builds:

- `dist\Hull Variants.exe`

## Run the Built App

```bat
dist\Hull Variants.exe
```

## Exports

Generated files are written to:

```text
exports/
```

Current export file names:

- `exports/holtrop_designspeed_dataset.mat`
- `exports/Holtrop_Resistance_Report.docx`
- `exports/Holtrop_Complete_Results.xlsx`

These files are overwritten on each new export unless renamed manually.

## Logs

If the native desktop launcher fails during startup, it writes a log file to:

```text
logs/
```

The launcher error popup includes the log path and recent log output to help diagnose startup failures.

## Notes on Native Packaging

- The desktop app runs Streamlit in a hidden child process and renders it inside a `pywebview` window.
- The packaged executable may take a few seconds to open on normal laptops because PyInstaller one-file apps unpack before launch.
- The app expects to run from a writable location because exports and logs are written beside the executable.

## Important Project Constraint

`holtrop_core.py` contains the current formula implementation and should be treated as the protected calculation core unless changes are explicitly approved.

## Related Docs

- `docs/app_blueprint.md`
- `docs/build_guideline.md`
- `docs/desktop_app_questions.txt`
