# -*- coding: utf-8 -*-
"""
This is the web App page to use the monte carlo simulation for option pricing
"""

##"imports
import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

image = Image.open(r"1280px-Logo_BCP.png")
sns.set(rc={"axes.facecolor":"#FFF9ED","figure.facecolor":"#FFF9ED"})
pallet = ["#682F2F","#ef6108","#280301", "#9E726F", "#e7c9c8", "#B9C0C9", "#9F8A78", "#F3AB60"]


container_0=st.container()
with container_0:
    col_1,col_2=container_0.columns([2,2])
    with col_1:
        st.markdown("<h1 style='font-size: 40px;'>Monte-Carlo simulation</h1>", unsafe_allow_html=True)
    with col_2 : 
        image_width = 255
        image_height = 225
        
        # Resize the image
        resized_image = image.resize((image_width, image_height))
        
        # Display the image in the top right corner
        st.image(resized_image, use_column_width=False, clamp=True, width=image_width)


st.sidebar.header("Monte-Carlo")

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
        
        La simulation de Monte Carlo est une technique puissante et largement 
        utilisée dans le domaine de l'option pricing. Cette méthode repose sur 
        la génération aléatoire de multiples scénarios possibles pour 
        l'évolution future du sous-jacent, en utilisant un modèle de diffusion 
        géométrique des prix (GBM). Pour chaque scénario, les valeurs d'option 
        sont évaluées à la date d'échéance, en fonction du prix du sous-jacent 
        et d'autres paramètres tels que la volatilité et les taux d'intérêt. 
        En répétant cette simulation des milliers de fois, on obtient une 
        distribution des valeurs d'option possibles, permettant ainsi de 
        calculer l'espérance mathématique, la médiane, et d'autres statistiques
        des prix des options. La simulation de Monte Carlo permet donc de 
        fournir une estimation numérique fiable du prix de l'option et des 
        mesures de risque associées, ce qui en fait un outil essentiel pour les
        traders et les professionnels de la finance pour prendre des décisions 
        éclairées en matière de gestion de portefeuille et de couverture de risques.
            Pour le moment les résultats fournis par cette page ne sont pas 
            exacts, le modèle est toujours en cours de réglage.
        </p>
        """,
        unsafe_allow_html=True,
    )


####Machinery
def compute(T,r0,vol,dr,n=1,title=None):
    """
    Parameters
    ----------
    T: float 
        Number of YEARS to expiration.
    r0 :float 
        initial rate
    vol : float
        exchange volatility rate
    dr : float
        domestic risk free rate
    n : integer, optional
        Number of simulations wanted. The default is 1.
    title : string, optional
        The couple of currency wnated to be displayed Ccy1/Ccy2. The default is None.

    Returns
    -------
    rates : List
        List containing the rates of the n simulations.
    """
    dt=T/1000
    drift=(dr-0.5*vol**2)*dt
    rates=[]
    times=np.arange(0,T+dt,dt)
    for i in tqdm(range(n),desc='Simulating paths'):
        rate=[]
        bm=0
        for t in times:
            bm+=np.random.normal(0,np.sqrt(dt))
            rate.append(r0*np.exp((drift-(vol**2)/2)*t+vol*bm))
        rates.append(rate)
        progress_bar.progress(round((i + 1)*100/n))
    f=plt.figure()
    plt.xlabel("Time")
    plt.ylabel("Exchange rate")
    plt.title(f"Monte Carlo Simuation of exchange rate {title} (10 simulations/{n})")
    for i in range(min(len(rates),10)):
        plt.plot(times,rates[i])
    if i==9:
        print(f"Only 10 paths are shown but {n} are computed.")
    return rates,f


def pricer(strike,T,dr,r0,vol,n=100,title=None):
    """
    Parameters
    ----------
    T: float 
        Number of YEARS to expiration.
    r0 :float 
        initial rate
    vol : float
        exchange volatility rate
    strike : float
        the strike rate of the option.
    dr : float
        the domestic discount rate.
    n : integer, optional
        number of simulation ran to price the option. The default is 100.
    title : string, optional
        The couple of currency wnated to be displayed Ccy1/Ccy2. The default is None.
    Returns
    -------
    Return the option price based on the empirical mean.

    """
    rates,fig=compute(T,r0,vol,dr,n=n,title=title)
    expir=[]
    for rate in tqdm(rates,desc='Computing means'):
        expir.append(rate[len(rate)-1])
    cp=0
    pp=0
    for i in expir:
        cp+=max(0,i-strike)
        pp+=max(0,strike-i)
    #call price
    dcp=(cp/len(expir))*np.exp(-dr*T)
    print(f"The call price for K={strike}, T={T} is {dcp}")
    #put price
    dpp=(pp/len(expir))*np.exp(-dr*T)
    print(f"The put price for K={strike}, T={T} is {dpp}")
    
    hist=plt.figure()
    plt.hist(expir,color='#682F2F')
    plt.xlabel("Rates at maturity")
    plt.ylabel('Frequency')
    plt.title(f"Distribution of the simulated {selected_pair} rates at maturity.")
    plt.axvline(x=strike,color='blue',linestyle='--')
    plt.axvline(x=spot,color='red',linestyle='--')

    return {'fig':fig,
            'call':round(dcp,5),
            'put':round(dpp,5),
            'hist':hist}


#############INPUTS###############
#currency pair
currency_pairs = ["EURUSD", "EURMAD", "USDMAD"]
selected_pair = st.selectbox("Select a currency pair:", currency_pairs)
st.write(f"You're computing a Monte-Carlo simulation for a {selected_pair} option.")

ccy1=selected_pair[0:3]
ccy2=selected_pair[3:]


#years to expiration
timete = st.number_input("Number of YEARS to expiration", min_value=0.0, max_value=1000000.0, 
                             value=0.0, step=0.01)
st.write(timete," YEARS to expiration")

#domestic rate
dom_input = st.number_input(f"Domestic interest rate ({ccy1}):", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')/100
st.write("The base interest rate is :", dom_input*100," %")

#Volatility
vol = st.number_input("Volatility of the currency pair", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')/100
st.write("The volatility is :", vol*100," %")

#strike
strike = st.number_input("Strike rate:", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')
st.write("The strike rate is :",strike)

#spot
spot = st.number_input("Spot  rate:", min_value=0.0, max_value=100.0, 
                             value=0.000, step=0.0001, format='%f')
st.write("The spot rate is :",spot)

#number of simulation
N = st.number_input("Number of simulations", min_value=0, max_value=1000000, 
                             value=0, step=1)
st.write(N,' simulations')

#############COMPUTATION###########

if st.button("Compute"):
    progress_bar = st.progress(0)
    d=pricer(strike,timete,dom_input,spot,vol,n=N,title=selected_pair)
    st.write(f"The estimated **call price** is **{d['call']}** and the estimated **put price** is **{d['put']}**.")
    
    cont=st.container()
    with cont:
        col1,col2=cont.columns([1,1])
        with col1 :
            
            st.pyplot(d['fig'])
        with col2:
            
            st.pyplot(d['hist'])
        
            st.write("The strike price is in blue and the spot price is in red.")
