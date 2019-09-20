# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.pipelines.images import ImagesPipeline

OUT_DIR = '/home/krispin/data/improved-happiness/'

class JsonWriterPipeline(ImagesPipeline):

    def open_spider(self, spider):
        self.file = open(f'{OUT_DIR}recipes.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item.asdict(item)) + "\n"
        self.file.write(line)
        return item
