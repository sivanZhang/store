from django.shortcuts import render
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

dmb     = DetectMobileBrowser()


def home(request):
    content ={}
    isMble  = dmb.process_request(request)

    if isMble:
        return render(request, 'm_home.html',content) 
    else:
        return render(request, 'home.html',content) 