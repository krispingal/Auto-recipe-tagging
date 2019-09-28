"""Preprocessing for tag generation"""

from tag_generation.util import utils
import jsonlines
import csv

# For test
FILE_LOC = '/home/krispin/data/improved-happiness/'
# For dev
#FILE_LOC = '/home/krispin/data/improved-happiness/proto/'

skipped, wrote = 0, 0

def get_recipe_tags(file_name: str,
                    common_tags: list):
    """Get a dict with preparation steps and tags"""
    global skipped, wrote
    with jsonlines.open(file_name) as reader:
        for recipe in reader:
            if 'preparation_steps' not in recipe or (not recipe['preparation_steps'][0].strip()) \
                    or recipe['preparation_steps'][0].strip() == 'N/A':
                skipped += 1
                continue
            target = {'preparation_steps': ''.join(recipe['preparation_steps'][0])}
            target['name'] = recipe['name'][0]
            wrote += 1
            if 'tags' not in recipe:
                target.update({tag: 0 for tag in common_tags})
            else:
                for tag in common_tags:
                    target[tag] = 1 if tag in recipe['tags'][0] else 0
            yield target


def create_tag_gen_file(file_name: str,
                        common_tags: list,
                        target_file):
    with open(target_file, 'w') as csvfile:
        fieldnames = ['name', 'preparation_steps'] + common_tags
        recipewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        recipewriter.writeheader()
        recipe_tags = get_recipe_tags(file_name, common_tags)
        for row in recipe_tags:
            recipewriter.writerow(row)


def main(k: int = 6):
    _file_name = FILE_LOC + 'recipes.jl'
    _tags = utils.get_k_most_common_tags(k, _file_name)
    _tags = [x for (x, c) in _tags]
    trg_filename = FILE_LOC + 'recipe_tags.csv'
    create_tag_gen_file(_file_name, _tags, trg_filename)
    print(f'Wrote {wrote} records; skipped {skipped}')


if __name__ == '__main__':
    main(k=10)