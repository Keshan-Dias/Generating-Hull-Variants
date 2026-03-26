# Native Wrapper App Blueprint

## Goal
To package the existing Streamlit codebase into a fully standalone, native desktop application window without rewriting the frontend code.

## Architecture: The "Native Wrapper"
Instead of opening the application in a standard web browser (like Chrome or Edge), we use a **WebView container** (specifically `pywebview`).
- **Backend:** Streamlit still runs securely in a hidden background Python thread.
- **Frontend:** `pywebview` creates a real Windows application frame (with an icon, minimize/maximize buttons, and its own taskbar presence) and renders the local Streamlit server directly inside of it. 
- **User Experience:** From the naval architect's perspective, they just double-click an executable, and a standalone application window opens up. They will never see a URL bar or a browser tab.

## Analysis of Tradeoffs

### 1. File Size (The "Heavy" Factor)
- **Estimated Size:** ~300MB to 500MB for the final `.exe` (or ZIP).
- **Reason:** Because Streamlit is essentially a web server, the executable has to be completely self-contained. It must heavily bundle:
  1. The entire Python 3.13 Runtime so the user doesn't have to install Python.
  2. Heavy mathematical libraries (Pandas, Numpy, Scipy).
  3. The Streamlit Tornado Web Server.
  4. The web-rendering engine components required by `pywebview`.
- **Verdict:** While 400MB sounds large for a simple calculator, it is completely standard for modern desktop apps (Electron apps like Discord, VSCode, and Slack are roughly the same size). File size does not affect runtime speed, it just means the `.zip` takes a minute longer to download or email.

### 2. Startup Execution Time
- **Estimated Time:** 5 to 15 seconds from double-click to the fully rendered GUI.
- **Reason:** When the `.exe` is double-clicked, Windows has to silently unpack the bundled Python environment into a temporary memory directory, internally boot up the local Streamlit server, wait exactly a second for the server port to bind, and finally launch the WebView container to point to that newly created server. 
- **Verdict:** The app itself will run blazingly fast once opened, but the initial "boot time" takes several seconds of a blank screen or loading cursor.
