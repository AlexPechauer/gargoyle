import os
from env_setup import setup_virtual_environment, install_requirements

# Main logic for hotkey detection
def main_logic():
    from hotkey import start_hotkey_listener
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
