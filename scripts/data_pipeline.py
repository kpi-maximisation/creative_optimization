'''
Library for pipelining the data extraction and preprocess
'''

import pandas as pd
from feature_extract import *
from data_extraction import *
from emotion_detection import get_emotion_values
from audio_features import get_audio_features
from audio_transcribe import get_text
from text_features import text_features
from feature_extraction_pipeline import *

class pipeline:
    '''
    This class will take the creative csv file and extract 
    the features in pipeline manner
    '''

    def __init__(self, url: str = '', save_location: str = './dashboard/extracted_assets/'):
        self.input_link = url
        self.game_id = ''
        self.output_path = save_location
        self.output_path_ext = save_location

    def extract_assets(self, input_link, landing_frame: bool = True, end_frame: bool = True, video: bool = True):

        self.input_link = input_link
        self.game_id = '-'.join(self.input_link.split('/')[-3:-2])
        self.output_path_ext = self.output_path + self.game_id + '/'

        # instantiate class object
        ext = creativeFrameExtractor(self.input_link)

        # create directory if it doesn't exist
        if not os.path.exists(self.output_path_ext):
            os.makedirs(self.output_path_ext)

        # extract the assets from the Creative Ad URL
        ext.generate_preview_video_and_frames(
                [self.input_link], output_path=self.output_path_ext)
        print("Extraction complete")
        
        status, message, dict_color = getDominantColors(self.output_path_ext + 'frames/', self.game_id)
        df_color = convert_color_dict_to_pandas_df(self.game_id,dict_color) 

        
        a, v, dict_colors = getCTALocation(self.output_path_ext, self.game_id)
        
        for i,k in dict_colors.items():
            df_color[i] = k     
        
        df_color.to_csv(self.output_path_ext + 'df_color.csv', index =False)
        
        
        self.preprocess()
        
        extraction_paths = [f'{self.output_path_ext}start_frame.png',
                            f'{self.output_path_ext}end_frame.png',
                            f'{self.output_path_ext}raw_video.mkv',
                            f'{self.output_path_ext}raw_video_cropped.mkv',
                            f'{self.output_path_ext}audio.mp3', 
                            f'{self.output_path_ext}df_final.csv', 
                            
                            ]

        return extraction_paths

    def preprocess(self):
        # preprocess the assets
        # Video
        print("Started Preprocessing")
        if os.path.isfile(f'{self.output_path_ext}raw_video.mkv') and os.path.isfile(f'{self.output_path_ext}start_frame.png'):
            x, y = get_image_size(f'{self.output_path_ext}start_frame.png')
            crop_video(
                filename=f'{self.output_path_ext}raw_video', height=x, width=y+10)
            chop_video(f'{self.output_path_ext}')
            print("Video Preprocessing: Finished")
        else:
            print(
                f"-----------\n FILE NOT FOUND:{self.output_path_ext}start_frame.png")

        # Audio

        if os.path.isfile(f'{self.output_path_ext}raw_video.mkv'):
            get_audio(f'{self.output_path_ext}')
            print("Audio Preprocessing: Finished")

        # Extract deep features
        # Image Features: Emotion Detection
        df_emotion = get_emotion_values([self.output_path_ext], self.game_id)
        
        print("get_audio_features:")
        # Audio Features: Audio Features
        df_audio = get_audio_features(self.output_path_ext, self.game_id)
        
        print("get_text:")
        # Audio Features: Audio Transcription
        text = get_text(self.output_path_ext + 'audio.mp3')
        
        print("get_text_features:")
        # Audio Features: Sentiment and word count
        df_text = text_features(text, self.game_id)
        # df_text.drop(columns=['clean_text'], inplace=True)
        df_color= pd.read_csv(self.output_path_ext + 'df_color.csv')
        
        df_all = df_audio.merge(df_emotion, on='game_id', how='inner')
        df_all = df_all.merge(df_text, on='game_id', how='inner')
        df_all = df_all.merge(df_color, on='game_id', how='inner')
        df_all.to_csv(self.output_path_ext + 'df_final.csv', index=False)

        
        


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


def getCTALocation(path, game_id):
    dict_cta = {}
    print("GET CTA:" + path)
    try:
        vals = locate_image_on_image("./dashboard/extracted_assets/0a59be2e7dd53d6de11a10ce3649c081_temp/cta.png", f"{path}end_frame.png")
        if vals is not None:
            dict_cta["cta_start_x"] = vals[2][0]
            dict_cta["cta_start_y"] = vals[2][1]
            dict_cta["cta_end_x"] = vals[3][0]
            dict_cta["cta_end_y"] = vals[3][1]
            dict_cta["cta_height"] = vals[0]
            dict_cta["cta_width"] = vals[1]
            return True ,"Success", dict_cta
        else:
            return False, "Unable to extract CTA location, try again with different images", None
    except Exception as e:
        print(e)
        return False, str(e), None

