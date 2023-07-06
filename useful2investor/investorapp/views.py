from django.shortcuts import render
from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.
def indexView(request):
    return render(request, 'index.html')

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