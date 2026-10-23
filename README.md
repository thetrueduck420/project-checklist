# Project Checklist
Project checklist is a GUI tool for managing tasks during a project.\
It uses a flask backend, and an html, css, javascript and pywebview frontend to provide a modern interface.

---
# Installation guide
Unfortunately, the automatic installation script does not fully work on windows systems, it is still able to install the application, however a desktop shortcut or terminal command will not be available.\
I deeply apologise for this inconvenience, but i just couldnt find any proper resources on making the installer.py script compatible with Windows :[

Because of this, the guide will only provide answers for Unix-like systems.\
Support for Windows WILL be available, but may be limited.

Installing the program is very simple, you only need the installer.py script once, thats all!\
You can install the entire program by running the following command:\
`python3 installer.py`\
The installer script will take care of everything, after which you can launch the GUI using the command:\
`projectchecklist` or `projectchecklist.py`

The installer will also install a .desktop file, which you will be able to add to your desktop, along with a command in ~/.local/bin/projectchecklist.