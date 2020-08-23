# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

## Long & Short - Verificação de Pares Cointegrados

# #### Operações Long & Short são operações onde você entra Long em um ativo e Short (vendido) em outro ativo. 
# #### Objetivo desse notebook é verificar se dois ativos são cointegrados, com essa resposta poderemos optar 
# #### por operar ou não um determinado ativo no momento em que for sinalizada uma entrada.
# 
# ### Funcionalidades
# 
# #### Download de cotação de dois ativos
# #### Plota gráfico dos dois ativos
# #### Verifica se o par é cointegrado
# #### Verifica se o resíduo é estacionário
# #### Plota gráfico do resíduo

# ## 1. Importação das Bibliotecas

# Referência bibliográfica

#https://minerandodados.com.br/analisando-dados-da-bolsa-de-valores-com-python/
#https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4
#https://aroussi.com/post/python-yahoo-finance
#https://medium.com/@pdquant/build-a-bitcoin-tegration-backtester-83e2b19125fd

import pandas as pd
import xlrd as xl
import numpy as np
import seaborn as sns
import os.path
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import yfinance as yf
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm
import streamlit as st
import datetime

plt.rcParams['figure.figsize'] = [20,8]

### 2. Pergunta ao usuário se ele deseja importar os dados da Web ou importar um arquivo local com as cotações
###    e carrega os dados da web ou local em um data frame para tratar os dados

def main():
    st.title('Long & Short - Verificação de Pares Cointegrados')
    st.sidebar.title('Parâmetros do Long & Short')
    
    # Input para usuário inserir o ticker dos ativos
    stock_1 = st.sidebar.text_input('Digite o ticker do ativo 1 que deseja analisar ')
    #if len(stock_1) == 5 and stock_1.isnumeric():
    #    st.text('Ticker OK')
    #else:
    #    st.text('Ticker Não OK')
    
    stock_2 = st.sidebar.text_input('Digite o ticker do ativo 2 que deseja analisar ')
    #if len(stock_2) == 5 and isnumeric(stock_2[-1]):
    #    st.text('Ticker OK')
    #else:
    #    st.text('Ticker Não OK')

    tickers = stock_1 + '.SA ' + stock_2 + '.SA'

    # Define uma data inicio e uma data fim 
    ini_date = st.sidebar.date_input('Data Inicial', datetime.date(2020,1,1))
    end_date = st.sidebar.date_input('Data Fim', datetime.date(2020,12,31))

    bt_check = st.sidebar.button("Iniciar verificação")

    if bt_check:
        # Faz download do histórico de cotações do 1º ativo informado
        pairs = yf.download(tickers, start=ini_date, end=end_date)['Adj Close']

        ticker1 = tickers.split()[0]
        ticker2 = tickers.split()[1]

        df_data = pd.DataFrame()
        df_data = pairs
        df_data = df_data.dropna()

        # Renomei a coluna de data para ficar com o nome maisuculo
        df_data.rename(columns={'Date':'DATE'}, inplace = True)

        df_data.head()
        
        ### 3. Cria a coluna de SPREAD, sendo ela a diferença entre o ativo 1 e o ativo 2 e plota o gráfico da 
        ###    cotação dos dois ativos Calcula o spread entre os dois ativos 
        st.text('Ativo 1:' + ticker1)
        st.text('Ativo 2:' + ticker2)
        st.text('Amostra do data frame dos ativos baixados')
        st.dataframe(df_data.head())

        # Plota o gráfico de linha dos ativos
        st.text('Gráfico de Linha dos Dois Ativos')
        #plt.plot(df[stock_1])
        #plt.plot(df[stock_2])
        plt.plot(df_data / df_data.iloc[0] * 100)
        st.pyplot()

        ## 4. Realiza o treino com os dados dos ativos
        # Selecionando amostra para o treinamento
        X_train, y_train = df_data[ticker1], df_data[ticker2]

        # Faz a regressão linear
        X = sm.add_constant(y_train)
        result = sm.OLS(X_train,X).fit()

        # Atribui parâmetros da regressão à variáveis e imprime valores
        slope, intercept, r_value, p_value, std_err = stats.linregress(df_data[ticker1], df_data[ticker2])
        df_data['PREDICAO'] = intercept + slope * df_data[ticker2]
        df_data['RESIDUO'] = df_data[ticker1] - intercept - slope * df_data[ticker2]
        result = adfuller(df_data['RESIDUO'])
        print(result[1])

        # Teste do p-valor
        if result[1] < 0.05:
            st.text('O resíduo é estacionário.')
            st.text('ADF Statistic: %f' % result[0])
            st.text('p-value: %f' % result[1])
            st.text('r-value: %f' % r_value)
            st.text('std_err: %f' % std_err)
            st.text('slope: %f' % slope)
        else:
            st.text('O resíduo NÃO é estacionário.')
            st.text('ADF Statistic: %f' % result[0])
            st.text('p-value: %f' % result[1])
            st.text('r-value: %f' % r_value)
            st.text('std_err: %f' % std_err)
            st.text('slope: %f' % slope)

        ### 7. Plota em um gráfico o Resíduo onde wnxergamos de forma gráfica a estacionariedade do resíduo 
        ###    desse par
        serie_z = df_data['RESIDUO']
        serie_z_mean = serie_z.mean()
        plt.plot(serie_z)
        plt.axhline(serie_z_mean+serie_z.std(),ls ='--')
        plt.axhline(serie_z.mean(),color='r')
        plt.axhline(serie_z_mean-serie_z.std(),ls ='--')
        st.pyplot()
        
if __name__ == '__main__':
    main()
