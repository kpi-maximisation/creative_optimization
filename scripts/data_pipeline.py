'''
Library for pipelining the data extraction and preprocess
'''

import pandas as pd
from feature_extract import creativeFrameExtractor


class pipeline:
    '''
    This class will take the creative csv file and extract 
    the features in pipeline manner
    '''

    def __init__(self, input_data: str, output_data: str = ''):
        self.input_path = input_data
        self.output_path = output_data
    
    def extract_assets(self, path):
        
        
    