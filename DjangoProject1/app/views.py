import datetime
from django.shortcuts import render
from .models import Name
nomes = ["Bubbles","Blossom","Buttercup", "Mojojojo","Professor Utonium"]
cidades = []
# Create your views here.
def response(request):
    #names = Name.objects.all()
    names = nomes
    cities = cidades
    message = "Welcome to the Webpage!"
    current_year = datetime.date.today().year
    
    data_to_send = { 'names': names, 'cities': cities , 'message':message, 'current_year': current_year}
    
    return render(request, 'name.html', data_to_send)
