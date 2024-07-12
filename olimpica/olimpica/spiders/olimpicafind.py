import scrapy
import pytz
from scrapy import Selector
from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy_selenium import SeleniumRequest
import time
import pandas
import datetime
import requests
import os



class OlimpicafindSpider(scrapy.Spider):
    name = 'olimpicafind'
    allowed_domains = ['www.olimpica.com']
    start_urls = ['https://www.olimpica.com//']

    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.olimpica.com/supermercado/',
            wait_time=5,
            screenshot=True,
            callback=self.parse,    
            #headers={'permissions-policy': 'interest-cohort=()'}
            headers={'User-Agent': self.userAgent}
        )    

    def parse(self, response):
        descargar_foto="No"
        #descargar_foto=input("Presione No si no quiere descargar la imagen: ")
        #pass
        driver=response.meta['driver']
        driver.set_window_size(1920, 1080)
        driver.save_screenshot('photo1.png')
        
        eans_unico=pandas.read_csv('eans_unico.csv', encoding='utf-8')
        eans=eans_unico['EAN'].str.replace('C','').tolist()        
        # print(eans[150:160])

        #eans_buscar=pandas.read_csv('ean_buscar_prob.csv', encoding='utf-8')
        #eans=eans_buscar['EAN'].tolist()
        #print(eans[0:10])
        
        # eans_unico=pandas.read_csv('eans_fotos.csv', encoding='utf-8')
        # eans=eans_unico['EAN'].astype(str).tolist()        
        #esperar a que cargue la pagina
        time.sleep(4)
        #for ean in eans[3890:]:
        #3318
        for ean in eans[135:]:

            search_input=driver.find_element_by_xpath("//input[contains(@class,'vtex-styleguide-9-x-input ma0 border-box vtex-styleguide-9-x-hideDecorators vtex-styleguide-9-x-noAppearance br2')]")        
            #search_input=driver.find_element_by_xpath("//input[contains(@class,'vtex-styleguide-9-x-input ma0 border-box vtex-styleguide-9-x-hideDecorators vtex-styleguide-9-x-noAppearance br2  br-0 br--left  w-100 bn outline-0 bg-base c-on-base b--muted-4 hover-b--muted-3 t-body pl5')]")    
            #search_input.clear()
            
            # ...
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.DELETE)

            search_input.send_keys(ean)
            #7702047005330
            #driver.save_screenshot('after_filling_input_'+ ean +'_.png')
            search_input.send_keys(Keys.ENTER)
            time.sleep(3)
            #driver.save_screenshot('after_click_'+ ean +'_.png')

            html = driver.page_source
            response_obj = Selector(text=html)
            
            nombre=""
            precio =""
            descuento =""
            imagen_link=""        

            try:
                nombre = response_obj.xpath("//span[contains(@class,'vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')][1]/text()").get()
            except:
                print("Sin nombre")  

            #if True:
            try:
                precio1 = response_obj.xpath("//span[@class='olimpica-dinamic-flags-0-x-currencyInteger'][1]/text()").get()
                precio=str(precio1)
                try:
                    precio2 = response_obj.xpath("//span[@class='olimpica-dinamic-flags-0-x-currencyInteger'][2]/text()").get()
                    precio=str(precio1)+str(precio2)

                    try:
                        precio3 = response_obj.xpath("//span[@class='olimpica-dinamic-flags-0-x-currencyInteger'][3]/text()").get()
                        precio=precio1+precio2+precio3 
                    except:
                         print("Sin precio3")               
                
                except:
                    print("Sin precio2") 

            except:
                print("Sin precio")                
            
                        
            try:
                #descuento = response_obj.xpath("//div[contains(@class,'')]/text()").get()
                descuento=""
            except:
                print("Sin descuento")
            

            # picture img:hover
            try:
            #if True:
                imagen_link=response_obj.xpath("//div[contains(@class,'dib relative vtex-product-summary-2-x-imageContainer')]/img/@src").get()
                imagen_link=imagen_link.replace('-300-300','-800-auto')
                imagen_link=imagen_link.replace('width=300','width=800')
                imagen_link=imagen_link.replace('height=300','height=auto')
                
                if descargar_foto!="No":
                    #print("--------------------------------------------------------------------------------------------------------------------"+imagen_link)
                    directorio_base=os.getcwd()
                    os.chdir(directorio_base+'/imagenes')
                    file = open(str(ean)+".png", "wb")
                    response = requests.get(imagen_link)
                    file.write(response.content)
                    file.close()
                    os.chdir(directorio_base)
            except:
                print("Sin foto")                
                        
            yield{'ean':ean,'nombre':nombre,'precio':precio, 'descuento':descuento
                    ,'imagen_link':imagen_link
            }                    
    
