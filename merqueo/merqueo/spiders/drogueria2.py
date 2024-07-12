import scrapy
from scrapy.exceptions import CloseSpider
import json
import pandas

class Drogueria2Spider(scrapy.Spider):
    name = 'drogueria2'
    allowed_domains = ['merqueo.com']
    #start_urls = ['https://merqueo.com/barranquilla/super-ahorro/drogueria/']
    #start_urls = ['https://merqueo.com/api/4.0/store/243/shelf/9250/warehouse/381/ac/1/ex/0/p/1']
    #start_urls = ['https://merqueo.com/api/3.1/stores/243/department/2907/shelves?zoneId=538']
    start_urls = ['https://merqueo.com/api/3.0/cities/main-and-neighborhoods?country_id=1']
    def parse(self, response):

        #if response.status == 500:
        #    raise CloseSpider('Reached last page...')
        ciudades= pandas.DataFrame({"id_ciudad":[],"nombre_ciudad":[],"principal":[],"id_store_covered":[],"warehouse_id_store_covered":[],"zone_id_store_covered":[]})
        resp = json.loads(response.body)
        ciudades_principales=resp.get('data').get('attributes').get('main')
        for ciudad in ciudades_principales:
            id=ciudad.get('id'),
            nombre=ciudad.get('slug'), 
            principal=ciudad.get('is_main'),
            id_store_covered=ciudad.get('store_covered').get('id'),
            warehouse_id_store_covered=ciudad.get('store_covered').get('warehouse_id'),
            zone_id_store_covered=ciudad.get('store_covered').get('zone_id')
            
            ciudad= pandas.DataFrame({"id_ciudad":[id],"nombre_ciudad":[nombre],"principal":[principal],"id_store_covered":[id_store_covered],"warehouse_id_store_covered":[warehouse_id_store_covered],"zone_id_store_covered":[zone_id_store_covered]})
            ciudades=ciudades.append(ciudad)
            
            # yield{
            #     'id':ciudad.get('id'),
            #     'nombre':ciudad.get('slug'), 
            #     'principal':ciudad.get('is_main'),
            #     'id_store_covered':ciudad.get('store_covered').get('id'),
            #     'warehouse_id_store_covered':ciudad.get('store_covered').get('warehouse_id'),
            #     'zone_id_store_covered':ciudad.get('store_covered').get('zone_id')
            # }

        ciudades_vecinas=resp.get('data').get('attributes').get('neighborhoods')
        for ciudad in ciudades_vecinas:
            id=ciudad.get('id'),
            nombre=ciudad.get('slug'), 
            principal=ciudad.get('is_main'),
            id_store_covered=ciudad.get('store_covered').get('id'),
            warehouse_id_store_covered=ciudad.get('store_covered').get('warehouse_id'),
            zone_id_store_covered=ciudad.get('store_covered').get('zone_id')
            
            ciudad= pandas.DataFrame({"id_ciudad":[id],"nombre_ciudad":[nombre],"principal":[principal],"id_store_covered":[id_store_covered],"warehouse_id_store_covered":[warehouse_id_store_covered],"zone_id_store_covered":[zone_id_store_covered]})
            ciudades=ciudades.append(ciudad)            

        zonas_stores=ciudades[['zone_id_store_covered','id_store_covered','warehouse_id_store_covered']].drop_duplicates()
        #for zona_store in zonas_stores:
        for i in range(len(zonas_stores)):
            # yield{
            #     'zona':zona
            # }
            zona=int(zonas_stores.iloc[i]['zone_id_store_covered'])
            ##Ojo, aca tuve que agregar indice 0 porque store estaba quedando como una tupla de 1 elemento
            store=int(zonas_stores.iloc[i]['id_store_covered'][0])
            warehouse_id_store_covered=int(zonas_stores.iloc[i]['warehouse_id_store_covered'][0])
            # if zona != 538:
            #     continue  
            print('zona: '+str(zona) + '; store: '+ str(store) + '; warehouse: '+ str(warehouse_id_store_covered))
            yield scrapy.Request(
                url=f'https://merqueo.com/api/3.0/stores/{store}/menus?zoneId={zona}',
                callback=self.parse_categorias
                ,meta={'zona':zona, 'store_covered':store,'warehouse_id_store_covered':warehouse_id_store_covered}
            )         

            # yield{
            #     'id':ciudad.get('id'),
            #     'nombre':ciudad.get('slug'), 
            #     'principal':ciudad.get('is_main'),
            #     'id_store_covered':ciudad.get('store_covered').get('id'),
            #     'warehouse_id_store_covered':ciudad.get('store_covered').get('warehouse_id'),
            #     'zone_id_store_covered':ciudad.get('store_covered').get('zone_id')
            # }        
        
        
        
        # categorias = resp.get('data')
        # for categoria in categorias[0:2]:
        #     id_categororia=categoria.get('id')
        #     name_categoria=categoria.get('attributes').get('attributes')
            # yield {
            #     'id':id_categororia,
            #     'name':name_categoria,
            #     'url':f'https://merqueo.com/api/4.0/store/243/shelf/{id_categororia}/warehouse/381/ac/1/ex/0/p/1'
            # }
            
            # yield scrapy.Request(
            #     url=f'https://merqueo.com/api/4.0/store/243/shelf/{id_categororia}/warehouse/381/ac/1/ex/0/p/1',
            #     callback=self.parse_items
            #     ,meta={'name_categoria':name_categoria}
            # )

    def parse_categorias(self, response):
        zona_meta=response.meta['zona']
        store_covered_meta=response.meta['store_covered']
        warehouse_meta=response.meta['warehouse_id_store_covered']
        categorias_zona=json.loads(response.body)
        categorias = categorias_zona.get('data')
        categorias_df= pandas.DataFrame({"zona":[],"store_covered":[],"warehouse":[],"id_macrocategoria":[]})
        for categoria in categorias:
            # yield{
            #     'zona':zona,
            #     'store_covered':store_covered,
            #     'id_macrocategoria':categoria.get('id'),
            #     'macrocategoria': categoria.get('attributes').get('slug')          
            # }       
            zona=zona_meta
            store_covered=store_covered_meta
            warehouse=warehouse_meta
            id_macrocategoria=categoria.get('id')
            macrocategoria=categoria.get('attributes').get('slug')     
            
            categoria_df=pandas.DataFrame({"zona":[zona],"store_covered":[store_covered],"warehouse":[warehouse],"id_macrocategoria":[id_macrocategoria]})
            categorias_df= categorias_df.append(categoria_df)
        
        macrocategoria_zona_store=categorias_df[['zona','id_macrocategoria','store_covered','warehouse']].drop_duplicates()
        #for zona_store in zonas_stores:
        #for i in range(len(macrocategoria_zona)):
        #print(macrocategoria_zona_store.iloc[0,:])
        for i in range(1):
            # yield{
            #     'zona':zona
            # }
            zona=int(macrocategoria_zona_store.iloc[i]['zona'])
            ##Ojo, aca tuve que agregar indice 0 porque store estaba quedando como una tupla de 1 elemento
            macrocategoria=int(macrocategoria_zona_store.iloc[i]['id_macrocategoria'])
            store=int(macrocategoria_zona_store.iloc[i]['store_covered'])
            warehouse=int(macrocategoria_zona_store.iloc[i]['warehouse'])
            # zona=int(macrocategoria_zona_store.iat[i,0])
            # macrocategoria=int(macrocategoria_zona_store.iat[i,1][0])
            # store=int(macrocategoria_zona_store.iat[i,2])
            # warehouse=int(macrocategoria_zona_store.iat[i,3][0])            
            # if zona != 538:
            #     continue  
            print('zona: '+str(zona) + '; macrocategoria: '+ str(macrocategoria) + '; store: '+ str(store))
            yield scrapy.Request(
                url=f'https://merqueo.com/api/3.1/stores/{store}/department/{macrocategoria}/shelves?zoneId={zona}',
                callback=self.parse_subcategorias
                ,meta={'zona':zona, 'store_covered':store,'warehouse':warehouse, 'macrocategoria':macrocategoria}
            )
    def parse_subcategorias(self, response):
        #print(response.meta)
        zona_meta=response.meta['zona']
        store_covered_meta=response.meta['store_covered']
        warehouse_meta=response.meta['warehouse']
        macrocategoria_meta=response.meta['macrocategoria']

        subcategorias_zona=json.loads(response.body)
        subcategorias = subcategorias_zona.get('data')
        subcategorias_df= pandas.DataFrame({"zona":[],"store_covered":[],"warehouse":[],"id_macrocategoria":[],"id_subcategoria":[]})
        for subcategoria in subcategorias:
            # yield{
            #     'id_subcategoria':subcategoria.get('id'),
            #     'sub_subcategoria':subcategoria.get('attributes').get('slug')
            # }
            zona=zona_meta
            store_covered=store_covered_meta
            warehouse=warehouse_meta
            id_macrocategoria=macrocategoria_meta           
            id_subcategoria=subcategoria.get('id')
            
            subcategoria_df=pandas.DataFrame({"zona":[zona],"store_covered":[store_covered],"warehouse":warehouse,"id_macrocategoria":[id_macrocategoria],"id_subcategoria":[id_subcategoria]})
            subcategorias_df=subcategorias_df.append(subcategoria_df)

        #subcategoria_zona_warehouse=subcategorias_df[['',''.'']].drop_duplicates()
        #for i in range(len(subcategorias_df)):
        for i in range(1):
            zona=int(subcategorias_df.iloc[i]['zona'])
            ##Ojo, aca tuve que agregar indice 0 porque store estaba quedando como una tupla de 1 elemento
            id_macrocategoria=int(subcategorias_df.iloc[i]['id_macrocategoria'])
            store=int(subcategorias_df.iloc[i]['store_covered'])
            warehouse=int(subcategorias_df.iloc[i]['warehouse'])
            id_subcategoria=int(subcategorias_df.iloc[i]['id_subcategoria'])

            # if zona != 538:
            #     continue  
            print('zona: '+str(zona)  + '; store: '+ str(store) + '; warehouse: '+ str(warehouse) + '; id_macrocategoria: '+ str(id_macrocategoria) + '; id_subcategoria: '+ str(id_subcategoria))
            yield scrapy.Request(
                url=f'https://merqueo.com/api/4.0/store/{store}/shelf/{id_subcategoria}/warehouse/{warehouse}/ac/1/ex/0/p/1',
                callback=self.parse_items
                ,meta={'zona':zona, 'store_covered':store,'warehouse':warehouse, 'id_macrocategoria':id_macrocategoria, 'subcategoria':id_subcategoria}
            )            

    def parse_items(self, response):
        #print('-------------------------------------4llegamos------------------------')
        items_subcategoria=json.loads(response.body)
        items = items_subcategoria.get('data')
        subcategoria_meta=response.meta['subcategoria']
        for item in items:
            yield{
                'subcategoria':subcategoria_meta,
                'name': item.get('attributes').get('name'),
                'price': item.get('attributes').get('price')            
            } 
        # items = resp.get('data')
        # for item in items:
        #     yield {
        #         'name': item.get('attributes').get('name'),
        #         'price': item.get('attributes').get('price')
        #     }
        
        #self.offset += self.INCREMENTED_BY
        # yield scrapy.Request(
        #     url=f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}',
        #     callback=self.parse
        # )
    #def parse(self, response):
    #    pass
