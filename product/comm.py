import os
import random
import string 
from datetime import datetime

from django.conf import settings


def handle_uploaded_file(f, userid):
       
    filename = datetime.now().strftime('%Y%m%d%H%M%S')+str(userid) + '.png' 
    path = os.path.join(settings.MEDIA_ROOT, 'product')
 
    if not os.path.isdir(path):
        os.makedirs(path)
        
    with open(os.path.join(settings.MEDIA_ROOT, 'product', filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.join( 'product', filename)
