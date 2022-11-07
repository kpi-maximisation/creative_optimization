import os
import subprocess
from subprocess import Popen, call
from os import path
import streamlit as st
from PIL import Image
import pandas as pd
import cv2
import sys
import os
import extcolors
from colormap import rgb2hex
import numpy as np

sys.path.append(os.path.abspath(os.path.join('./scripts')))
from feature_extraction_pipeline import *
is_all_upload = 0
from data_pipeline import pipeline

data_pipe = pipeline(save_location='./dashboard/extracted_assets/')


def setPredictLinkTitle():
    if 'link' not in st.session_state:
        st.session_state['link'] = 0
    st.markdown("`*` Predict KPI From the Creative")
    st.write("")
    st.subheader("Please input the website link for the Creative Ad")
    st.write("")
    linkUpload()
    applyButton()


def linkUpload():
    url = st.text_input('Insert the URL link')
    if url is not None:
        st.session_state['url'] = url
        st.session_state['urlset'] = 1


def extractAssetsFromLandingPage():
    dict_all = {}
    st.write('running process')
    # try:
    vals = data_pipe.extract_assets(input_link = st.session_state['url'])

    if vals is not None:
        dict_all["start_frame"] = vals[0]
        dict_all["end_frame"] = vals[1]
        dict_all["raw_vid_path"] = vals[2]
        dict_all["cropped_vid_path"] = vals[3]
        dict_all["audio_path"] = vals[4]
        dict_all['df_all'] = vals[5]
        
        display_extract_result(dict_all)
        
        return True, "Success"
    
    else:
        return False, "Unable to extract Assets, try again with different creative", None
    # except Exception as e:
    #     st.write("not working")
    #     return False, str(e), None



def applyButton():
    is_disabled = st.session_state['urlset'] == 1

    if st.button('Predict', disabled=not is_disabled):
        a, b = extractAssetsFromLandingPage()

def display_extract_result(dict_all):
    st.write("Extracted Images: ")
    beg_image = Image.open(dict_all['start_frame'])
    st.image(beg_image, caption='Landing Page')
    
    end_image = Image.open(dict_all['end_frame'])
    st.image(end_image, caption='End Frame')
    
    st.write("Extracted Video: ")
    video_file = open(dict_all['raw_vid_path'], 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    
    st.write("Cropped Video: ")
    video_file_2 = open(dict_all['cropped_vid_path'], 'rb')
    video_bytes_2 = video_file_2.read()
    st.video(video_bytes_2)
    
    
    st.write("Extracted Audio: ")
    audio_file = open(dict_all['audio_path'], 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
    
    st.write("Extracted Dataframe: ")
    df = pd.read_csv(dict_all['df_all'])
    st.dataframe(df)  
    