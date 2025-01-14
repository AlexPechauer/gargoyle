from hotkey import start_hotkey_listener
from sentence_tracker import run

def start_app():
    try:
        # start_hotkey_listener()
        run()
    except KeyboardInterrupt:
        print("Exiting application...")
