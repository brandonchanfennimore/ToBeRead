#IDEA: SAVE EVERYTHING THROUGH THE CLOUD THROUGH GITHUB. CREATE A FUNCTION THAT SAVES AND PUSHES THE FILES AND DATA TO GITHUB OR MAYBE JUST THE DATA
#IDEA: CREATE CHROME EXTENSION THAT USER CAN ALLOW TO AUTOMATICALLY UPDATE PROGRAM WHEN READING OR WATCHING ON BROWSER

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

#def complete(arg=None): pass
def update(arg=None): pass
#def list_media(arg=None): pass
def sort(arg=None): pass
#def delete_media(arg=None): pass
def edit(arg=None): pass
def purge(arg=None): pass
def wipe(arg=None): pass
def settings(arg=None): pass
def help_user(arg=None): pass
#def add(arg=None): add_media() REDUCED CODE, SHOULD DO THAT FOR ALL THE ONES ABOVE THIS ONE

rows = []


def load_file(): #opens file and translate each row to a dictionary so code can easily edit
    global rows
    try:
        with open("data.csv", newline = "") as f:
            print("File opened successfully\n")
            reader = csv.reader(f)
            data = [row for row in reader if any(cell.strip() for cell in row)]  # skip blank lines
            # ensure each row maps to your properties (truncate/pad if needed)
            fixed = []
            for row in data:
                if len(row) < len(properties):
                    row = row + [""] * (len(properties) - len(row))
                elif len(row) > len(properties):
                    row = row[:len(properties)]
                fixed.append(dict(zip(properties, row)))
            rows = fixed
    except FileNotFoundError:
        print("File not found. Creating a new one...\n")
        with open("data.csv", "w", newline = "") as f:
            pass
        rows = []


def save_file(): #saves the file by writing the edited dictionaries to the rows
    try:
        with open("data.csv", "w", newline="") as f:
            csv.writer(f).writerows([[r[k] for k in properties] for r in rows])
    except IOError as e:
        print(f"An error occured while saving the file: {e}")

def animation(message, duration): #function to print message animation 
    os.system("cls" if os.name == "nt" else "clear")
    frames = [
            message,
            message + " .  ",
            message + " . .  ",
            message + " . . .  "
        ]
    for _ in range(duration):
        os.system("cls" if os.name == "nt" else "clear")
        for frame in frames:
            print(f"\r{frame}", end='', flush=True)
            time.sleep(0.3)

    os.system("cls" if os.name == "nt" else "clear")

def run_anim(msg: str, dur: int): #helper function to avoid "noneteype object not callable" error
    run_in_terminal(lambda: animation(msg, dur))

def cancel(arg=None): #cancels function and uses animation
    os.system("cls" if os.name == "nt" else "clear")
    get_app().exit(result=1)
    run_anim("Cancelling function", 2)


def exit(arg=""): #exits the program but runs animation first
    os.system("cls" if os.name == "nt" else "clear")
    save_file()
    if arg == "":
        animation("Exiting program", 2)
        os.system("cls" if os.name == "nt" else "clear")
        sys.exit()
    elif arg == "q":
        sys.exit()
    else:
        print("Sorry I don't know what you're asking for...")

async def temp_message(info_field, text, duration = 5): #function to write message below add prompt
    info_field.text = text
    get_app().invalidate()
    await asyncio.sleep(duration)
    info_field.text = ""
    get_app().invalidate()

def check_for_existence(media): #helper function to check to make sure media exists
    global rows
    for r in rows:
        if r["title"].lower() == media.lower():
            return True
    '''os.system("cls" if os.name == "nt" else "clear")
    print("Error! Media not found. Please make sure your spelling is correct or that you're not delusional.\n")
    time.sleep(2)
    os.system("cls" if os.name== "nt" else "clear")'''
    return False


def check_for_duplicate(media): #helper function to check for duplicates
    global rows

    anime = 0
    tv = 0
    movie = 0
    book = 0
    manga = 0
    manwha = 0
    for r in rows:
        if r["title"].lower() == media.lower():
            if r["type"] == "anime":
                anime += 1
            elif r["type"] == "tv":
                tv += 1
            elif r["type"] == "movie":
                movie += 1
            elif r["type"] == "book":
                book += 1
            elif r["type"] == "manga":
                manga += 1
            elif r["type"] == "manwha":
                manwha += 1

    
    if anime > 1 or tv > 1 or movie > 1 or book > 1 or manga > 1 or manwha > 1: #checks for duplicates, if so spits out list of duplicates
        return False
    
    return True #true in sense that we're all good not in that there are duplicates


