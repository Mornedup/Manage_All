from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


def homepage(request):
    return render(request, 'home_app/homepage.html')

class Home(TemplateView):
    template_name = 'home.html'