from django.shortcuts import render
from .models import Name
nomes =["cerry","blossom","ababanana", "abc"]
# Create your views here.
def response(request):
    names = nomes
    return render(request, 'name.html', {'names': names})
