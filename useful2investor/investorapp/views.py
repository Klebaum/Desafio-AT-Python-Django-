from django.shortcuts import render
from django.core.mail import send_mail
import pandas as pd
import yfinance as yf
import schedule
import time


# Create your views here.
def indexView(request):
    return render(request, "index.html")


"""
def enviar_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        send_mail(
            'Compra ativos',
            'Você deveria comprar ativos!',
            'kleberalmendro01@gmail.com',
            [email],
            fail_silently=False,
        )
        return render(request, 'sucesso.html')
    return render(request, 'index.html')

"""


def salvar_email(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # Salvar o e-mail em um arquivo de texto
        with open("emails.txt", "r") as file:
            emails = file.read().splitlines()

            if email not in emails:
                with open("emails.txt", "a+") as file:
                    file.write(email + "\n")

        return render(request, "sucesso.html")
    return render(request, "index.html")


def cotações(ativo):
    # ativos_b3 = pd.read_csv('acoes-listadas.csv')
    # ativos_b3 = ativos_b3.iloc[:, 0].astype(str).values.tolist()

    ticker_aux = ativo.upper() + ".SA"

    # Obter o objeto Ticker para a ação 'ticker'
    ticker = yf.Ticker(ticker_aux)

    # Obter os dados da cotação mais recente
    cotacao_atual = ticker.history(period="1d")
    cotacao_atual = ticker.history(period="1d")

    # Exibir os dados
    return cotacao_atual["Close"].values.tolist()


def mostrar_cotacoes(request):
    if request.method == "POST":
        ativos = request.POST.get("ativos")
        ativos = ativos.upper().split(",")

        cotacoes = []
        for ativo in ativos:
            cotacao = cotações(ativo.strip())
            cotacoes.append({"ativo": ativo.strip(), "cotacao": cotacao})

        return render(request, "index.html", {"cotacoes": cotacoes})
