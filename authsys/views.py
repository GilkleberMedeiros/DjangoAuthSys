from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def pag1(request):
    return render(request, "pag1.html")

def pag2(request):
    return render(request, "pag2.html")