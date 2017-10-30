from django.shortcuts import render
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from django.conf import settings
from sitecontent.models import AdaptorBaseBlock

dmb     = DetectMobileBrowser()



def home(request):
    content ={}
    isMble  = dmb.process_request(request)

    sitecontents = AdaptorBaseBlock.objects.all()#sget_available_content()
    content['sitecontents'] = sitecontents
    content['mediaroot'] = settings.MEDIA_URL

    if isMble:
        return render(request, 'm_home.html',content) 
    else:
        return render(request, 'home.html',content) 