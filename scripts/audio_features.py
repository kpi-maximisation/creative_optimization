import pandas as pd
from pydub import AudioSegment
import numpy as np
import os

def get_audio_features(path, game_id):
    df_audio = pd.DataFrame(columns=['game_id','audio_duration(ms)','audio_intensity','audio_frame_count'])


    audio_features = {
        'game_id': '',
        'audio_duration(ms)': np.NaN,
        'audio_intensity': np.NaN,
        'audio_frame_count': np.NaN

    }
    if os.path.isfile(path  + 'audio.mp3'):
        audio_path = path + 'audio.mp3'
        audio_segment = AudioSegment.from_file(audio_path)
        audio_features['audio_duration(ms)'] = len(audio_segment)
        audio_features['audio_intensity'] = audio_segment.dBFS
        audio_features['audio_frame_count'] = audio_segment.frame_count()

    else:
        print(f"-----------\n FILE NOT FOUND:{game_id}")
    
    audio_features['game_id'] = game_id

    df = pd.DataFrame.from_dict([audio_features])
    df_audio = pd.concat([df,df_audio],ignore_index=True)
    print(f"processed:{game_id}")
        
      # df_audio.to_csv('./audio_features.csv',index=False)
    return df_audio

def run():
    df_all = pd.read_csv('../data/performance_data.csv')
    names = df_all.game_id
    audio_path = '../data/audio/'

    df_audio = get_audio_features(audio_path, names)
    df_audio.to_csv('../data/audio_features.csv',index=False)
    print(df_audio.isnull().sum())