from django.contrib.auth import authenticate, login
from django.shortcuts import render

from authentification.forms import UserForm, RegisterForm
from authentification.models import CustomUser

def main(request, id =None):

    if request.method == 'POST':
        form = UserForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return render(request, 'authentification/authentification.html', {
                'error_message' : 'Bonne saisie',
                'form' : form})
        
        else:
            return render(request, 'authentification/authentification.html', {
                'error_message' : 'Les champs renseignés sont invalides',
                'form' : form})

    else:
        form = UserForm()
        return render(request, 'authentification/authentification.html', {'form' : form})

def registration(request, id=None):

    if request.method == 'POST':
        form=RegisterForm(request.POST)
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        password_repeat  = request.POST['password_repeat']

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'authentification/registration.html', {
                'error_message' : "Nom d'utilisateur déjà utilisé",
                'form' : form})
        elif password != password_repeat:
            return render(request, 'authentification/registration.html', {
                'error_message' : "Mots de passe différents",
                'form' : form})
        else:
            user = CustomUser.objects.create_user(username=username, password=password)
            user.save()
            return render(request, 'authentification/registration.html', {
            'error_message' : "ok",
            'form' : form})

    else:
        form = RegisterForm()
        return render(request, 'authentification/registration.html', {'form' : form})
