def autopopulate_text(text):
    from pynput.keyboard import Controller
    keyboard = Controller()
    for char in text:
        keyboard.type(char)