import scrapy
from scrapy.loader import ItemLoader
from crawler.items import Recipe
from pprint import pprint

#switch for development
DEV = True

class RecipesSpider(scrapy.Spider):
    name = "recipes"
    start_urls = [
            "https://www.epicurious.com/search/?content=recipe&page=1"
        ]

    def parse(self, response):
        """ Parse search pages
            Iterate over each recipe in the search page and invoke
            parse_recipe to etract data
        """
        _, _, page_num = response.url.partition('page=')
        page_num = int(page_num)

        recipe_urls = response.xpath('//a[@class="view-complete-item"]/@href').getall()
        for recipe in recipe_urls[:5]:
            yield response.follow(recipe, self.parse_recipe)
        if page_num % 20 == 0:
            self.logger.info(f'Processed {page_num}')

        next_page = response.xpath('//a[@class="a-next-page"]/@href').get()
        if next_page:
            if DEV and page_num > 3:
                return
            yield response.follow(next_page, self.parse)

    def parse_recipe(self, response):
        """ Extract data from recipe

        :param response:
        :return:
        """
        r_name = response.url.split("/")[-1]
        print(r_name)
        r = ItemLoader(item=Recipe(), response= response)
        r.add_value('name', r_name)
        r.add_xpath('servings', '//dd[@class="yield"]/text()')
        r.add_xpath('ingredients', '//li[@class="ingredient"]/text()')
        r.add_xpath('preparation_steps', '//li[@class="preparation-step"]/text()')
        r.add_xpath('rating', '//span[@class="rating"]/text()')
        r.add_xpath('tags', '//meta[@name="keywords"]/@content')
        r.load_item()
        pprint(r)
        #r.add_xpath()
        #r.add_xpath()
        #recipe_name = response.url.split("/")[-1]
        #servings = response.xpath('//dd[@class="yield"]/text()').get().split(' ')[0]
        #ingredients = response.xpath('//li[@class="ingredient"]/text()').getall()
        #preparation_steps = self.clean_prep_step(response.xpath('//li[@class="preparation-step"]/text()').getall())
        #rating = response.xpath('//span[@class="rating"]/text()').get()
        #tags = response.xpath('//meta[@name="keywords"]/@content').get()

        #print(f'{response.url},   {recipe_name}')

