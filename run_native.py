from __future__ import annotations

import argparse
import atexit
import ctypes
import os
import socket
import subprocess
import sys
import time
import urllib.request
from collections import deque
from dataclasses import dataclass
from pathlib import Path


APP_TITLE = "Hull Variants"
SERVER_HOST = "127.0.0.1"
STARTUP_TIMEOUT_SECONDS = 90
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 960
WINDOW_MIN_SIZE = (1000, 700)
LOG_TAIL_LINE_COUNT = 25


@dataclass
class StreamlitChildProcess:
    process: subprocess.Popen
    log_path: Path


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def get_bundle_dir() -> Path:
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS"))

    return Path(__file__).resolve().parent


def get_launch_dir() -> Path:
    if is_frozen():
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


def get_logs_dir() -> Path:
    logs_dir = get_launch_dir() / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


def get_app_script_path() -> Path:
    app_path = get_bundle_dir() / "app.py"
    if not app_path.exists():
        raise FileNotFoundError(f"Unable to locate bundled Streamlit app: {app_path}")

    return app_path


def pick_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((SERVER_HOST, 0))
        return sock.getsockname()[1]


def show_error(message: str) -> None:
    if os.name == "nt":
        ctypes.windll.user32.MessageBoxW(0, message, APP_TITLE, 0x10)
        return

    print(message, file=sys.stderr)


def create_log_path() -> Path:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return get_logs_dir() / f"streamlit_{timestamp}_{os.getpid()}.log"


def read_log_tail(log_path: Path, max_lines: int = LOG_TAIL_LINE_COUNT) -> str:
    if not log_path.exists():
        return ""

    with log_path.open("r", encoding="utf-8", errors="replace") as log_file:
        lines = deque(log_file, maxlen=max_lines)

    return "".join(lines).strip()


def build_startup_error(message: str, log_path: Path) -> str:
    log_tail = read_log_tail(log_path)

    if not log_tail:
        return f"{message}\n\nLog file: {log_path}"

    return (
        f"{message}\n\n"
        f"Log file: {log_path}\n\n"
        "Recent log output:\n"
        f"{log_tail}"
    )


def start_streamlit_subprocess(port: int) -> StreamlitChildProcess:
    if is_frozen():
        command = [sys.executable, "--streamlit-child", "--port", str(port)]
    else:
        command = [sys.executable, str(Path(__file__).resolve()), "--streamlit-child", "--port", str(port)]

    creationflags = 0
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    log_path = create_log_path()
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    with log_path.open("w", encoding="utf-8", errors="replace") as log_file:
        process = subprocess.Popen(
            command,
            cwd=str(get_launch_dir()),
            creationflags=creationflags,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            env=env,
        )

    return StreamlitChildProcess(process=process, log_path=log_path)


def stop_streamlit_process(process: subprocess.Popen | None) -> None:
    if process is None or process.poll() is not None:
        return

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def wait_for_server(port: int, child: StreamlitChildProcess) -> None:
    process = child.process
    healthcheck_url = f"http://{SERVER_HOST}:{port}/_stcore/health"
    deadline = time.time() + STARTUP_TIMEOUT_SECONDS

    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError(
                build_startup_error(
                    f"Streamlit exited before the desktop window opened. Exit code: {process.returncode}.",
                    child.log_path,
                )
            )

        try:
            with urllib.request.urlopen(healthcheck_url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.25)

    raise TimeoutError(
        build_startup_error(
            "Timed out while waiting for the embedded Streamlit server to start.",
            child.log_path,
        )
    )


def run_streamlit_server(port: int) -> None:
    from streamlit import config as streamlit_config
    from streamlit.runtime.credentials import check_credentials
    from streamlit.web import bootstrap

    flag_options = {
        "server_headless": True,
        "server_address": SERVER_HOST,
        "server_port": port,
        "server_fileWatcherType": "none",
        "browser_serverAddress": SERVER_HOST,
        "browser_serverPort": port,
        "browser_gatherUsageStats": False,
        "logger_hideWelcomeMessage": True,
        "global_developmentMode": False,
    }

    main_script_path = str(get_app_script_path().resolve())
    streamlit_config._main_script_path = main_script_path
    bootstrap.load_config_options(flag_options=flag_options)
    check_credentials()
    bootstrap.run(main_script_path, False, [], flag_options)


def launch_native_window(port: int) -> None:
    import webview

    app_url = f"http://{SERVER_HOST}:{port}"
    webview.create_window(
        APP_TITLE,
        app_url,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=WINDOW_MIN_SIZE,
        resizable=True,
    )
    webview.start()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--streamlit-child", action="store_true")
    parser.add_argument("--port", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.streamlit_child:
        if args.port <= 0:
            raise SystemExit("Missing --port for Streamlit child process.")
        run_streamlit_server(args.port)
        return 0

    child: StreamlitChildProcess | None = None

    try:
        port = pick_free_port()
        child = start_streamlit_subprocess(port)
        atexit.register(stop_streamlit_process, child.process)
        wait_for_server(port, child)
        launch_native_window(port)
        return 0
    except Exception as exc:
        show_error(str(exc))
        return 1
    finally:
        stop_streamlit_process(child.process if child else None)


if __name__ == "__main__":
    raise SystemExit(main())
