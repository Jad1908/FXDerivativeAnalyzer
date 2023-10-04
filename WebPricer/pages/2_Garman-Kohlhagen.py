# -*- coding: utf-8 -*-
"""
This is the web App page used to price option using Garman-Kohlhagen model 
"""
##"imports
import streamlit as st
from PIL import Image
import math as m
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

image = Image.open(r"1280px-Logo_BCP.png")
sns.set(rc={"axes.facecolor":"#FFF9ED","figure.facecolor":"#FFF9ED"})
pallet = ["#682F2F","#ef6108","#280301", "#9E726F", "#e7c9c8", "#B9C0C9", "#9F8A78", "#F3AB60"]


container_0=st.container()
with container_0:
    col_1,col_2=container_0.columns([2,2])
    with col_1:
        st.markdown("<h1 style='font-size: 40px;'>Garman-Kohlhagen</h1>", unsafe_allow_html=True)
    with col_2 : 
        image_width = 255
        image_height = 225
        
        # Resize the image
        resized_image = image.resize((image_width, image_height))
        
        # Display the image in the top right corner
        st.image(resized_image, use_column_width=False, clamp=True, width=image_width)


st.sidebar.header("Garman-Kohlhagen")

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
        Le modèle de Garman-Kohlhagen est une extension du modèle de Black-Scholes 
        pour évaluer les options sur devises. Il prend en compte la volatilité des 
        taux de change et les taux d'intérêt entre les deux devises, permettant une 
        meilleure évaluation des options forex. C'est un outil essentiel pour les 
        investisseurs et les entreprises souhaitant gérer leurs risques liés aux 
        fluctuations des taux de change.
        Ici on côte des options dites vanilles, c'est à dire des Calls et des Puts 
        simples.
            
        </p>
        """,
        unsafe_allow_html=True,
    )


####Machinery 1
def d_plus(t,r_dom,r_for,v,K,spot):
    """
    Parameters
    ----------
    t : float
        time at which we want to compute the option price.
    x : float
        option price.
    v : float
        volatility.
    K : float
        strike price of the option.
    r_dom : float
        domestic risk-free interest rate.
    r_for : float
        foreign risk-free interest rate.

    Returns
    -------
    TYPE
        DESCRIPTION.
    """
    num = np.log(spot / K) + (r_dom - r_for + (v ** 2) / 2) * t / 360
    den = v * np.sqrt(t / 360)
    return num / den
    

def d_moins(t,r_dom,r_for,v,K,spot):
    """
    Parameters
    ----------
    t : float
        time at which we want to compute the option price.
    x : float
        option price.
    v : float
        volatility.
    K : float
        strike price of the option.
    r_dom : float
        domestic risk-free interest rate.
    r_for : float
        foreign risk-free interest rate.

    Returns
    -------
    TYPE
        DESCRIPTION.
    """

    num = np.log(spot / K) + (r_dom - r_for - (v ** 2) / 2) * t / 360
    den = v * np.sqrt(t / 360)
    return num / den


def GK_call(t,spot,r_dom,r_for,v,K):
    """
    Parameters
    ----------
    t : float
        time to expiration.
    x : float
        option price.
    v : float
        volatility.
    K : float
        strike price of the option.
    r_dom : float
        domestic risk-free interest rate.
    r_for : float
        foreign risk-free interest rate.

    Returns
    -------
    TYPE
        DESCRIPTION.
    """

    return spot * norm.cdf(d_plus(t, r_dom, r_for, v, K, spot)) * m.exp(-r_for * t / 360) \
           - K * m.exp(-r_dom * t / 360) * norm.cdf(d_moins(t, r_dom, r_for, v, K, spot))
           
def GK_put(t,spot,r_dom,r_for,v,K):
    """
    Parameters
    ----------
    t : float
        time to expiration.
    x : float
        option price.
    v : float
        volatility.
    K : float
        strike price of the option.
    r : float
        interest rate.

    Returns
    -------
    The value of such a put option.
    """
   
    return -spot * norm.cdf(-d_plus(t, r_dom, r_for, v, K, spot)) * m.exp(-r_for * t / 360) \
           + K * m.exp(-r_dom * t / 360) * norm.cdf(-d_moins(t, r_dom, r_for, v, K, spot))



#############INPUTS###############
#currency pair
currency_pairs = ["EURUSD", "EURMAD", "USDMAD"]
selected_pair = st.selectbox("Select a currency pair:", currency_pairs)
st.write(f"You're pricing a {selected_pair} option.")

ccy1=selected_pair[0:3]
ccy2=selected_pair[3:]


#Days to expiration
timete = st.number_input("Number of days to expiration", min_value=0, max_value=1000000, 
                             value=0, step=1)
st.write(timete," days to expiration")


#Volatility
vol = st.number_input("Volatility of the currency pair", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')/100
st.write("The volatility is :", vol*100," %")

#base rate
bir_input = st.number_input(f"Base interest rate ({ccy1}):", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')/100
st.write("The base interest rate is :", bir_input*100," %")
#foreign rate
fir_input = st.number_input(f"Foreign interest rate ({ccy2}):", min_value=0.0, max_value=100.0, 
                     value=0.0, step=0.0001, format='%f')/100
st.write("The foreign interest rate is :", fir_input*100," %")

#strike
strike = st.number_input("Strike rate:", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')
st.write("The strike rate is :",strike)

#spot
spot = st.number_input("Spot  rate:", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')
st.write("The spot rate is :",spot)

if st.button("Compute"):
    call=GK_call(timete,spot,bir_input,fir_input,vol,strike)
    put=GK_put(timete,spot,bir_input,fir_input,vol,strike)
    r_call=round(call,5)
    r_put=round(put,5)
    st.write(f"The **call price** is **{r_call}** and the **put price** is **{r_put}**.")
    

if st.button("Visualize"):
    container_vis=st.container()
    with container_vis:
        col1,col2=st.columns([1,1])
        with col1 :
            ##vol
            f=plt.figure()
            GKs_c=[]
            GKs_p=[]
            vols=np.linspace(0,1,1000)
            for v in vols: 
                GKs_c.append(GK_call(timete,spot,bir_input,fir_input,v,strike))
                GKs_p.append(GK_put(timete,spot,bir_input,fir_input,v,strike))
            plt.xlabel("Volatility")
            plt.ylabel("Option price") 
            plt.title(f"{selected_pair} forex option prices with respect to volatility (K={strike}, maturity={timete}, spot={spot})")  
            plt.plot(vols,GKs_c,color='#682F2F')
            plt.plot(vols,GKs_p,color='#ef6108')
            plt.legend(labels=["call",'put'])
            st.pyplot(f)
            
            ##maturity
            f=plt.figure()
            GKs_c=[]
            GKs_p=[]
            times=np.linspace(0,timete,500)
            for t in times: 
                GKs_c.append(GK_call(t,spot,bir_input,fir_input,vol,strike))
                GKs_p.append(GK_put(t,spot,bir_input,fir_input,vol,strike))
            plt.xlabel("Time to maturity")
            plt.ylabel("Option price") 
            plt.title(f"{selected_pair} forex option prices with respect to time to maturity (K={strike}, vol={vol}%, spot={spot})")  
            plt.plot(times,GKs_c,color='#682F2F')
            plt.plot(times,GKs_p,color='#ef6108')
            plt.legend(labels=["call",'put'])
            st.pyplot(f)
            
        with col2 :
            ##Strike
            f=plt.figure()
            GKs_c=[]
            GKs_p=[]
            strikes=np.linspace(strike-0.5,strike+0.5,1000)
            for s in strikes: 
                GKs_c.append(GK_call(timete,spot,bir_input,fir_input,vol,s))
                GKs_p.append(GK_put(timete,spot,bir_input,fir_input,vol,s))
            plt.xlabel("Strike")
            plt.ylabel("Option price") 
            plt.title(f"{selected_pair} forex option prices with respect to strike price (vol={vol}%, maturity={timete}, spot={spot})")  
            plt.plot(strikes,GKs_c,color='#682F2F')
            plt.plot(strikes,GKs_p,color='#ef6108')
            plt.axvline(x=spot, color='red', linestyle='--')
            plt.axvline(x=strike, color='blue', linestyle='--')
            plt.legend(labels=["call",'put'])
            st.pyplot(f)
    
            ###spot
            f=plt.figure()
            GKs_c=[]
            GKs_p=[]
            spots=np.linspace(spot-0.5,spot+0.5,1000)
            for sp in spots: 
                GKs_c.append(GK_call(timete,sp,bir_input,fir_input,vol,strike))
                GKs_p.append(GK_put(timete,sp,bir_input,fir_input,vol,strike))
            plt.xlabel("Spot")
            plt.ylabel("Option price") 
            plt.title(f"{selected_pair} forex option prices with respect to spot price (K={strike}, maturity={timete}, vol={vol}%)")  
            plt.plot(spots,GKs_c,color='#682F2F')
            plt.plot(spots,GKs_p,color='#ef6108')
            plt.axvline(x=spot, color='red', linestyle='--')
            plt.axvline(x=strike, color='blue', linestyle='--')
            plt.legend(labels=["call",'put'])
            
            st.pyplot(f)
            
            
        st.write("################    The spot price is in red and the strike price in blue   ################ ")