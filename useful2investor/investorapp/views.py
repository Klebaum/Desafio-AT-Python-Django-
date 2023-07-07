from django.shortcuts import render
from django.core.mail import send_mail
import pandas as pd
import yfinance as yf
import schedule
import time


# Create your views here.
def indexView(request):
    return render(request, "index.html")


def send_email(request):
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


def save_email_assets(request):
    if request.method == "POST":
        email = request.POST.get("email")
        assets = request.POST.get("assets")
        # Salvar o e-mail em um arquivo de texto
        with open("emails.txt", "r") as file:
            emails = file.read()

            if email not in emails:
                with open("emails.txt", "a+") as file:
                    assets = str(assets.upper().split(",")).strip("[]")
                    file.write(email + " " + assets +  "\n")
        return render(request, "stock_prices.html")
    return render(request, "index.html")


def get_stock_price(ativo):
    ticker_aux = ativo.upper() + ".SA"

    # Obter o objeto Ticker para a ação 'ticker'
    ticker = yf.Ticker(ticker_aux)

    # Obter os dados da cotação mais recente
    current_price = ticker.history(period="1d")

    # Exibir os dados
    return current_price["Close"].values.tolist()


def show_stock_prices(request):
    if request.method == "POST":
        assets = request.POST.get("assets")
        assets = assets.upper().split(",")

        stock_prices = []
        for asset in assets:
            stock_price = get_stock_price(asset.strip())
            stock_prices.append({"asset": asset.strip(), "stock_price": stock_price})

        return render(request, "stock_prices.html", {"stock_prices": stock_prices})
    return render(request, "index.html")
