from quicktext.hotkey import start_hotkey_listener
# from sentence_tracker import run

if __name__ == "__main__":
    try:
        # start_hotkey_listener()
        start_hotkey_listener()
    except KeyboardInterrupt:
        print("Exiting application...")
