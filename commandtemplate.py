#!/usr/bin/python

import os

InstallDir = __INSTALLDIRECTORY__
AppScript = __APPSCRIPT__

os.chdir(InstallDir)
os.execve("/usr/bin/python", ("/usr/bin/python", f"{InstallDir}/{AppScript}"), os.environ)