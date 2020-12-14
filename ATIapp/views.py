from django.shortcuts import render
#from django.shortcuts import HttpResponse
# Create your views here.

def get_html_content(request):
    import requests
    producto = request.GET.get('producto')
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    producto = producto.replace(" ", "+")
    webfravega = session.get(f'https://www.fravega.com/l/?keyword={producto}&sorting=LOWEST_SALE_PRICE').text
    webgarbarino = session.get(f'https://www.garbarino.com/q/{producto}/srch?sort_by=price_asc&q={producto}').text
    html_content = webfravega+webgarbarino
    #print(html_content)
    return html_content

def home(request):
    info_garbarino = None
    info_fravega = None
    if 'producto' in request.GET:

        html_content=get_html_content(request)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        info_fravega= dict()

        if soup.find('div',attrs={'class':'PiecePricing__PiecePriceWrapper-acjwpt-0 jSabjj'}):
            #para tener los diferentes span de los precios
            var = soup.find('div',attrs={'class':'PiecePricing__PiecePriceWrapper-acjwpt-0 jSabjj'})

            var2= soup.find('div',attrs={'class':'ProductCard__Card-sc-1w5guu7-2 hlRWOw'})


            if var2.findAll('h4',{'class':['PieceTitle-sc-1eg7yvt-0 akEoc']}):
                info_fravega['nombre'] = soup.find('h4', attrs={'class': 'PieceTitle-sc-1eg7yvt-0 akEoc'}).text
                # print('entro')
            else:
                info_fravega['nombre'] =''
                # print('no entro')
            if var.findAll("span",{"class":['ListPrice-sc-1nq6iaq-0 ezHsVN']}):
                info_fravega['plista'] = soup.find('span',attrs={'ListPrice-sc-1nq6iaq-0 ezHsVN'}).text
            else:
                info_fravega['plista'] =''

            if var.findAll("span",{"class":['SalePrice-sc-17gadvb-0 egaLpU']}):
                info_fravega['precio']= soup.find('span', attrs={'class': 'SalePrice-sc-17gadvb-0 egaLpU'}).text
            else:
                info_fravega['precio'] = ""

            if var.findAll("span",{'class': 'Discount-sc-51o9d0-0 jVGWkx'}):
                info_fravega['descuento']= soup.find('span', attrs={'class': 'Discount-sc-51o9d0-0 jVGWkx'}).text
            else:
                info_fravega['descuento'] = ""
            link=soup.find('div', attrs={'class': 'ProductCard__Card-sc-1w5guu7-2 hlRWOw'}).find('a')['href']
            # link2=soup.find('div', attrs={'class': 'itemBox--features'}).find('a')['href']
            info_fravega['link']=link


<<<<<<< HEAD
        imagen=soup.find_all('img')
        info_fravega['imagen']=imagen[0].attrs['src']
=======
            imagen=soup.find_all('img')
            info_fravega['imagen']=imagen[0].attrs['src']
>>>>>>> andres

        #variable=soup.find('span', attrs={'class': 'otra'}).text
        #print(variable)
        # if tag_link = soup.find('span', attrs={'class': 'otra'}).text:
        #     print(tag_link)
        # else:
        #     print("there is no class of 'Label' or no attribute of 'href'! ")
        # if soup.find('span', attrs={'class': 'otra'}).text :
        #    javascript = "bien"
        # # Otherwise assume that the javascript is contained within the tags
        # else:
        #    javascript = "mal"
        # print(javascript)


        # link=soup.find('div', attrs={'class': 'img-container main slick-slide slick-current slick-active'}).find('a')['href']
        # link=soup.find('div', attrs={'class': 'itemBox--features'}).find('a')['href']



        #info_garbarino['precio']= soup.find('span', attrs={'id': 'price-e81cb65a86'}).text
<<<<<<< HEAD
    else:
        print('no existe item')

    if  soup.find('div', attrs={'class':'itemBox'}):
        info_garbarino=dict()
        var2=soup.find('div', attrs={'class':'itemBox--info'})
        var3=soup.find('div', attrs={'class':'itemBox--carousel'})

        info_garbarino['nombre']=soup.find('h3', attrs={'itemprop': 'name'}).text

        info_garbarino['precio']=soup.find('span',attrs={'class':'value-item'}).text

        link=var2.find('a')['href']
        info_garbarino['link']=link
        if var2.find('del'):
            info_garbarino['preciolista']=var2.find('del').text
            info_garbarino['descuento']=var2.find('span',attrs={'class':'value-item--discount'}).text
=======
>>>>>>> andres
        else:
            print('no existe item')

        if  soup.find('div', attrs={'class':'itemBox'}):
            info_garbarino=dict()
            var2=soup.find('div', attrs={'class':'itemBox--info'})
            var3=soup.find('div', attrs={'class':'itemBox--carousel'})

            info_garbarino['nombre']=soup.find('h3', attrs={'itemprop': 'name'}).text

            info_garbarino['precio']=soup.find('span',attrs={'class':'value-item'}).text

            link=var2.find('a')['href']
            info_garbarino['link']=link
            if var2.find('del'):
                info_garbarino['preciolista']=var2.find('del').text
                info_garbarino['descuento']=var2.find('span',attrs={'class':'value-item--discount'}).text
            else:
                info_garbarino['preciolista']=''
            imagen=var3.find_all('img')
            info_garbarino['imagen']=imagen[0].attrs['src']

        else:
            print('no existe item')
    return render(request, 'ATIapp/home.html',{'fravega':info_fravega,'garbarino':info_garbarino})
