#IDEA: SAVE EVERYTHING THROUGH THE CLOUD THROUGH GITHUB. CREATE A FUNCTION THAT SAVES AND PUSHES THE FILES AND DATA TO GITHUB OR MAYBE JUST THE DATA
#IDEA: CREATE CHROME EXTENSION THAT USER CAN ALLOW TO AUTOMATICALLY UPDATE PROGRAM WHEN READING OR WATCHING ON BROWSER

#PROGRAM CHANGES: 1. ADD AUTHOR/DIRECTOR ATTRIBUTE FOR BOOKS, MANGA, manhwa, MOVIES
#TODO: CODE LIST DETAILS, SORT, HELP, WIPE, AND EDIT (I WANT EDIT TO BE LIKE ADD APPLICATION)

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

properties = ["index", "type", "title", "lastupdated", "status", "progress", "rating", "dateadded", "datecompleted"]
now = datetime.now().strftime("%Y-%m-%d")

#def complete(arg=None): pass
#def update(arg=None): pass
#def list_media(arg=None): pass
def sort(arg=None): pass
#def delete_media(arg=None): pass
def edit(arg=None): pass
#def purge(arg=None): pass
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

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def animation(message, duration): #function to print message animation 
    clear_terminal()
    frames = [
            message,
            message + " .  ",
            message + " . .  ",
            message + " . . .  "
        ]
    for _ in range(duration):
        clear_terminal()
        for frame in frames:
            print(f"\r{frame}", end='', flush=True)
            time.sleep(0.3)

    clear_terminal()

def run_anim(msg: str, dur: int): #helper function to avoid "noneteype object not callable" error
    run_in_terminal(lambda: animation(msg, dur))

def cancel(arg=None): #cancels function and uses animation
    clear_terminal()
    get_app().exit(result=1)
    run_anim("Cancelling function", 2)

def exit(arg=""): #exits the program but runs animation first
    clear_terminal()
    save_file()
    if arg == "":
        animation("Exiting program", 2)
        clear_terminal()
        sys.exit(0)
    elif arg == "q":
        sys.exit(0)
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
    '''clear_terminal()
    print("Error! Media not found. Please make sure your spelling is correct or that you're not delusional.\n")
    time.sleep(2)
    os.system("cls" if os.name== "nt" else "clear")'''
    return False

def findNextIndex(arg=None):
    biggest = 0
    for r in rows:
        try:
            idx = int(r.get("index", 0))
        except ValueError:
            idx = 0
        if idx > biggest:
            biggest = idx
    return biggest + 1

def printIndex(arg=None):
    clear_terminal()
    nextIndex = findNextIndex()
    print(nextIndex)
    time.sleep(3)
    return

def check_for_duplicate(media): #function to check for duplicates
    global rows

    counts = {
        "anime": 0,
        "tv": 0,
        "movie": 0,
        "book": 0,
        "manga": 0,
        "manhwa": 0
    }

    target = media.strip().lower()

    for r in rows:
        title = r["title"].strip().lower()
        media_type = r["type"].strip().lower()

        if title == target and media_type in counts:
            counts[media_type] += 1

    for media_type, count in counts.items():
        if count > 1:
            return media_type, count #returns the duplicate type and the number of duplicates

    return -1, -1 #returns -1 in the sense that there are NO duplicates


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

def get_page(progress): #helper function to grab page out of progress
    page_index = progress.find("pg")
    if (page_index == -1 or
        page_index != 2 
        ):
        return None
    
    page_number = progress[page_index + 1:]

    if not page_number or not page_number.isdigit():
        return None
    
    return int(page_number)

def get_chapter(progress): #helper function to grab chapter out of progress
    chapter_index = progress.find("ch")
    if (chapter_index == -1 or
        chapter_index != 2 
        ):
        return None
    
    chapter_number = progress[chapter_index + 1 : ]

    if not chapter_number or not chapter_number.isdigit():
        return None
    
    return int(chapter_number)

