# https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github
import curses
import pickle
import os
import sys

project_list = []
cursor = 0
TESTING = True
header = '''
 _____                        _____       _ _
/  ___|                      /  ___|     | (_)
\\ `--.  ___ __ _ _ __ _   _  \\ `--. _ __ | |_  ___ ___
 `--. \\/ __/ _` | '__| | | |  `--. \\ '_ \\| | |/ __/ _ \\
/\\__/ / (_| (_| | |  | |_| | /\\__/ / |_) | | | (_|  __/
\\____/ \\___\\__,_|_|   \\__, | \\____/| .__/|_|_|\\___\\___|
                       __/ |       | |
                      |___/        |_|
'''


class AbletonProject():
    def __init__(self, path):
        self.name = 'test'
        self.path = path

def quit(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()

def save():
    with open('data.dat', 'wb') as f:
        pickle.dump(project_list, f)
        f.close()


def read_keys(scr):
    global project_list
    global cursor
    k = scr.getch()
    if k == ord('q') or k == ord('Q'):
        quit(scr)
    elif k == ord('d') or k == ord('D'):
        if len(project_list) > 0:
            project_list.pop(cursor)
            save()
    elif k == ord('f') and TESTING == True:
        makeDummyAbletonProjects()
    elif k == curses.KEY_UP:
        cursor = max(cursor - 1, 0)
    elif k == curses.KEY_DOWN:
        cursor = min(cursor + 1, max(0, len(project_list)-1))


def makeDummyAbletonProjects():
    project_list = []
    project_list.append(AbletonProject('/User/whatever'))
    project_list.append(AbletonProject('/User/whatever/als'))
    save()


def main(args):
    global project_list
    if os.path.exists(os.path.join(os.getcwd(), 'data.dat')):
        with open('data.dat', 'rb') as f:
            project_list = pickle.load(f)
            f.close()
    else:
        project_list = []
    # project_list.append(args)
    scr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    scr.nodelay(True)
    scr.keypad(True)
    while True:
        scr.addstr(0, 0, header, curses.color_pair(3))
        yOff = 10
        scr.addstr(yOff, 0, "[Q]uit\t\t[S]ync\t\t[D]elete", curses.color_pair(3))
        yOff += 2
        scr.addstr(yOff, 0, "Tracked Projects:", curses.color_pair(3))
        yOff += 1
        for i, tp in enumerate(project_list):
            scr.addstr(yOff + i, 0, '\t' + tp.name)
        scr.addstr(yOff + cursor, 0, '>')

        read_keys(scr)



if __name__ == '__main__':
    main(sys.argv)
