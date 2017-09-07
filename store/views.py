from django.shortcuts import render

def home(request):
    content ={}
    return render(request, 'home.html',content) 