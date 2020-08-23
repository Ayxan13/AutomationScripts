from typing import Final
import os
import sys
import shelve
import re
import subprocess

# JSON key for uic.exe
UIC_KEY: Final = "UicPath"

# JSON key for Current project dir to search for input ui files
UI_DIR_KEY: Final = "UiDir"


def set_uic(shelf: shelve.Shelf):
    if len(sys.argv) != 3:
        print("Wrong argument count")
        return

    uic_path = sys.argv[2]

    if not uic_path.endswith("uic.exe"):
        print("path doesn't end with `uic.exe`")
        return

    if not os.path.isfile(uic_path):
        print("path does not exist")
        return

    shelf[UIC_KEY] = uic_path
    shelf.sync()


def set_ui_dir(shelf: shelve.Shelf):
    if len(sys.argv) != 3:
        print("Wrong argument count")
        return

    ui_dir = sys.argv[2]

    if not os.path.isdir(ui_dir):
        print("path does not exist")
        return

    shelf[UI_DIR_KEY] = ui_dir
    shelf.sync()


def run_uic(shelf: shelve.Shelf):
    if len(sys.argv) != 3:
        print("Wrong argument count")
        return

    if UIC_KEY not in shelf or not os.path.isfile(shelf[UIC_KEY]):
        print("Uic path not set")
        return

    if UI_DIR_KEY not in shelf or not os.path.isdir(shelf[UI_DIR_KEY]):
        print("UI dir not set")
        return

    input_file = sys.argv[2]

    input_file_fmt = re.compile(r"(.+)\.ui")

    match = re.findall(input_file_fmt, input_file)

    if len(match) == 0:
        print("Input file must be in this format: file.ui")
        return

    input_file = shelf[UI_DIR_KEY] + "/" + input_file
    output_file = shelf[UI_DIR_KEY] + "/" + f'ui_{match[0]}.h'

    if not os.path.isfile(input_file):
        print(f"No File: {input_file}")
        return

    try:
        os.remove(output_file)
    except OSError:
        pass

    print(subprocess.check_output([shelf[UIC_KEY], f'{input_file}', '-o', output_file]))


def show_uic_file(shelf: shelve.Shelf):
    if len(sys.argv) != 2:
        print("Wrong argument count")
        return

    if UIC_KEY not in shelf:
        print("uic.exe path not set")
        return

    uic_path = shelf[UIC_KEY]
    print(uic_path)

    if not os.path.isfile(uic_path):
        print("Warning: uic.exe path is invalid")
        return


def show_ui_dir(shelf: shelve.Shelf):
    if len(sys.argv) != 2:
        print("Wrong argument count")
        return

    if UI_DIR_KEY not in shelf:
        print("uic.exe path not set")
        return

    ui_dir = shelf[UI_DIR_KEY]
    print(ui_dir)

    if not os.path.isdir(ui_dir):
        print("Warning: ui dir path is invalid")
        return


def main():
    
    set_uic_arg: Final = "--set-uic"
    set_ui_dir_arg: Final = "--set-ui-dir"
    run_uic_arg: Final = "--run"
    show_uic_file_arg: Final = "--uic-path"
    show_ui_dir_arg: Final = "--ui-dir-path"

    options: Final = {
        set_uic_arg: set_uic,
        set_ui_dir_arg: set_ui_dir,
        run_uic_arg: run_uic,
        show_uic_file_arg: show_uic_file,
        show_ui_dir_arg: show_ui_dir
    }

    if len(sys.argv) == 1 or sys.argv[1] not in options:
        print(f"{sys.argv[0]} {set_uic_arg} [path] # set uic.exe path")
        print(f"{sys.argv[0]} {set_ui_dir_arg} [path] # set path to directory with ui files")
        print(f"{sys.argv[0]} {run_uic_arg} [file.ui] # run uic.exe for `file.ui`")
        print(f"{sys.argv[0]} {show_uic_file_arg} # show path to uic.exe")
        print(f"{sys.argv[0]} {show_ui_dir_arg} show path to directory with ui files")
        print(f"{sys.argv[0]} --help # show this help")

    else:
        with shelve.open("run_uic.py") as shelf:
            options[sys.argv[1]](shelf)
    

if "__main__" == __name__:
    main()
