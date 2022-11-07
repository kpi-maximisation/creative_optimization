import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join('./scripts')))

import extcolors
from feature_extract import *
from data_extraction import *
from emotion_detection import get_emotion_values
from audio_features import get_audio_features
from audio_transcribe import get_text

from text_features import text_features

from feature_extraction_pipeline import *

def getDominantColors(path, game_id):
    print("GET Dominant colors:" + path)
    
    color_dict = {}
    final_dict = {}
    try:
        dir = path
        for subdir, dirs, files in os.walk(dir):
            for f in files:
                colors_x = extcolors.extract_from_path(f"{dir}/{f}", tolerance = 12, limit = 12)
                df_color = color_to_df(colors_x)
                color_dict[f] = {
                    'colors':[],
                    'values':[]
                }
                for i,row in df_color.iterrows():
                    if i >=5:
                        break
                    
                    color_dict[f]['colors'].append(row['c_code'])
                    color_dict[f]['values'].append(row['occurence'])
            break
        final_dict = return_sorted_dominant_colors(color_dict)
        return True, "Success", final_dict
    except Exception as e:
        print(e)
        return False, str(e), None
    

a, v, c = getDominantColors('./dashboard/extracted_assets/0a59be2e7dd53d6de11a10ce3649c081/frames/', '0a59be2e7dd53d6de11a10ce3649c081')


df = convert_color_dict_to_pandas_df('0a59be2e7dd53d6de11a10ce3649c081', c)
print(df)

# df_colors = pd.DataFrame.from_dict([c])
# df_colors.to_csv('./dashboard/extracted_assets/temp.csv')