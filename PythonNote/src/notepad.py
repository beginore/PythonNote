from tkinter import *
from tkinter import messagebox
import ctypes
import re
import os
import pygame



pygame.init()
pygame.mixer.init()
buttonsound = pygame.mixer.Sound("button.wav")
def play_sound(event=None):
    pygame.mixer.Channel(1).play(buttonsound)


def save_file(event=None):
    with open('executor.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))
    messagebox.showinfo("File Saved", "File has been saved")  # Show message box

def execute(event=None):
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    os.system('start cmd /K "python run.py"')


def changes(event=None):
    global previousText

    if editArea.get('1.0', END) == previousText:
        return

    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)

            i += 1

    previousText = editArea.get('1.0', END)


def search_re(pattern, text):
    matches = []
    text = text.splitlines()

    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches


def rgb(rgb):
    return "#%02x%02x%02x" % rgb


ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
root.geometry('700x500')
root.title('Редактор кода')
previousText = ''

normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
font = 'Consolas 15'


repl = [
    ['(^| )(False|True|and|def|else|for|from|if|import|in|or|return|while|with|print)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
]


editArea = Text(
    root, background=background, foreground=normal, insertbackground=normal, relief=FLAT, borderwidth=30, font=font
)

editArea.pack(fill=BOTH, expand=1)

editArea.insert('1.0', """print('Hello World')
""")

editArea.bind('<KeyRelease>', changes)
root.bind('<Control-s>', save_file)
root.bind('<Control-r>', execute)
root.bind('<Key>', play_sound)


changes()
root.mainloop()