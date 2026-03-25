import os
import sys
import multiprocessing

# --- DEPENDENCY INJECTION FOR PYINSTALLER ---
# By importing these here, PyInstaller's analyzer native detects and perfectly 
# bundles all their C-extensions and submodules without needing manual flags.
import streamlit
import pandas
import numpy
import matplotlib.pyplot
import scipy.io
import docx
import openpyxl
import holtrop_core
# --------------------------------------------

if __name__ == '__main__':
    # CRITICAL: Prevent infinite loop fork-bombs on Windows
    multiprocessing.freeze_support()
    
    import streamlit.web.cli as stcli

    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    # The path to the streamlit script
    script_path = os.path.join(application_path, 'app.py')

    # Directly invoke the Streamlit CLI (bypassing subprocesses)
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--global.developmentMode=false"
    ]
    
    sys.exit(stcli.main())
