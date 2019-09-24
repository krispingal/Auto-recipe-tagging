import scrapy
from scrapy.loader import ItemLoader
from crawler.items import Recipe

#switch for development
DEV = False

class RecipesSpider(scrapy.Spider):
    name = "recipes"
    start_urls = [
            "https://www.epicurious.com/search/?content=recipe&page=1"
        ]
        

    def parse(self, response):
        """ Parse search pages
            Iterate over each recipe in the search page and invoke
            parse_recipe to extract data
        """
        page_num = response.url.split('page=', 1)[1]
        page_num = int(page_num)

        recipe_urls = response.xpath('//a[@class="view-complete-item"]/@href').getall()
        for recipe in recipe_urls:
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
        r = ItemLoader(item=Recipe(), response=response)
        r.add_value('name', r_name)
        r.add_xpath('servings', '//dd[@class="yield"]/text()')
        r.add_xpath('ingredients', '//li[@class="ingredient"]/text()')
        r.add_xpath('preparation_steps', '//li[@class="preparation-step"]/text()')
        r.add_xpath('rating', '//span[@class="rating"]/text()')
        r.add_xpath('tags', '//meta[@name="keywords"]/@content', default=[])
        return r.load_item()
