import streamlit as st
from pages.predict_with_image import *
from pages.predict_with_video import *
from pages.all_steps import *

st.set_page_config(page_title="Dashboard", layout="wide")

def mainPage():
    st.title("Computer Vision for Creative Optimisation: KPI maximisation through image analysis")
    st.write("")
    st.header("Business Objective")
    st.markdown("""
    `*`Computer vision is a field of artificial intelligence that trains computers to
interpret and understand the visual world. Using digital images from cameras
and videos and deep learning models, machines can accurately identify and
classify objects and then react to what they “see.”
    """)
    st.markdown("""
   `*` Dynamic creative is a method of programmatic advertising in which ad
components such as headlines, descriptions, images, CTAs, etc. are changed
in real time according to parameters predefined by the advertiser. Common
parameters include the time of day, weather, location, etc.
    """)
    st.markdown("""
   `*` Develop a deep learning-based computer vision algorithm that segments
objects from creative assets and relates them to the KPI parameters of the
corresponding campaigns.
    """)
    st.write("")
    st.header("About the client")
    st.markdown("""
    `*`Your client this week is **Adludio** - an online mobile ad business. Adludio
provides the following service to its clients
    """)
    st.markdown("""
   `*` Adludio has been running a vast number of advertisements and each
advertisement has its own Creative. These creatives were made based on the
experience of designers and company needs. As a result, there is no way of
evaluating creatives during production and knowing how well they might
perform when they are served.
    """)

    st.write("")
    st.header("About the data")
    st.markdown("""
    `*`The Dataset Archive is composed of an **Assets** folder and a **performance_data** CSV file. As the names suggest the folder 
    contains the asset image used to build the creatives and the CSV file contains the performance values for each creative.
     Each folder within the **Assets** folder is a **game_id** string value and its reference performance is available in the CSV file.
    """)
    st.subheader("""
    performace_data.csv
    """)
    st.markdown("""
    `*` **game_id** - Represents a unique identifier of a creative for the performance values\n
    `*` **ER** - Represents the engagement rate score of the creative\n
    `*` **CTR** - Represents the click-through rate score of the creative
    """)
    st.write("")
    with st.expander("Extracted Features"):
        st.subheader("Extracted Features")
        st.markdown("""
            `*` **Logo and logo positions**\n
            `*` **Emotions for the human faces**\n
            `*` **The transition time between click & engagement screen**\n
            `*` **Audio Extraction**\n
            `*` **Text transcription from extracted audio**\n
            `*` **Sentiment analysis on the extracted texts**\n
            `*` **Word count (from transcribed text)**\n
            `*` **Dominant colors**\n
            `*` **The CTA button (Apply Now button in the figure above)**\n
            `*` **Transcribed text from audio.**
        """)


    st.write("")
    st.subheader("Some Plots")
    getImages()


def getImages():
    st.write("")
    image = Image.open('./dashboard/dashboard_images/cta_positions.png')
    st.image(image, caption='CTA Postions')

    with st.expander("Random Forest Result"):
        st.subheader(" `*` Engagement Rate(ER)")
        st.write("""`*` Feature Importance""")
        image = Image.open('./dashboard/dashboard_images/all_features_RF_feature_importanceER.png')
        st.image(image, caption='Feature Importance')

        st.write("""`*` Prediction vs True Value""")
        image = Image.open('./dashboard/dashboard_images/all_features_RF_predictionsER.png')
        st.image(image, caption='Predictions')

        st.subheader("Click Through(CTR) Rate")
        st.write("""`*` Feature Importance""")
        image = Image.open('./dashboard/dashboard_images/all_features_RF_feature_importanceCTR.png')
        st.image(image, caption='Feature Importance')

        st.write("""`*` Prediction vs True Value""")
        image = Image.open('./dashboard/dashboard_images/all_features_RF_predictionsCTR.png')
        st.image(image, caption='Predictions')
    
    with st.expander("Deep Learning Model Result"):
        st.subheader("""`*` Engagement Rate(ER)""")
        st.write("""`*` Validation LOSS""")
        image = Image.open('./dashboard/dashboard_images/val_loss_all_features.png')
        st.image(image, caption='loss')

        st.write("""`*` LOSS""")
        image = Image.open('./dashboard/dashboard_images/all_features_loss.png')
        st.image(image, caption='loss')

        st.write("""`*` MEAN ABSOLUTE ERROR""")
        image = Image.open('./dashboard/dashboard_images/all_features_MAE.png')
        st.image(image, caption='mae')

        st.write("""`*` MEAN STANDARD ERROR""")
        image = Image.open('./dashboard/dashboard_images/all_features_MSE.png')
        st.image(image, caption='mse')

        st.subheader("""`*` Click Through Rate(ER)""")
        st.write("""`*` Validation LOSS""")
        image = Image.open('./dashboard/dashboard_images/val_loss_all_features_CTR.png')
        st.image(image, caption='loss')

        st.write("""`*` LOSS""")
        image = Image.open('./dashboard/dashboard_images/all_features_loss_CTR.png')
        st.image(image, caption='loss')

        st.write("""`*` MEAN STANDARD ERROR""")
        image = Image.open('./dashboard/dashboard_images/all_features_MSE_CTR.png')
        st.image(image, caption='mse')


def PredictUsingImage():
    st.sidebar.markdown("# Predict KPI Using Images/Assets ❄️")
    st.title("Predict Using Images/Assets")
    setPredictTitle()

def PredictUsingVideo():
    st.sidebar.markdown("# Predict KPI Using Creative AD ❄️")
    st.title("Predict Using Creative AD Video")
    setPredictVideoTitle()

def PredictUsingLink():
    st.sidebar.markdown("# Predict KPI Using Creative AD ❄️")
    st.title("Predict Using Creative AD URL Link")
    setPredictLinkTitle()


page_names_to_funcs = {
    "Overview": mainPage,
    "Predict Using Image": PredictUsingImage,
    "Predict Using Video": PredictUsingVideo,
    "Predict Using Link" : PredictUsingLink,
} 

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()