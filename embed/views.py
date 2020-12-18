from django.shortcuts import render, HttpResponse
from .forms import urlInputForm
import re
from urllib.parse import urlparse


def embed(request):
    if request.method == 'POST':
        form = urlInputForm(request.POST)
        url = request.POST.get('url')
        parsed = urlparse(url)
        domain = parsed.netloc
        rooturl = domain
        if rooturl == 'imgur.com':
            regex = r'^.+/([^/]+)(\.[^/]+)?$'
            found = re.findall(regex, url)
            img_id = found[0][0]
            embedurl = "<blockquote class=\"imgur-embed-pub\" lang=\"en\" data-id=\" {0} \"><a href=\" {1} \">View post on imgur.com</a></blockquote><script async src=\"//s.imgur.com/min/embed.js\" charset=\"utf-8\"></script>".format(img_id, url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        if rooturl == 'in.pinterest.com':
            found = re.split('/pin/', url)
            img_id = found[1]
            x = slice(0, -1)
            embedurl = "<iframe src=\"https://assets.pinterest.com/ext/embed.html?id={}\" height=\"612\" width=\"345\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(img_id[x])
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        if rooturl == 'giphy.com':
            found = re.split('/gifs/', url)
            img_id = found[1]
            embedurl = "<iframe src=\"https://giphy.com/embed/{}\" width=\"480\" height=\"480\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"{}\">via GIPHY</a></p>".format(img_id, url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        if rooturl == 'www.pexels.com' or 'www.pollstar.com':
            embedurl = "<iframe src=\"{}\" height=\"600\" width=\"500\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        if rooturl == 'kuula.co':
            found = re.split('/post/', url)
            img_id = found[1]
            embedurl = "<iframe width=\"100%\" height=\"640\" style=\"width: 100%; height: 640px; border: none; max-width: 100%;\" frameborder=\"0\" allowfullscreen allow=\"xr-spatial-tracking; gyroscope; accelerometer\" scrolling=\"no\" src=\"https://kuula.co/share/{}?fs=1&vr=0&sd=1&thumbs=1&info=1&logo=1\"></iframe>".format(img_id)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        return render(request, 'embed.html' , {'form':form})
    else:
        form = urlInputForm()
        return render(request, 'embed.html' , {'form':form})