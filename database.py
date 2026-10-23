import sqlite3 as sql
import os
from pathlib import Path
from sys import platform
from re import sub

Home = Path.home()

DbName = "src/projects.db"

# Initializes the database
def InitDb():
    # We use append mode here, since we dont want to overwrite the whole thing
    open(DbName, 'a').write("")
    Connection = sql.connect(DbName, check_same_thread=False, isolation_level=None)
    Cursor = Connection.cursor()

    return Connection, Cursor

# Creates a new checklist
def NewChecklist(Name: str, Checklist: list, Cursor, Connection):
    TableItems = ""

    for Check in Checklist:
        TableItems += f"'{Check}' BOOL, "
    
    TableItems = sub(", $", "", TableItems)
    try:
        Cursor.execute(f"""
                        CREATE TABLE '{Name}' (Name,Done)
                       """)
        
        for Task in Checklist:
            Cursor.execute(f"INSERT INTO '{Name}' VALUES ('{Task}', '')")
    
    except:
        pass

# Deletes a checklist, simplest function in here
def DeleteChecklist(Name: str, Cursor):
    Cursor.execute(f"DROP TABLE '{Name}'")

# Returns a list of all projects (tables) in the database
def ListProjects(Connection, Cursor):
        Cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        List = []

        for Project in Cursor.fetchall():
            List.append(Project[0])

        return List

# Returns every task and its value from a database
def ReadProject(Name: str, Cursor):
    Cursor.execute(f"SELECT * FROM {Name}")
    return Cursor.fetchall()

# Modifies a checklist
# This is the function i had to debug the most :'D
def ModChecklist(Data, Cursor):
    Name = Data["hiddenname"]

    # Gets all tasks from a project
    Cursor.execute(f"SELECT Name FROM '{Name}'")
    Tasks = Cursor.fetchall()
    Tasks = [Task[0] for Task in Tasks]

    # Clears the project briefly
    Cursor.execute(f"UPDATE '{Name}' SET 'Done' = '' WHERE Done = 'checked' ")

    Checked = []

    for CheckBox in Data.keys():
        # If this ID is present, the task is new
        NewId = "__!NEW!__"

        # Ignore this new task if its the hidden name, or if its already in the table
        if not CheckBox in Tasks and CheckBox != "hiddenname":
            Value = "''"

            if not NewId in CheckBox:
                if Data[CheckBox] == "on":
                    Value = "'checked'"
            
            CheckBoxNoId = CheckBox.replace(NewId, "")

            # Inserts the new task into the table
            Cursor.execute(f"INSERT INTO '{Name}' VALUES ('{CheckBoxNoId}', {Value})")

        if Data[CheckBox] == "on":
            Checked.append(CheckBox)
    
    # Uodates every task
    for CheckBox in Checked:
        Cursor.execute(f"UPDATE '{Name}' SET 'Done' = 'checked' WHERE Name='{CheckBox}'")