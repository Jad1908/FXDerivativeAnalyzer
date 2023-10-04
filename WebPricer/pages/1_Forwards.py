# -*- coding: utf-8 -*-
"""
This is the web App page we'll be using to price forwards
"""

##imports
import streamlit as st
from PIL import Image
import pandas as pd

rates=pd.read_excel("data/Classeur1 (002).xlsx")
image = Image.open(r"1280px-Logo_BCP.png")


container_0=st.container()
with container_0:
    col_1,col_2=container_0.columns([2,2])
    with col_1:
        st.markdown("<h1 style='font-size: 40px;'>Forwards</h1>", unsafe_allow_html=True)
    with col_2 : 
        image_width = 255
        image_height = 225
        
        # Resize the image
        resized_image = image.resize((image_width, image_height))
        
        # Display the image in the top right corner
        st.image(resized_image, use_column_width=False, clamp=True, width=image_width)


st.sidebar.header("Forwards")

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
    <p class="custom-subheader">Description</p>
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
        Dans cette section on a la possibilité de côter des forwards rates pour 
        tous les couples formés par USD, EUR et MAD (pour un horizon inférieur à 
                                                     360 jours).
        On peut utiliser l'interpolation linéaire pour estimer les taux si on
        le souhaite.
            
        </p>
        """,
        unsafe_allow_html=True,
    )

####################MAchinery
def forward_rate(spot,base,fore,ttm):
    """
    Parameters
    ----------
    spot : float
        spot price for the conversion.
    base : float
        interest rate of the base currency.
    fore : float
        interest rate of the foreign currency.
    ttm : integer
        time to maturity in days.

    Returns
    -------
    float : the forward rate of our forward contract
    """
    
    return spot * (1+base*(ttm/360))/(1+fore*(ttm/360))



def linear_interpolation(NbDays, data_frame, col):
    """
    Perform linear interpolation to approximate the interest rate for the given number of days.

    Parameters
    ----------
    NbDays : integer
        Number of days to expiration of the contract.
    data_frame : pd.DataFrame
        The DataFrame containing our data on interest rates.
    col : str
        The name of the column for the currency.

    Returns
    -------
    float : Interpolated value of the interest rate.
    """

    # Sort the data frame based on the "Days" column
    sorted_data = data_frame.sort_values('NbDays')

    # Find the index of the two nearest data points for the given number of days
    lower_index = sorted_data['NbDays'].le(NbDays).idxmax() - 1
    upper_index = sorted_data['NbDays'].ge(NbDays).idxmax()

    if lower_index < 0:
        return sorted_data.at[upper_index, col]
    if upper_index >= len(sorted_data):
        return sorted_data.at[lower_index, col]

    # Extract the values of the two nearest data points
    lower_days, lower_value = sorted_data.at[lower_index, 'NbDays'], sorted_data.at[lower_index, col]
    upper_days, upper_value = sorted_data.at[upper_index, 'NbDays'], sorted_data.at[upper_index, col]

    # Perform linear interpolation
    interpolated_value = lower_value + (NbDays - lower_days) * (upper_value - lower_value) / (upper_days - lower_days)

    return interpolated_value




#############INPUTS###############
#currency pair
currency_pairs = ["EURUSD", "EURMAD", "USDMAD"]
selected_pair = st.selectbox("Select a currency pair:", currency_pairs)
st.write(f"You're pricing a {selected_pair} forward.")

ccy1=selected_pair[0:3]
ccy2=selected_pair[3:]


#Days to expiration
timete = st.number_input("Number of days to expiration", min_value=0, max_value=360, 
                             value=0, step=1)
st.write(timete," days to expiration")


# base interest input
container2=st.container()
with container2:
    col1 , col2 = container2.columns([5, 2])
    with col1:
        bir_input = st.number_input(f"Base interest rate ({ccy1}):", min_value=0.0, max_value=100.0, 
                                     value=0.000, step=0.0001, format='%f')
        st.write("The base interest rate is :", bir_input," %")
    with col2 :
        if st.button("Estimate base rate"):
            col='MID_'+ccy1
            base_estimated_value = linear_interpolation(timete, rates, col)*100
            st.write(f"Estimated rate for {ccy1}: {base_estimated_value} %")

# foreign interest input
container3=st.container()
with container3:
    col1, col2 = container3.columns([5,2])
    with col1:
        fir_input = st.number_input(f"Foreign interest rate ({ccy2}):", min_value=0.0, max_value=100.0, 
                             value=0.0, step=0.0001, format='%f')
        st.write("The foreign interest rate is :", fir_input," %")
    with col2: 
        if st.button("Estimate foreign rate"):
            col='MID_'+ccy2
            for_estimated_value = linear_interpolation(timete, rates, col)*100
            st.write(f"Estimated rate for {ccy2}: {for_estimated_value} %")


#spot rate
spot = st.number_input("Spot rate:", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')
st.write("The spot rate is :",spot)

###Computation
if st.button("Compute"):
    price=forward_rate(spot,bir_input/100,fir_input/100,timete)
    r_price=round(price,5)
    ps=round(price-spot,5)
    st.write(f"The forward rate for the {selected_pair} pair in {timete} days is **{r_price}**.")
    st.write(f"Swap points : {ps}.")
    




