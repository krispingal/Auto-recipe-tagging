import scrapy

#switch for development
DEV = True

class RecipesSpider(scrapy.Spider):
    name = "recipes"
    start_urls = [
            "https://www.epicurious.com/search/?content=recipe&page=1"
        ]

    def parse(self, response):
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
        recipe_name = response.url.split("/")[-1]
        print(f'{response.url},   {recipe_name}')