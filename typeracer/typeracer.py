import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    """
    Clears the screen and displays the welcome message.
    """
    stdscr.clear()
    stdscr.addstr("Welcome to TypeRacer!")
    stdscr.addstr("\nTest your typing speed (wpm) by typing out the phrase on screen"
                  "\nas quick as possible without making any mistakes!")
    stdscr.addstr("\nPress any key to begin typing")
    stdscr.addstr("\nPress the esc key anytime to quit")
    stdscr.refresh()
    # Register user's keystrokes and store in variable
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    """
    Displays the target text and the user's input.
    """
    stdscr.addstr(1, 0, target)
    stdscr.addstr(0, 0, f"WPM: {wpm}")
 
    # enumerate give us the current element and its index in the list
    for i, char in enumerate(current):
        color = curses.color_pair(1)
        # if current char is not the correct char in the target text, switch colors
        if char != target[i]:
            color = curses.color_pair(2)
        stdscr.addstr(1, i, char, color)

def load_text():
    try:
        with open("textfile.txt", "r") as f:
            lines = f.readlines()
            return random.choice(lines).strip()
    except FileNotFoundError:
        return "No text file found. Please create a text file named 'text.txt' in the same directory."

def wpm_test(stdscr):
    """
    Runs the WPM test.
    """
    target_text = load_text()
    current_text = []
    wpm = 0

    start_time = time.time()
    stdscr.nodelay(True)
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        # calculate the wpm. Characters per minute divided by 5 is the words per minute assuming the average word has 5 characters
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # Ending the game
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # handle exceptions
        try:
            key = stdscr.getkey()
        except:
            continue

        # if the ordinal value of key is 27 (the ASCII representation of esc key on the keyboard)
        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
    

def main(stdscr):
    """
    Main function that initializes curses and calls the appropriate functions.
    """
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

    # option to play again
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)

