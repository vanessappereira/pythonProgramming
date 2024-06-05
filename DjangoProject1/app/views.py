from django.shortcuts import render
from .models import Name
nomes = ["Bubbles","Blossom","Buttercup", "Mojojojo"]
cidades = ["Lisboa", "Porto", "Coimbra", "Faro"]
# Create your views here.
def response(request):
    #names = Name.objects.all()
    names = nomes
    cities = cidades
    return render(request, 'name.html', {'names': names, 'cities': cities})
