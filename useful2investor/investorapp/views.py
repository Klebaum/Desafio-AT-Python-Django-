from django.shortcuts import render, redirect
from django.core.mail import send_mail
import pandas as pd
import yfinance as yf
import ast

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
                    assets = str(assets.upper().split(",")).replace(" ", "")
                    file.write(email + " " + assets + "\n")
        return redirect(show_stock_prices, email = email)
    return render(request, "index.html")


def get_stock_price(asset):
    ticker_aux = asset + ".SA"

    # Obter o objeto Ticker para a ação 'ticker'
    ticker = yf.Ticker(ticker_aux)

    # Obter os dados da cotação mais recente
    current_price = ticker.history(period="1d")

    # Exibir os dados
    return current_price["Close"].values.tolist()


def get_stock_price_2_txt(email):
    with open("emails.txt", "r") as archive:
        lines = archive.readlines()
    
    assets_founds = []
    for line in lines:
        email_line = line.split()[0]
        print(email_line)
        if email_line == email:
            assets_founds = ast.literal_eval(line.split('[', 1)[1].split(']', 1)[0])
            break
            
    return assets_founds  # Retorna uma lista vazia se o email não for encontrado 


def show_stock_prices(request, email):
    assets = get_stock_price_2_txt(email)
    stock_prices = []

    for asset in assets:
        stock_price = get_stock_price(asset)
        stock_prices.append({"asset": asset, "stock_price": stock_price})
    return render(request, "stock_prices.html", {"stock_prices": stock_prices})
    