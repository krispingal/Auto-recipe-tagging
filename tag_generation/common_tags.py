"""Find the k most common tags"""

from collections import Counter
from tag_generation.util.common import get_recipe
from pprint import pprint

def get_k_most_common_tags(k, file_loc):
    recipes = get_recipe(file_loc=file_loc)
    tag_counter = Counter()
    for idx, recipe in enumerate(recipes):
        try:
            tags = recipe['tags'][0].split(',')
            tag_counter.update(tags)
        except:
            print(idx)
            pprint(recipe)
            break
    return tag_counter.most_common(k)


if __name__ == '__main__':
    file_loc = '/home/krispin/data/improved-happiness/recipes_bkup.jl'
    k = 6
    common_tags = get_k_most_common_tags(k, file_loc)
    print(common_tags)

