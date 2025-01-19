import json
from pynput import keyboard
from pynput.keyboard import Controller, Key
import os
import json
from keyboard.key_typing import autopopulate_text

current_dir = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(current_dir, "sentences.json")

def load_sentences():
    if not os.path.exists(JSON_FILE):
        raise FileNotFoundError(f"sentences.json not found at {JSON_FILE}")
    with open(JSON_FILE, "r") as file:
        return json.load(file)
        
def start_hotkey_listener():
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