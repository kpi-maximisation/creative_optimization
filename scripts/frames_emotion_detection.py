import os
import cv2
import pandas as pd
from deepface import DeepFace

def get_frame_count(dir_path):
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count

def get_emotion_values(image_dir, game_id):
   
    total_prediction = {'angry': 0,
                   'disgust': 0,
                   'fear':0,
                   'happy': 0,
                   'sad': 0,
                   'surprise': 0,
                   'neutral': 0
                    }
    
    count = get_frame_count(image_dir)
    
    for i in range(count):
        image_path= image_dir + 'frame'+ str(i) + '.jpg'
        img = cv2.imread(image_path)
        predictions = DeepFace.analyze(img, actions = ['age', 'emotion'])
        total_prediction['angry']+=predictions['emotion']['angry']
        total_prediction['disgust']+=predictions['emotion']['disgust']
        total_prediction['fear']+=predictions['emotion']['fear']
        total_prediction['happy']+=predictions['emotion']['happy']
        total_prediction['sad']+=predictions['emotion']['sad']
        total_prediction['surprise']+=predictions['emotion']['surprise']
        total_prediction['neutral']+=predictions['emotion']['neutral']
    

    total_prediction['angry']/= count
    total_prediction['disgust']/= count
    total_prediction['fear']/= count
    total_prediction['happy']/= count
    total_prediction['sad']/= count
    total_prediction['surprise']/= count
    total_prediction['neutral']/= count
    total_prediction['game_id'] = game_id
    
    return total_prediction
    

df = pd.read_csv('./file_names.csv')

dir_list = df.game_id

for path in dir_list:
    emotions = get_emotion_values(f'../images/{path}/')
    

