from django.shortcuts import render
from django.http import HttpResponse
from .form import LoginForm
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request, 'index.html')


def my_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse("login success")
            else:
                return render(request, 'index')
        else:
            return HttpResponse('login failed, password incorrect')
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'form.html', {'form': login_form})
