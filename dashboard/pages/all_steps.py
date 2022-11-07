from pytesseract import pytesseract
import re
import os
import signal
import ffmpeg
import pyautogui
import subprocess
from subprocess import Popen, call
from os import path
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from time import sleep
from typing import Tuple
from data_pipeline import pipeline
import streamlit as st
from PIL import Image
import pandas as pd
import cv2
import sys
import os
import extcolors
from colormap import rgb2hex
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import LabelEncoder

sys.path.append(os.path.abspath(os.path.join('./scripts')))
is_all_upload = 0
from feature_extraction_pipeline import *

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
    st.write(vals)
    if vals is not None:
        # dict_all["csv_path"] = vals[0]
        dict_all["img_start_path"] = vals[0]
        dict_all["img_end_path"] = vals[1]
        dict_all["vid_path"] = vals[2]
        return True, "Success", dict_all
    else:
        return False, "Unable to extract Assets, try again with different creative", None
    # except Exception as e:
    #     st.write("not working")
    #     return False, str(e), None



def applyButton():
    is_disabled = st.session_state['urlset'] == 1

    if st.button('Predict', disabled=not is_disabled):
        img1, img2, video = extractAssetsFromLandingPage()
