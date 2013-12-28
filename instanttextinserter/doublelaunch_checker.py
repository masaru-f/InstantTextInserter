# encoding: shift-jis

import os
import sys

import util_win.multiplelaunch as multiplelaunch

import dialog_wrapper
import selfinfo

def check_and_dispose():
    """
    二重起動だったらメッセージを出して即座に終了する.
    """
    if multiplelaunch.is_already_running(selfinfo.WINDOWCLASSNAME):
        dialog_wrapper.ok(
            "二重起動です." + os.linesep +
            "新しく起動した方は終了します."
        )
        sys.exit(0)
