""""Common functions"""
import jsonlines
from collections import Counter
from pprint import pprint

def get_k_most_common_tags(k, file_loc):
    recipes = get_recipe(file_loc=file_loc)
    tag_counter = Counter()
    for idx, recipe in enumerate(recipes):
        try:
            tags = recipe['tags'][0].split(',')
            tag_counter.update(tags)
        except:
            pprint(recipe)
            break
    return tag_counter.most_common(k)

def get_recipe(file_loc):
    with jsonlines.open(file_loc) as reader:
        for recipe in reader:
            yield recipe
