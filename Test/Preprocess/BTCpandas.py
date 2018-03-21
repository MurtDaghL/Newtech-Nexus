# Inspiré de: https://github.com/dashee87/blogScripts/blob/master/Jupyter/2017-11-20-predicting-cryptocurrency-prices-with-deep-learning.ipynb
import pandas as pd, numpy as np
import time, os.path
from sklearn.preprocessing import scale, MinMaxScaler


# Téléchargement des données si elles ne sont pas présentes:
if os.path.isfile('D:\\Domanis\\GitHub\\Newtech-Nexus\\Datas\\Cryptos\\BTC\\btc.csv') == False:
    debut = time.time()
    print('Téléchargement des données du bitcoin en cours...')
    btc = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end="+time.strftime("%Y%m%d"))[0]
    # Nettoyage des données et conversion:
    btc.loc[btc['Volume']=="-",'Volume']=0
    btc['Volume'] = btc['Volume'].astype('int64')
    del btc['Date']
    btc.to_csv('D:\\Domanis\\GitHub\\Newtech-Nexus\\Datas\\Cryptos\\BTC\\btc.csv')
    fin = time.time()
    print('Données enregistrées en {durée} secondes !'.format(durée = fin- debut))
    

else:
    debut = time.time()
    btc = pd.read_csv('D:\\Domanis\\GitHub\\Newtech-Nexus\\Datas\\Cryptos\\BTC\\btc.csv')
    fin = time.time()
    print('Données importées en {durée} secondes !'.format(durée = fin- debut))
print('Données avant normalisation:')
print(btc.head())
print(btc.describe())

# Enregistrement de plusieurs normalisation différentes:
btc_scale = pd.DataFrame(scale(btc))
btc_minmax = pd.DataFrame(MinMaxScaler().fit_transform(btc)) 


print('\n\nDonnées scale:')
print(btc_scale.head())
print(btc_scale.describe())
btc.to_csv('D:\\Domanis\\GitHub\\Newtech-Nexus\\Datas\\Cryptos\\BTC\\btc_scale.csv')
print('\n\nDonnées minmax:')
print(btc_minmax.head())
print(btc_minmax.describe())
btc.to_csv('D:\\Domanis\\GitHub\\Newtech-Nexus\\Datas\\Cryptos\\BTC\\btc_minmax.csv')