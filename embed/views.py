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
        print(rooturl)
        
        #imgur
        if rooturl == 'imgur.com':
            regex = r'^.+/([^/]+)(\.[^/]+)?$'
            found = re.findall(regex, url)
            print(found)
            img_id = found[0][0]
            if '/t/' in url:
                embedurl = "<blockquote class=\"imgur-embed-pub\" lang=\"en\" data-id=\"a/{0}\"><a href=\"{1}\">View post on imgur.com</a></blockquote><script async src=\"//s.imgur.com/min/embed.js\" charset=\"utf-8\"></script>".format(img_id, url)
            else:
                embedurl = "<blockquote class=\"imgur-embed-pub\" lang=\"en\" data-id=\"{0}\"><a href=\"{1}\">View post on imgur.com</a></blockquote><script async src=\"//s.imgur.com/min/embed.js\" charset=\"utf-8\"></script>".format(img_id, url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        #pinterest
        if 'pinterest' in rooturl:
            found = re.split('/pin/', url)
            img_id = found[1]
            x = slice(0, -1)
            domain = "pinterest"
            embedurl = "<iframe src=\"https://assets.pinterest.com/ext/embed.html?id={}\" id=\"pinterest\" height=\"612\" width=\"345\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(img_id[x])
            return render(request, 'embed.html' , {'form':form , "link":embedurl, "domain":domain})
        
        #giphy
        if 'giphy.com' in rooturl:
            found = re.split('/gifs/', url)
            img_id = found[1]
            embedurl = "<iframe src=\"https://giphy.com/embed/{}\" width=\"480\" height=\"480\" frameBorder=\"0\" class=\"giphy-embed\" allowFullScreen></iframe><p><a href=\"{}\">via GIPHY</a></p>".format(img_id, url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        #kuulo
        if 'kuula.co' in rooturl:
            found = re.split('/post/', url)
            img_id = found[1]
            embedurl = "<iframe width=\"100%\" height=\"640\" style=\"width: 100%; height: 640px; border: none; max-width: 100%;\" frameborder=\"0\" allowfullscreen allow=\"xr-spatial-tracking; gyroscope; accelerometer\" scrolling=\"no\" src=\"https://kuula.co/share/{}?fs=1&vr=0&sd=1&thumbs=1&info=1&logo=1\"></iframe>".format(img_id)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        if rooturl == 'weheartit.com':
            found = re.split('.com', url)
            img_id = found[1]
            embedurl = '<iframe src=\"//weheartit.com/widget{}/?avatar=1&title=1&subtitle=1\" style=\"width:500px;height:453px\" frameborder=\"0\"></iframe>'.format(img_id)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        #pexels , pollstar
        if rooturl == 'www.pexels.com' or rooturl == 'www.pollstar.com':
            embedurl = "<iframe src=\"{}\" height=\"600\" width=\"500\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})  
       
        if rooturl == 'dribbble.com':
            embedurl = "<iframe src=\"{}\" height=\"600\" width=\"500\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl}) 
        #gfycat
        if rooturl == 'gfycat.com':
            found = re.split('.com/', url)
            img_id = found[1]
            if '-' in img_id:
                new_id = re.split('-', img_id)
                img_id = new_id[0]
            embedurl = "<iframe src=\"https://gfycat.com/ifr/{}\" height=\"640\" width=\"450\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(img_id)
            return render(request, 'embed.html' , {'form':form , "link":embedurl}) 
        
        if rooturl == 'gist.github.com':
            embedurl = "<script src=\"{}.js\"></script>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        if rooturl == 'www.hackster.io':
            embedurl = "<iframe frameborder=\'0\' height=\'385\' scrolling=\'no\' src=\'{}/embed\' width=\'350\'></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        if rooturl == "www.reddit.com":
            embedurl = "<blockquote class=\"reddit-card\"><a href=\"{0}\"></a></blockquote><script async src=\"//embed.redditmedia.com/widgets/platform.js\" charset=\"UTF-8\"></script>".format(url,)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        return render(request, 'embed.html' , {'form':form})
    else:
        form = urlInputForm()
        return render(request, 'embed.html' , {'form':form})