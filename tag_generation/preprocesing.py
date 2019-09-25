"""Preprocessing for tag generation"""

import pandas as pd
from tag_generation.util import utils

def preprocessing(file_loc):
    df = pd.read_json(file_loc, lines=True)
    
if __name__ == '__main__':
    file_loc = '/home/krispin/data/improved-happiness/recipes_bkup.jl'
    k = 6
    common_tags = utils.get_k_most_common_tags(k, file_loc)
    print(common_tags)

