import os
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


ERROR_LOG_NAME = "gargoyle_error.log"


def _error_log_path() -> Path:
    # Frozen (e.g. PyInstaller): put log next to the .exe so it is easy to find.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / ERROR_LOG_NAME
    return Path(__file__).resolve().parent / ERROR_LOG_NAME


def _write_crash_log() -> Path:
    path = _error_log_path()
    stamp = datetime.now(timezone.utc).isoformat()
    body = f"{stamp} (UTC)\n\n{traceback.format_exc()}"
    path.write_text(body, encoding="utf-8")
    return path


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _local_venv_python(root: Path) -> Optional[Path]:
    if sys.platform == "win32":
        candidates = [
            root / "venv" / "Scripts" / "python.exe",
            root / ".venv" / "Scripts" / "python.exe",
        ]
    else:
        candidates = [
            root / "venv" / "bin" / "python",
            root / ".venv" / "bin" / "python",
        ]
    for py in candidates:
        if py.is_file():
            return py
    return None


def _is_project_venv(project_root: Path, venv_root: Path) -> bool:
    try:
        resolved = venv_root.resolve()
        return resolved in {
            (project_root / "venv").resolve(),
            (project_root / ".venv").resolve(),
        }
    except OSError:
        return False


def _ensure_venv_exists(root: Path) -> None:
    if getattr(sys, "frozen", False):
        return
    if _local_venv_python(root) is not None:
        return
    venv_dir = root / "venv"
    print("Creating virtual environment in ./venv ...", file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "venv", str(venv_dir)],
        cwd=root,
        check=True,
    )


def _reexec_with_local_venv(root: Path) -> None:
    """If launched with a non-venv interpreter, re-exec using ./venv or ./.venv when present."""
    if getattr(sys, "frozen", False):
        return
    if sys.prefix != sys.base_prefix:
        return
    venv_py = _local_venv_python(root)
    if venv_py is None:
        return
    this = Path(sys.executable).resolve()
    resolved = venv_py.resolve()
    if resolved == this:
        return
    os.execv(str(resolved), [str(resolved), *sys.argv])


def _sync_pip_dependencies(root: Path) -> None:
    if getattr(sys, "frozen", False):
        return
    if sys.prefix == sys.base_prefix:
        return
    venv_root = Path(sys.prefix)
    if not _is_project_venv(root, venv_root):
        return
    req = root / "requirements.txt"
    if not req.is_file():
        return
    stamp = venv_root / ".pip_sync_stamp"
    try:
        req_mtime = str(req.stat().st_mtime_ns)
    except OSError:
        return
    if stamp.is_file():
        try:
            if stamp.read_text(encoding="utf-8").strip() == req_mtime:
                return
        except OSError:
            pass
    print("Installing dependencies from requirements.txt ...", file=sys.stderr)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "-r",
            str(req),
        ],
        cwd=root,
        check=True,
    )
    stamp.write_text(req_mtime, encoding="utf-8")


def _bootstrap_project_environment() -> None:
    if getattr(sys, "frozen", False):
        return
    root = _project_root()
    _ensure_venv_exists(root)
    _reexec_with_local_venv(root)
    _sync_pip_dependencies(root)


def main() -> None:
    from quicktext.hotkey import start_hotkey_listener

    start_hotkey_listener()


if __name__ == "__main__":
    _bootstrap_project_environment()
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting application...")
    except Exception:
        try:
            log_path = _write_crash_log()
            print(f"Error details were written to:\n{log_path}", file=sys.stderr)
        except OSError as log_err:
            print(f"Could not write {ERROR_LOG_NAME}: {log_err}", file=sys.stderr)
            traceback.print_exc()
        sys.exit(1)
