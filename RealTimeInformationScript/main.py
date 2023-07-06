import pandas as pd
import yfinance as yf

ativos_b3 = pd.read_csv('acoes-listadas.csv')
ativos_b3 = ativos_b3.iloc[:, 0].astype(str).values.tolist()

ticker = input('Digite o ticker: ').upper() + '.SA'

#Obter o objeto Ticker para a ação 'ticker'
ticker = yf.Ticker(ticker)

# Obter os dados da cotação mais recente
cotacao_atual = ticker.history(period="1d")

# Exibir os dados
print(cotacao_atual)