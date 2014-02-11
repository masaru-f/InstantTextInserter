# encoding: shift-jis

import dialog_wrapper

def func1():
    dialog_wrapper.ok("func1")
def func2():
    dialog_wrapper.ok("func22222")
def func3():
    dialog_wrapper.ok("func333333333333333333333333")

callback_map = {
    "reload"              : func1,
    "open_snippet_folder" : func2,
    "version"             : func3
}
