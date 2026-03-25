# Step-by-Step Guideline: Building the Desktop Executable

Follow these steps to turn the Streamlit application into a distributable Windows `.exe`.

## Phase 1: Preparation

1. **Ensure Virtual Environment is Active**
   Make sure you are working inside the `venv` where all dependencies (Streamlit, Pandas, SciPy, etc.) are installed.
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Install Packaging Tools**
   Install PyInstaller, which is the tool that compiles python into `.exe` files.
   ```powershell
   pip install pyinstaller
   ```

## Phase 2: Create the Launcher Script

Create a new file in the root directory named `run_app.py`. This script will act as the entry point for the compiled software. It will silently start the Streamlit server and automatically open the web browser.

**Content for `run_app.py`:**
```python
import os
import sys
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    import streamlit.web.cli as stcli

    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    script_path = os.path.join(application_path, 'app.py')

    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false"
    ]
    
    sys.exit(stcli.main())
```
*(Note: A slightly different launcher approach using `streamlit.web.cli` is also possible if the subprocess approach triggers antivirus warnings).*

## Phase 3: Compile with PyInstaller

We need to tell PyInstaller to include your Python scripts (`app.py`, `holtrop_core.py`) and Streamlit's hidden web files.

1. **Run the initial PyInstaller command** to generate a `.spec` file:
   ```powershell
   pyinstaller --name "HullVariants" --windowed --add-data "app.py;." --add-data "holtrop_core.py;." --copy-metadata streamlit run_app.py
   ```
   * `--windowed`: Prevents the black console window from showing up.
   * `--add-data`: Bundles your specific code files.
   * `--copy-metadata`: Ensures Streamlit can find its own version info.

2. **Wait for the build to finish.** PyInstaller will create a `build/` folder and a `dist/` folder.

## Phase 4: Testing & Distribution

1. **Locate the Executable**
   Go into the `dist/HullVariants/` directory. You will find `HullVariants.exe`.
2. **Test It**
   Double-click `HullVariants.exe`. The black terminal window should NOT appear (or should flash briefly), and your default web browser should open automatically displaying the "General Cargo Vessel Resistance" tool.
3. **Verify Functionality**
   Test the graphs, dataset generation, and the MATLAB / Word exports to ensure file paths resolve correctly in the packaged mode.
4. **Distribute**
   Zip the entire `dist/HullVariants/` folder. Send this `.zip` file to your end-users. They just need to extract it and double-click the `.exe`!
