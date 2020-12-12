from django.shortcuts import render
#from django.shortcuts import HttpResponse
# Create your views here.

def get_html_content(request):
    import requests
    productos = request.GET.get('productos')
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    productos = productos.replace(" ", "+")
    html_content = session.get(f'https://www.fravega.com/l/?keyword={productos}&sorting=LOWEST_SALE_PRICE').text
    return html_content


def home(request):
    info_fravega = None
    if 'productos' in request.GET:

        html_content=get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        info_fravega= dict()
        info_fravega['nombre'] = soup.find('h4', attrs={'class': 'PieceTitle-sc-1eg7yvt-0 akEoc'}).text
        info_fravega['plista'] = soup.find('span',attrs={'ListPrice-sc-1nq6iaq-0 ezHsVN'}).text
        info_fravega['precio']= soup.find('span', attrs={'class': 'SalePrice-sc-17gadvb-0 egaLpU'}).text
        info_fravega['descuento']= soup.find('span', attrs={'class': 'Discount-sc-51o9d0-0 jVGWkx'}).text
        link=soup.find('div', attrs={'class': 'ProductCard__Card-sc-1w5guu7-2 hlRWOw'}).find('a')['href']
        info_fravega['link']=link
        imagen=soup.find_all('img')
        
        info_fravega['imagen']=imagen[0].attrs['src']

    return render(request, 'ATIapp/home.html',{'fravega':info_fravega})
