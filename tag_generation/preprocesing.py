"""Preprocessing for tag generation"""

from tag_generation.util import utils
import jsonlines
import csv


def get_recipe_tags(file_name: str,
                    common_tags: list):
    """Get a dict with preparation steps and tags"""
    with jsonlines.open(file_name) as reader:
        for recipe in reader:
            if 'preparation_steps' not in recipe:
                print(f"Skipped {recipe['name']}")
                continue
            target = {'preparation_steps': ''.join(recipe['preparation_steps'][0])}
            if 'tags' not in recipe:
                target.update({tag: 0 for tag in common_tags})
            else:
                for tag in common_tags:
                    target[tag] = 1 if tag in recipe['tags'] else 0
            yield target


def create_tag_gen_file(file_name: str,
                        common_tags: list,
                        target_file):
    with open(target_file, 'w') as csvfile:
        fieldnames = ['preparation_steps'] + common_tags
        recipewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        recipewriter.writeheader()
        recipe_tags = get_recipe_tags(file_name, common_tags)
        for row in recipe_tags:
            recipewriter.writerow(row)


if __name__ == '__main__':
    #For test
    #file_loc = '/home/krispin/data/improved-happiness/'
    #For dev
    file_loc = '/home/krispin/data/improved-happiness/proto/'
    file_name = file_loc + 'recipes.jl'
    k = 6
    _tags = utils.get_k_most_common_tags(k, file_name)
    _tags = [x for (x, c) in _tags]
    trg_filename = file_loc + 'recipe_tags.csv'
    create_tag_gen_file(file_name, _tags, trg_filename)
