from django.shortcuts import render

def manage(request):
    content ={}
    return render(request, 'category.html',content)