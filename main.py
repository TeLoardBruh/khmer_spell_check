from typing import Optional

from fastapi import FastAPI

import json
import os
import pkg_resources
from symspellpy import SymSpell, Verbosity
from hunspell import Hunspell


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}





# word_segmentation 

@app.get("/words/{str}")
def read_item(str: str, q: Optional[str] = None):
    sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
    dictionary_path = './files/dict/own_dic_v2.txt'
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    # print(sym_spell.words.items())
    # lookup suggestions for single-word input strings
    input_term = "ខ្ញុំចង់"  # misspelling of "members"
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


# word correction in SymSpell

@app.get("/words_correct_s/{str}")
def read_item(str: str):
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = './files/dict/own_dic_v2.txt'

    sym_spell.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    result = sym_spell.lookup(str, Verbosity.CLOSEST,
                               max_edit_distance=2)
    results = []
    for suggestion in result:
        results.append(suggestion)
    return {"str": results,'each word': 'word'}


# word correction in hunspell

@app.get("/words_correct_h/{str}")
def read_item(str: str):
    # adding the dictionary
    h = Hunspell('km_KH', hunspell_data_dir='./files/dict')
    # True
    print(h.spell('ស្រឡាញ់'))
    if(h.spell(str)):
        return {"str": str,'each word': 'word'}
    else:
        result = h.suggest(str)
        return {"str": result,'each word': 'word'}


# words seg + correction
@app.get("/words_sc/{str}")
def read_item(str: str, q: Optional[str] = None):
    sym_spell_s = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
    sym_spell_c = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = './files/dict/own_dic_v2.txt'
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell_s.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    sym_spell_c.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    # print(sym_spell.words.items())
    # lookup suggestions for single-word input strings
    input_term = "ខ្ញុំចង់"  # misspelling of "members"
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_dictionary_edit_distance)
    # suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST,
    #                            max_edit_distance=2, )
    # # display suggestion term, term frequency, and edit distance
    # # display suggestion term, term frequency, and edit distance
    # print("in here")
    # for suggestion in suggestions:
    #     print(suggestion)
    result = sym_spell_s.word_segmentation(str)
    words = result.corrected_string
    print("{}, {}, {}".format(result.corrected_string, result.distance_sum,
                          result.log_prob_sum))
    # print(type(words))
    segmentation_split = words.split()
    segmentation_split_res = []
    res_arr = []
    for i in segmentation_split:
        segmentation_split_res.append(i)
        # print(i)
    for i in range(len(segmentation_split_res)):
        # print(arr[i])
        result = sym_spell_c.lookup(segmentation_split_res[i], Verbosity.CLOSEST,
                               max_edit_distance=2)
        for suggestion in result:
            res_arr.append(suggestion)
        # res.append(result)

    return {"sentence : ": words,"words in segment correction : ": res_arr }
    
    