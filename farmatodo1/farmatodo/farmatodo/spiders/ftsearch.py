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
import pandas



class FtsearchSpider(scrapy.Spider):
    name = 'ftsearch'
    allowed_domains = ['www.farmatodo.com.co/']
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.farmatodo.com.co/buscar/',
            wait_time=5,
            screenshot=True,
            callback=self.parse_item_encontrado,    
            headers={'User-Agent': self.userAgent}
        )

    def parse_item_encontrado(self, response):

        #webdriver. I am using chrome
        driver=response.meta['driver']
        driver.set_window_size(1920, 1080)

        #screenshot
        driver.save_screenshot('photo1_farmatodo.png')
        
        #loading list of elements to search
        eans_unico=pandas.read_csv('eans_unico.csv', encoding='utf-8')
        eans=eans_unico['EAN'].str.replace('C','').tolist()  

        #time.sleep(3)

        #process to activate search button. This part is unique for farmatodo webpage
        search_input=driver.find_element_by_xpath("//input[contains(@class,'ng-untouched ng-pristine ng-valid')]")        
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.DELETE)
        search_input.send_keys('zzzzzz')    
        button =driver.find_element_by_css_selector(".search-content .search")
        button.click()

        #searching each element
        for ean in eans[0:4]:            
            
            #geting search input element
            search_input=driver.find_element_by_xpath("//input[contains(@class,'ng-valid ng-dirty ng-touched')]")        
            
            #cleaning input box
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.DELETE)

            #input ean
            search_input.send_keys(ean)
            driver.save_screenshot('after_input_'+ ean +'_.png')
            
            #execute searching
            #search_input.send_keys(Keys.ENTER)
            button =driver.find_element_by_css_selector(".search-content .search")
            button.click()
 
            #waitint for website loading
            time.sleep(5)

            #get current html of webpage
            driver.save_screenshot('after_search_'+ ean +'_.png')
            html = driver.page_source
            response_obj = Selector(text=html)
            

            #loading all results of search
            initial_items=len(response_obj.xpath("//div[@class='card-ftd']"))-1
            flag=True
            cont=0
            while flag:
                try:
                    button =driver.find_element_by_css_selector(".text-center .cont-button-more")
                    button.click()
                    time.sleep(3)
                    cont=cont+1
                    driver.save_screenshot('after_loading_'+str(cont)+'_'+ ean +'.png')                
                    html = driver.page_source
                    response_obj = Selector(text=html)
                    total_items=len(response_obj.xpath("//div[@class='card-ftd']"))
                    if total_items<=initial_items:
                        flag=False
                    initial_items=total_items
                except:
                    flag=False
                    print('There is no more results')
            
            #getting all results of search
            productos=response_obj.xpath("//div[@class='card-ftd']")
            for producto in productos:
                #save data
                yield{
                    'searched_word:':ean,
                    'nombre':producto.xpath(".//p[contains(@class,'text-title')]/text()").get()+producto.xpath(".//p[contains(@class,'text-description')]/text()").get(),
                    'precio':producto.xpath(".//span[contains(@class,'text-price')]/text()").get(),                    
                    'imagen_link':producto.xpath(".//img[@class='image']/@src").get()
                }
            