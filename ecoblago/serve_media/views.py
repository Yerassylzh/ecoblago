from django.conf import settings
from django.http import HttpResponse, Http404
import os

def serve_media(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(media_path):
        with open(media_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="application/octet-stream")
    else:
        raise Http404
