import os
import sys
import subprocess
import venv
import stat

# Virtual environment and dependencies setup
VENV_DIR = "venv"
REQUIREMENTS = ["pynput"]

# Ensure the virtual environment activation script is executable
def ensure_activation_permissions():
    if os.name != "nt":  # Only applies to Unix-based systems
        activate_script = os.path.join(VENV_DIR, "bin", "activate")
        if os.path.exists(activate_script):
            print("Setting execute permissions for the activation script...")
            os.chmod(activate_script, os.stat(activate_script).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

# Create and activate the virtual environment
def setup_virtual_environment():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
        ensure_activation_permissions()

    # Ensure the virtual environment is activated
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

# Install necessary libraries
def install_requirements():
    for package in REQUIREMENTS:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Main logic for hotkey detection
def main_logic():
    import json
    from pynput import keyboard

    # File that stores the triggers and sentences
    JSON_FILE = "sentences.json"

    # Ensure the JSON file exists with default values
    def ensure_json_file():
        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, "w") as file:
                json.dump({
                    "/rec": "This is the predefined text to autopopulate.",
                    "/greet": "Hello! How can I assist you today?"
                }, file)
            print(f"Created default JSON file: {JSON_FILE}")

    # Load predefined sentences from JSON
    def load_sentences():
        with open(JSON_FILE, "r") as file:
            return json.load(file)

    # Simulate typing text
    def autopopulate_text(text):
        from pynput.keyboard import Controller
        keyboard = Controller()
        for char in text:
            keyboard.type(char)

    # Start hotkey detection logic
    def start_hotkey_listener():
        from pynput.keyboard import Controller, Key

        sentences = load_sentences()
        current_input = []
        keyboard_controller = Controller()  # Controller to simulate key presses

        def on_press(key):
            nonlocal current_input
            try:
                # Append the character to the current input if it exists
                if hasattr(key, 'char') and key.char is not None:
                    current_input.append(key.char)
            except AttributeError:
                # Handle special keys
                if key == Key.space:
                    current_input.append(" ")
                elif key == Key.enter:
                    current_input.append("\n")
                elif key == Key.backspace:
                    if current_input:
                        current_input.pop()

            # Convert list of keys to string
            typed_text = "".join(current_input)
            for trigger, sentence in sentences.items():
                if typed_text.endswith(trigger):
                    print(f"Trigger detected: {trigger}")
                    # Simulate backspaces to remove the trigger from the active application
                    for _ in range(len(trigger)):
                        keyboard_controller.press(Key.backspace)
                        keyboard_controller.release(Key.backspace)
                    # Simulate typing the predefined sentence
                    autopopulate_text(sentence)
                    current_input.clear()  # Clear the input buffer
                    break  # Avoid multiple triggers being processed at once

        def on_release(key):
            if key == Key.esc:
                return False

        print("Listening for text triggers... (Press Esc to exit)")
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    # Ensure JSON file exists
    ensure_json_file()

    # Start hotkey listener
    try:
        start_hotkey_listener()
    except KeyboardInterrupt:
        print("Exiting application...")

# Main entry point
if __name__ == "__main__":
    setup_virtual_environment()
    install_requirements()
    main_logic()
