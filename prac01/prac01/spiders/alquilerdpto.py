import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json


class AlquilerdptoSpider(scrapy.Spider):
    name = "alquilerdpto"
    # Ruta de dominio para que el scrapy no salga de este dominio
    allowed_domains = ["properati.com.pe"]
    # Página de inicio de búsqueda
    start_urls = ["https://www.properati.com.pe/s/lima/departamento/alquiler"]

    FEED_FORMAT = 'json'
    FEED_URI = 'output.json'

    # VAmos a setear los parámetros que sólo vamos a recorrer las 10 primeras páginas.
    # La otra consideración es que estamos definiendo un USER_AGENT para que las peticiones simulen que se estan realizando desde una PC.
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT':11,
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Se esta considerando un tiempo de demora entre consulta y consulta de 3 segundos para evitar que se detecte que se está scrapeando
    # Este delay también contribuye a que el servidor no se sature con multiples peticiones en un corto tiempo.
    DOWNLOAD_DELAY = 3
    
    def parse(self, response):
        # Extraer información de los libros en la página actual
        n=0
        strsUrl = ''
        
        # Vamos a recorrer las 10 primeras páginas capturando el URL de la información que deseamos acceder
        for dpto in response.css("div.listing-card__information"):
            strn = str(n+1)
            strsId='/html/body/main/div[2]/div/div[2]/section/div[2]/a['+strn+']/@href'
            #urls.append('https://www.properati.com.pe/'+strsId)
            strsUrl = 'https://www.properati.com.pe'+response.xpath(strsId).get()
            item = {
                "itempage": strn,
                "url": strsUrl,
                "ubicacion": dpto.css("div.listing-card__location::text").get(),
                "precio": dpto.css("div.price::text").get(),
            }
            
            yield item
            n=n+1
            
        # Cargamos en un variable la ruta de la siguiente página para ceder a ella
        next_page = response.xpath('/html/body/main/div[2]/div/div[2]/div/div[1]/a[5]/@href').get()
        # Abre la siguiente página
        yield response.follow(next_page, self.parse)

class AlquilerdptodetSpider(scrapy.Spider):
    name = "alquilerdptodet"

    # Vamos a leer el archivo JSON donde se ha capturado los URLs que deseamos acceder
    def start_requests(self):
        with open('alquilerdpto.json', 'r') as f:
            data = json.load(f)
        
        # Recorremos para acceder al URL y capturar la información
        for item in data:
            url = item["url"]
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        url_activo = response.url
        
        #Capturamos toda la información relevante de ínteres de los inmuebles a alquilar
        yield {
            'title': response.css('div.main-title h1::text').get(),
            'location': response.css('div.location::text').get(),
            'price': response.css('div.prices-and-fees__price::text').get(),
            'bedroom': response.css('div.details-item-value::text').get(),
            'bathroom': response.xpath('/html/body/section/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/text()').get(),
            'area': response.xpath('/html/body/section/div[2]/div[1]/div[2]/div[1]/div[3]/div[3]/div[2]/text()').get(),
            'year_contruction': response.xpath('/html/body/section/div[2]/div[1]/div[2]/div[1]/div[4]/div[3]/div/span[2]/text()').get(),
            'maintenance': response.css('div.prices-and-fees__community-price::text').get(),
            'housing_type': response.xpath('/html/body/section/div[2]/div[1]/div[2]/div[1]/div[4]/div[1]/div/span[2]/text()').get(),
            'operation_type': response.xpath('/html/body/section/div[2]/div[1]/div[2]/div[1]/div[4]/div[2]/div/span[2]/text()').get(),
            'date_pub': response.xpath('/html/body/section/div[2]/div[1]/div[2]/div[1]/div[5]/text()').get(),
            'url': url_activo,
            }
