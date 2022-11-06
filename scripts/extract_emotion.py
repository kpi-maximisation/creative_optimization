import os
import cv2
import pandas as pd
from deepface import DeepFace



def get_emotion_values(image_dir, game_id):
   
    total_prediction = {'angry_beg': 0,
                   'disgust_beg': 0,
                   'fear_beg':0,
                   'happy_beg': 0,
                   'sad_beg': 0,
                   'surprise_beg': 0,
                   'neutral_beg': 0,
                   'angry_end': 0,
                   'disgust_end': 0,
                   'fear_end':0,
                   'happy_end': 0,
                   'sad_end': 0,
                   'surprise_end': 0,
                   'neutral_end': 0
                    }
    
    count = get_frame_count(image_dir)
    
    for i in range(count):
        image_path= image_dir + 'frame'+ str(i) + '.jpg'
        img = cv2.imread(image_path)
        predictions = DeepFace.analyze(img, enforce_detection=False)
        total_prediction['angry_beg']+=predictions['emotion']['angry']
        total_prediction['disgust_beg']+=predictions['emotion']['disgust']
        total_prediction['fear_beg']+=predictions['emotion']['fear']
        total_prediction['happy_beg']+=predictions['emotion']['happy']
        total_prediction['sad_beg']+=predictions['emotion']['sad']
        total_prediction['surprise_beg']+=predictions['emotion']['surprise']
        total_prediction['neutral_beg']+=predictions['emotion']['neutral']
    

    total_prediction['angry']/= count
    total_prediction['disgust']/= count
    total_prediction['fear']/= count
    total_prediction['happy']/= count
    total_prediction['sad']/= count
    total_prediction['surprise']/= count
    total_prediction['neutral']/= count
    total_prediction['game_id'] = game_id
    df = pd.DataFrame.from_dict([total_prediction])
    return df
    

df = pd.read_csv('./file_names.csv')

dir_list = df.game_id
df_emotion = pd.DataFrame(columns = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral', 'game_id'])
for path in dir_list:
    emotion = get_emotion_values(f'../images/{path}/', path)
    df_emotion = pd.concat([emotion,df_emotion],ignore_index=True)
    
df_emotion.to_csv('./emotion_score.csv', index=False)

