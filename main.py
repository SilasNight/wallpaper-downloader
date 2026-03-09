"""
This is a side project that I worked on a long time ago to just get
some nice wallpapers.
"""

from multiprocessing.spawn import freeze_support

import requests
import winshell
import FreeSimpleGUI as Sg

# Getting the relevant file paths
username = winshell.desktop()[:-7]
text_file_name = "Wallpaper Downloader.txt"
filepath = fr"{username}\Documents\{text_file_name}"


def main() -> None:
    """
    The main window that will prompt the user for the folder where
    the images will be downloaded as well as downloading those pictures.
    """

    # This is my api key. It is used to get access to the pictures
    api_key = "1qT5nfSAXcr7VcrlhrzdtXw3YLReTC049uGA1Elo"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    # Getting the content from NASA website for the day
    request = requests.get(url)
    content = request.json()

    # If there is an image it gets the image url
    image_url = content["hdurl"]

    # Making the name the image will be called
    image_name = "\\" + content["date"] + ".jpg"

    # This is the settings for the window that will be displayed
    explain = Sg.Text("Choose the filepath where you want to download the NASA daily images to.")
    filepath_input = Sg.Input("Filepath Here", key="Path")
    check_box = Sg.Checkbox("Would you like this to automatically run on startup?", key="check")
    button_choose_filepath = Sg.FolderBrowse("Choose", key="file")
    button = Sg.Button("DONE", key="Done")
    layout = [[explain],
              [check_box],
              [filepath_input, button_choose_filepath],
              [button]]

    window = Sg.Window("wallpaper Downloader", layout=layout)

    # Checking if there is a folder to download to. Or if one need to
    # be set.
    images_path = ""
    try:
        with open(filepath, "r") as file:
            images_path = file.read()

    # Launching the window
    except FileNotFoundError:
        while True:
            event, values = window.read()
            match event:

                # Set the file path and make set up auto run if selected.
                case "Done":
                    images_path = values["Path"]
                    if check_path(images_path):
                        window['Path'].update("Seems the filepath might not be right please check it.")
                    else:
                        with open(filepath, "w") as file:
                            file.write(images_path)

                        if values['check']:
                            make_shortcut()
                        break

                # Selecting the file to download to in the program.
                case "file":
                    images_path = values["file"]
                    window['Path'].update(images_path)

                # If the window was closed then end the program as well.
                case Sg.WIN_CLOSED:
                    break

        window.close()

    # Check of the image has already been downloaded
    try:
        with open(images_path + image_name, "rb") as file:
            file.read()

    # Download and save the image.
    except FileNotFoundError:
        image_bits = requests.get(image_url)
        with open(images_path + image_name, "wb") as file:
            file.write(image_bits.content)
    window.close()


def make_shortcut() -> None:
    """
    This creates a shortcut from the absolute path of the program straight
    to the windows start-up folder so that it is run as the pc is started.

    Please note that depending on the method used to distribute this
    application running the application will unpack and run the program
    from a different folder which means the absolute path will not be
    where the program is located.
    """

    second_part = r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    import os
    from win32com.client import Dispatch

    # Getting the absolute path and the startup folder path
    w_dir = fr"{username}{second_part}"
    path = fr"{w_dir}\main.exe - Shortcut.lnk"
    target = fr"{os.path.abspath(os.path.dirname(__file__))}\main.exe"

    # Creating the shortcut.
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = w_dir
    shortcut.save()


def check_path(filepath_check: str) -> bool:
    """
    This checks for a common error that happened

    :param filepath_check: This is the file path that is to be checked
    :return: A boolean check
    """

    items_path = filepath_check.split('/')
    if ":" in items_path[0]:
        return False
    else:
        return True


if __name__ == '__main__':
    freeze_support()
    main()
