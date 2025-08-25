from django.core.files.storage import default_storage
from django.http import HttpRequest
from .interfaces import ImageStorage   # el punto "." indica que está en el mismo módulo
from django.conf import settings
import os



class ImageLocalStorage:
    def store(self, uploaded_file):
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        return f'/media/images/{uploaded_file.name}'