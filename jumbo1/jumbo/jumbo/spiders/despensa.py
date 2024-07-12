import scrapy
from scrapy import Selector
from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class DespensaSpider(scrapy.Spider):
    name = 'despensa'
    allowed_domains = ['tiendasjumbo.co']
    #start_urls = ['https://www.tiendasjumbo.co/supermercado/']
    
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'


    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.tiendasjumbo.co/supermercado/',
            wait_time=20,
            screenshot=True,
            callback=self.parse,    
            #headers={'permissions-policy': 'interest-cohort=()'}
            headers={'User-Agent': self.userAgent}
        )

    def parse(self, response):
        #pass
        driver=response.meta['driver']
        driver.set_window_size(1920, 1080)
        driver.save_screenshot('primera imagen.png') 
        macrocategorias=response.xpath("//li[@class='flex-item']")
        macrocategorias_df=[]

        for macrocategoria in macrocategorias[0:1]:
            nombre=macrocategoria.xpath(".//a/img/@alt").get()
            link=macrocategoria.xpath(".//a/@href").get()
            macrocategorias_df.append(nombre)
            #yield{'nombre':nombre_limpio}
            print(nombre)
            yield SeleniumRequest(
                url=link,
                wait_time=20,
                screenshot=True,
                callback=self.parse_macrocategoria,
                meta={'macrocategoria':nombre},
                #headers={'permissions-policy': 'interest-cohort=()'}
                headers={'User-Agent': self.userAgent}
            )     
    def parse_macrocategoria(self, response):
        macrocategoria_meta=response.meta['macrocategoria']
        driver=response.meta['driver']        
        #driver.set_window_size(1920, 9080)
        driver.set_window_size(610, 9080)
        #driver.maximize_window()
        driver.save_screenshot('macrocategoria paso1.png')

        print("_________________________________________________Inicia________________________________________________")
        productos=response.xpath("//div[contains(@class,'product-item product-item')]")
        print("cantidad productos: "+str(len(productos)))

        next_page=response.xpath("//div[@class='btn second-border filter-button mobile']").get()
        if next_page:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            html=driver.page_source
            response_obj=Selector(text=html)
            productos=response_obj.xpath("//div[contains(@class,'product-item product-item')]")
            print("________________cantidad productos2: "+str(len(productos)))
            #next_page=response_obj.xpath("//div[@class='btn second-border filter-button mobile']").get()      
            driver.save_screenshot('macrocategoria 2pagina.png') 
        
        html=driver.page_source
        response_obj=Selector(text=html)
        productos=response_obj.xpath("//div[contains(@class,'product-item product-item')]")
        for producto in productos:
            yield{
                'macrocategoria':macrocategoria_meta,
                'sku':producto.xpath(".//@data-sku").get(),
                'nombre':producto.xpath(".//div[@class='product-item__bottom']/div/a/@title").get(),
                'precio':producto.xpath(".//div[@class='product-item__bottom']/div[@class='product-prices__wrapper product-prices__wrapper--single product-prices__wrapper--measurable']/div[@class='product-prices__price product-prices__price--regular-price']/span[@class='product-prices__value product-prices__value--best-price']/text()").get(),
                'descuento':producto.xpath(".//div[@class='product-item__image-wrapper']/div[@class='product-item__flags']/div[@class='flag discount-percent']/@data-discount").get(),
                'imagen':producto.xpath(".//div[@class='product-item__image-wrapper']/a/img/@src").get()
            }
