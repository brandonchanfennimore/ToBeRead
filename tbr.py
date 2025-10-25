import os 
import sys
import csv
import time
import asyncio
from datetime import datetime
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.widgets import Label, TextArea, Button
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal


properties = ["type", "title", "lastupdated", "status", "progress", "rating", "dateadded", "datecompleted"]
prefix = '!'
now = datetime.now().strftime("%Y-%m-%d")

def complete(arg=None): pass
def update(arg=None): pass
def list_media(arg=None): pass
def sort(arg=None): pass
#def delete_media(arg=None): pass
def edit(arg=None): pass
def purge(arg=None): pass
def wipe(arg=None): pass
def settings(arg=None): pass
def help_user(arg=None): pass
#def add(arg=None): add_media() REDUCED CODE, SHOULD DO THAT FOR ALL THE ONES ABOVE THIS ONE

rows = []

def load_file():
    global rows
    try:
        with open("data.csv", newline = "") as f:
            print("File opened successfully")
            rows = [dict(zip(properties, row)) for row in csv.reader(f)]
    except FileNotFoundError:
        print("File not found. Creating a new one...")
        with open("data.csv", "w", newline = "") as f:
            pass
        rows = []



def save_file():
    try:
        with open("data.csv", "w", newline="") as f:
            csv.writer(f).writerows([[r[k] for k in properties] for r in rows])
        print("File saved successfully!")
    except IOError as e:
        print(f"An error occured while saving the file: {e}")

def cancel():
    get_app().exit()
    
    def _cancel_animation():
        os.system("cls" if os.name == "nt" else "clear")
        frames = [
            "Cancelling function",
            "Cancelling function .  ",
            "Cancelling function . .  ",
            "Cancelling function . . .  "
        ]

        for _ in range(3):
            for frame in frames:
                print(f"\r{frame}", end='', flush=True)
                time.sleep(0.3)

        os.system("cls" if os.name == "nt" else "clear")

    run_in_terminal(_cancel_animation)


def exit():
    os.system("cls" if os.name == "nt" else "clear")
    save_file()
    frames = [
            "Exiting program",
            "Exiting program .  ",
            "Exiting program . .  ",
            "Exiting program . . .  "
        ]

    for i in range(2):  # Repeat animation 3 times
        for frame in frames:
            print(f"\r{frame}", end='', flush=True)
            time.sleep(0.2)
    sys.exit(0)
    run_in_terminal(_exit_cleanly)
    get_app().exit()

def add_media(arg=None):
    title_field = TextArea(height=1, prompt='', multiline=False)
    type_field = TextArea(height=1, prompt='', multiline=False)
    status_field = TextArea(height=1, prompt='', multiline=False)
    progress_field = TextArea(height=1, prompt='', multiline=False)
    result_field = TextArea(height=1, style="class:output", read_only=True)

    def on_submit():
        title = title_field.text.strip()
        type_ = type_field.text.strip()
        status = status_field.text.strip()
        progress = progress_field.text.strip()

        if not title or not type_ or not status or not progress:
            result_field.text = "Error: All fields must be filled."
            return

        rows.append({
            "type": type_,
            "title": title,
            "lastupdated": now,
            "status": status,
            "progress": progress,
            "rating": "",
            "dateadded": now,
            "datecompleted": ""
        })
        save_file()
        result_field.text = f"Successfully added: {title}"
        app.exit(result=0)

    def on_cancel():
        app.exit(result=1)
        os.system("cls" if os.name == "nt" else "clear")
        frames = [
            "Cancelling function",
            "Cancelling function .  ",
            "Cancelling function . .  ",
            "Cancelling function . . .  "
        ]

        for i in range(2):  # Repeat animation 3 times
            for frame in frames:
                print(f"\r{frame}", end='', flush=True)
                time.sleep(0.2)

    kb = KeyBindings()

    @kb.add('enter')
    def _(event):
        event.app.layout.focus_next()

    @kb.add('tab')
    def _(event):
        event.app.layout.focus_next()

    @kb.add('down')
    def _(event):
        event.app.layout.focus_next()

    @kb.add('up')
    def _(event):
        event.app.layout.focus_previous()

    @kb.add('s-tab')
    def _(event):
        event.app.layout.focus_previous()

    layout = HSplit([
        VSplit([Label("title: ", width=10), title_field]),
        VSplit([Label("type: ", width=10), type_field]),
        VSplit([Label("status: ", width=10), status_field]),
        VSplit([Label("progress: ", width=10), progress_field]),
        VSplit([Button(text="Submit", handler=on_submit)], align="LEFT"),
        VSplit([Button(text="Cancel", handler=cancel)], align="LEFT"),
        result_field,
    ])

    app = Application(layout=Layout(layout), key_bindings=kb, full_screen=True)
    result = app.run()

    if result == 1:
        # cancelled, just return to prompt normally
        return




def list_media(arg=None):
    if not rows:
        print("No media entries found.")
        return

    print(f"{'Title':<30} {'Type':<15} {'Status':<10}")
    print("-" * 60)
    for r in rows:
        print(f"{r['title']:<30} {r['type']:<15} {r['status']:<10}")



def delete_media(arg=None):
    global rows
    deletetitle = arg.strip()
    matching_row = [r for r in rows if r['title'].lower() == deletetitle.lower()]
    if not matching_row:
        print(f"No media found with title {deletetitle}")
        return
    
    confirm = input(f"Are you sure you want to delete '{deletetitle}'? Y/N")
    if confirm.upper() == "Y":
        print(f"deleted {deletetitle}")
        rows = [r for r in rows if r['title'].lower() != deletetitle.lower()]
        save_file()
    elif confirm.upper() == "N":
        print("Delete cancelled.")
    else:
        print("Uhhh...I'm just going to assume that means no. Delete cancelled.")    



def prompt():
    try:
        while True:
            print("Your current prefix is: " + prefix)
            x = input("Enter command: ")
            for cmd in commands:
                if x.startswith(cmd):
                    argument = x[len(cmd):].strip()
                    function = commands[cmd]
                    function(argument)  # call synchronously
                    break
            else:
                print("Unknown command. Enter '" + prefix + "h' to see all the commands")
    except EOFError:
        print("An error occured.")
        time.sleep(0.5)
        exit()




def set_prefix(new_prefix):
    global prefix, commands
    prefix = new_prefix
    print("Your prefix is now set to '" + prefix + "'")



commands = { #COMMANDS SHOULD BE AT THE BOTTOM SO THAT ALL THE FUNCTIONS ARE DEFINED
    prefix + "c": complete,
    prefix + "u": update,
    prefix + "l": list_media,
    prefix + "s": sort,
    prefix + "a": add_media,
    prefix + "d": delete_media,
    prefix + "e": edit,
    prefix + "p": purge,
    prefix + "w": wipe,
    prefix + "t": settings,
    prefix + "h": help_user,
    prefix + "exit": exit
}



def main():
    load_file()
    prompt()
if __name__ == "__main__":
    main()
