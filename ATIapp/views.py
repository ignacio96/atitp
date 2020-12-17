from django.shortcuts import render
#from django.shortcuts import HttpResponse
# Create your views here.
import operator


def is_float(value):
  try:
    float(value)
    return True
  except:
    return False

def nom_prod(request):
    import requests
    producto = request.GET.get('producto')
    return producto

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
    # webfravega = session.get(f'https://www.fravega.com/l/?keyword={producto}').text
    webgarbarino = session.get(f'https://www.garbarino.com/q/{producto}/srch?sort_by=price_asc&q={producto}').text
    # webgarbarino = session.get(f'https://www.garbarino.com/q/{producto}/srch?q={producto}').text

    html_content = webfravega+webgarbarino
    #print(html_content)
    return html_content

def prod(request):
    import requests
    producto = request.GET.get('producto')
    return producto

def recorrer_listado(listado,nombre):
    diccionario =dict()
    sin_encontrar = True
    # print(sin_encontrar)
    # Codigo que devuelve diccionario
    for elem in listado:     #accedemos a cada elemento de la lista (en este caso cada elemento es un dictionario)
         for k,v in elem.items():
            # print(k)
            # print(v)      #acedemos a cada llave(k), valor(v) de cada diccionario
            if k == 'nombre' :
                if nombre.lower() in v.lower() and sin_encontrar == True:
                    diccionario = elem
                    sin_encontrar = False
    return diccionario


def home(request):
    info_garbarino = None
    info_fravega = None
    if 'producto' in request.GET:
        producto=nom_prod(request)
        print(producto)

        html_content=get_html_content(request)

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        if soup.find('ul',attrs={'class':'listingDesktopstyled__SearchResultList-wzwlr8-6 fCKkuk'}):
            data1 = soup.find('ul',attrs={'class':'listingDesktopstyled__SearchResultList-wzwlr8-6 fCKkuk'})
            print(data1)
            data2=data1.find_all('div',attrs={'class':'ProductCard__Card-sc-1w5guu7-2 hlRWOw'})
            resultadoFravega=[]
            print('entro al primer if')
            for div in data2:
                link=div.a.get('href')
                nombre=div.a.article.div.h4.text
                # precio=div.a.article.div.span.text
                precio= div.a.article.div.find('span',attrs={'class':'SalePrice-sc-17gadvb-0 egaLpU'}).text
                # ver si es necesario ahcer reemplazo de "." por " " apra poder erdenar por precio
                x=(precio.split(' ')[1]).replace(".", "")
                x=float(x.replace(",","."))
                # print(x)

                imagen=div.a.article.figure.img.get('src')
                resultadoFravega.append({'precio':x,'link':link , 'nombre':nombre, 'imagen':imagen})
            # print(resultadoFravega)

            # for elem in resultadoFravega:      #accedemos a cada elemento de la lista (en este caso cada elemento es un dictionario)
            #     for k,v in elem.items():        #acedemos a cada llave(k), valor(v) de cada diccionario
            #         print(k, v)
            newlist = sorted(resultadoFravega, key=lambda k: k['precio'])
            
        # para traerme el nombre
            info_fravega= dict()

        # info=newlist[0]

            info_fravega = recorrer_listado(newlist,producto)
        else:
            print('no existe item')
        # ver que pasa si info_fravega esta vacio
        # if info_fravega = none




        if  soup.find('div', attrs={'class':'col-xs-7 col-sm-9 col-md-10'}):

            info_garbarino=dict()
            var1=soup.find('div', attrs={'class':'row itemList'})
            var2=var1.find_all('div',attrs={'class':'col-xs-12 col-sm-4 col-md-3'})
            resultadoGarbarino=[]
            # print(var2)
            for div in var2:
                link=div.a.get('href')
                nombre=div.div.h3.text
                imagen=div.a.img.get('src')

                precio=div.find('div',attrs={'class':'itemBox--price'})
                precio2=precio.find('meta',attrs={'itemprop':'price'}).get('content')
                x=float(precio2)

                resultadoGarbarino.append({'precio':x,'link':link , 'nombre':nombre, 'imagen':imagen})
            # print(resultadoGarbarino)

            newlist2 = sorted(resultadoGarbarino, key=lambda k: k['precio'])
            info_garbarino=dict()
            info_garbarino = recorrer_listado(newlist2,producto)
            # var3=soup.find('div', attrs={'class':'itemBox--carousel'})
            # # variable=soup.find_all('div', attrs={'class':'col-xs-12 col-sm-4 col-md-3'}).text
            #
            # info_garbarino['nombre']=soup.find('h3', attrs={'itemprop': 'name'}).text
            #
            # info_garbarino['precio']=soup.find('span',attrs={'class':'value-item'}).text
            #
            # link=var2.find('a')['href']
            # info_garbarino['link']=link
            # if var2.find('del'):
            #     info_garbarino['preciolista']=var2.find('del').text
            #     info_garbarino['descuento']=var2.find('span',attrs={'class':'value-item--discount'}).text
            # else:
            #     info_garbarino['preciolista']=''
            # imagen=var3.find_all('img')
            # info_garbarino['imagen']=imagen[0].attrs['src']

        else:
            print('no existe item')
    return render(request, 'ATIapp/home.html',{'fravega':info_fravega,'garbarino':info_garbarino})
