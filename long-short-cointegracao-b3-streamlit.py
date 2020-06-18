#!/usr/bin/env python
# coding: utf-8

# # Long & Short - Verificação de Pares Cointegrados

# #### Operações Long & Short são conhecidas como operações "cash neutral", onde você entra Long em um ativo e Short (vendido) em outro ativo. Objetivo desse notebook é verificar se dois ativos são cointegrados, com essa resposta poderemos optar por operar ou não um determinado ativo no momento em que for sinalizada uma entrada.
# 
# ### Funcionalidades
# 
# #### Download de cotação de dois ativos
# #### Plota gráfico dos dois ativos
# #### Verifica se o par é cointegrado
# #### Verifica se o resíduo é estacionário
# #### Plota gráfico do resíduo

# Referência bibliográfica

#https://minerandodados.com.br/analisando-dados-da-bolsa-de-valores-com-python/
#https://towardsdatascience.com/a-comprehensive-guide-to-downloading-stock-prices-in-python-2cd93ff821d4
#https://aroussi.com/post/python-yahoo-finance
#https://medium.com/@pdquant/build-a-bitcoin-tegration-backtester-83e2b19125fd

# ## 1. Importação das Bibliotecas

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
#import pandas_datareader.data as web
import yfinance as yf
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm
import streamlit as st
import datetime

plt.rcParams['figure.figsize'] = [20,8]

# ## 2. Pergunta ao usuário se ele deseja importar os dados da Web ou importar um arquivo local com as cotações e carrega os dados da web ou local em um data frame para tratar os dados

def main():
    st.title('Long & Short - Pares Cointegrados na B3')
    st.sidebar.title('Parâmetros do Long & Short')
    # Input para usuário inserir o ticker dos ativos
    stock_1 = st.sidebar.text_input('Digite o ticker do ativo 1 que deseja analisar ')
    stock_2 = st.sidebar.text_input('Digite o ticker do ativo 2 que deseja analisar ')

    #Define uma data inicio e uma data fim 
    ini_date = st.sidebar.date_input('Data Inicial', datetime.date(2020,1,1))
    end_date = st.sidebar.date_input('Data Fim', datetime.date(2020,12,31))

    bt_check = st.sidebar.button("Iniciar verificação")

    if bt_check:
        # Faz download do histórico de cotações do 1º ativo informado
        df_data1 = yf.download(stock_1 + '.SA', start=ini_date, end=end_date)

        # Faz download do histórico de cotações do 2º ativo informado
        df_data2 = yf.download(stock_2 + '.SA', start=ini_date, end=end_date)

        # Deleta as colunas com os valores: Abertura, Maxima, Minima, Ajuste, Volume do ativo 1
        df_data1 = df_data1.drop('Open', axis =1)
        df_data1 = df_data1.drop('High', axis =1)
        df_data1 = df_data1.drop('Low', axis =1)
        df_data1 = df_data1.drop('Adj Close', axis =1)
        df_data1 = df_data1.drop('Volume', axis =1)

        # Deleta as colunas com os valores: Abertura, Maxima, Minima, Ajuste, Volume do ativo 2
        df_data2 = df_data2.drop('Open', axis =1)
        df_data2 = df_data2.drop('High', axis =1)
        df_data2 = df_data2.drop('Low', axis =1)
        df_data2 = df_data2.drop('Adj Close', axis =1)
        df_data2 = df_data2.drop('Volume', axis =1)

        # Faz um slice no nome dos ativos para expurgar o final do nome que vem com ".SA"
        stock_1 = stock_1[0:5]
        stock_2 = stock_2[0:5]

        #Reseta o indice do data frame para poder fazer o merge entre os dois data frames
        df_data1.reset_index(drop=False, inplace=True)
        df_data2.reset_index(drop=False, inplace=True)

        # Renomei o nome das colunas para remover o ".SA" do final
        df_data1.rename(columns={'Close':stock_1}, inplace = True)
        df_data2.rename(columns={'Close':stock_2}, inplace = True)

            # Renomei a coluna de data para ficar com o nome maisuculo
        df_data1.rename(columns={'Date':'DATE'}, inplace = True)
        df_data2.rename(columns={'Date':'DATE'}, inplace = True)

        df_data1.head()
        # Faz o merge entre os data frames dos ativos
        df = df_data1.merge(df_data2, on=['DATE'])

        # Deleta as variaveis abaixo para limpar a memória =D
        del df_data1
        del df_data2

        # ## 3. Cria a coluna de SPREAD, sendo ela a diferença entre o ativo 1 e o ativo 2 e plota o gráfico da cotação dos dois ativos 

        # Calcula o spread entre os dois ativos 
        df['SPREAD'] = df[stock_1] - df[stock_2]
        st.text('Ativo 1:' + stock_1)
        st.text('Ativo 2:' + stock_2)
        st.text('Amostra do data frame dos ativos baixados')
        st.dataframe(df.head())

        # Plota o gráfico de linha dos ativos
        st.text('Gráfico de Linha dos Dois Ativos')
        plt.plot(df[stock_1])
        plt.plot(df[stock_2])
        st.pyplot()

        # ## 4. Realiza o treino com os dados dos ativo
        # Selecionando amostra para o treinamento
        X_train, y_train = df[stock_1], df[stock_2]
        # Cria o treino da coluna spread tbm 
        spread_train = X_train - y_train
        #print(y_train)

        #5. Verifica se os pares são cointegrados e dá retorno para o usuário

        # A função coint retorna 3 valors: t stat, p-value and critical value
        t, p, crit = coint(X_train,y_train)

        # Teste do p-valor
        print(p)
        if p <0.05:
            st.text('O par é Cointegrado!.')
        else:
            st.text('O par NÃO é Cointegrado!.')

        #6. Verifica se o resíduo é estacionário , ou seja, se realmente há retorno a média na relação dos dois ativos

        # Fazendo teste adf para verificar estacionariedade
        pval_spread = adfuller(spread_train)[1]
        if pval_spread <0.05:
            print(pval_spread,'Dados são estacionários!')
        else:
            print(pval_spread, 'Dados NÃO são estacionários!')

        #build linear model to find beta that gives I(0) combination of pair
        X = sm.add_constant(y_train)
        result = sm.OLS(X_train,X).fit()

        print(result.params)
        #define new stationary spread as 'z'
        #'b' value gives the parameter of our linear model
        b = result.params[stock_2]
        #simply define our new cointegrated series as z = stock - b* stock
        z = X_train - b * y_train
        print(b)

        # Rodar teste adf novamente após a regressão linear
        z_pval = adfuller(z)[1]

        if z_pval<0.01:
            st.text('O resíduo é estacionário.')
        else:
            st.text('O resíduo NÃO é estacionário.')

        # ## 7. Plota em um gráfico o Resíduo onde wnxergamos de forma gráfica a estacionariedade do resíduo desse par
   
        #calculate cointegrated series 'full_z' for the whole (train + test) dataset
        spread = df['SPREAD']
        serie_z = df[stock_1] - b * df[stock_2]
        #lets plot the raw spread, the stationary spread and for reference the 'spread daily percent change' or 'returns'
        #the green vertical line shows the end of the training set period.

        serie_z_mean = serie_z.mean()
        plt.plot(serie_z)
        plt.axhline(serie_z_mean+serie_z.std(),ls ='--')
        plt.axhline(serie_z.mean(),color='r')
        plt.axhline(serie_z_mean-serie_z.std(),ls ='--')
        st.pyplot()
        #print(serie_z)
        #print(serie_z.std())
        
if __name__ == '__main__':
    main()


