# Long Short de Ações da B3

## Objetivo: O Objetivo desse código é receber do usuário 2 ações da B3 e um intervalo de data para que o par seja analisado periodo, através desses parâmetros o programa verifica se os pares são cointegrados no intervalo de tempo informado.

### Funcionalidades futuras
- [X] Entrada de dados do usuário (Ticker da ação e intervalo de tempo)
- [ ] Validar o ticker das ações informadas pelo usuário
- [X] Plotar 5 linhas do data frame com os dados obtido do yfinance
- [X] Plotar gráfico de linha com o valor de fechamento das duas ações no intervalo de tempo informado 
- [X] Fazer teste adfuller e verificar se os pares são cointegrados
- [X] Usar Streamlit como Frontend
- [X] Plotar o gráfico dos resíduos
- [ ] Realizar backtest de um par selecionado
- [ ] Criar um job para rodar a estratégia diariamente buscando por pares com entradas por L&S.
- [ ] Fazer o deploy no Heroku ou outra plataforma para disponbilizar online