def get_timestamp(progress): #helper function to grab hours and minutes out of progress
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
        
        if type_.lower() in ("anime", "tv"):
            s, e = get_season_episode(progress)
            if s is None or e is None:
                asyncio.create_task(temp_message(result_field, "Error! Please make sure the progress follows this format: 's#e#' (s for season, e for episode, # for the number)"))
                return
        elif type_.lower() in ("book"):
            page_index = progress.find("pg")
            if page_index == -1 or page_index != 0 or not progress[page_index + 1].isdigit():
                asyncio.create_task(temp_message(result_field, "Error! Please make sure the progress follows this format: 'pg#' (pg for page, # for number)"))
                return
        elif type_.lower() in ("manga", "manhwa"):
            chapter_index = progress.find("ch")
            if chapter_index == -1 or chapter_index != 0 or not progress[chapter_index + 1].isdigit():
                asyncio.create_task(temp_message(result_field, "Error! Please make sure the progress follows this format: 'ch#' (ch for chapter, # for number)"))
                return
        elif type_.lower() in ("movie"):
            colon_index = progress.find(":")
            if colon_index != 2 or not progress[0].isdigit() or not progress[1].isdigit() or not progress[3].isdigit() or not progress[4].isdigit() or len(progress) > 5:
                asyncio.create_task(temp_message(result_field, "Error! Please make sure the progress follows this format: 'hh:mm' (hh for hour, mm for minute)"))
                return

        for r in rows:
            if r["title"].lower() == title.lower():
                if r["type"].lower() == type.lower():
                    asyncio.create_task(temp_message(result_field, "Error! A media with the same name and type exists already. Please edit your attempted addition or edit the already existing media."))
                    return  

        nextIndex = findNextIndex()

        rows.append({
            "index": nextIndex,
            "type": type_,
            "title": title,
            "lastupdated": now,
            "status": status,
            "progress": progress,
            "rating": "-",
            "dateadded": now,
            "datecompleted": "-"
        })
        save_file()
        app.exit(result=0)

        # After app exits, show confirmation for 3 seconds
        clear_terminal()
        print(f"Successfully added '{title}'!")
        time.sleep(3)
        clear_terminal()


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

listadvanced = False #boolean to see if we list everything
listindef = False #boolean to let system know that indefinite listing is off (default is off but might improve code to )
def list_media(view=""): #lists everything in database and accepts arguments for specified views
    global listadvanced, listindef, rows

    if view.lower() in ("indef","indefinite"): #if argument is "indef" or "indefinite"
        listindef = True #turn on indefinite listing
        return #return now bc prompt is going to print it from now on before asking
    elif view.lower() == "stop": #if argument is "stop"
        listindef = False #turn off indefinite listing
        return #return now because function will list the media now if not returned
    elif view.lower() == "advanced":
        listadvanced = True
    elif view.lower() == "simple":
        listadvanced = False

    if not rows: 
        print("No media entries found.")
        return

    if listadvanced == False:
        clear_terminal()
        print(f"{'Title':<30} {'Type':<10} {'Status':<10} {'Progress':<10} {'Rating':<5}")
        print("-" * 75)
        for r in rows:
            print(f"{r['title']:<30} {r['type']:<10} {r['status']:<10} {r['progress']:<10} {r['rating']:<5}")
        print("\n")    
    elif listadvanced == True:
        clear_terminal()
        print(f"{'Title':<30} {'Type':<10} {'Status':<10} {'Progress':<10} {'Rating':<10} {'Date Created':<15} {'Last Updated':<15} {'Date Completed':<15}")
        print("-" * 121)
        for r in rows:
            print(f"{r['title']:<30} {r['type']:<10} {r['status']:<10} {r['progress']:<10} {r['rating']:<10} {r['dateadded']:<15} {r['lastupdated']:<15} {r['datecompleted']:<15}")
        print("\n")  

