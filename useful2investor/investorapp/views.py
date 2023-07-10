from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import User, Email, Asset
from django.utils import timezone
from datetime import datetime
import yfinance as yf


# Create your views here.
def indexView(request):
    """View function for the index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered index page.
    """
    return render(request, "index.html")


def save_values(request):
    """Function to save the values from the form in the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Redirect: Redirect the user to show_asset_info view with the email at the URL.
        HttpResponse: The HTTP response object containing the rendered index page.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        assets = request.POST.get("assets").upper().split(",")
        verification_time = request.POST.get("verification_time").split(",")
        superior_limits = request.POST.get("superior_limits").split(",")
        inferior_limits = request.POST.get("inferior_limits").split(",")

        for superior_limit, inferior_limit in zip(superior_limits, inferior_limits):
            if float(superior_limit) < float(inferior_limit):
                return render(
                    request,
                    "index.html",
                    {
                        "error": "O limite superior deve ser maior que o limite inferior."
                    },
                )
            
        if Email.objects.filter(address=email).exists():
            # O email já existe, redirecionar para show_asset_info com o email digitado
            return redirect("show_asset_info", email=email)

        user = User(name=name)
        user.save()

        email_obj = Email(address=email, user=user)
        email_obj.save()

        for i, asset in enumerate(assets):
            asset_obj = Asset(
                name=asset.strip() + ".SA",
                verification_time=int(verification_time[i].strip()),
                superior_limit=float(superior_limits[i].strip()),
                inferior_limit=float(inferior_limits[i].strip()),
                user=user,
            )
            asset_obj.save()

        return redirect("show_asset_info", email=email)

    return render(request, "index.html")


def show_values(request):
    """Function to show values from the database in the Html form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered stock_price page and the values.
    """
    users = User.objects.all()
    values = []

    for user in users:
        email = Email.objects.filter(user=user).first()
        assets = Asset.objects.filter(user=user)

        value = {
            "name": user.name,
            "email": email.address if email else "",
            "assets": assets,
        }

        values.append(value)

    return render(request, "stock_prices.html", {"values": values})


def get_assets_info(email):
    """Function to get the assets information from the database.

    Args:
        email (str): The email of the user.

    Returns:
        List: A list of dictionaries containing the assets information.
    """
    assets = Asset.objects.filter(user__email__address=email)
    asset_info_list = []

    for asset in assets:
        info = yf.Ticker(asset.name).history(period="1d")
        asset_info_list.append(
            {
                "name": asset.name,
                "superior_limit": asset.superior_limit,
                "inferior_limit": asset.inferior_limit,
                "verification_time": asset.verification_time,
                "info": info.reset_index().to_dict("records"),
            }
        )

    return asset_info_list


def show_asset_info(request, email):
    """Function to show the assets information in the Html page.

    Args:
        request (HttpRequest): The HTTP request object.
        email (str): The email of the user.

    Returns:
        email (str): The email of the user.
        HttpResponse: The HTTP response object containing the rendered assets_info page and the assets information.
    """
    asset_info_list = get_assets_info(email)
    send_email(asset_info_list, email)
    return render(
        request,
        "assets_info.html",
        {"asset_info_list": asset_info_list, "email": email},
    )


def send_email(asset_info_list, email):
    """Function to send an email to the user if the asset price is above the superior limit or
    below the inferior limit.

    Args:
        asset_info_list (List): A list of dictionaries containing the assets information.
        email (str): The email of the user.

    Returns:
        None
    """
    email_obj = Email.objects.get(address=email)
    user = email_obj.user

    current_time = timezone.make_aware(datetime.now(), timezone.get_current_timezone())

    for asset_info in asset_info_list:
        assets = Asset.objects.filter(user=user, name=asset_info["name"])

        for asset in assets:
            last_updated = asset.updated_at
            time_difference = current_time - last_updated

            if time_difference.total_seconds() >= asset.verification_time * 60:
                if asset_info["info"][0]["Close"] > asset.superior_limit:
                    message = f"Venda ativos: {asset_info['name']}"
                    send_mail(
                        "Venda ativos",
                        message,
                        email_obj.address,
                        [email_obj.address],
                        fail_silently=False,
                    )
                elif asset_info["info"][0]["Close"] < asset.inferior_limit:
                    message = f"Compre ativos: {asset_info['name']}"
                    send_mail(
                        "Compre ativos",
                        message,
                        email_obj.address,
                        [email_obj.address],
                        fail_silently=False,
                    )

                # Atualizar o campo updated_at para o tempo atual
                asset.updated_at = current_time
                asset.save()


def add_assets(request, email):
    """Function to add assets to the database.

    Args:
        request (HttpRequest): The HTTP request object.
        email (str): The email of the user.

    Returns:
        Redirect: Redirects to the show_asset_info page view with the email at the URL.
        HttpResponse: The HTTP response object containing the rendered add_assets page.
    """
    if request.method == "POST":
        asset_name = request.POST.get("asset_name")
        verification_time = int(request.POST.get("verification_time"))
        superior_limit = float(request.POST.get("superior_limit"))
        inferior_limit = float(request.POST.get("inferior_limit"))

        user = User.objects.get(email__address=email)
        Asset.objects.create(
            name=asset_name.upper() + ".SA",
            verification_time=verification_time,
            superior_limit=superior_limit,
            inferior_limit=inferior_limit,
            user=user,
        )

        return redirect("show_asset_info", email=email)

    return render(request, "add_assets.html")


def remove_assets(request, email):
    """Function to remove assets from the database.

    Args:
        request (HttpRequest): The HTTP request object.
        email (str): The email of the user.

    Returns:
        Redirect: Redirects to the show_asset_info page view with the email at the URL.
        HttpResponse: The HTTP response object containing the rendered remove_assets page.
    """
    user = User.objects.get(email__address=email)
    assets = Asset.objects.filter(user=user)

    if request.method == "POST":
        assets_to_remove = request.POST.getlist("assets_to_remove")

        for asset_id in assets_to_remove:
            Asset.objects.filter(id=asset_id).delete()

        return redirect("show_asset_info", email=email)

    return render(request, "remove_assets.html", {"assets": assets})


def update_asset(request, email, asset):
    """Function to update the asset information in the database.

    Args:
        request (HttpRequest): The HTTP request object.
        email (str): The email of the user.
        asset (str): The name of the asset.

    Returns:
        Redirect: Redirects to the show_asset_info page view with the email at the URL.
        HttpResponse: The HTTP response object containing the rendered update_asset page.
    """
    user = User.objects.get(email__address=email)
    asset = Asset.objects.get(user=user, name=asset)

    if request.method == "POST":
        verification_time = int(request.POST.get("verification_time"))
        superior_limit = float(request.POST.get("superior_limit"))
        inferior_limit = float(request.POST.get("inferior_limit"))

        asset.verification_time = verification_time
        asset.superior_limit = superior_limit
        asset.inferior_limit = inferior_limit
        asset.save()

        return redirect("show_asset_info", email=email)

    return render(request, "update_asset.html", {"asset": asset})
