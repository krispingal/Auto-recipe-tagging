""""Common functions"""
import jsonlines

def get_recipe(file_loc):
    with jsonlines.open(file_loc) as reader:
        for recipe in reader:
            yield recipe
