# Build Guideline: Streamlit Native Wrapper

This document outlines the exact technical pipeline for converting the Streamlit application into a true native desktop window using `pywebview`.

## Phase 1: New Dependencies
We need a library capable of generating native Windows application frames and rendering web content inside them without relying on traditional browsers.
```powershell
pip install pywebview
```

## Phase 2: The Core Launcher (`run_native.py`)
We must create a brand new multi-threaded launcher script that performs two critical tasks simultaneously:
1. **Background Server:** Spawns a background daemon thread that natively initializes `streamlit.web.cli.main()`, effectively starting the hidden web server on port 8501.
2. **Foreground UI:** Spawns the main thread that calls `webview.create_window` and `webview.start()`, pointing it exclusively to `http://localhost:8501`.

*Note: With an enclosed webview, we no longer need the 5-minute inactivity auto-shutdown logic we built previously. Because the Streamlit window is intrinsically locked to the WebView, we can programmatically instruct `pywebview` to forcefully kill the Streamlit thread the exact millisecond the user clicks the red 'X' to close the application window.*

## Phase 3: PyInstaller Compilation
We will compile the script using PyInstaller, making sure to bundle the PyWebView dependencies alongside our existing strict imports array.

```powershell
pyinstaller -y --name "HullVariantsNative" --windowed --add-data "app.py;." --collect-all streamlit --collect-data docx --hidden-import pandas --hidden-import numpy --hidden-import matplotlib --hidden-import scipy.io --hidden-import openpyxl --hidden-import holtrop_core run_native.py
```
