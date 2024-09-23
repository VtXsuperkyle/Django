from django.shortcuts import render
from.forms import CreateUserForm, LoginForm

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
            #returen redirect('')

    context = {'form': form}

    return render(request,'website/register.html', context=context)