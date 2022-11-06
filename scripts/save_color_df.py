import unittest
import pandas as pd
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2
import extcolors

from colormap import rgb2hex

sys.path.append(os.path.abspath(os.path.join("../creative_optimization/")))

from scripts import feature_extraction_pipeline
#0b1ee11406e97cc6fb4229deeb19e6b7

def publish_color_extractor_result():
    colors_x = extcolors.extract_from_path("./scripts/sample/_preview.png", tolerance = 12, limit = 12)
    df_color = feature_extraction_pipeline.color_to_df(colors_x)
    color_dict= {
        'colors':[],
        'values':[]
    }
    # print(df_color.shape)
    with open("./scripts/sample/result.txt", 'w') as f:
        for i,row in df_color.iterrows():
            f.write(f"{row['c_code']}: {row['occurence']}\n")
            # color_dict['colors'].append(row['c_code'])
            # color_dict['values'].append(row['occurence'])
    
    
if __name__ == '__main__':
    publish_color_extractor_result()