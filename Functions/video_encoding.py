import cv2
import glob
import tkinter
from tkinter.filedialog import asksaveasfile


def EraseFile(directory: "path") -> None:
    """
    :param directory: directory to erase the content
    :return: None
    """
    import os

    files=os.listdir(directory)
    for i in range(0,len(files)):
        os.remove(directory+'/'+files[i])

def encode(input_directory: "path", output_directory: "path", frame_rate: int) -> None:
    """
    :param input_directory: file with the images
    :param output_directory: directory to stock the video
    :param frame_rate: frame rate of the video
    :return: None
    """
    img_array = []
    size=(0,0)
    i=0
    for files in glob.glob(input_directory):
        filename=".\Capture_For_Video\cap{}.png".format(i)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        i+=1

    if size!=(0,0):
        out = cv2.VideoWriter(output_directory,cv2.VideoWriter_fourcc(*'DIVX'), frame_rate, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        EraseFile('.\Capture_For_Video')
        print("encode successful")
    else:
        print("error during encode")

def new_path(type: str, path: str) -> str:
    """
    :param type: extension of the file to create
    :param path: initialized path for the user
    :return: The user new path
    """
    root = tkinter.Tk()
    root.withdraw()
    root.focus_force()
    files=[('file', type), ('All Files', '*.*')]
    path = asksaveasfile(initialdir=path, filetypes=files, defaultextension=files)
    root.destroy()
    return path.name
