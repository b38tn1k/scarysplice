# https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github
import curses
import pickle
import os
import sys
import datetime
from time import sleep

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
        self.name = path.split('/')[-1]
        self.path = path
        self.als = []
        self.xmls = []
        self.is_tracked = False
        self.last_modified = None
        self.get_als_info()
        self.check_and_git_init()

    def check_and_git_init(self):
        if os.path.isdir(os.path.join(self.path, '.git')):
            self.is_tracked = True
        else:
            path = self.path.replace(' ', '\ ')
            os.system('cd && cd ' + path + ' && echo \'*.DS_Store\n*.als\' > .gitignore && git init -q')
            sleep(0.2)
            os.system('cd && cd ' + path + ' && git add .gitignore && git add .')

    def get_als_info(self):
        self.als = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f)) and '.als' in f]
        self.xmls = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f)) and '.xml' in f]
        times = []
        for als in self.als:
            times.append(os.path.getmtime(os.path.join(self.path, als)))
        if len(self.als) > 0:
            self.last_modified = datetime.datetime.fromtimestamp(max(times)).strftime('%Y-%m-%d_%H:%M')

    def make_xmls(self):
        path = self.path.replace(' ', '\ ')
        os.system('cd ' + os.path.join(path) + ' && rm *.xml ||:')
        for als in self.als:
            als = als.replace(' ', '\ ')
            os.system('cd ' + os.path.join(path) + ' && mkdir -p ' + 'backup-' + str(self.last_modified))
            target = os.path.join(path, 'backup-' + str(self.last_modified))
            os.system('cp '+ os.path.join(path, als) + ' ' + os.path.join(target , als))
            os.system('gzip -cd ' + os.path.join(path, als) + ' > ' + os.path.join(path, als.replace('.als', '.xml')))
        self.get_als_info()

    def make_als(self):
        path = self.path.replace(' ', '\ ')
        for als in self.als:
            als = als.replace(' ', '\ ')
            os.system('cd ' + os.path.join(path) + ' && mkdir -p ' + 'backup-' + str(self.last_modified) + '_deleted')
            target = os.path.join(path, 'backup-' + str(self.last_modified) + '_deleted')
            os.system('mv '+ os.path.join(path, als) + ' ' + os.path.join(target , als))
        for xml in self.xmls:
            xml = xml.replace(' ', '\ ')
            os.system('gzip ' + os.path.join(path, xml))
            sleep(1)
            xml = xml+'.gz'
            os.system('cp ' + os.path.join(path, xml) + ' ' + os.path.join(path, xml.replace('.xml.gz', '.als')))
        sleep(1)
        os.system('cd && cd ' + os.path.join(path) + ' && rm *.gz')
        self.get_als_info()


def quit(scr):
    save()
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()

def save():
    with open('data.dat', 'wb') as f:
        pickle.dump(project_list, f)
        f.close()

def refresh():
    global project_list
    dates = []
    for tp in project_list:
        tp.get_als_info()
        tp.check_and_git_init()
        dates.append(tp.last_modified)
    dates.sort()
    new_list = []
    while len(dates) != 0:
        for tp in project_list:
            if tp.last_modified == dates[0]:
                new_list.append(tp)
                dates.pop(0)
    project_list = new_list
    save()


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
            scr.erase()
    elif k == ord('r') or k == ord('R'):
        refresh()
        scr.erase()
        save()
    elif k == ord('p') or k == ord('P'):
        if len(project_list) > 0:
            project_list[cursor].make_xmls()
            save()
    elif k == ord('u') or k == ord('U'):
        if len(project_list) > 0:
            project_list[cursor].make_als()
            save()
    elif k == curses.KEY_UP:
        cursor = max(cursor - 1, 0)
    elif k == curses.KEY_DOWN:
        cursor = min(cursor + 1, max(0, (len(project_list)-1)))

def main(args=None):
    global project_list
    if os.path.exists(os.path.join(os.getcwd(), 'data.dat')):
        with open('data.dat', 'rb') as f:
            project_list = pickle.load(f)
            f.close()
        refresh()
    else:
        project_list = []
    if args is not None:
        add = True
        for tp in project_list:
            if tp.path in args:
                add = False
        if add == True:
            project_list.append(AbletonProject(args))
            save()
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
        scr.refresh()
        scr.move(0, 0)
        scr.addstr(0, 0, header, curses.color_pair(3))
        yOff = 10
        scr.addstr(yOff, 0, "[U]npack\t[P]ack", curses.color_pair(3))
        yOff += 1
        scr.addstr(yOff, 0, "[Q]uit\t\t[D]elete\t\t[R]efresh", curses.color_pair(3))
        yOff += 2
        scr.addstr(yOff, 0, "Tracked Projects:", curses.color_pair(3))
        yOff += 1
        i = 0
        for tp in project_list:
            scr.addstr(yOff + i, 0, '\t' + len(tp.name)*' ' + '\t' + str(tp.last_modified) + ' tracking: ' + str(tp.is_tracked), curses.color_pair(2)) # + '\t' + tp.path[0: 10] + '...' + tp.path[-9:]
            # scr.addstr(yOff + i, 0, '\t' + len(tp.name)*' ' + '\t' + str(tp.last_modified) + ' tracking: ', curses.color_pair(2)) # + '\t' + tp.path[0: 10] + '...' + tp.path[-9:]
            scr.addstr(yOff + i, 0, '  ' + str(i) + '\t' + tp.name)
            i += 1
        scr.addstr(yOff + cursor, 0, '>')
        scr.move(yOff + i + 1, 0)
        read_keys(scr)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