def get_season_episode(progress): #helper function to grab season and episode out of progress
    season_index = progress.find("s")
    episode_index = progress.find("e")

    if (season_index != 0 or  
        season_index == -1 or  
        episode_index == -1 or
        episode_index <= season_index + 1
        ):

        return None, None
    
    season_number = progress[season_index + 1:episode_index]
    episode_number = progress[episode_index + 1:]
    
    if not season_number or not episode_number or not season_number.isdigit() or not episode_number.isdigit():
        return None, None


    return int(season_number), int(episode_number)

def get_page(progress):
    page_index = progress.find("pg")
    if (page_index == -1 or
        page_index != 2 
        ):
        return None
    
    page_number = progress[page_index + 1:]

    if not page_number or not page_number.isdigit():
        return None
    
    return int(page_number)

def get_chapter(progress):
    chapter_index = progress.find("ch")
    if (chapter_index == -1 or
        chapter_index != 2 
        ):
        return None
    
    chapter_number = progress[chapter_index + 1 : ]

    if not chapter_number or not chapter_number.isdigit():
        return None
    
    return int(chapter_number)

def get_timestamp(progress):
    colon_index = progress.find(":")
    if(colon_index == -1 or
       colon_index != 2
       ):
        return None
    hh = progress[0 : colon_index]
    mm = progress[colon_index : ]

    if not hh or not hh.isdigit() or not mm or not mm.isdigit():
        return int(hh), int(mm)

def add_media(arg=None): #function to prompt user to add media and intakes all information
    title_field = TextArea(height=1, prompt='', multiline=False)
    type_field = TextArea(height=1, prompt='', multiline=False)
    status_field = TextArea(height=1, prompt='', multiline=False)
    progress_field = TextArea(height=1, prompt='', multiline=False)
    result_field = TextArea(height=1, style="class:output", read_only=True)

    def on_submit(): #checks all prompts to make sure they obey rules and append it to the dictionary
        title = title_field.text.strip()
        type_ = type_field.text.strip()
        status = status_field.text.strip()
        progress = progress_field.text.strip()

        if not title or not type_ or not status or not progress:
            result_field.text = "Error: All fields must be filled."
            return
        
        ALLOWED_TYPES = {"anime", "manga", "manhwa", "book", "movie", "tv"}
        ALLOWED_STATUS = {"planned", "ongoing", "completed", "dropped"}


        if type_.lower() not in ALLOWED_TYPES:
            asyncio.create_task(temp_message(result_field, "Please make sure the type is one of: anime, manga, manhwa, book, movie, or tv."))
            return
        
        if status.lower() not in ALLOWED_STATUS:
            asyncio.create_task(temp_message(result_field, "Please make sure the status is one of the following: planned, ongoing, completed, or dropped."))
            return
        
        if type_.lower() == "anime" or "tv":
            s, e = get_season_episode(progress)
            if s is None or e is None:
                asyncio.create_task(temp_message(result_field, "Error! Please make sure the progress follows this format: 's#e#' (s for season, e for episode, # for the number)"))
                return
        elif type_.lower() == "book":
            page_index = progress.find("pg")
            if page_index == -1 or page_index != 0 or not progress[page_index + 1].isdigit():
                asyncio.create_task(temp_message(result_field, "Error! Please make sure the progress follows this format: 'pg#' (pg for page, # for number)"))
                return
        elif type_.lower() == "manga" or "manwha":
            chapter_index = progress.find("ch")
            if chapter_index == -1 or chapter_index != 0 or not progress[chapter_index + 1].isdigit():
                asyncio.create_task(temp_message(result_field, "Error! Please make sure the progress follows this format: 'ch#' (ch for chapter, # for number)"))
                return
        elif type_.lower() == "movie":
            colon_index = progress.find(":")
            if colon_index != 2 or not progress[0].isdigit() or not progress[1].isdigit() or not progress[3].isdigit() or not progress[4].isdigit() or len(progress) > 5:
                asyncio.create_task(temp_message(result_field, "Error! Please make sure the progress follows this format: 'hh:mm' (hh for hour, mm for minute)"))
                return

        for r in rows:
            if r["title"].lower() == title.lower():
                if r["type"].lower() == type.lower():
                    asyncio.create_task(temp_message(result_field, "Error! A media with the same name and type exists already. Please edit your attempted addition or edit the already existing media."))
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
        app.exit(result=0)

        # After app exits, show confirmation for 3 seconds
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Successfully added '{title}'!")
        time.sleep(3)
        os.system("cls" if os.name == "nt" else "clear")


    kb = KeyBindings()

    @kb.add('enter')
    def _(event): #function for easy control via keyboard for the prompts and buttons during the add function
    # Check which control currently has focus
        ctrl = event.app.layout.current_control

        try:
            # Get the underlying prompt_toolkit controls for the buttons
            button_controls = {on_submit.button, cancel.button}
        except Exception:
            button_controls = set()

        # If Enter is pressed while one of these buttons is focused,
        # let the button handle it normally (so it actually activates)
        if ctrl in button_controls:
            return  # do nothing — button handles its own Enter press

        # Otherwise (e.g., when focused on text fields), move to next widget
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

