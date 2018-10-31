from django.shortcuts import render

# Create your views here.


def homepage(request):
    return render(request, 'home_app/home_app_home.html')
