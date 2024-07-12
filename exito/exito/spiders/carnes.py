import scrapy
from scrapy import Selector
from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy_selenium import SeleniumRequest

class CarnesSpider(scrapy.Spider):
    name = 'carnes'
    #allowed_domains = ['exito.com/','exito.com/mercado/']
    #se usa el siguiente codigo en lugar del anterior pues cuando entro a la pagina de la macrocategoria me toca asi.
    allowed_domains =[]
    #start_urls = ['https://www.exito.com/mercado/']
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    # def __init__(self):
    #     chrome_path=which("chromedriver.exe")
    #     chrome_options=Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument(f'user-agent={self.userAgent}')

    #     driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
    #     driver.set_window_size(1920, 1080)
    #     driver.get('https://www.exito.com/mercado/')
        
    #     self.html= driver.page_source
    #     driver.close()   

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.exito.com/mercado/',
            wait_time=15,
            screenshot=True,
            callback=self.parse,    
            #headers={'permissions-policy': 'interest-cohort=()'}
            headers={'User-Agent': self.userAgent}
        )
    # def parse(self, response):
    #     macrocategorias=response.xpath("//div[contains(@class,'exito-filters-0-x-categoryItemChildren')]")
    #     macrocategorias_df=[]
    #     for macrocategoria in macrocategorias:
    #         nombre=macrocategoria.xpath(".//text()").get()
    #         nombre_limpio=nombre.replace(',','').lower().replace(' ','-')
    #         macrocategorias_df.append(nombre_limpio)
    #         yield{'nombre':nombre_limpio}
    #     print(macrocategorias_df)
    #     pass
    def parse(self, response):
        #pass
        # img=response.meta['screenshot']
        # with open('screenshot.png','wb') as f:
        #     f.write(img)  
        driver=response.meta['driver']
        search_input=driver.find_element_by_xpath("//input[@id='react-select-2-input']")
        search_input.send_keys('Bogotá')
        #driver.save_screenshot('set location.png')   
        search_input.send_keys(Keys.ENTER)
        #driver.save_screenshot('send location.png')          
        confirm_button=driver.find_element_by_xpath("//div[@class='exito-geolocation-3-x-requestEmailActions flex justify-center']")
        confirm_button.click()
        driver.set_window_size(1920, 1080)
        #driver.maximize_window()
        #driver.save_screenshot('confirm location.png') 
        print("_________________________________________________yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy________________________________________________")
        html=driver.page_source
        response_obj=Selector(text=html)
        #print(str(response_obj)) no pude hacer este
        #driver.save_screenshot('confirm location3.png') 
        macrocategorias=response_obj.xpath("//div[contains(@class,'exito-filters-0-x-categoryItemChildren')]")
        print("_________________________________________________zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz________________________________________________")
        print("cantidad macrocategorias: "+str(len(macrocategorias)))
        macrocategorias_df=[]
        for macrocategoria in macrocategorias[0:1]:
            nombre=macrocategoria.xpath(".//text()").get()
            nombre_limpio=nombre.replace(',','').lower().replace(' ','-')
            macrocategorias_df.append(nombre_limpio)
            #yield{'nombre':nombre_limpio}
            print('https://www.exito.com/mercado/'+nombre_limpio+'/')
            yield SeleniumRequest(
                url='https://www.exito.com/mercado/'+nombre_limpio+'/',
                wait_time=30,
                screenshot=True,
                callback=self.parse_macrocategoria,
                meta={'macrocategoria':nombre_limpio},
                #headers={'permissions-policy': 'interest-cohort=()'}
                headers={'User-Agent': self.userAgent}
            ) 
    def parse_macrocategoria(self, response):
        macrocategoria_meta=response.meta['macrocategoria']
        driver=response.meta['driver']        
        driver.set_window_size(1920, 1080)
        
        #driver.maximize_window()
        #driver.manage().window().fullscreen()

        #options = Options()
        #options.page_load_strategy = 'eager'

        #lo siguiente no es necesario pues antes ya lo hice en el metodo parse
        #driver.save_screenshot('macrocategoria_page03.png') 
        # search_input=driver.find_element_by_xpath("//input[@id='react-select-2-input']")
        # search_input.send_keys('Bogotá')
        # search_input.send_keys(Keys.ENTER)       
        # confirm_button=driver.find_element_by_xpath("//div[@class='exito-geolocation-3-x-requestEmailActions flex justify-center']")
        # confirm_button.click()        
        # driver.set_window_size(1920, 1080)
        # driver.save_screenshot('macrocategoria_page1.png')   
         
        # prueba para ver si estaba capturando los productos     
        print("_________________________________________________aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa________________________________________________")
        productos=response.xpath("//div[contains(@class,'vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryI')]")
        print("cantidad productos: "+str(len(productos)))
        # yield{
        #     'num_productos':len(productos)
        # } 
        #load_products_button=response.xpath("//button[contains(@class,'vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h')]")
        #load_products_button=driver.find_elements_by_xpath("//button[contains(@class,'vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--')]")
        #print("elemento boton tamano: "+str(len(load_products_button)))        

        #se comenda esto. Antse se usaba cuando solo se sacaba la info de la primera pagina.
        # for producto in productos:
        #     yield{
        #         'nombre':producto.xpath(".//section/a/article/div/div[@class='exito-product-summary-3-x-nameContainer undefined ']/div/text()").get()
        #         ,'precio':producto.xpath(".//section/a/article/div/div[contains(@style,'display: initial')]/div/span/text()").get()
        #         ,'descuento':producto.xpath(".//section/a/article/div/div[contains(@class,'exito-product-details-3-x-elementScroll')]/div/div/text()").get()
                
        #     }
        
        # load_products_button=driver.find_element_by_xpath("//button[contains(@class,'vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--small bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer')]")
        # load_products_button.click() 
        # productos=response.xpath("//div[contains(@class,'vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryI')]")
        # load_products_button=driver.find_element_by_xpath("//button[contains(@class,'vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--small bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer')]")
        # load_products_button.click()
        # load_products_button=driver.find_element_by_xpath("//button[contains(@class,'vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--small bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer')]")
        # load_products_button.click()
        # print("cantidad productos2: "+str(len(productos)))

        # load_products_button=driver.find_element_by_xpath("//button[.='Mostrar más']")
        # load_products_button.click() 
        # html=driver.page_source
        # response_obj=Selector(text=html)

        #productos=response_obj.xpath("//div[contains(@class,'vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryI')]")
        #print("cantidad productos2: "+str(len(productos)))
        next_page=response.xpath("//button[.='Mostrar más']").get()
        #driver.save_screenshot('carness_1.png') 
        #c=1
        while next_page:
            #c=c+1
            load_products_button=driver.find_element_by_xpath("//button[.='Mostrar más']")
            load_products_button.click()                                                                
            html=driver.page_source
            response_obj=Selector(text=html)
            productos=response_obj.xpath("//div[contains(@class,'vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryI')]")
            print("________________cantidad productos3: "+str(len(productos)))
            next_page=response_obj.xpath("//button[.='Mostrar más']").get()      
            #driver.save_screenshot('carness_'+str(c)+'.png') 
        #load_products_button=driver.find_element_by_xpath("//button[.='Mostrar más']")
        #load_products_button.click()                                                                
        #html=driver.page_source
        #response_obj=Selector(text=html)
        productos=response_obj.xpath("//div[contains(@class,'vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryI')]")
        print("________________cantidad productos final: "+str(len(productos)))

        for producto in productos:
            yield{
                'macrocategoria':macrocategoria_meta
                ,'id':producto.xpath(".//section/a/article/div/div[1]/div/div/@id").get()
                ,'nombre':producto.xpath(".//section/a/article/div/div[@class='exito-product-summary-3-x-nameContainer undefined ']/div/text()").get()
                ,'precio':producto.xpath(".//section/a/article/div/div[contains(@style,'display: initial')]/div/span/text()").get()
                ,'descuento':producto.xpath(".//section/a/article/div/div[contains(@class,'exito-product-details-3-x-elementScroll')]/div/div/text()").get()
                #//div[contains(@class,'exito-product-details-3-x-badgeExito absolute f6 ph1 flex items-center pv1 search-result-exito-product-summary-name-product-name')]
            }        
        #print(macrocategorias_df)
        #//div[@class='vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal pa4']
        
 
        #resp=Selector(text=self.html)      
        #print(self.html)
        #//div[@class='exito-autocomplete-3']
        #display: inline-block;
        #//button[@class='exito-geolocation-3-x-primaryButton shippingaddress-confirmar']
        #//button[contains(@class,'vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2 min-h-small t-action--small bg-action-primary b--action-primary c-on-action-primary hover-bg-action-primary hover-b--action-primary hover-c-on-action-primary pointer')]
        #//div[contains(@class,'flex f5 fw5 pa0 flex items-center justify-start w-100 search-result-exito-vtex-components-selling-price exito-vtex-components-4-x-alliedDiscountPrice')]/text()
        #//div[contains(@class,'exito-product-details-3-x-stylePlp')]/text()
        
