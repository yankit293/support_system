from django.shortcuts import render, HttpResponse
from .forms import urlInputForm
import re
from urllib.parse import urlparse
from .embed import get_embed

def invite(request):
    return render(request, 'invite.html')

def ImgZoom(request):
    return render(request, 'img_zoom.html')

def embed(request):
    if request.method == 'POST':
        form = urlInputForm(request.POST)
        url = request.POST.get('url')
        embedurl = get_embed(url)
        domain = None
        if type(embedurl) == tuple:
            domain = embedurl[1]
            embedurl = embedurl[0]
            print(domain)
        return render(request, 'embed.html' , {'form':form , 'link':embedurl, 'domain':domain})
    else:
        form = urlInputForm()
        return render(request, 'embed.html' , {'form':form})