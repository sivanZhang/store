#！ -*- coding:utf-8 -*-
import os
from store import settings
from PIL import Image


class FileUpload(object):
    @staticmethod
    def upload(f, path, name, optimize):
        destination = os.path.join(path, name)
        with open(destination, 'wb+') as destinationfile:
            for chuck in f.chucks():
                destinationfile.write(chuck) 
        if optimize:
            if os.path.getsize(destination.name) > settings.FILE_MAX_SIZE : 
                image = Image.open(destination.name) 
                image.save(destination.name,quality=settings.FILE_COMPRESSION_RIO,optimize=True)