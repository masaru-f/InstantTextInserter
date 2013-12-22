#! c:/Python26/python.exe
# encoding: shift-jis

import os

from distutils.core import setup
import py2exe

"""
[bundle_files]
bundle dlls in the zipfile or the exe.
3 = don't bundle (default)
2 = bundle everything but the Python interpreter
1 = bundle everything, including the Python interpreter

[optimize]
string or int of optimization level (0, 1, or 2)
0 = don’t optimize (generate .pyc)
1 = normal optimization (like python -O)
2 = extra optimization (like python -OO)

detail of dll_excludes:
 w9xpopen.exe: win98で動作するなら必要, そのつもりはないので除外.
 mswsock.dll: win32file 利用時にバンドルされるdll, とりあえず除外.
"""
option = {
    "compressed"    : True,
    "optimize"      : 2,
    "bundle_files"  : 2,
    "dll_excludes"  : ['w9xpopen.exe',"mswsock.dll", "MSWSOCK.dll"]
}

"""
[zipfile]
name of shared zipfile to generate;
may specify a subdirectory;
defaults to 'library.zip'.
If zipfile is set to None,
the files will be bundled within the executable instead of 'library.zip'.
"""
setup(
    options = {
        "py2exe"    : option,
    },
    #console = [
    windows = [{
            "script"   : "entrypoint.py",
            "icon_resources": [(0, os.path.join("for_dist", "app.ico"))]
        },
    ],
    zipfile = None
)

