from django.shortcuts import render
#from django.shortcuts import HttpResponse
# Create your views here.

def get_html_content(request):
    import requests
    ciudad = request.GET.get('ciudad')
    ciudad = ciudad.replace(" ", "+")
     #ciudad = request.GET.get('ciudad')
     #ciudad = ciudad.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    ciudad = ciudad.replace(" ", "+")
    html_content = session.get(f'https://www.google.com/search?q=weather+{ciudad}').text
    return html_content

def home(request):
    info_clima = None
    if 'ciudad' in request.GET:
        #traer info del clima
        #ciudad= request.GET.get('ciudad')
        html_content=get_html_content(request)
        # print(html_content)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        info_clima= dict()
        info_clima['region'] = soup.find('div', attrs={'id': 'wob_loc'}).text
        info_clima['daytime']= soup.find('div', attrs={'id': 'wob_dts'}).text
        info_clima['estado']= soup.find('span', attrs={'id': 'wob_dc'}).text
        #info_clima['temp']= soup.find_all('span', attrs={'id': 'wob_t'}).text
        info_clima['temp']= soup.find('span', attrs={'class': 'wob_t'}).text
        #region= soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['wob_t'])
         #print(region)
        # pass
    return render(request, 'ATIapp/home.html',{'clima':info_clima})
