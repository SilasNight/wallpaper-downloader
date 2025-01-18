from multiprocessing.spawn import freeze_support

import requests
import FreeSimpleGUI as sg
import time




def main():
    api_key = "1qT5nfSAXcr7VcrlhrzdtXw3YLReTC049uGA1Elo"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"


    request = requests.get(url)
    content = request.json()


    image_url = content["hdurl"]
    image_bits = requests.get(image_url)
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
        with open("filepath.txt", "r") as file:
            images_path = file.read()
    except FileNotFoundError:
        while True:
            event, values = window.read()
            match event:
                case "Done":
                    print("great")
                    images_path = values["Path"]
                    with open("filepath.txt","w") as file:
                        file.write(images_path)

                    if values['check']:
                        make_shortcut()
                    break
                case "file":
                    images_path = values["file"]
                    window['Path'].update(images_path)
                case sg.WIN_CLOSED:
                    window.close()
    try:

        with open(images_path + image_name, "rb") as file:
            file.read()
        print("was there")
    except FileNotFoundError:
        print("wasn't there")
        with open(images_path+image_name,"wb") as file:
            file.write(image_bits.content)
    window.close()

def make_shortcut():
    second_part = r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    import os,winshell
    from win32com.client import Dispatch


    username = winshell.desktop()[:-7]
    w_dir = fr"{username}{second_part}"
    path = fr"{w_dir}\main.lnk"
    target = fr"{os.path.abspath(os.path.dirname(__file__))}\main.exe"


    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = w_dir
    shortcut.save()


if __name__ == '__main__':
    freeze_support()
    main()
    time.sleep(300)