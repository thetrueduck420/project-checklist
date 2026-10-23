#!/usr/bin/python
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from tkinter import Tk
import database
import config
import commoncalls as common
import webview
import multiprocessing

Window = Tk()
Window.geometry("800x600")

App = Flask("Project Checklist")

# Load in the server config data
Config = config.IntoDict()
Ip = Config["server"]["host"]
Port = int(Config["server"]["port"])

# Initialize database
Connection, Cursor = database.InitDb()

# Home page
@App.route("/")
def index():
    # Get a list of projects, and the configuration
    Projects, Config = common.Reload(Connection, Cursor, database)

    # Get the username, and the random quote
    Name = common.GetName()
    Quote = common.GetQuote()

    return render_template("index.html", conf=Config, projects=Projects, name=Name, quote=Quote, adress=Ip)

# About page
@App.route("/About")
def about():
    _, Config = common.Reload(Connection, Cursor, database)
    # Get the about.txt file as a list
    About = common.GetAbout()
    return render_template("about.html", conf=Config, about=About)


#
#   SETTINGS
#

# Settings page... its kinda obvious
@App.route("/Settings")
def settings():
    _, Config = common.Reload(Connection, Cursor, database)
    return render_template("settings.html", conf=Config)

# This route is used to modify settings
@App.route("/Settings/mod/", methods=["POST"])
def settingsmod():
    # Construct the new settings into a toml dictionary
    NewSettings = config.ConstructIntoConf(request.form)
    # Write the new settings
    config.WriteConf(NewSettings)
    return redirect("/Settings")

# Route for resetting all settings back to the defaults
@App.route("/Settings/reset", methods=["POST"])
def resetsettings():
    config.ResetConfig()
    return redirect("/Settings")

#
#   PROJECT ROUTES
#

@App.route("/Projects/new")
def newproject():
    _, Config = common.Reload(Connection, Cursor, database)
    return render_template("newproject.html", conf=Config)

@App.route("/Projects/delete/<projectname>")
def deleteproject(projectname):
    database.DeleteChecklist(projectname, Cursor)
    return redirect("/")

@App.route("/Projects/new/data/", methods=["POST"])
def makenewproject():
    Checklist = request.form["checklist"].split("\r\n")
    database.NewChecklist(request.form["name"], Checklist, Connection, Cursor)

    return redirect("/")

@App.route("/Projects/<projectname>")
def getchecklist(projectname):
    _, Config = common.Reload(Connection, Cursor, database)
    Project = database.ReadProject(projectname, Cursor)
    Name = projectname.replace("'", "")
    Name = Name.replace("\"", "")

    print(Project)
    return render_template("project.html", conf=Config, list=Project, name=Name)

@App.route("/Projects/mod/", methods=["POST"])
def modifychecklist():
    print(request.form)
    database.ModChecklist(request.form, Cursor)
    return redirect(f"/Projects/'{request.form["hiddenname"]}'")

def RunWeb():
    App.run(host=Ip, port=Port)

if __name__ == "__main__":
    WebProc = multiprocessing.Process(target=RunWeb)
    webview.create_window("Project Checklist", f"http://{Ip}:{Port}")

    WebProc.start()
    webview.start()
    WebProc.terminate()


    
