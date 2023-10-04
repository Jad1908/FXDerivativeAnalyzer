# -*- coding: utf-8 -*-
"""
Web app to gather all the pricing scripts
"""

##imports
import streamlit as st
from PIL import Image

###Titles of the tab

st.set_page_config(page_title="FX Pricing",layout="wide")
# Load the image
image = Image.open(r"1280px-Logo_BCP.png")


container_0=st.container()
with container_0:
    col_1,col_2=container_0.columns([2,2])
    with col_1:
        st.markdown("<h1 style='font-size: 40px;'>FX Pricing</h1>", unsafe_allow_html=True)
    with col_2 : 
        image_width = 255
        image_height = 225
        
        # Resize the image
        resized_image = image.resize((image_width, image_height))
        
        # Display the image in the top right corner
        st.image(resized_image, use_column_width=False, clamp=True, width=image_width)


st.sidebar.header("Accueil")


####################################################################
####Partie introductive

container_1=st.container()
with container_1:


   st.markdown(
        """
        <style>
        .custom-subheader {
            font-size: 25 px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    ) 
   st.markdown(
    """
    <p class="custom-subheader">Contexte</p>
    """,
    unsafe_allow_html=True,
)

   st.markdown(
        """
        <style>
        .custom-text {
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
   st.markdown(
        """
        <p class="custom-text">
        Cette application web permet le pricing de différents instruments 
        financiers forex et l'analyse des paramètres influant sur ces derniers. 
        Choisir l'onglet correspondant à la technique que vous souhaitez utiliser
        ou
        au produit que vous souhaitez pricer.
        </p>
        """,
        unsafe_allow_html=True,
    )



  