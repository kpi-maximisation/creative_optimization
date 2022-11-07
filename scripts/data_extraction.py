import cv2
import os
import ffmpeg
from subprocess import Popen, call
import subprocess
import pandas as pd



vid_path = '../video/'

def get_image_size(filename: str):
    im = cv2.imread(filename)
    return im.shape[:2]

    

def crop_video(filename: str, x_pos: float = 0, y_pos: float = 200, width: float = 650, height: float = 900) -> None:
    '''
    Function to crop a video with a location and size parameters
    '''
    input_video = ffmpeg.input(f"{filename}.mkv")
    cropped_video = ffmpeg.crop(input_video, x_pos, y_pos, width, height)
    output_video = ffmpeg.output(cropped_video, f"{filename}_cropped.mkv")
    ffmpeg.run(output_video)
    
def get_audio(filename: str):
    cmd_get_audio = f" ffmpeg -i {filename}raw_video.mkv -q:a 0 -map a {filename}audio.mp3 -y"
    fetch_audio = Popen(cmd_get_audio, stdout=subprocess.PIPE,
                        shell=True, preexec_fn=os.setsid)
    exitcode = fetch_audio.wait()


def chop_video(filename: str):
    cap = cv2.VideoCapture(f'{filename}raw_video_cropped.mkv')

    time_skips = float(500) #skip every 0.5 seconds. 
    count = 0
    success,image = cap.read()
    while success:
        if not os.path.exists(f'{filename}frames/'):
            os.makedirs(f'{filename}frames/')
        name = f'{filename}frames/frame' + str(count) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, image)     
        cap.set(cv2.CAP_PROP_POS_MSEC, 
        (count*time_skips))    
        # move the time
        success,image = cap.read()
        count += 1

    # release after reading    
    cap.release()

def get_file_names():
    links = pd.read_csv('./processed.csv').processed
    file_names =[]
    for link in links:
        file_names.append('-'.join(link.split('/')[-3:-2]))
    return file_names



        

def run():    

    # for file_ in file_names:
        
    #     if os.path.isfile(vid_path + file_ + '.mkv') and  os.path.isfile('../start_frame/' + file_ + '_start_frame.png'): 
    #         x, y = get_image_size(file_)
    #         crop_video(filename=file_ , height=x, width=y+10)
    #     else:
    #         print(f"-----------\n FILE NOT FOUND:{file_}")
    file_names = list(set(get_file_names()))
    for file_ in file_names[:5]:
        if os.path.isfile('../vid_cropped/' + file_ + '_cropped.mkv'): 
            chop_video(file_)
        else:
            print(f"-----------\n FILE NOT FOUND:{file_}")
         