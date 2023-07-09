from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import ast

# Create your views here.
def indexView(request):
    return render(request, "index.html")


from django.shortcuts import render, redirect
from .models import User, Email, Asset


def save_values(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        assets = request.POST.get('assets').upper().split(',')
        verification_time = request.POST.get('verification_time').split(',')
        superior_limits = request.POST.get('superior_limits').split(',')
        inferior_limits = request.POST.get('inferior_limits').split(',')

        user = User(name=name)
        user.save()

        email_obj = Email(address=email, user=user)
        email_obj.save()

        for i, asset in enumerate(assets):
            asset_obj = Asset(name=asset.strip() + ".SA", verification_time =int(verification_time[i].strip()),
                              superior_limit = float(superior_limits[i].strip()),
                              inferior_limit = float(inferior_limits[i].strip()),
                              user=user)
            asset_obj.save()

        return redirect('show_asset_info', email=email)

    return render(request, 'index.html')


def show_values(request):
    users = User.objects.all()
    values = []
    
    for user in users:
        email = Email.objects.filter(user=user).first()
        assets = Asset.objects.filter(user=user)
        
        value = {
            'name': user.name,
            'email': email.address if email else '',
            'assets': assets,
        }
        
        values.append(value)
    
    return render(request, 'stock_prices.html', {'values': values})


def get_assets_info(email):
    assets = Asset.objects.filter(user__email__address=email)
    asset_info_list = []
    
    for asset in assets:
        info = yf.Ticker(asset.name).history(period="1d")
        asset_info_list.append(
            {'name': asset.name, 'superior_limit': asset.superior_limit, 'inferior_limit': asset.inferior_limit,
             'verification_time': asset.verification_time, 'info': info.reset_index().to_dict('records')})
    
    return asset_info_list


def show_asset_info(request, email):
    asset_info_list = get_assets_info(email)
    send_email(asset_info_list, email)
    return render(request, 'assets_info.html', {'asset_info_list': asset_info_list})

def send_email(asset_info_list, email):
    email_obj = Email.objects.get(address=email)
    user = email_obj.user
    
    current_time = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
    
    for asset_info in asset_info_list:
        assets = Asset.objects.filter(user=user, name=asset_info['name'])
        
        for asset in assets:
            last_updated = asset.updated_at
            time_difference = current_time - last_updated
            
            if time_difference.total_seconds() >= asset.verification_time * 60:
                if asset_info['info'][0]['Close'] > asset.superior_limit:
                    message = f"Venda ativos: {asset_info['name']}"
                    send_mail(
                        'Venda ativos',
                        message,
                        email_obj.address,
                        [email_obj.address],
                        fail_silently=False,
                    )
                elif asset_info['info'][0]['Close'] < asset.inferior_limit:
                    message = f"Compre ativos: {asset_info['name']}"
                    send_mail(
                        'Compre ativos',
                        message,
                        email_obj.address,
                        [email_obj.address],
                        fail_silently=False,
                    )
                
                # Atualizar o campo updated_at para o tempo atual
                asset.updated_at = current_time
                asset.save()

