import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import models
from datetime import  datetime, timezone, timedelta



import time

# Create your views here.



# Create your views here
#from core.models import Produto
from online_users.models import OnlineUserActivity
from pycotacao import get_exchange_rates, CurrencyCodes


def login_user(request):
    return render(request,'login.html')


def registro(request):
    return render(request,'registro.html')



def logout_user(request):
    logout(request)
    return redirect('/')
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username,password=password)
        if usuario is not None:
            login(request,usuario)
            return redirect('/')
        else:
            messages.error(request,"Usuário ou senha invalido")


    return  redirect('/')

def submit_registro(request):
    print(request.POST)
    if request.POST:
        senha = request.POST.get('password')
        usuario = request.POST.get ( 'username' )
        email =   request.POST.get ( 'email' )
        try:
            print("e aqui?")
            user = User.objects.create_user ( str(usuario), str(email) ,  str(senha) )




        except:
            User.objects.get(usuario = usuario)
            User.objects.get(email = email)


            return HttpResponse('<h1> Usuario já cadastrado </h1>')

        print("hey")
        return redirect('/')
    return HttpResponse('<h1> faça um post </h1>')



@login_required(login_url='/login/')
def inicio(request):
    number_of_active_users = quantidadeOnline()
    dados = {"quantidadeUsuariosOnline":str(number_of_active_users)}
    return render(request,'inicio.html',dados)
@login_required(login_url='/login/')
def Euro(request):
    number_of_active_users = quantidadeOnline()
    valorDollar = conseguirValorDollar()
    valorEuro = conseguirValorEuro()
    valorLibra = conseguirValorLibra()
    dados = {
        "quantidadeUsuariosOnline": str(number_of_active_users),
        "valorDollar": str(valorDollar),
        "valorEuro": str(valorEuro),
        "valorLibra": str(valorLibra),
    }
    return render(request,'Euro.html',dados)

'''
codigo comentado blab
alba
lbal
ba
'''

def quantidadeOnline():
    user_activity_objects = OnlineUserActivity.get_user_activities()
    number_of_active_users = user_activity_objects.count()
    return number_of_active_users


def conseguirValorDollar():
    return get_exchange_rates(CurrencyCodes.USD).selling_rate


def conseguirValorEuro():
    return get_exchange_rates(CurrencyCodes.EUR).selling_rate


def conseguirValorLibra():
    return get_exchange_rates(CurrencyCodes.GBP).selling_rate
