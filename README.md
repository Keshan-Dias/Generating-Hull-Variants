# Generating Hull Variants

A Streamlit-based desktop application for calculating calm-water resistance and carrying capacity for general cargo vessels using the Holtrop–Mennen method. 

## Features
- **Resistance Calculations:** Calculates frictional, wave-making, and total resistance.
- **Carrying Capacity:** Computes deadweight, payload, and operational parameters.
- **Hull Form Generation:** Automatically generates a robust dataset of hull variants within specified boundary limits.
- **Data Export:** Auto-generates formal reports in Word (.docx), Excel (.xlsx) spreadsheets, and MATLAB (.mat) arrays.
- **Standalone Executable:** Fully packaged PyInstaller desktop app with smart process management (auto-shutdowns after 5 minutes of background inactivity).

## Tech Stack
- **Python 3.13**
- **Streamlit** (User Interface)
- **pandas, numpy, scipy** (Core Mathematics & Iterators)
- **matplotlib** (Vessel Visualizations)
- **python-docx, openpyxl** (Reporting Pipeline)

## Usage

### Using the Pre-Compiled Executable
The application has been securely packaged into a standalone Windows environment. 
To run it, simply navigate to the `dist/HullVariants` folder and double-click `HullVariants.exe`. The server will silently start in the background and your default web browser will automatically open the application.

*Note: The background server utilizes an autonomous death-switch. If you close the browser tab or leave it idle for exactly 5 minutes, it will automatically terminate the memory-resident background process to keep your computer fast.*

### Running from Source Code
If you prefer to run the raw source code or develop new features:
```powershell
# 1. Activate the environment
.\venv\Scripts\Activate.ps1

# 2. Install dependencies (if not already done)
pip install -r requirements.txt

# 3. Run the Streamlit server
streamlit run app.py
```
