import json
import pkg_resources
from symspellpy import SymSpell, Verbosity


def create_ditc():
    sym_spell = SymSpell()
    corpus_path = './km_KH.txt'
    sym_spell.create_dictionary(corpus_path,encoding='utf8')


    # creating file 
    with open('own_dic.txt', 'w', encoding='utf-8') as file:
        for key, value in sym_spell.words.items(): 
            file.write('%s %s \n' % (key, value)) # use `json.loads` to do the reverse


    print((sym_spell.words.items()))


def check_up():
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = './own_dic.txt'
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    # print(sym_spell.words.items())
    # lookup suggestions for single-word input strings
    input_term = "ចក"  # misspelling of "members"
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_dictionary_edit_distance)
    suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST,
                               max_edit_distance=2, )
    # display suggestion term, term frequency, and edit distance
    # display suggestion term, term frequency, and edit distance
    print("in here")
    for suggestion in suggestions:
        print(suggestion)


check_up()