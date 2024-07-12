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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class ExitofindSpider(scrapy.Spider):
    name = 'exitofind'
    #allowed_domains = ['exito.com/']
    allowed_domains = []
    start_urls = ['https://www.exito.com/mercado/']
    
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.exito.com/mercado/',
            wait_time=5,
            screenshot=True,
            callback=self.parse,    
            headers={'User-Agent': self.userAgent}
        )    
    
    
    
    def parse(self, response):
        #definir si se quiere descargar la imagen del item
        descargar_foto="No"
        #descargar_foto=input("Presione No si no quiere descargar la imagen: ")
        
        #definir webdriver. Estoy usando chrome
        driver=response.meta['driver']

        #especificar la ciudad ya que la pagina lo pregunta, en este caso Bogota.
        search_input=driver.find_element_by_xpath("//input[@id='react-select-2-input']")
        search_input.send_keys('Bogotá')
        driver.save_screenshot('set location.png')   
        search_input.send_keys(Keys.ENTER)         
        confirm_button=driver.find_element_by_xpath("//div[@class='exito-geolocation-3-x-requestEmailActions flex justify-center']")
        confirm_button.click()
        driver.set_window_size(1920, 1080)
        
        #listado de eans a buscar
        eans_unico=pandas.read_csv('eans_unico.csv', encoding='utf-8')
        eans=eans_unico['EAN'].str.replace('C','').tolist()
        # print(eans[10:15])

        # eans_unico=pandas.read_csv('eans_fotos4.csv', encoding='utf-8')
        # eans=eans_unico['EAN'].astype(str).tolist()  
        #esperar a que cargue la pagina. revisra de 7423 hasta 7700
        time.sleep(10)
        for ean in eans[0:5]:
            #input de busqueda dentro de la pagina
            #se agrego una letra ('v')
            #search_input=driver.find_element_by_xpath("//input[contains(@class,'tex
            search_input=driver.find_element_by_xpath("//input[contains(@class,'vtex-styleguide-9-x-input ma0 border-box vtex-styleguide-9-x-hideDecorators')]")        
            driver.save_screenshot('before_inpu'+ ean +'_.png')
            #limpiar input box
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.DELETE)

            #ingresar ean a buscar
            search_input.send_keys(ean)
            search_input.send_keys(Keys.ENTER)

            #wait = WebDriverWait(driver, 10)

            #wait_time_in_sec = 6
            #try:
                #WebDriverWait(driver, wait_time_in_sec).until(EC.text_to_be_present_in_element_value((By.XPATH, "//script[@type='application/ld+json']/text()"), str(ean)))
                #WebDriverWait(driver, wait_time_in_sec).until(EC.text_to_be_present_in_element_value((By.XPATH, "//title[1]/text()"), str(ean)))
            #WebDriverWait(driver, wait_time_in_sec).until(EC.text_to_be_present_in_element_value((By.XPATH, "//a[contains(@href,'/search?_query=')]/text()"), str(ean)))

                
            #except:
             #   print("--------------------se acabo el tiempo")
            #esperar 3 segundos a que cargue la pagina
            
            
            
            time.sleep(4)

            #traer codigo html de la pagina
            driver.save_screenshot('after_wait_'+ ean +'_.png')
            html = driver.page_source
            response_obj = Selector(text=html)
            
            nombre="NoHaCargado"
            precioA =""
            precioB =""
            precioC =""
            precio =""
            descuento =""
            imagen_link=""
            
            ean_encontrado=""
            try:
                ean_encontrado=response_obj.xpath("//a[contains(@href,'/search?_query=')]/text()").get()
            except:
                print("---------------------------------------ean no cargo1")        

            if ean_encontrado!=str(ean):
                print("---------------------------------------ean no cargo2")
                yield{
                    'ean':ean,'nombre':nombre,'precio':precio
                    ,'descuento':descuento
                    ,'imagen_link':imagen_link
                }
                continue            
            #extraer la informacion si la encuentra
            #nombre
            try:
                nombre=response_obj.xpath("//div[contains(@class,'exito-product-details-3-x-stylePlp')]/text()").get()
            except:
                print("Sin nombre")              
            #precio
            try:
                precioA=response_obj.xpath("//div[contains(@class,'exito-vtex-components-4-x-otherSellingPrice')]/span/text()").get()
            except:
                print("Sin precioA")  
            
            try:
                precioB=response_obj.xpath("//div[contains(@class,'exito-vtex-components-4-x-alliedDiscountPrice')]/span/text()").get()
            except:
                print("Sin precioB")

            try:
                precioC=response_obj.xpath("//div[contains(@class,'exito-vtex-components-4-x-priceTagDel')]/span/text()").get()
            except:
                print("Sin precioC")                                
            
            precio=precioA or precioB or precioC
            
            #tag de descuento
            try:
                descuento=response_obj.xpath("//div[contains(@class,'exito-product-details-3-x-badgeExito')]/text()").get()
            except:
                print("Sin descuento") 
            
            
            #link de la imagen
            try:
                imagen_link=response_obj.xpath("//div[contains(@class,'dib relative vtex-product-summary-2-x-imageContainer vtex-product-summary-2-x-imageStackContainer')]/img/@src").get()
                imagen_link=imagen_link.replace('-500-auto','-1000-auto')
                imagen_link=imagen_link.replace('width=500','width=1000')
                #imagen_link=response_obj.xpath("//a[contains(@href,'/search?_query=')]/text()").get()
                #descargar imagen si asi se especifico                                
                if descargar_foto!="No":
                    directorio_base=os.getcwd()
                    os.chdir(directorio_base+'\imagenes')
                    file = open(str(ean)+".png", "wb")
                    response = requests.get(imagen_link)
                    file.write(response.content)
                    file.close()
                    os.chdir(directorio_base)
            except:
                print("Sin imagen") 

            
            
            yield{
                'ean':ean,'nombre':nombre,'precio':precio
                ,'descuento':descuento
                ,'imagen_link':imagen_link
            }
        
        print(str(datetime.datetime.now(pytz.timezone('America/Bogota')))+' Termina -----------------------')
