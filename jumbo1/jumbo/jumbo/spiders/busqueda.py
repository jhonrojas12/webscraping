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


class BusquedaSpider(scrapy.Spider):
    name = 'busqueda'
    allowed_domains = ['tiendasjumbo.co/supermercado/']
    #start_urls = ['https://www.tiendasjumbo.co/supermercado/']
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.tiendasjumbo.co/supermercado/',
            wait_time=5,
            screenshot=True,
            callback=self.parse_item_encontrado,    
            #headers={'permissions-policy': 'interest-cohort=()'}
            headers={'User-Agent': self.userAgent}
        )

    def parse(self, response):
        yield SeleniumRequest(
            url='https://www.tiendasjumbo.co/supermercado/',
            wait_time=5,
            screenshot=True,
            callback=self.parse_item_encontrado,
            headers={'User-Agent': self.userAgent}
        ) 



    def parse_item_encontrado(self, response):
        ###############This function is important to expand elements of shadow root. It will be use bellow.
        def expand_shadow_element(element):
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
            return shadow_root


        #webdriver. I am using chrome 
        driver=response.meta['driver']
        driver.set_window_size(1920, 1080)
        driver.save_screenshot('photo1_website.png')
        
        #loading list of elements to search
        eans_unico=pandas.read_csv('eans_unico.csv', encoding='utf-8')
        eans=eans_unico['EAN'].str.replace('C','').tolist() 
        
        #searching each element. I am only searching a few elemenents in order to do some tests of the code.
        for ean in eans[0:6]:            
            
            ###############Handling first shadow root, in order to search words in webpage. This is a special issue of Jumbo webpage.
            #extract info of shadow root. 
            root1 = driver.find_element_by_css_selector('impulse-autocomplete')
            #expand info
            print("1-----------------------------------------------------------------------------------------------------")           
            shadow_root1 = expand_shadow_element(root1)
            print(shadow_root1)

            #get input box webelement to search
            search_button = shadow_root1.find_element_by_class_name("impulse-input")

            #clean input box
            search_button.send_keys(Keys.CONTROL + "a")
            search_button.send_keys(Keys.DELETE)
            
            #input word to search in webpage
            search_button.send_keys(ean)
            driver.save_screenshot('after_filling_input_'+ ean +'.png')

            #execute search
            search_button.send_keys(Keys.ENTER)
            #waitint for website to load
            time.sleep(3)

            driver.save_screenshot('after_search_'+ ean +'.png')  


            ###############Handling second shadow root, in order to extract data of product. This is a special issue of Jumbo webpage.
            #Extract info of shadow root.             
            root2 = driver.find_element_by_css_selector('impulse-search')
            #expand info
            shadow_root2 = expand_shadow_element(root2)
           
            #get list of first element that appear in the results of search
            productos=shadow_root2.find_elements_by_css_selector(".group-impulse-card-content")
            
            #extract information of each result
            for producto in productos:
                yield{
                    'searched_word':ean,
                    'nombre':producto.find_element_by_css_selector(".group-name-brand h1 a span").text,
                    'precio':producto.find_element_by_class_name("impulse-currency").text,
                    'imagen_link':producto.find_element_by_css_selector("a picture img").get_attribute('src')
                }
