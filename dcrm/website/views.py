from django.shortcuts import render, redirect
from.forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages

from .models import Gamedata

from django.conf import settings
import requests

# Create your views here.


from django.http import HttpResponse

def home(request):
    return render(request, "website/index.html")

#register a user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('my-login')

    context = {'form': form}

    return render(request,'website/register.html', context=context)



def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    context = {'login_form':form}
    return render(request,'website/my-login.html', context=context)

#logout a user
def user_logout(request):

    auth.logout(request)
    messages.success(request, "Logout success!")
    return redirect("my-login")

#dashboard -
@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()
    context = {'records':my_records}

    return render(request, 'website/dashboard.html', context=context)

#create a record
@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your record was created!")
            return redirect("dashboard")
        
    context = {'create_form': form}
    return render(request, 'website/create-record.html', context=context)

# update a record
@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)

    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect("dashboard")
        
    context = {'update_form': form}
    return render(request, 'website/update-record.html',context=context)

# Read a single record
@login_required(login_url="my-login")
def singular_record(request,pk):

    one_record = Record.objects.get(id=pk)
    context = {'record':one_record}
    return render(request, 'website/view-record.html', context = context)

#delete a record 
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Your record was Deleted!")
    return redirect("dashboard")

#cats view
@login_required(login_url='my-login')
def cats(request):
    return render(request, 'website/cats.html')

#game data view
@login_required(login_url='my-login')
def game_data(request):

    data = Gamedata.objects.all()
    context = {'data': data}

    return render(request,'website/game-data.html', context=context )

#weather api
def weather_data(request):


    print("loading weather view")
    if request.method == "POST":

        city=request.POST.get("city")
        key=settings.MY_API_KEY

        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q="

        url = BASE_URL + city + "&appid" + key

        json_data = request.get(url).json() 

        weather = json_data['weather'][0]['main']
        temperature = int(json_data['main']['temp'] - 273.15)
        min = int(json_data['main']['temp_min'] - 273.15)
        max = int(json_data['main']['temp_max'] - 273.15)
        icon = json_data['weather'][0]['icon']

        data = {
            "location": city,
            "weather": weather,
            "temperature": temperature,
            "min": min,
            "max": max,
            "icon":icon
        }


        context = {'data': data}

        return render(request, 'website/weather-data.html',context=context )
    else:
        return render(request, 'website/weatehr-data.html' )