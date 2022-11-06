import streamlit as st
from PIL import Image
import os,sys
import time
import cv2
import extcolors
from colormap import rgb2hex
from pages.predict_with_image import predict_result

sys.path.append(os.path.abspath(os.path.join('./scripts')))
from feature_extraction_pipeline import *

def setPredictVideoTitle():
    if 'logo' not in st.session_state:
        st.session_state['logo'] = 0
    if 'cta' not in st.session_state:
        st.session_state['cta'] = 0
    if 'video' not in st.session_state:
        st.session_state['video'] = 0
    st.markdown("`*` Predict KPI Using Creative AD Video")
    st.write("")
    st.subheader("Please input your Creative AD Video and Assets below")
    logoUpload()
    ctaUpload()
    videoUpload()
    applyButton()


def logoUpload():
    
    uploaded_file = st.file_uploader("Choose a logo")
    if uploaded_file is not None:
        st.session_state['logo']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/video_uploaded_files/logo.png', 'wb') as f:
            f.write(bytes_data)
        
        image = Image.open('./dashboard/video_uploaded_files/logo.png')

        st.image(image, caption='Logo')

def ctaUpload():
    
    uploaded_file = st.file_uploader("Choose a CTA Image ")
    if uploaded_file is not None:
        st.session_state['cta']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/video_uploaded_files/cta.png', 'wb') as f:
            f.write(bytes_data)
        image = Image.open('./dashboard/video_uploaded_files/cta.png')

        st.image(image, caption='CTA')

def videoUpload():
    uploaded_file = st.file_uploader("Choose a Video ", type=['mp4', 'mkv'])
    if uploaded_file is not None:
        st.session_state['video']=1
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        with open('./dashboard/video_uploaded_files/video.mp4', 'wb') as f:
            f.write(bytes_data)
        # image = Image.open('./dashboard/video_uploaded_files/cta.png')

        # st.image(image, caption='CTA')
        video_file = open('./dashboard/video_uploaded_files/video.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)


def applyButton():
    is_disabled = st.session_state['logo'] == 1 and st.session_state['cta'] == 1 \
    and st.session_state['video'] == 1
    if st.button('Predict', disabled=not is_disabled):
        status, message = extractFramesFromVideo()
        if status:
            st.write(message)
            status, message,dict_color = getDominantColors()
            if status:
                st.write("Top 5 Dominant Colors Extracted")
                st.write(dict_color)
                status, message,dict_logo = getLogoFromLandingPage()
                if status:
                    st.write("Logo Position Extracted")
                    st.write(dict_logo)
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
                        # predict_result(df)
                    else:
                        st.error(message, icon="🚨")
                else:
                    st.error(message, icon="🚨")
            else:
                st.error(message, icon="🚨")
        else:
            st.error(message, icon="🚨")



def extractFramesFromVideo():
    try:
        os.system('rm -rf ./dashboard/extracted_from_video/*')
        time.sleep(2)
        cap = cv2.VideoCapture('./dashboard/video_uploaded_files/video.mp4')
        time_skips = float(1000) #skip every 0.5 seconds.
        count = 1
        success,image = cap.read()
        while success:
            name = './dashboard/extracted_from_video/frame' + str(count) + '.png'
            cv2.imwrite(name, image)
            cap.set(cv2.CAP_PROP_POS_MSEC,
            (count*time_skips))
            # move the time
            success,image = cap.read()
            count += 1
        # release after reading
        cap.release()
        return True, f"{count} Images Extracted"

    except Exception as e:
        return False, str(e)


def getDominantColors():
    color_dict = {}
    final_dict = {}
    try:
        dir = "./dashboard/extracted_from_video/"
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


def getLogoFromLandingPage():
    dict_logo = {}
    try:
        vals = locate_image_on_image("./dashboard/video_uploaded_files/logo.png", "./dashboard/extracted_from_video/frame1.png")
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

def getCTALocation():
    dict_cta = {}
    status = False
    message = ""
    try:
        for subdir, dirs, files in os.walk("./dashboard/extracted_from_video/"):
            vals = locate_image_on_image("./dashboard/video_uploaded_files/cta.png", f"./dashboard/extracted_from_video/frame{len(files)}.png")
            st.write(vals)
            if vals is not None:
                dict_cta["cta_start_x"] = vals[2][0]
                dict_cta["cta_start_y"] = vals[2][1]
                dict_cta["cta_end_x"] = vals[3][0]
                dict_cta["cta_end_y"] = vals[3][1]
                dict_cta["cta_height"] = vals[0]
                dict_cta["cta_width"] = vals[1]
                status = True
                message = "Success"
            else:
                status = False
                message = "Unable to extract CTA location, try again with different images"
            break
        return status ,message, dict_cta

    except Exception as e:
        return False, str(e), None