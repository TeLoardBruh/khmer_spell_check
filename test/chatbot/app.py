from symspellpy import SymSpell, Verbosity

def words_seg():
    sym_spell_s = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
    sym_spell_c = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = '../../files/dict/own_dic_v2.txt'
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell_s.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    sym_spell_c.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    # print(sym_spell.words.items())
    # lookup suggestions for single-word input strings
    input_term = "តើខ្ញុំអាចសួរអ្នកអំពីអាហារូបករណ៍សាលាបានទេ?"  # misspelling of "members"
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_dictionary_edit_distance)
    # suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST,
    #                            max_edit_distance=2, )
    # # display suggestion term, term frequency, and edit distance
    # # display suggestion term, term frequency, and edit distance
    # print("in here")
    # for suggestion in suggestions:
    #     print(suggestion)
    result = sym_spell_s.word_segmentation(input_term)
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
    for i in res_arr:
        print(i)

words_seg()