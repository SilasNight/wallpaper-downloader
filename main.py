from multiprocessing.spawn import freeze_support

import requests
import FreeSimpleGUI as sg

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
    button = sg.Button("DONE",key="Done")
    layout = [[explain],
              [filepath_input,button]]

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
                    break


    with open(images_path+image_name,"wb") as file:
        file.write(image_bits.content)

if __name__ == '__main__':
    freeze_support()
    main()