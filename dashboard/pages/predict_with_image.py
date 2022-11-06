import streamlit as st
from PIL import Image
import pandas as pd
import cv2
import sys,os
import extcolors
from colormap import rgb2hex
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import LabelEncoder

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
                    predict_result(df)
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



def predict_result(df):
    df_1 = df.copy()
    df_1['area'] = calc_area(df_1)
    df_1['cta_position'] = encode_coordinates(df_1)
    df_final = df_1.drop(["logo_start_x","logo_start_y","logo_end_x",
        "logo_end_y", "logo_height","cta_start_x", "cta_start_y", "cta_end_x",
        "cta_end_y","cta_height","cta_width","logo_width"],axis=1)

    numerical_cols = get_numerical_columns(df_final)
    categorical_cols = get_categorical_columns(df_final)

    categorical_cols_encoded = label_encoder(df_final)

    X=pd.DataFrame()
    X = pd.concat([X, categorical_cols_encoded], axis=1)

    scale_cols = scale_columns(X, X.columns.tolist(),range_tup=(-1,1))
    scaled_data = change_datatypes(scale_cols)
    predict_tensorflow(scaled_data)

def predict_tensorflow(df):
    model = load_model('./models/LSTM_ER 2022-11-06-01:47:47.pkl')
    # df = df[['color_1', 'color_1_occurance', 'color_2', 'color_2_occurance',
    #    'color_3', 'color_3_occurance', 'color_4', 'color_4_occurance',
    #    'color_5', 'color_5_occurance', 'cta_position', 'area']]
    df = np.asarray(df).astype(np.float32)
    result = model.predict(df)
    st.write(np.exp(result))


def get_numerical_columns(df: pd.DataFrame) -> list:
    numerical_columns = df.select_dtypes(include='number').columns.tolist()
    return numerical_columns

def get_categorical_columns(df: pd.DataFrame) -> list:
    categorical_columns = df.select_dtypes(
        include=['object']).columns.tolist()
    return categorical_columns

def label_encoder(x):
    lb = LabelEncoder()
    cat_cols = get_categorical_columns(x)
    for col in cat_cols:
        x[col] = lb.fit_transform(x[col])

    return x


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

def return_position_val(x,y):
    if x < 300 and y < 300:
        return "top_left"
    elif x < 300 and y < 600:
        return "center_left"
    elif x < 300 and y < 900:
        return "bottom_left"
    elif x < 600 and y < 300:
        return "top_center"
    elif x < 600 and y < 600:
        return "center"
    elif x < 600 and y < 900:
        return "bottom_center"
    elif x < 940 and y < 300:
        return "top_right"
    elif x < 940 and y < 600:
        return "top_center"
    else: return "bottom_right"

def encode_coordinates(df):
    encoded_val = []
    for i,row in df.iterrows():
        encoded_val.append(return_position_val(row['cta_start_x'],row['cta_start_y']))
    return encoded_val

def calc_area(df):
    area = []
    for i,row in df.iterrows():
        area.append(row['cta_width']*row['cta_height'])
    return area

def scale_column(df, column: str, range_tup: tuple = (0, 1)) -> pd.DataFrame:
    """
        Returns the objects DataFrames column normalized using Normalizer
        Parameters
    """
    try:
        std_column_df = pd.DataFrame(df[column])
        std_column_values = std_column_df.values
        minmax_scaler = MinMaxScaler(feature_range=range_tup)
        normalized_data = minmax_scaler.fit_transform(std_column_values)
        df[column] = normalized_data
        return df
    except Exception as e:
        print(f"scale_column----->{e}")


def scale_columns(df, columns: list, range_tup: tuple = (0, 1)) -> pd.DataFrame:
    try:
        for col in columns:
            df = scale_column(df, col, range_tup)
        return df
    except Exception as e:
        return None