listindef = False #boolean to let system know that indefinite listing is off (default is off but might improve code to )
def list_media(view=""): #lists everything in dictionary and accepts arguments for specified views
    global listindef, rows

    if view.lower() in ("indef","indefinite"): #if argument is "indef" or "indefinite"
        listindef = True #turn on indefinite listing
        return #return now bc prompt is going to print it from now on before asking
    elif view.lower() == "stop": #if argument is "stop"
        listindef = False #turn off indefinite listing
        return #return now because function will list the media now if not returned
    
    if not rows: 
        print("No media entries found.")
        return

    print(f"{'Title':<30} {'Type':<15} {'Status':<10} {'Progress':<10}")
    print("-" * 70)
    for r in rows:
        print(f"{r['title']:<30} {r['type']:<15} {r['status']:<10} {r['progress']:<10}")
    print("\n")


def delete_media(arg=None): #deletes media from dictionary
    global rows
    deletetitle = arg.strip()
    matching_row = [r for r in rows if r['title'].lower() == deletetitle.lower()]
    if not matching_row:
        print(f"No media found with title {deletetitle}\n")
        return
    
    confirm = input(f"Are you sure you want to delete '{deletetitle}'? (Y/N) ")
    if confirm.upper() == "Y":
        print(f"deleted {deletetitle}")
        rows = [r for r in rows if r['title'].lower() != deletetitle.lower()]
        save_file()
    elif confirm.upper() == "N":
        print("Delete cancelled.\n")
    else:
        print("Uhhh...I'm just going to assume that means no. Delete cancelled.\n")
    save_file()  

def complete(media): #changes the status of a media to complete
    found = False
    for r in rows:
        if r["title"].lower() == media.lower():
            if r["status"] == "completed":
                print("Media is already completed...")
                time.sleep(3)
                os.system("cls" if os.name == "nt" else "clear")
                return
            r["status"] = "completed"
            r["progress"] = "-"
            r["lastupdated"] = now
            r["datecompleted"] = now
            found = True
            print("Completion successful!\n")
            time.sleep(1)
            break
    if not found:
        print("Unable to identify media.\n")
        return



def check(media): #user function to check media for duplicates, if so, will print all duplicates
    if check_for_duplicate(media):
        print("No media was found with no duplicates")
    elif not check_for_duplicate(media):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{'Title':<30} {'Type':<15} {'Status':<10} {'Progress':<10}")
        print("-" * 70)
        for r in rows:
            if r["title"].lower() == media.lower():
                print(f"{r['title']:<30} {r['type']:<15} {r['status']:<10} {r['progress']:<10}")
        print("\n")
        print("Error! You have multiple listings with the same name AND type. Please change the name or the type of either.\n")
        time.sleep(3)
           