def delete_media(media): #deletes media from database
    global rows
    deletetitle = media.strip()
    matching_row = [r for r in rows if r['title'].lower() == deletetitle.lower()]
    if not matching_row:
        print(f"No media found with title {deletetitle}\n")
        return
    type, number = check_for_duplicate(media)
    if type and number != -1:
        clear_terminal()
        print("Error! You have" + number + "duplicates")
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
                clear_terminal()
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
    if not media:
        print("Please enter a media to check duplicates for")
        return
    type, numberofduplicates = check_for_duplicate(media)
    if type == -1:
        print("No duplicates was found for the media you entered.")
    elif type != -1:
        target = media.strip().lower()
        display_index = 1
        clear_terminal()
        print(f"{' ':<4} {'Title':<30} {'Type':<15} {'Status':<10} {'Progress':<10} {'Rating':<10}")
        print("-" * 80)
        for r in rows:
            title = r["title"].strip().lower()
            mediatype = r["type"].strip().lower()
            if title == target and  mediatype == type:
                print(f"{display_index:<4} {r['title']:<30} {r['type']:<15} {r['status']:<10} {r['progress']:<10} {r['rating']:<10}")
                display_index += 1
        print("\n")
        print("Error! You have multiple listings with the same name AND type. Please delete one or change the name/type of either.\n")

        #while True:
            #print("Error! You have multiple listings with the same name AND type. Please delete one or change the name/type of either.\n")
            #user_selection = input("Please choose which one would you like to delete or edit: ")
        time.sleep(3)
           
def update(media, progress = ""): #updates progress on media, accepts given progress but if not given a progress then auto updates by 1
    if check_for_existence(media) == False: #if media entered doesn't exist
        print("Unable to identify media.\n")
        return
    for r in rows:
        if r["title"].lower() == media.lower():
            if progress == "": #if no specific progress
                if r["type"] in ("anime", "tv"): #updates anime and tv shows by either 1 season or 1 episode
                    s, e = get_season_episode(r["progress"])

                    if s == None or e == None:
                        clear_terminal()
                        print("Error! There's something wrong with your progress attribute of the media you entered. Please list and edit if necessary.")
                        time.sleep(3)
                        return

                    clear_terminal()
                    while True: 
                        whichone = input("Which one would you like to update: 'season' or 'episode'? ")
                        if whichone.lower() == "season":
                            s += 1
                            e = 0
                            r["progress"] = f"s{s}e{e}"
                            r["lastupdated"] = now
                            clear_terminal()
                            print("Update successful!")
                            time.sleep(1)
                            return
                        elif whichone.lower() == "episode": 
                            e += 1
                            r["progress"] = f"s{s}e{e}"
                            r["lastupdated"] = now
                            clear_terminal()
                            print("Update successful!")
                            time.sleep(1)
                            return
                        else:
                            clear_terminal()
                            print("Not a valid answer...\n")
                            time.sleep(2)
                            clear_terminal()
                
                if r["type"] == "book": #updates books by 1 page
                    pg = get_page(r["progress"])

                    if pg == None:
                        clear_terminal()
                        print("Error! There's something wrong with your progress attribute of the media you entered. Please list and edit if necessary.")
                        time.sleep(3)
                        return
                    
                    pg += 1
                    r["progress"] = f"pg{pg}"
                    r["lastupdated"] = now
                    clear_terminal()
                    print("Update successful!")
                    time.sleep(1)
                    return

                if r["type"] in ("manga", "manhwa"): #updates manga and manhwa by 1 chapter
                    ch = get_chapter(r["progress"])

                    if ch == None:
                        clear_terminal()
                        print("Error! There's something wrong with your progress attribute of the media you entered. Please list and edit if necessary.")
                        time.sleep(3)
                        return
                    
                    ch += 1
                    r["progress"] = f"ch{ch}"
                    r["lastupdated"] = now
                    clear_terminal()
                    print("Update successful!")
                    time.sleep(1)
                    return

                if r["type"] == "movie": #prints that can't really update movie progress without specified timestamp
                    clear_terminal()
                    print("Error! We can't really update a movie progress for you without a specific timestamp. Give me a specific timestamp or just finish the movie.")
                    time.sleep(3)
                    return
                
            if r["type"] in ("anime", "tv"): #update anime and tv shows with specified season and episode
                s, e = get_season_episode(progress)
                
                if s == None or e == None:
                    clear_terminal()
                    print("Error! Please make sure the progress follows this format: 's#e#' (s for season, e for episode, # for the number)")
                    time.sleep(3)
                    return
                
                r["progress"] = f"s{s}e{e}"
                r["lastupdated"] = now
                clear_terminal()
                print("Update successful!")
                time.sleep(1)
                return

            if r["type"] == "book": #update books with specified page
                pg = get_page(progress)

                if pg == None:
                    clear_terminal()
                    print("Error! Please make sure the progress follows this format: 'pg#' (pg for page, # for number)")
                    time.sleep(3)
                    return
                
                r["progress"] = f"pg{pg}"
                r["lastupdated"] = now
                clear_terminal()
                print("Update successful!")
                time.sleep(1)
                return

            if r["type"] in ("manga", "manhwa"): #update manga and manhwa with specified chapter
                ch = get_chapter(progress)
                
                if ch == None:
                    clear_terminal()
                    print("Error! Please make sure the progress follows this format: 'ch#' (ch for chapter, # for number)")
                    time.sleep(3)
                    return
                
                r["progress"] = f"ch{ch}"
                r["lastupdated"] = now
                clear_terminal()
                print("Update successful!")
                time.sleep(1)
                return

            if r["type"] == "movie": #update movie with specificed timestamp
                hh, mm = get_timestamp(progress)
                
                if hh == None or mm == None:
                    clear_terminal()
                    print("Error! Please make sure the progress follows this format: 'hh:mm' (hh for hour, mm for minute)")
                    time.sleep(3)
                    return
                
                r["progress"] = f"{hh}:{mm}"
                r["lastupdated"] = now
                clear_terminal()
                print("Update successful!")
                time.sleep(1)
                return       

