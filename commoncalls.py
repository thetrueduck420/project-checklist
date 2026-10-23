from random import randint
import os
import config


# Resource directory
Src = "src"

# Gets a random quote
def GetQuote():
    with open(f"{Src}/welcomequotes.txt", "r") as Quotes:
        Quotes = Quotes.read()
        WelcomeQuotes = Quotes.split("\n")
    
    # Select a random quote
    Quote = randint(0, len(WelcomeQuotes) - 1)
    Quote = WelcomeQuotes[Quote]

    return Quote

# Gets the about.txt in form of a list
def GetAbout():
    # This is the text shown on the "/About" page
    with open(f"{Src}/about.txt", "r") as About:
        About = About.read()
        About = About.split("\n")
    
    return About

# Get the username
def GetName():
    return config.IntoDict()["general"]["username"]

# Returns the new projects list and configuration
def Reload(Connection, Cursor, database):
    Projects = database.ListProjects(Connection, Cursor)
    Config = config.IntoDict()

    return Projects, Config