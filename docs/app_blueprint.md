# Generating Hull Variants - Desktop Application Blueprint

## 1. Project Objectives
Transform the existing Streamlit-based web application into a distributable, standalone software package for Windows. 
- **Target Audience:** Naval architects and engineers with no coding background or Python installation.
- **Platform:** Windows OS.
- **Key Features:** Data inputs, parametric hull generation, resistance/hydrostatic calculations, visualization (Matplotlib graphs), and data export (MATLAB/Excel/Word).

## 2. Architectural Decision
Based on the software constraints (basic future complexity, graphical emphasis, no file size limit) and an openness to different frameworks:

**Decision:** We will retain the **Streamlit** frontend and package it using **PyInstaller** along with a silent launcher script.

**Why not a CustomTkinter / PyQt rewrite?**
1. **Visual Excellence:** The current Streamlit UI already handles the complex Matplotlib graphs, data tables, and tabbed layout perfectly. Rebuilding this level of responsive data-visualization in Tkinter or PyQt is disproportionately time-consuming.
2. **"Sufficient" Browser UI:** Since a browser-based local UI is acceptable to the end-users, there is no strict need to spend hours rewriting the UI when we can achieve the "double-click executable" experience instantly with Streamlit.

## 3. System Architecture
The distributable `.exe` will contain three layers:

1. **The Launcher (`run_app.py`):** 
   A lightweight Python script compiled into a windowless executable (`.exe`). When the user double-clicks this, it silently triggers the Streamlit server.
2. **The Streamlit Server (`app.py`):** 
   The core application logic and UI. The launcher automatically opens the user's default web browser (Edge/Chrome) pointing to `localhost:8501`.
3. **The Core Engine (`holtrop_core.py`):**
   The mathematical logic handling the Holtrop-Mennen resistance calculations.

## 4. Packaging Strategy
We will use **PyInstaller** to bundle the Python interpreter, Streamlit, Pandas, Matplotlib, SciPy, and all application scripts into a single, redistributable directory or one-file executable.

- **PyInstaller Hook:** Streamlit requires specific PyInstaller "hooks" to copy its internal static web assets over to the executable.
- **Entry Point:** A custom `run_app.py` script will be the entry point.
- **Distribution:** The app will be provided as a zip file containing the `.exe` and associated data files, meaning end-users simply "unzip and click".

## 5. Development Phases
1. **Create the Launcher Script** (`run_app.py`)
2. **Test the Launcher** locally
3. **Configure PyInstaller** (via a `.spec` file) to bundle Streamlit's web assets
4. **Build the Executable** using PyInstaller
5. **Quality Assurance:** Run the `.exe` outside the development environment to ensure it opens the browser, renders graphs, and exports `.mat` files successfully.