def purge(arg = ""): #function to delete all medias in csv file
    global rows
    if not rows: #announces no media to delete
        clear_terminal()
        print(f"No media to delete.\n")
        time.sleep(2)
        return
    
    confirm = input(f"Are you sure you want to delete EVERYTHING? There is no going back after this. (Y/N) ")
    if confirm.upper() == "Y":
        rows.clear_terminal()
        clear_terminal()
        print(f"Successfully purged everything")
        time.sleep(2)
        save_file()
    elif confirm.upper() == "N":
        print("Purge cancelled.\n")
    else:
        print("Uhhh...I'm just going to assume that means no. Purge cancelled.\n")
    
def prompt(): #constantly allows user to enter commands to do whatever they want
    global listindef
    try:
        while True:
            if listindef == True:
                list_media()
            x = input("Enter command: ")
            x = x.lower()
            clear_terminal()
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
            if x in ("exit", "exit q"):
                break
            # Otherwise, find the longest command key that prefixes x
            matches = [cmd for cmd in commands if x.startswith(cmd)]
            if matches:
                cmd = max(matches, key=len)          # longest wins (!exit beats !e)
                argument = x[len(cmd):].lstrip()     # allow with/without a space
                commands[cmd](argument)
            else:
                print(f"Unknown command. Enter 'help' to see all the commands\n")

    except EOFError:
        print("An error occured.")
        time.sleep(0.5)
        exit()

'''def set_prefix(new_prefix): #allows user to enter commands via prefix
    global prefix, commands
    prefix = new_prefix
    print("Your prefix is now set to '" +  "'")'''


commands = { #COMMANDS SHOULD BE AT THE BOTTOM SO THAT ALL THE FUNCTIONS ARE DEFINED
     "complete": complete,
     "update": update,
     "list": list_media,
     "sort": sort,
     "add": add_media,
     "delete": delete_media,
     "edit": edit,
     "purge": purge,
     "wipe": wipe,
     "settings": settings,
     "help": help_user,
     "exit": exit,
     "checkforduplicate": check_for_duplicate,
     "check": check,
     "index": printIndex
}


def main(): #loads files and prompts user to do whatever they want
    load_file()
    prompt()
    sys.exit(0)
if __name__ == "__main__":
    main()
