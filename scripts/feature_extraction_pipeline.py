import pandas as pd
from colormap import rgb2hex
import itertools 

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