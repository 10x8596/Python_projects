import curses
from curses import wrapper

def start_screen(stdscr):

    stdscr.clear()
    stdscr.addstr("Welcome to TypeRacer!")
    stdscr.addstr("\nTest your typing speed (wpm) by typing out the phrase on screen as quick as possible without making any mistakes!")
    stdscr.addstr("\nPress any key to start typing")
    stdscr.refresh()
    # Register user's keystrokes and store in variable
    stdscr.getkey()

def wpm_test(stdscr):

    target_text = "Test your typing speed (wpm) by typing out the phrase on screen"
    current_text = []
    stdscr.clear()
    stdscr.addstr(target_text)
    stdscr.refresh()

    while True:
        key = stdscr.getkey()
        current_text.append(key)

        for char in current_text:
            stdscr.addstr(char, curses.color_pair(1))
            stdscr.addstr(char, curses.color_pair(2))

def main(stdscr):

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    wpm_test(stdscr)

wrapper(main)
