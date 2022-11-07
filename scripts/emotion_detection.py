import pandas as pd

# !pip install deepface

import os
import cv2
import pandas as pd
from deepface import DeepFace

df_all = pd.read_csv('../data/performance_data.csv')

import numpy as np

def get_emotion_values(names, game_id):
    df_emotion = pd.DataFrame(columns=['game_id', 'beg_frame_angry', 'beg_frame_disgust', 'beg_frame_fear',
       'beg_frame_happy', 'beg_frame_sad', 'beg_frame_surprise',
       'beg_frame_neutral', 'end_frame_angry', 'end_frame_disgust',
       'end_frame_fear', 'end_frame_happy', 'end_frame_sad',
       'end_frame_surprise', 'end_frame_neutral', 'beg_frame_age',
       'end_frame_age'])
    for name in names:
      total_prediction = {
          'game_id' : '',
          'beg_frame_angry': np.NaN,
          'beg_frame_disgust': np.NaN,
          'beg_frame_fear':np.NaN,
          'beg_frame_happy': np.NaN,
          'beg_frame_sad': np.NaN,
          'beg_frame_surprise': np.NaN,
          'beg_frame_neutral': np.NaN,
          'end_frame_angry': np.NaN,
          'end_frame_disgust': np.NaN,
          'end_frame_fear':np.NaN,
          'end_frame_happy': np.NaN,
          'end_frame_sad': np.NaN,
          'end_frame_surprise': np.NaN,
          'end_frame_neutral': np.NaN,
          'beg_frame_age' : np.NaN,
          'end_frame_age' : np.NaN
                    
                      }
      
      
      # for beginning frame
      if os.path.isfile(name + 'start_frame.png'): 
          image_path= name + 'start_frame.png'
          img = cv2.imread(image_path)
          predictions = DeepFace.analyze(img, enforce_detection=False, actions = ['age', 'emotion'])
          total_prediction['beg_frame_angry']=predictions['emotion']['angry']
          total_prediction['beg_frame_disgust']=predictions['emotion']['disgust']
          total_prediction['beg_frame_fear']=predictions['emotion']['fear']
          total_prediction['beg_frame_happy']=predictions['emotion']['happy']
          total_prediction['beg_frame_sad']=predictions['emotion']['sad']
          total_prediction['beg_frame_surprise']=predictions['emotion']['surprise']
          total_prediction['beg_frame_neutral']=predictions['emotion']['neutral']
          total_prediction['beg_frame_age']=predictions['age']
      else:
          print(f"-----------\n FILE NOT FOUND:{name}")

      # for ending frame

      if os.path.isfile(name + 'end_frame.png'): 
          image_path= name + 'end_frame.png'
          img = cv2.imread(image_path)
          predictions = DeepFace.analyze(img, enforce_detection=False, actions = ['age', 'emotion'])
          total_prediction['end_frame_angry']=predictions['emotion']['angry']
          total_prediction['end_frame_disgust']=predictions['emotion']['disgust']
          total_prediction['end_frame_fear']=predictions['emotion']['fear']
          total_prediction['end_frame_happy']=predictions['emotion']['happy']
          total_prediction['end_frame_sad']=predictions['emotion']['sad']
          total_prediction['end_frame_surprise']=predictions['emotion']['surprise']
          total_prediction['end_frame_neutral']=predictions['emotion']['neutral']
          total_prediction['end_frame_age']=predictions['age']
      else:
          print(f"-----------\n FILE NOT FOUND:{name}")
      total_prediction['game_id'] = game_id

      df = pd.DataFrame.from_dict([total_prediction])
      df_emotion = pd.concat([df,df_emotion],ignore_index=True)
      print(f"processed:{name}")
      # df_emotion.to_csv('./emotions.csv',index=False)
    return df_emotion


def run():
    names = df_all.game_id
    df_emotions = get_emotion_values(names)
    
    # return df_emotions
    df_emotions.to_csv('../data/emotion_features.csv',index=False)
