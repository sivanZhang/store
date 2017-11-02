#！ -*- coding:utf-8 -*-
import os 
import random
import string 
from store import settings
from PIL import Image
from datetime import datetime

class FileUpload(object):
    @staticmethod
    def image_upload(f, path, name, optimize):
        destination = os.path.join(path, name)
        with open(destination, 'wb+') as destinationfile:
            for chuck in f.chucks():
                destinationfile.write(chuck) 
        if optimize:
            if os.path.getsize(destination.name) > settings.FILE_MAX_SIZE : 
                image = Image.open(destination.name) 
                image.save(destination.name,quality=settings.FILE_COMPRESSION_RIO,optimize=True)

def handle_uploaded_file(f, userid, related_path = 'product'):
       
    filename = datetime.now().strftime('%Y%m%d%H%M%S')+str(userid) + '.png' 
    path = os.path.join(settings.MEDIA_ROOT, related_path)
 
    if not os.path.isdir(path):
        os.makedirs(path)
        
    with open(os.path.join(settings.MEDIA_ROOT, related_path, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.join(related_path, filename)