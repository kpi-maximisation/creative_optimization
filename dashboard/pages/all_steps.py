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
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

sys.path.append(os.path.abspath(os.path.join('./scripts')))
is_all_upload = 0
from data_pipeline import pipeline
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




def applyButton():
    is_disabled = st.session_state['urlset'] == 1

    if st.button('Predict', disabled=not is_disabled):
        a, b = extractAssetsFromLandingPage()

def display_extract_result(dict_all):
    st.write("Extracted Images: ")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Landing Page")
        beg_image = Image.open(dict_all['start_frame'])
        st.image(beg_image, caption='Landing Page')
    with col2:
        st.header("Ending Frame")
        end_image = Image.open(dict_all['end_frame'])
        st.image(end_image, caption='End Frame')
    
    col1_a, col2_a = st.columns(2)
    with col1_a:
        st.header("Cropped Video")
        video_file_2 = open(dict_all['cropped_vid_path'], 'rb')
        video_bytes_2 = video_file_2.read()
        st.video(video_bytes_2)
    with col2_a:
        st.write('')
    
    
    st.write("Extracted Audio: ")
    audio_file = open(dict_all['audio_path'], 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')
    
    st.write("Extracted Dataframe: ")
    df = pd.read_csv(dict_all['df_all'])
    st.dataframe(df)  
    
    r1, r2 = predict_tensorflow(df)
    
    st.header('Prediction')
    st.write(f'Engagement Rate: {r1.flatten()[0]}' )
    st.write(f'CTR: {r2.flatten()[0]}' )


def predict_tensorflow(df):
    df.drop(columns=['game_id', 'text'], inplace=True)
    df_new = encode_df(df)
    
    model1 = load_model('./models/LSTM_ER 2022-11-06-16:49:54.pkl')
    model2 = load_model('./models/LSTM_CTR 2022-11-06-18:22:55.pkl')
    
    df_astype = np.asarray(df_new).astype(np.float32)
    result1 = model1.predict(df_astype)
    result2 = model2.predict(df_astype)
    st.write("Result Generated!")
    return result1, result2


def encode_df(df):
    # label encode 
    non_numericals = ['color_3', 'color_2', 'color_4', 'color_5', 'color_1','sentiment']
    le = LabelEncoder()
    for col in non_numericals:
        df[col+'_l_encoded'] = le.fit_transform(df[col])

    df.drop(columns=non_numericals, axis=1, inplace=True)
    df[['sentiment_a']] = 1
    df[['sentiment_b']] = 0
    
    return df

def change_datatypes(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    A simple function which changes the data types of the dataframe and returns it
    """
    try:
        data_types = dataframe.dtypes
        changes = ['float64', 'int64']
        for col in data_types.index:
            if(data_types[col] in changes):
                if(data_types[col] == 'float64'):
                    dataframe[col] = pd.to_numeric(
                        dataframe[col], downcast='float')
                elif(data_types[col] == 'int64'):
                    dataframe[col] = pd.to_numeric(
                        dataframe[col], downcast='unsigned')     
    except Exception as e:
        print(e)

    return dataframe