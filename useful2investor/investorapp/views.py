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
        minutes = request.POST.get("minutes")
        # Salvar o e-mail em um arquivo de texto
        with open("emails.txt", "r") as file:
            emails = file.read()

            if email not in emails:
                with open("emails.txt", "a+") as file:
                    assets = str(assets.upper().split(",")).replace(" ", "")
                    file.write(email + " " + minutes + " " + assets + "\n")
        return redirect(show_stock_prices, email = email, minutes = minutes)
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
    
    assets_found = []
    for line in lines:
        parts = line.split()
        email_line = parts[0]
        if email_line == email:
            # Encontrou o e-mail correspondente
            for part in parts[1:]:
                if part.startswith('[') and part.endswith(']'):
                    # Parte contendo os ativos
                    assets_found = ast.literal_eval(part)
                    break
            break
            
    return assets_found


def show_stock_prices(request, email, minutes):
    assets = get_stock_price_2_txt(email)
    stock_prices = []

    for asset in assets:
        stock_price = get_stock_price(asset)
        stock_prices.append({"asset": asset, "stock_price": stock_price})
    return render(request, "stock_prices.html", {"stock_prices": stock_prices, "minutes": minutes})
    