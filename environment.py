import os
import sys
import subprocess
import venv
import stat

def read_requirements(file_path="requirements.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

VENV_DIR = "venv"
REQUIREMENTS = read_requirements()

def ensure_activation_permissions():
    if os.name != "nt":  # Only applies to Unix-based systems
        activate_script = os.path.join(VENV_DIR, "bin", "activate")
        if os.path.exists(activate_script):
            print("Setting execute permissions for the activation script...")
            os.chmod(activate_script, os.stat(activate_script).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def setup_virtual_environment():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
        ensure_activation_permissions()

    if "VIRTUAL_ENV" not in os.environ:
        print("Activating virtual environment...")
        activate_script = os.path.join(VENV_DIR, "Scripts", "activate") if os.name == "nt" else os.path.join(VENV_DIR, "bin", "activate")
        if os.name != "nt":
            ensure_activation_permissions()
            activate_command = f"source {activate_script} && python {sys.argv[0]}"
        else:
            activate_command = f"{activate_script} && python {sys.argv[0]}"
        os.system(activate_command)
        sys.exit()

def install_requirements():
    for package in REQUIREMENTS:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


setup_virtual_environment()
install_requirements()