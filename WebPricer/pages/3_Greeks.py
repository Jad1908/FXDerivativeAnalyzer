# -*- coding: utf-8 -*-
"""
This is the web App page to compute and visualize the greeks of the options.
"""


##"imports
import streamlit as st
from PIL import Image
import math as m
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

image = Image.open(r"1280px-Logo_BCP.png")
sns.set(rc={"axes.facecolor":"#FFF9ED","figure.facecolor":"#FFF9ED"})
pallet = ["#682F2F","#ef6108","#280301", "#9E726F", "#e7c9c8", "#B9C0C9", "#9F8A78", "#F3AB60"]


container_0=st.container()
with container_0:
    col_1,col_2=container_0.columns([2,2])
    with col_1:
        st.markdown("<h1 style='font-size: 40px;'>The Greeks</h1>", unsafe_allow_html=True)
    with col_2 : 
        image_width = 255
        image_height = 225
        
        # Resize the image
        resized_image = image.resize((image_width, image_height))
        
        # Display the image in the top right corner
        st.image(resized_image, use_column_width=False, clamp=True, width=image_width)


st.sidebar.header("Greeks")

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
        
        Les grecques, également connues sous le nom de "sensitivités", sont des mesures 
        utilisées en trading d'options pour évaluer le risque et la sensibilité d'une 
        option aux différents facteurs du marché. Ces facteurs comprennent le sous-jacent, 
        la volatilité, le temps restant jusqu'à l'échéance, les taux d'intérêt et les 
        variations du prix de l'actif sous-jacent.

        Les principales grecques utilisées sont les suivantes :

        - Delta : Mesure la sensibilité du prix de l'option par rapport au 
        mouvement du sous-jacent. Un delta de 0,50 signifie que pour chaque 
        augmentation de 1 unité du sous-jacent, le prix de l'option augmentera 
        d'environ 0,50 unité.

        - Gamma : Représente la sensibilité du delta par rapport aux mouvements 
        du sous-jacent. Une valeur élevée de gamma indique que le delta peut 
        changer rapidement, ce qui peut augmenter le risque d'exposition.

        - Theta : Mesure la dépréciation quotidienne de la valeur de l'option due 
        à l'écoulement du temps. Theta indique combien la valeur de l'option 
        diminue à mesure que l'échéance approche.

        - Vega : Évalue la sensibilité de l'option à la volatilité du sous-jacent. 
        Une augmentation de la volatilité entraîne généralement une augmentation
        de la valeur de l'option, et vice versa.

        - Rho (à ajouter) : Mesure la sensibilité de l'option aux variations des taux 
        d'intérêt. Une augmentation des taux d'intérêt peut entraîner une 
        augmentation de la valeur de l'option d'achat et une diminution de la 
        valeur de l'option de vente.

        En utilisant les grecques, les traders d'options peuvent mieux 
        comprendre et gérer le risque associé à leurs positions. Par exemple,
        en équilibrant les deltas ou en utilisant des stratégies basées sur 
        les variations de volatilité, ils peuvent prendre des décisions plus 
        éclairées sur la gestion de leurs portefeuilles d'options. Les grecques
        jouent donc un rôle essentiel dans l'analyse et la gestion des options, 
        en aidant les traders à adapter leurs stratégies en fonction des 
        conditions du marché et à optimiser leurs rendements potentiels.
            
        </p>
        """,
        unsafe_allow_html=True,
    )


##########Machinery#############
#functions############################################
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

###Greeks###################################################################

def delta(t,T,r_dom,r_for,v,K,spot):
    """
    delta is always postive. It's the first derivative of the option with 
    respect to the underlying price. It quantifies the option price change
    when the underlying price moves.
    Parameters
    ----------
    T : float
        maturity in days
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
    Dictionnary with the delta of the put and call.
    """
    call=norm.cdf(d_plus(T-t,r_dom,r_for,v,K,spot))
    put=call-1
    return {'Call':call,
            'Put':put ,
            'Greek':'Delta'}
    
def gamma(t,T,r_dom,r_for,v,K,spot):
    """
    gamma is always positive. It's the second derivative of the option with 
    respect to the underlying price. It quantifies the changes of delta when the
    underlying price changes.
    Parameters
    ----------
    T : float
        maturity in days
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
    None.
    """
    call=norm.pdf(d_plus(T-t,r_dom,r_for,v,K,spot))/(v*spot*np.sqrt((T-t)/360))
    put=call
    return {'Call':call,
            'Put':put,
            'Greek':'Gamma'}

def vega(t,T,r_dom,r_for,v,K,spot):
    """
    vega is the sensitivity of the option price to the implied volatility. It's
    a useful tool to gauge the changes in market sentiment and conditions.'
    Parameters
    ----------
    T : float
        maturity in days
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
    Dictionnary with the vega of the put and call.
    """
    call=norm.pdf(d_plus(T-t,r_dom,r_for,v,K,spot))*spot*np.sqrt((T-t)/360)
    put=call
    return {'Call':call,
            'Put':put,
            'Greek':'Vega'}

def theta(t,T,r_dom,r_for,v,K,spot):
    """
    Theta is the the first derivative of the option price with respect to time.
    It measures the sensitivity of the price to the passage of time, it's a 
    rate of change (the price increases of decreases depending on the sign of
    theta).'
    Parameters
    ----------
    T : float
        maturity in days
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
    Dictionnary with the theta of the put and call.
    """
    pone=-(spot*norm.pdf(d_plus(T-t,r_dom,r_for,v,K,spot))*v)/(2*np.sqrt((T-t)/360))
    call=pone - (r_dom-r_for)*K*np.exp(-(r_dom-r_for)*(T-t)/360)*norm.cdf(d_moins(T-t,r_dom,r_for,v,K,spot))
    put=pone + (r_dom-r_for)*K*np.exp(-(r_dom-r_for)*(T-t)/360)*norm.cdf(-d_moins(T-t,r_dom,r_for,v,K,spot))
    

    return {'Greek':'Theta',
        'Call':call,
            'Put':put}


#############INPUTS###############
#currency pair
currency_pairs = ["EURUSD", "EURMAD", "USDMAD"]
selected_pair = st.selectbox("Select a currency pair:", currency_pairs)
st.write(f"You're computing the greeks for a {selected_pair} option.")

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


###computation
if st.button("Compute"):
    deltas=delta(0,timete,bir_input,fir_input,vol,strike,spot)
    gammas=gamma(0,timete,bir_input,fir_input,vol,strike,spot)
    thetas=theta(0,timete,bir_input,fir_input,vol,strike,spot)
    vegas=vega(0,timete,bir_input,fir_input,vol,strike,spot)
    
    
    tables=[deltas,gammas,vegas,thetas]
    df = pd.DataFrame(tables, columns=['Greek', 'Call', 'Put'])
    st.table(df)
    
###visualisation
if st.button("Visualize"):  
    containerg=st.container()
    with containerg:
        col1,col2=containerg.columns([1,1])
        with col1 :
    
            #delta
            f=plt.figure()
            puts=[]
            calls=[]
            spots=np.linspace(spot-1,spot+1,1000)
            for s in spots:
                pc=delta(0,timete,bir_input,fir_input,vol,strike,s)
                puts.append(pc['Put'])
                calls.append(pc['Call'])
            plt.title(f'Delta vs Spot price (K={strike}, maturity={timete},vol={vol*100}%)')
            plt.xlabel("Spot price")
            plt.ylabel("Delta")
            plt.plot(spots,calls,color='#682F2F')
            plt.plot(spots,puts,color='#ef6108')
            plt.legend(['Call','Put'])
            
            st.pyplot(f)
            
            #gamma
            f=plt.figure()
            calls=[]

            for s in spots:
                pc=gamma(0,timete,bir_input,fir_input,vol,strike,s)
                calls.append(pc['Call'])
            plt.title(f'Gamma vs Spot price (K={strike}, maturity={timete},vol={vol*100}%)')
            plt.xlabel("Spot price")
            plt.ylabel("Gamma")
            plt.plot(spots,calls,color='#682F2F')
            plt.legend(['Call/Put'])
            st.pyplot(f)
        
        with col2:
            #Vega
            f=plt.figure()
            calls=[]

            ivs=np.linspace(0,1,10000)
            for vs in ivs:
                pc=vega(0,timete,bir_input,fir_input,vs,strike,spot)
                calls.append(pc['Call'])
            plt.title(f'Vega vs implied volatility (K={strike}, maturity={timete}, Spot={spot})')
            plt.xlabel("Implied volatility (%)")
            plt.ylabel("Vega")
            plt.plot(ivs,calls,color='#682F2F')
            plt.legend(['Call/Put'])
            st.pyplot(f)
            
            #Theta
            f=plt.figure()
            puts=[]
            calls=[]

            times=np.linspace(0,timete,1000)
            for t in times:
                pc=theta(t,timete,bir_input,fir_input,vol,strike,spot)
                puts.append(pc['Put'])
                calls.append(pc['Call'])
            plt.title(f'Theta vs time (K={strike}, Spot={spot},vol={vol*100}%)')
            plt.xlabel("Time")
            plt.ylabel("Theta")
            plt.plot(times,calls,color='#682F2F')
            plt.plot(times,puts,color='#ef6108')
            plt.legend(['Call','Put'])
            st.pyplot(f)