def update(media, progress = ""): #updates progress on media, accepts given progress but if not given a progress then auto updates by 1
    if check_for_existence(media) == False: #if media entered doesn't exist
        print("Unable to identify media.\n")
        return
    for r in rows:
        if r["title"].lower() == media.lower():
            if progress == "": #if no specific progress
                if r["type"] == "anime" or r["type"] == "tv": #updates anime and tv shows by either 1 season or 1 episode
                    s, e = get_season_episode(r["progress"])

                    if s == None or e == None:
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Error! There's something wrong with your progress attribute of the media you entered. Please edit your media progress to match the following format: s#e#.")
                        time.sleep(3)
                        return

                    os.system("cls" if os.name == "nt" else "clear")
                    while True: 
                        whichone = input("Which one would you like to update: 'season' or 'episode'? ")
                        if whichone.lower() == "season":
                            s += 1
                            e = 0
                            r["progress"] = f"s{s}e{e}"
                            os.system("cls" if os.name == "nt" else "clear")
                            print("Update successful!")
                            time.sleep(1)
                            return
                        elif whichone.lower() == "episode": 
                            e += 1
                            r["progress"] = f"s{s}e{e}"
                            os.system("cls" if os.name == "nt" else "clear")
                            print("Update successful!")
                            time.sleep(1)
                            return
                        else:
                            os.system("cls" if os.name == "nt" else "clear")
                            print("Not a valid answer...\n")
                            time.sleep(2)
                            os.system("cls" if os.name == "nt" else "clear")
                
                if r["type"] == "book": #updates books by 1 page
                    pg = get_page(r["progress"])

                    if pg == None:
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Error! There's something wrong with your progress attribute of the media you entered. Please list and edit if necessary.")
                        time.sleep(3)
                        return
                    
                    pg += 1
                    r["progress"] = f"pg{pg}"
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Update successful!")
                    time.sleep(1)
                    return

                if r["type"] == "manga" or r["type"] == "manwha": #updates manga and manwha by 1 chapter
                    ch = get_chapter(r["progress"])

                    if ch == None:
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Error! There's something wrong with your progress attribute of the media you entered. Please list and edit if necessary.")
                        time.sleep(3)
                        return
                    
                    ch += 1
                    r["progress"] = f"ch{ch}"
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Update successful!")
                    time.sleep(1)
                    return

                if r["type"] == "movie": #prints that can't really update movie progress without specified timestamp
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Error! We can't really update a movie progress for you without a specific timestamp. Give me a specific timestamp or just finish the movie.")
                    time.sleep(3)
                    return
                
            if r["type"] == "anime" or r["type"] == "tv": #update anime and tv shows with specified season and episode
                s, e = get_season_episode(progress)
                
                if s == None or e == None:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Error! Please make sure the progress follows this format: 's#e#' (s for season, e for episode, # for the number)")
                    time.sleep(3)
                    return
                
                r["progress"] = f"s{s}e{e}"
                os.system("cls" if os.name == "nt" else "clear")
                print("Update successful!")
                time.sleep(1)
                return

            if r["type"] == "book": #update books with specified page
                pg = get_page(progress)

                if pg == None:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Error! Please make sure the progress follows this format: 'pg#' (pg for page, # for number)")
                    time.sleep(3)
                    return
                
                r["progress"] = f"pg{pg}"
                os.system("cls" if os.name == "nt" else "clear")
                print("Update successful!")
                time.sleep(1)
                return

            if r["type"] == "manga" or r["type"] == "manwha": #update manga and manwha with specified chapter
                ch = get_chapter(progress)
                
                if ch == None:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Error! Please make sure the progress follows this format: 'ch#' (ch for chapter, # for number)")
                    time.sleep(3)
                    return
                
                r["progress"] = f"ch{ch}"
                os.system("cls" if os.name == "nt" else "clear")
                print("Update successful!")
                time.sleep(1)
                return

            if r["type"] == "movie": #update movie with specificed timestamp
                hh, mm = get_timestamp(progress)
                
                if hh == None or mm == None:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Error! Please make sure the progress follows this format: 'hh:mm' (hh for hour, mm for minute)")
                    time.sleep(3)
                    return
                
                r["progress"] = f"{hh}:{mm}"
                os.system("cls" if os.name == "nt" else "clear")
                print("Update successful!")
                time.sleep(1)
                return



        


                    


def prompt(): #constantly allows user to enter commands to do whatever they want
    global listindef
    try:
        while True:
            if listindef == True:
                list_media()
            print("Your current prefix is: " + prefix)
            x = input("Enter command: ")
            x = x.lower()
            os.system("cls" if os.name == "nt" else "clear")
            # split into command + optional argument
            if ' ' in x:
                cmd_in, argument = x.split(' ', 1)
            else:
                cmd_in, argument = x, ""
            # x already read and stripped above
            # Try exact match first
            if x in commands:
                commands[x]("")
                continue

            # Otherwise, find the longest command key that prefixes x
            matches = [cmd for cmd in commands if x.startswith(cmd)]
            if matches:
                cmd = max(matches, key=len)          # longest wins (!exit beats !e)
                argument = x[len(cmd):].lstrip()     # allow with/without a space
                commands[cmd](argument)
            else:
                print(f"Unknown command. Enter '{prefix}h' to see all the commands\n")

    except EOFError:
        print("An error occured.")
        time.sleep(0.5)
        exit()


def set_prefix(new_prefix): #allows user to enter commands via prefix
    global prefix, commands
    prefix = new_prefix
    print("Your prefix is now set to '" + prefix + "'")


commands = { #COMMANDS SHOULD BE AT THE BOTTOM SO THAT ALL THE FUNCTIONS ARE DEFINED
    prefix + "complete": complete,
    prefix + "update": update,
    prefix + "list": list_media,
    prefix + "sort": sort,
    prefix + "add": add_media,
    prefix + "delete": delete_media,
    prefix + "edit": edit,
    prefix + "purge": purge,
    prefix + "wipe": wipe,
    prefix + "settings": settings,
    prefix + "help": help_user,
    prefix + "exit": exit,
    prefix + "check": check
}


def main(): #loads files and prompts user to do whatever they want
    load_file()
    prompt()
if __name__ == "__main__":
    main()
