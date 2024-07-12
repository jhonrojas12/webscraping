import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options




class DrogueriaSpider(scrapy.Spider):
    name = 'drogueria'
    allowed_domains = ['merqueo.com']
    start_urls = ['https://merqueo.com/barranquilla/super-ahorro/drogueria/']

    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    def __init__(self):
        chrome_path=which("chromedriver.exe")
        chrome_options=Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f'user-agent={self.userAgent}')

        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get('https://merqueo.com/barranquilla/super-ahorro/drogueria/')
        
        #rur_tab = driver.find_element_by_class_name("filterPanelItem___2z5Gb")
        #rur_tab[4].click()

        self.html= driver.page_source
        driver.close()    

    # def start_requests(self):
    #     yield SeleniumRequest(
    #         url='https://merqueo.com/barranquilla/super-ahorro/drogueria/',
    #         wait_time=10,
    #         screenshot=True,
    #         callback=self.parse,    
    #         #headers={'permissions-policy': 'interest-cohort=()'}
    #         headers={'User-Agent': self.user_agent}
    #     )

    # def parse(self, response):
    #     items=response.xpath("//")
    #     for item in items:
    #         yield{
    #             'nombre',
    #             'precio'
    #         }
        #pass
    # def parse(self, response):
    #     img=response.meta['screenshot']

    #     with open('screenshot2.png','wb') as f:
    #         f.write(img)        
    #     print(self.html)
    def parse(self, response):
        resp=Selector(text=self.html)
        
        # yield {
        #     'htmlmarkup':resp.get()
        # }   
        yield{
            'macrocategoria':resp.xpath("//h1/text()").get()

        }
