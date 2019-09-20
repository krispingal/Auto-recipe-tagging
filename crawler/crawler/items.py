# -*- coding: utf-8 -*-


import scrapy
from scrapy.loader.processors import TakeFirst, Compose, MapCompose

def clean_prep_step(prep_step: str):
    return prep_step.strip().replace('\n', '')

def extract_num_servings(servings: str):
    return servings.split(' ')[0]

class Recipe(scrapy.Item):
    name = scrapy.Field(input_processor=TakeFirst())
    servings = scrapy.Field(input_processor=Compose(TakeFirst(), extract_num_servings))
    ingredients = scrapy.Field()
    preparation_steps = scrapy.Field(input_processor=MapCompose(clean_prep_step))
    rating = scrapy.Field(input_processor=Compose(TakeFirst(), TakeFirst()))
    tags = scrapy.Field(input_processor=TakeFirst())
    image_urls = scrapy.Field()
    images = scrapy.Field()

    def asdict(self, item):
        image_fields = set(['image_urls', 'images'])
        item_dict = {x : item[x] for x in item if x not in image_fields}
        item_dict = 
        return item_dict
