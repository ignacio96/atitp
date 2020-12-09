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
    html_content = session.get(f'https://www.fravega.com/l/?keyword={ciudad}').text
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
        info_clima['nombre'] = soup.find('h4', attrs={'class': 'PieceTitle-sc-1eg7yvt-0 akEoc'}).text
        info_clima['precio']= soup.find('span', attrs={'class': 'ListPrice-sc-1nq6iaq-0 ezHsVN'}).text
        info_clima['descuento']= soup.find('span', attrs={'class': 'Discount-sc-51o9d0-0 jVGWkx'}).text
        info_clima['temp']= soup.find('div', attrs={'class': 'ProductCard__Card-sc-1w5guu7-2 hlRWOw'}).find('a')['href']
        info_clima['temp']= 'https://www.fravega.com'+info_clima['temp']
        #info_clima['imagen']== soup.find('img', attrs={'class': 'PieceFigure__Img-sc-18uorlj-0 fUyGUS'}).text
        # info_clima['temp']= soup.find('img', attrs={'class': 'PieceFigure__Img-sc-18uorlj-0 fUyGUS'}).text
        # print(info_clima)
        # image_tags = soup.findAll('img')
        # # print out image urls
        # for image_tag in image_tags:
        #     print(image_tag.get('src'))
        #print(info_clima['imagen'])
        # import re
        #for link in soup.find_all('a'):print(link.get('href'))# http://example.com/elsie# http://example.com/lacie# http://example.com/tillie
        # pastebin_regex = re.compile(r"^https://www.fravega.com/[\w]+$")

        # for link in soup.findAll('a', attrs={"href": pastebin_regex}):
        #  print(link["href"])
        #result = soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['wob_t'])
        #result=soup.find('span', attrs={'class': 'wob_t'}).text
        #print(result)
        # pass
    return render(request, 'ATIapp/home.html',{'clima':info_clima})
