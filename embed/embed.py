import re, json
import requests
from urllib.parse import urlparse
from embed import api_auth


def get_embed(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    rooturl = domain
    #imgur
    if 'fb.watch' in rooturl:
        api_url = "https://graph.facebook.com/v9.0/oembed_video?url="+ url + "&access_token=" + api_auth.insta_app_id + "|" + api_auth.insta_client_token
        data = requests.get(api_url).json()
        print(data)
        embedurl = data['html'] 
        return embedurl
    
    if 'www.facebook.com' in rooturl:
        if 'post' in url:
            api_url = "https://graph.facebook.com/v9.0/oembed_post?url="+ url + "&access_token=" + api_auth.insta_app_id + "|" + api_auth.insta_client_token
        data = requests.get(api_url).json()
        print(data)
        embedurl = data['html'] 
        return embedurl

    if 'flic.kr' in rooturl or 'www.flicker.com' in rooturl:
        photo_id = "Ankit"
        if 'flic.kr' in url:
            photo_id = str(url).split('/p/')[1]
        else:
            photo_id = str(url).split('/photos/')[1].split('/')[1]
        api_url = "https://www.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key="+api_auth.flicker_api_key+"&photo_id="+photo_id+"&secret="+api_auth.flicker_secret+"&format=json&nojsoncallback=1"
        print(api_url)
        data = requests.get(api_url).json()
        img_id = data['photo']['id'] 
        server_id = data['photo']['server']
        secret = data['photo']['secret']
        title = data['photo']['title']['_content']
        url = data['photo']['urls']['url'][0]['_content']
        embedurl = f"<a data-flickr-embed=\"true\" data-context=\"true\" href=\"{url}\" title=\"{title}\"><img src=\"https://live.staticflickr.com/{server_id}/{img_id}_{secret}.jpg\" width=\"100%\" alt=\"{title}\"></a><script async src=\"//embedr.flickr.com/assets/client-code.js\" charset=\"utf-8\"></script>"
        return embedurl

    if 'www.instagram.com' in rooturl:
        url = url.replace(r'/\?.*$/', "")
        api_url = "https://graph.facebook.com/v8.0/instagram_oembed?url=" + url + "&access_token=" + api_auth.insta_app_id + "|" + api_auth.insta_client_token
        data = requests.get(api_url).json()
        embedurl = data['html'] 
        return embedurl
        
    if 'www.slideshare.net' in rooturl:
        api_url = "https://www.slideshare.net/api/oembed/2?url="+ url +"&format=json"
        data = requests.get(api_url).json()
        embedurl = data['html']
        return embedurl

    if 'imgur.com' in rooturl:
        regex = r'^.+/([^/]+)(\.[^/]+)?$'
        found = re.findall(regex, url)
        img_id = found[0][0]
        if '/t/' in url:
            embedurl = "<blockquote class=\"imgur-embed-pub embed-responsive-item\" lang=\"en\" data-id=\"a/{0}\"><a href=\"{1}\">View post on imgur.com</a></blockquote><script async src=\"//s.imgur.com/min/embed.js\" charset=\"utf-8\"></script>".format(img_id, url)
        else:
            embedurl = "<blockquote class=\"imgur-embed-pub\" lang=\"en\" data-id=\"{0}\"><a href=\"{1}\">View post on imgur.com</a></blockquote><script async src=\"//s.imgur.com/min/embed.js\" charset=\"utf-8\"></script>".format(img_id, url)
        return embedurl
    
    #pinterest
    if 'pinterest' in rooturl:
        found = re.split('/pin/', url)
        img_id = found[1]
        x = slice(0, -1)
        domain = "pinterest"
        embedurl = "<iframe class=\"embed-responsive-item\" src=\"https://assets.pinterest.com/ext/embed.html?id={}\" id=\"pinterest\" height=\"612\" width=\"345\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(img_id[x])
        return embedurl, domain
    
    #giphy
    if 'giphy.com' in rooturl:
        found = re.split('/gifs/', url)
        img_id = found[1]
        if '-' in img_id:
            new_id = re.split('-', img_id)
            img_id = new_id[-1]
        embedurl = "<iframe  src=\"https://giphy.com/embed/{}\" class=\"giphy-embed embed-responsive-item\" allowFullScreen></iframe><p><a href=\"{}\">via GIPHY</a></p>".format(img_id, url)
        return embedurl
    
    #kuulo 
    if 'kuula.co' in rooturl:
        found = re.split('/post/', url)
        img_id = found[1]
        embedurl = "<iframe  class=\"embed-responsive-item\" width=\"100%\" height=\"640\" style=\"width: 100%; height: 640px; border: none; max-width: 100%;\" frameborder=\"0\" allowfullscreen allow=\"xr-spatial-tracking; gyroscope; accelerometer\" scrolling=\"no\" src=\"https://kuula.co/share/{}?fs=1&vr=0&sd=1&thumbs=1&info=1&logo=1\"></iframe>".format(img_id)
        return embedurl
    
    if 'weheartit.com' in rooturl:
        found = re.split('.com', url)
        img_id = found[1]
        embedurl = '<iframe class=\"embed-responsive-item\" src=\"//weheartit.com/widget{}/?avatar=1&title=1&subtitle=1\" style=\"width:500px;height:453px\" frameborder=\"0\"></iframe>'.format(img_id)
        return embedurl
    
    #pexels , pollstar
    if 'www.pexels.com' in rooturl or 'www.pollstar.com' in rooturl:
        embedurl = "<iframe class=\"embed-responsive-item\"src=\"{}\" height=\"600\" width=\"500\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(url)
        return embedurl
    
    if 'dribbble.com' in rooturl:
        embedurl = "<iframe class=\"embed-responsive-item\" src=\"{}\" height=\"600\" width=\"500\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(url)
        return embedurl
    #gfycat
    if 'gfycat.com' in rooturl:
        found = re.split('.com/', url)
        img_id = found[1]
        if '-' in img_id:
            new_id = re.split('-', img_id)
            img_id = new_id[0]
        embedurl = "<iframe class=\"embed-responsive-item\" src=\"https://gfycat.com/ifr/{}\" height=\"640\" width=\"450\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(img_id)
        return embedurl 
    
    if 'gist.github.com' in rooturl:
        embedurl = "<script src=\"{}.js\"></script>".format(url)
        return embedurl

    if 'www.hackster.io' in rooturl:
        embedurl = "<iframe class=\"embed-responsive-item\" frameborder=\'0\' height=\'385\' scrolling=\'no\' src=\'{}/embed\' width=\'350\'></iframe>".format(url)
        return embedurl

    if "www.reddit.com" in rooturl:
        embedurl = "<blockquote class=\"reddit-card\"><a href=\"{0}\"></a></blockquote><script async src=\"//embed.redditmedia.com/widgets/platform.js\" charset=\"UTF-8\"></script>".format(url,)
        return embedurl


    if 'codepen.io' in rooturl:
        new_url = str(url).replace('/pen/', '/embed/')
        embedurl = "<iframe class=\"embed-responsive-item\" src=\"{}\" height=\"600\" width=\"700\" frameborder=\"0\" scrolling=\"no\" ></iframe>".format(new_url)
        return embedurl
    
    if 'jsfiddle.net' in rooturl:
        url = str(url).split(':', 1)[1]
        embedurl = "<iframe class=\"embed-responsive-item\" width=\"100%\" height=\"300\" src=\"{}embedded/\" allowfullscreen=\"allowfullscreen\" allowpaymentrequest frameborder=\"0\"></iframe>".format(url)
        return embedurl

    if 'vizhub.com' in rooturl:
        embedurl = "<iframe class=\"embed-responsive-item\" width=\"100%\" height=\"300\" src=\"{}?mode=embed\" title=\"Hello VizHub\" height=\"300\" width=\"400\" frameborder=\"0\"></iframe>".format(url)
        return embedurl

    if 'posixion.com' in rooturl:
        url = str(url).replace("/question/", "/widget/question/")        
        embedurl = "<iframe class=\"posixion-iframe\" src=\"{}\" frameborder=\"0\" scrolling=\"no\"></iframe>".format(url)
        return embedurl
    
    if 'strawpoll.com' in rooturl:
        poll_id = str(url).split(".com/")[1]
        embedurl = "<iframe class=\"embed-responsive-item\" width=\"620\" height=\"552\" src=\"https://strawpoll.com/embed/{}\" style=\"width: 100%; height: 552px;\" frameborder=\"0\" allowfullscreen></iframe>".format(poll_id)
        return embedurl
    
    if 'actionbutton' in rooturl:
        action_id = str(url).split("/library/")[1]
        embedurl = "<iframe class=\"embed-responsive-item\" style=\'width: 100%\' frameborder=\'0\' scrolling=\'no\' height=\'450\' src=\'https://embed.actionbutton.co/widget/widget-iframe.html?widgetId={}\'></iframe>".format(action_id)
        return embedurl
    
    if 'pollforall' in rooturl:
        poll_id = str(url).split(".com/")[1]
        embedurl = "<iframe class=\"embed-responsive-item\" scrolling=\"no\" frameborder=\"0\" style=\"display: block; height: 760px; width: 100%; max-width: 460px;\"src=\"https://embed.pollforall.com/?pollId={}\"></iframe>".format(poll_id)
        return embedurl

    if 'snippet.uilicious.com' in rooturl:
        url = str(url).replace("/test/", "/embed/test/")
        embedurl = "<iframe class=\"embed-responsive-item\"  src=\"{}?stepNum=1&autoplay=0\" frameborder=\"0\" scrolling=\"no\" width=\"600px;\" height=\"400px;\"></iframe>".format(url)
        return embedurl

    if 'www.kickstarter.com' in rooturl:
        url = str(url).split("?ref=")[0]
        embedurl = "<iframe class=\"embed-responsive-item\" src=\"{}/widget/card.html?v=2\" frameborder=\"0\" scrolling=\"no\" width=\"220px;\" height=\"400px;\"></iframe>".format(url)
        return embedurl

    if 'datastudio.google.com' in rooturl:
        url = str(url).replace("/reporting/", "/embed/reporting/")
        embedurl = "<iframe class=\"embed-responsive-item\" width=\"600\" height=\"477\" src=\"{}\" frameborder=\"0\" style=\"border:0\" allowfullscreen></iframe>".format(url)
        return embedurl
    
    if 'tunein.com' in rooturl:
        url = str(url).split("-")[-1]
        embedurl = "<iframe class=\"embed-responsive-item\" src=\"https://tunein.com/embed/player/{}\" style=\"width:100%; height:100px;\" scrolling=\"no\" frameborder=\"no\"></iframe>".format(url)
        return embedurl

    if 'codeply.com' in rooturl:
        embedurl = "<iframe class=\"embed-responsive-item\" width=\"600\" height=\"477\" src=\"{}\" frameborder=\"0\" style=\"border:0\" allowfullscreen></iframe>".format(url)
        return embedurl
        
    if 'relayto.com' in rooturl:
        url = str(url).split("//")[1]
        embedurl = "<iframe class=\"embed-responsive-item\" seamless allowfullscreen src=\"https://embed.{}\" width=\"100%\" height=\"600\" style=\"border: none\"></iframe>".format(url)
        return embedurl

    if 'commaful' in rooturl:
        url = str(url).split("//")[1]
        url = url.replace("/play", "")
        embedurl = "<div style=\"max-width:600px;min-width:300px;max-height:600px;\"><div style=\"position:relative;padding-top:100%;width:100%;\"><iframe src=\"https://embed.{}\" height=\"500\" width=\"500\" style=\"position:absolute;top:0;left:0;width:100%;height:100%;\"></iframe></div></div>".format(url)
        return embedurl
    
    if 'facer.io' in rooturl:
        embedurl = "<iframe class=\"embed-responsive-item\" src=\"{}/embed\" width=\"435\" height=\"580\" style=\"border:0;\"></iframe>".format(url)
        return embedurl
    
    if 'tech.io' in rooturl:
        snippet_id = str(url).split("/snippet/")[1]
        embedurl = "<iframe class=\"embed-responsive-item\"  src=\"https://tech.io/snippet-widget/{}\" width=\"100%\" frameborder=\"0\" scrolling=\"no\" allowtransparency=\"true\" style=\"visibility:hidden\"></iframe><script async src=\"https://files.codingame.com/codingame/iframe-v-1-4.js\"></script>".format(snippet_id)
        return embedurl

    if 'snack.expo.io' in rooturl:
        code_id = str(url).split(".io/")[1]
        embedurl = "<div data-snack-id=\"{}\" data-snack-platform=\"web\" data-snack-preview=\"true\" data-snack-theme=\"light\" style=\"overflow:hidden;background:#F9F9F9;border:1px solid var(--color-border);border-radius:4px;height:505px;width:100%\"></div><script async src=\"https://snack.expo.io/embed.js\"></script>".format(code_id)
        return embedurl

    if 'prezi.com' in rooturl:
        data_id = str(url).split("/i/")[1]
        data_id = str(url).split("/")[0]
        embedurl = "<script async src=\"https://e.prezicdn.net/v1/design.js\"></script><div class=\"prezi-design-embed\" data-project-id=\"{}\"></div>".format(data_id)
        return embedurl