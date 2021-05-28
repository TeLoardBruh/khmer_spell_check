from typing import Optional

from fastapi import FastAPI

import json
import pkg_resources
from symspellpy import SymSpell, Verbosity


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/words/{str}")
def read_item(str: str, q: Optional[str] = None):
    sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
    dictionary_path = './files/dict/own_dic.txt'
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    # print(sym_spell.words.items())
    # lookup suggestions for single-word input strings
    input_term = "ខ្ញុំ ចង់"  # misspelling of "members"
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_dictionary_edit_distance)
    # suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST,
    #                            max_edit_distance=2, )
    # # display suggestion term, term frequency, and edit distance
    # # display suggestion term, term frequency, and edit distance
    # print("in here")
    # for suggestion in suggestions:
    #     print(suggestion)
    result = sym_spell.word_segmentation(str)
    words = result.corrected_string
    print("{}, {}, {}".format(result.corrected_string, result.distance_sum,
                          result.log_prob_sum))
    return {"str": words,}