import json
from pynput import keyboard

# File that stores the triggers and sentences
JSON_FILE = "sentences.json"

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