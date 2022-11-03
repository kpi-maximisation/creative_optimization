import pandas as pd
from colormap import rgb2hex
import itertools 
import cv2
from typing import List, Tuple
from matplotlib import pyplot as plt

def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df

def return_sorted_dominant_colors(color_dict):
    sorted_dict = {
    }
    for k,v in color_dict.items():
        for i,color in enumerate(v['colors']):
            if color in sorted_dict.keys():
                if v['values'][i] > sorted_dict[color]:
                    sorted_dict[color] = v['values'][i]
            else:
                sorted_dict[color] = v['values'][i]
    val = {k: v for k, v in sorted(sorted_dict.items(), key=lambda item: int(item[1]), reverse=True)}
    return dict(itertools.islice(val.items(), 5)) 


def convert_color_dict_to_pandas_df(game_id, sorted_color_dict):
    pd_dict = {}
    for index,k in enumerate(sorted_color_dict.keys()):
        pd_dict[f'color_{index+1}'] = k
        pd_dict[f'color_{index+1}_occurance'] = sorted_color_dict[k]
    pd_dict['game_id'] = game_id
    # return pd_dict
    return pd.DataFrame(pd_dict,index=[0])


def locate_image_on_image(locate_image: str, on_image: str, prefix: str = '', visualize: bool = False, color: Tuple[int, int, int] = (0, 0, 255)):
    try:

        image = cv2.imread(on_image)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        template = cv2.imread(locate_image, 0)

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        height, width = template.shape[:2]

        top_left = max_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)

        if visualize:
            cv2.rectangle(image, top_left, bottom_right, color, 1)
            plt.figure(figsize=(10, 10))
            plt.axis('off')
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            plt.imshow(image)

        # return {f'{prefix}top_left_pos': top_left, f'{prefix}bottom_right_pos': bottom_right}
        return height, width, top_left, bottom_right

    except cv2.error as err:
        print(err)
