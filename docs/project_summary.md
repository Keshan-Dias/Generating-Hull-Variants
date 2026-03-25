# Project Summary: Desktop Packaging and Optimization

This document provides a comprehensive chronological summary of the engineering work done to refine and package a web-based Streamlit application into a highly robust, standalone Windows executable.

## 1. Initial Review and Bug Fixes
- **Environment Setup:** Standardized the ecosystem by creating a strict `requirements.txt` containing `streamlit`, `pandas`, `numpy`, `matplotlib`, `scipy`, `python-docx`, and `openpyxl`. Initialized an isolated Python 3.13 virtual environment.
- **MATLAB Export Bug Fix:** Identified and patched a crashing `NameError` in `app.py`. The bug occurred during the boundary generation step where `L_min`, `B_min`, and other physical parameters were being referenced in the MATLAB exporter before they had been defined.

## 2. Desktop Strategy
- **Architectural Decision:** Evaluated rewriting the UI in a native framework like CustomTkinter vs. packaging Streamlit. We decided to package Streamlit using **PyInstaller** to preserve the rich graphical Matplotlib output and existing feature set while meeting the user's desktop standalone requirement without compromising on aesthetics.

## 3. The Packaging Journey
- **Attempt 1 (The Fork Bomb):** The first PyInstaller build utilized a standard `subprocess.Popen` launcher to boot the server. Due to how Windows identically forks memory in nested Python executables, this caused an infinite loop (a fork bomb) where the `.exe` rapidly spawned hundreds of invisible background processes, freezing the host machine.
- **Attempt 2 (The 404 Error):** Rewrote the launcher script (`run_app.py`) to bypass subprocessing and instead directly invoke `streamlit.web.cli.main()`, strictly enforcing `multiprocessing.freeze_support()`. This fixed the infinite crashing loop, but the application loaded an "HTTP 404 Not Found" blank screen because PyInstaller is blind to dynamic assets and failed to bundle Streamlit's static web files (HTML/CSS).
- **Attempt 3 (Missing Submodules):** Injected the PyInstaller `--collect-all streamlit` flag. The UI loaded perfectly, but interacting with the app resulted in a `ModuleNotFoundError: No module named 'docx'` and subsequently `scipy.io`. PyInstaller was blind to the dependencies inside `app.py` because the Streamlit payload was being treated as purely a string data file instead of an executable AST tree.
- **Attempt 4 (Native Dependency Injection):** Instead of playing whack-a-mole with PyInstaller's hidden-import flags (which often misses C-extensions for massive libraries like Scipy), we injected a native dependency mapping block at the very top of `run_app.py`. By explicitly importing `streamlit`, `pandas`, `numpy`, `docx`, `scipy.io`, `openpyxl`, and `holtrop_core` inside the launcher, we forced PyInstaller's AST analyzer to flawlessly hook and bundle every single deeply nested C-extension and submodule during compilation.

## 5. Smart Process Management
- Unlike standard `.exe` applications bounded by a window frame, browser-based native executables leave zombie Python processes running in system memory forever if the user simply closes out their Chrome tab.
- **Auto-Shutdown Implementation:** Engineered and injected a daemon thread into `app.py` utilizing Streamlit's `@st.cache_resource` singleton wrapper. This thread acts as an autonomous dead-man's switch. Every user interaction on the frontend organically resets a global timestamp. If the user walks away from their desk or closes the tab, the timestamp ages. At exactly 5 minutes of total inactivity, the daemon triggers `os._exit(0)`, completely resolving the zombie memory-leak and returning the host computer to a completely clean state.

## 6. Final Delivery
The web-based application now exists as a highly robust, zero-install standalone Windows native app in `dist/HullVariants`. It behaves exactly like traditional software for naval architects, complete with custom autonomous memory management, no required dependencies, and an intact heavy-duty data export pipeline.
