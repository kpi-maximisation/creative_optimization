import streamlit as st
from PIL import Image
import pandas as pd
import cv2
import sys,os
import extcolors
from colormap import rgb2hex

sys.path.append(os.path.abspath(os.path.join('./scripts')))
from feature_extraction_pipeline import *

is_all_upload=0

def setPredictTitle():
    if 'logo' not in st.session_state:
        st.session_state['logo'] = 0
    if 'start_frame' not in st.session_state:
        st.session_state['start_frame'] = 0
    if 'frame_1' not in st.session_state:
        st.session_state['frame_1'] = 0
    if 'frame_2' not in st.session_state:
        st.session_state['frame_2'] = 0
    if 'frame_3' not in st.session_state:
        st.session_state['frame_3'] = 0
    if 'cta' not in st.session_state:
        st.session_state['cta'] = 0
    if 'end_frame' not in st.session_state:
        st.session_state['end_frame'] = 0
    st.markdown("`*` Predict KPI Using Images")
    st.write("")
    st.subheader("Please input your info about the creative AD below")
    st.write("")
    logoUpload()
    landigUpload()
    adImage1Upload()
    adImage2Upload()
    adImage3Upload()
    ctaUpload()
    endframeUpload()
    applyButton()
    # st.write(st.session_state['is_all_upload'])





def logoUpload():
    
    uploaded_file = st.file_uploader("Choose a logo")
    if uploaded_file is not None:
        st.session_state['logo']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/uploaded_files/logo.png', 'wb') as f:
            f.write(bytes_data)
        
        image = Image.open('./dashboard/uploaded_files/logo.png')

        st.image(image, caption='Logo')


def landigUpload():
    
    uploaded_file = st.file_uploader("Choose a landing image")
    if uploaded_file is not None:
        st.session_state['start_frame']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/uploaded_files/start_frame.png', 'wb') as f:
            f.write(bytes_data)
        image = Image.open('./dashboard/uploaded_files/start_frame.png')

        st.image(image, caption='Start Frame')

def adImage1Upload():
    uploaded_file = st.file_uploader("Choose Advertisement Image 1")
    if uploaded_file is not None:
        st.session_state['frame_1']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/uploaded_files/frame_1.png', 'wb') as f:
            f.write(bytes_data)
        image = Image.open('./dashboard/uploaded_files/frame_1.png')

        st.image(image, caption='Frame 1')

def adImage2Upload():
    
    uploaded_file = st.file_uploader("Choose Advertisement Image 2")
    if uploaded_file is not None:
        st.session_state['frame_2']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/uploaded_files/frame_2.png', 'wb') as f:
            f.write(bytes_data)

        image = Image.open('./dashboard/uploaded_files/frame_2.png')

        st.image(image, caption='Frame 2')

def adImage3Upload():
    
    uploaded_file = st.file_uploader("Choose Advertisement Image 3")
    if uploaded_file is not None:
        st.session_state['frame_3']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/uploaded_files/frame_3.png', 'wb') as f:
            f.write(bytes_data)
        image = Image.open('./dashboard/uploaded_files/frame_3.png')

        st.image(image, caption='Frame 3')


def ctaUpload():
    
    uploaded_file = st.file_uploader("Choose a CTA Image ")
    if uploaded_file is not None:
        st.session_state['cta']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/uploaded_files/cta.png', 'wb') as f:
            f.write(bytes_data)
        image = Image.open('./dashboard/uploaded_files/cta.png')

        st.image(image, caption='CTA')

def endframeUpload():
    
    uploaded_file = st.file_uploader("Choose a End Frame Image")
    if uploaded_file is not None:
        st.session_state['end_frame']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/uploaded_files/end_frame.png', 'wb') as f:
            f.write(bytes_data)
        image = Image.open('./dashboard/uploaded_files/end_frame.png')

        st.image(image, caption='End Frame')

def applyButton():
    is_disabled = st.session_state['logo'] == 1 and st.session_state['start_frame'] == 1 \
    and st.session_state['frame_1'] == 1 \
        and st.session_state['frame_2'] == 1 and  st.session_state['frame_3'] == 1 and \
            st.session_state['end_frame'] == 1 and st.session_state['cta'] == 1 
    if st.button('Predict', disabled=not is_disabled):
        status, message,dict_logo = getLogoFromLandingPage()
        if status:
            st.write("Logo Position Extracted")
            st.write(dict_logo)
            status, message,dict_color = getDominantColors()
            if status:
                st.write("Top 5 Dominant Colors Extracted")
                st.write(dict_color)
                status, message,dict_cta = getCTALocation()
                if status:
                    st.write("CTA Position Extracted")
                    st.write(dict_cta)
                    df = convert_color_dict_to_pandas_df("game_id",dict_color) 
                    for k,v in dict_logo.items():
                        df[k] = v
                    for k, v in dict_cta.items():
                        df[k] = v
                    df = df.drop(['game_id'], axis=1)
                    st.write("Generated csv file")
                    st.write(df)
                else:
                    st.error(message, icon="🚨")
            else:
                st.error(message, icon="🚨")
        else:
            st.error(message, icon="🚨")
        

def getLogoFromLandingPage():
    dict_logo = {}
    try:
        vals = locate_image_on_image("./dashboard/uploaded_files/logo.png", "./dashboard/uploaded_files/start_frame.png")
        st.write(vals)
        if vals is not None:
            dict_logo["logo_start_x"] = vals[2][0]
            dict_logo["logo_start_y"] = vals[2][1]
            dict_logo["logo_end_x"] = vals[3][0]
            dict_logo["logo_end_y"] = vals[3][1]
            dict_logo["logo_height"] = vals[0]
            dict_logo["logo_width"] = vals[1]
            return True ,"Success", dict_logo
        else:
            return False, "Unable to extract logo location, try again with different images", None
    except Exception as e:
        return False, str(e), None


def getDominantColors():
    color_dict = {}
    final_dict = {}
    try:
        dir = "./dashboard/uploaded_files/"
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
        return False, str(e), None


def getCTALocation():
    dict_cta = {}
    try:
        vals = locate_image_on_image("./dashboard/uploaded_files/cta.png", "./dashboard/uploaded_files/end_frame.png")
        st.write(vals)
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
        return False, str(e), None

