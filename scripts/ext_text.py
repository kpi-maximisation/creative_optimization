from PIL import Image
from pytesseract import pytesseract
import os
import re
import cv2
path_to_tesseract = r"/usr/bin/tesseract"


def get_frame_count(dir_path):
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count



def generate_text_from_image_series(image_dir):
   
    l=[]
    count = get_frame_count(image_dir)
    
    for i in range(count):
        image_path= image_dir + 'frame'+ str(i) + '.jpg'
        img = Image.open(image_path)
        pytesseract.tesseract_cmd = path_to_tesseract
        text = pytesseract.image_to_string(img)
        if(len(text)!=0):
            l.append(text)
    sorted(set(l), key=l.index)

    return l

