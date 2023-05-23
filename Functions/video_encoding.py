import cv2
import glob

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
    for filename in glob.glob(input_directory):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    if size!=(0,0):
        out = cv2.VideoWriter(output_directory,cv2.VideoWriter_fourcc(*'DIVX'), frame_rate, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        EraseFile('.\Capture_For_Video')



