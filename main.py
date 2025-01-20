from multiprocessing.spawn import freeze_support

import requests,winshell
import FreeSimpleGUI as sg
import time

username = winshell.desktop()[:-7]
text_file_name = "Wallpaper Downloader.txt"
filepath = fr"{username}\Documents\{text_file_name}"


def main():
    api_key = "1qT5nfSAXcr7VcrlhrzdtXw3YLReTC049uGA1Elo"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"


    request = requests.get(url)
    content = request.json()


    image_url = content["hdurl"]

    image_name = "\\"+content["date"] + ".jpg"

    explain = sg.Text("Choose the filepath where you want to download the NASA daily images to.")
    filepath_input = sg.Input("Filepath Here",key= "Path")
    check_box = sg.Checkbox("Would you like this to automatically run on startup?",key="check")
    button_choose_filepath = sg.FolderBrowse("Choose",key="file")
    button = sg.Button("DONE",key="Done")
    layout = [[explain],
              [check_box],
              [filepath_input,button_choose_filepath],
              [button]]

    window = sg.Window("wallpaper Downloader", layout=layout)
    try:
        with open(filepath, "r") as file:
            images_path = file.read()
    except FileNotFoundError:
        while True:
            event, values = window.read()
            match event:
                case "Done":

                    images_path = values["Path"]
                    if check_path(images_path):
                        window['Path'].update("Seems the filepath might not be right please check it.")
                    else:
                        with open(filepath,"w") as file:
                            file.write(images_path)

                        if values['check']:
                            make_shortcut()
                        break
                case "file":
                    images_path = values["file"]
                    window['Path'].update(images_path)
                case sg.WIN_CLOSED:
                    break
        window.close()
    try:

        with open(images_path + image_name, "rb") as file:
            file.read()

    except FileNotFoundError:
        image_bits = requests.get(image_url)
        with open(images_path+image_name,"wb") as file:
            file.write(image_bits.content)
    window.close()


def make_shortcut():
    second_part = r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    import os
    from win32com.client import Dispatch



    w_dir = fr"{username}{second_part}"
    path = fr"{w_dir}\main.exe - Shortcut.lnk"
    target = fr"{os.path.abspath(os.path.dirname(__file__))}\main.exe"



    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = w_dir
    shortcut.save()


def check_path(filepath):
    items_path = filepath.split('/')
    if ":" in items_path[0]:
        return False
    else:
        return True

if __name__ == '__main__':
    freeze_support()
    main()
    time.sleep(300)