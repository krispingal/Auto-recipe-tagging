# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Compose, MapCompose


def clean_prep_step(prep_step: str):
    return prep_step.strip().replace('\n', '')

def extract_num_servings(servings: str):
    return servings.split(' ')[0]

class Recipe(scrapy.Item):
    name = scrapy.Field()
    servings = scrapy.Field(input_processor=Compose(TakeFirst(), extract_num_servings))
    ingredients = scrapy.Field()
    preparation_steps = scrapy.Field(input_processor=MapCompose(clean_prep_step))
    rating = scrapy.Field(input_processor=TakeFirst())
    tags = scrapy.Field(input_processor=TakeFirst())
