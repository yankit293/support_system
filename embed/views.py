from django.shortcuts import render, HttpResponse
from .forms import urlInputForm
import re
from urllib.parse import urlparse

def invite(request):
    return render(request, 'invite.html')
def embed(request):
    
    if request.method == 'POST':
        form = urlInputForm(request.POST)
        url = request.POST.get('url')
        parsed = urlparse(url)
        domain = parsed.netloc
        rooturl = domain
        
        #imgur
        if rooturl == 'imgur.com':
            regex = r'^.+/([^/]+)(\.[^/]+)?$'
            found = re.findall(regex, url)
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


        if 'codepen.io' in rooturl:
            new_url = str(url).replace('/pen/', '/embed/')
            embedurl = "<iframe src=\"{}\" height=\"600\" width=\"700\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(new_url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        if 'jsfiddle.net' in rooturl:
            url = str(url).split(':', 1)[1]
            embedurl = "<iframe width=\"100%\" height=\"300\" src=\"{}embedded/\" allowfullscreen=\"allowfullscreen\" allowpaymentrequest frameborder=\"0\"></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        if 'vizhub.com' in rooturl:
            embedurl = "<iframe width=\"100%\" height=\"300\" src=\"{}?mode=embed\" title=\"Hello VizHub\" height=\"300\" width=\"400\" frameborder=\"0\"></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        if 'posixion.com' in rooturl:
            url = str(url).replace("/question/", "/widget/question/")        
            embedurl = "<iframe class=\"posixion-iframe\" src=\"{}\" frameborder=\"0\" scrolling=\"no\"></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        if 'strawpoll.com' in rooturl:
            poll_id = str(url).split(".com/")[1]
            embedurl = "<iframe width=\"620\" height=\"552\" src=\"https://strawpoll.com/embed/{}\" style=\"width: 100%; height: 552px;\" frameborder=\"0\" allowfullscreen></iframe>".format(poll_id)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        if 'actionbutton' in rooturl:
            action_id = str(url).split("/library/")[1]
            embedurl = "<iframe style=\'width: 100%\' frameborder=\'0\' scrolling=\'no\' height=\'450\' src=\'https://embed.actionbutton.co/widget/widget-iframe.html?widgetId={}\'></iframe>".format(action_id)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        if 'pollforall' in rooturl:
            poll_id = str(url).split(".com/")[1]
            embedurl = "<iframe scrolling=\"no\" frameborder=\"0\" style=\"display: block; height: 760px; width: 100%; max-width: 460px;\"src=\"https://embed.pollforall.com/?pollId={}\"></iframe>".format(poll_id)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        if 'snippet.uilicious.com' in rooturl:
            url = str(url).replace("/test/", "/embed/test/")
            embedurl = "<iframe  src=\"{}?stepNum=1&autoplay=0\" frameborder=\"0\" scrolling=\"no\" width=\"600px;\" height=\"400px;\"></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        if 'www.kickstarter.com' in rooturl:
            url = str(url).split("?ref=")[0]
            embedurl = "<iframe  src=\"{}/widget/card.html?v=2\" frameborder=\"0\" scrolling=\"no\" width=\"220px;\" height=\"400px;\"></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        if 'datastudio.google.com' in rooturl:
            url = str(url).replace("/reporting/", "/embed/reporting/")
            embedurl = "<iframe width=\"600\" height=\"477\" src=\"{}\" frameborder=\"0\" style=\"border:0\" allowfullscreen></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
        
        if 'tunein.com' in rooturl:
            url = str(url).split("-")[-1]
            embedurl = "<iframe src=\"https://tunein.com/embed/player/{}\" style=\"width:100%; height:100px;\" scrolling=\"no\" frameborder=\"no\"></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        if 'codeply.com' in rooturl:
            embedurl = "<iframe width=\"600\" height=\"477\" src=\"{}\" frameborder=\"0\" style=\"border:0\" allowfullscreen></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})
            
        if 'relayto.com' in rooturl:
            url = str(url).split("//")[1]
            embedurl = "<iframe seamless allowfullscreen src=\"https://embed.{}\" width=\"100%\" height=\"600\" style=\"border: none\"></iframe>".format(url)
            return render(request, 'embed.html' , {'form':form , "link":embedurl})

        return render(request, 'embed.html' , {'form':form})
    else:
        form = urlInputForm()
        return render(request, 'embed.html' , {'form':form})