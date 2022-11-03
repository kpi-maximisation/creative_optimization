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
class TestColorToDF(unittest.TestCase):
    
    def test_color_to_extractor(self):
        colors_x = extcolors.extract_from_path("./tests/sample/_preview.png", tolerance = 12, limit = 12)
        df_color = feature_extraction_pipeline.color_to_df(colors_x)
        color_dict= {
            'colors':[],
            'values':[]
        }
        # print(df_color.shape)
        for i,row in df_color.iterrows():
            color_dict['colors'].append(row['c_code'])
            color_dict['values'].append(row['occurence'])
        self.assertEqual(color_dict['colors'],['#132139', '#454D5A', '#050D1A', '#FFFFFF', '#3B2B24', '#E5002E', '#202121', '#000943', '#C2C5CA', '#DDA606', '#6F7176'])
        self.assertEqual(color_dict['values'],['215776', '116968', '77812', '60093', '20008', '19750', '10075', '7476', '3584', '2026', '1415'])




if __name__ == "__main__":
    unittest.main()
