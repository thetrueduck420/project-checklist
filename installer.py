from os import listdir
from os import path as path
from os import remove
from os import makedirs
from os import chmod
from sys import argv
from shutil import copyfile
from shutil import copytree
from shutil import rmtree
import pathlib
import stat
import platform

Version = "1.0"
AppScript = "app.py"

def main():
    Home = pathlib.Path.home()

    IgnoredFiles = open("installignore", "r").read().split("\n")
    ToInstall = listdir()
    ToInstall = [File for File in ToInstall if not File in IgnoredFiles]

    DesktopTemplate = open("template.desktop", "r").read()
    CommandTemplate = open("commandtemplate.py", "r").read()

    try:
        InstallPath = argv[1]
    except:
        InstallPath = input("Please provide a path to which the program will be installed: ")
    
    if not path.exists(InstallPath):
        print("Path does not exist!")
        exit(1)
    
    InstallPath += "/.projectchecklist"

    if not path.exists(InstallPath):
        makedirs(InstallPath)

    DesktopFile = f"{Home}/.local/share/applications/projectchecklist.desktop"
    CommandFile = f"{Home}/.local/bin/projectchecklist"

    DesktopTemplate = DesktopTemplate.replace("__REPLACEVER__", Version)
    DesktopTemplate = DesktopTemplate.replace("__REPLACEEXEC__", CommandFile)

    CommandTemplate = CommandTemplate.replace("__INSTALLDIRECTORY__", f"\"{InstallPath}\"")
    CommandTemplate = CommandTemplate.replace("__APPSCRIPT__", f"\"{AppScript}\"")

    for File in ToInstall:
        InstallTo = f"{InstallPath}/{File}"

        if path.exists(InstallTo):
            if path.isdir(InstallTo):
                rmtree(InstallTo)
            
            else:
                remove(InstallTo)

        if path.isdir(File):
            copytree(File, InstallTo)
        
        else:
            copyfile(File, InstallTo)

    if platform.system() == "Windows":
        print("The application has been installed, unfortunately, the installer does not fully support windows systems, meaning that you will need to manually run the app from its app.py script.")
        exit(0)

    if path.exists(DesktopFile):
        remove(DesktopFile)
    
    if path.exists(CommandFile):
        remove(CommandFile)


    with open(DesktopFile, "w") as Desktop:
        Desktop.write(DesktopTemplate)

    with open(CommandFile, "w") as Command:
        Command.write(CommandTemplate)
    
    chmod(CommandFile, stat.S_IRWXU)
        
    


if __name__ == "__main__":
    main()