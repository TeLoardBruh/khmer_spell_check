from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json
import os
import pkg_resources
from symspellpy import SymSpell, Verbosity
from hunspell import Hunspell
from itertools import islice
from fastapi.middleware.cors import CORSMiddleware

from hunspell import Hunspell
import json
import time

from util.rnn import segment
SPACE = '\u200b'

# load both dictionary.
with open('files/split/ph_to_kh_dict.json') as f:
  ph_to_kh_dict = json.load(f)
with open('files/split/kh_to_ph_dict.json') as f:
  kh_to_ph_dict = json.load(f)

# term_index is the column of the term and count_index is the
# column of the term frequency
# sym_spell_s.load_dictionary(dictionary_path, 0, 1, encoding="utf8")

# load hunspell.
hunspell = Hunspell('km_KH', hunspell_data_dir='files/dict')

# call symspell for spliting the input
# sym_spell_s = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = './files/dict/own_dic_v2.txt'

# importing for testing performance purpose 
import time
start_time = time.time()
# print(start_time)
def timeCounter():

    a = time.time() - start_time
    # print("Elapsed time:", t1_stop, 'ns', t1_start, 'ns') 
    return a
# =========================================

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


origins = [
    "http://localhost",
    # i use port 400 for frontend
    "http://localhost:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, words):
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = './files/dict/own_dic_v2.txt'

    sym_spell.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    result = sym_spell.lookup(words, Verbosity.CLOSEST,
                              max_edit_distance=2,)

    results = []

    list_k_p = {}
    kh_w_frontend = []
    if words:
        for suggestion in result:
            results.append(suggestion)
        for i in results:
            a = check_to_pho(i.term)
            # print((a))
            kh, ph = a
            kh_w_frontend.append(kh)
            list_k_p[kh] = ph.replace(" ", "")
        # return {"str": list_k_p,'each word': 'word'}
    return templates.TemplateResponse("index.html", {"request": request, "id": list_k_p, "kh": kh_w_frontend})


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

    return {"str": words, }


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
    return {"str": results, 'each word': 'word'}


# words sym pho
def check_to_pho(string):
    
    f = open("./files/dict/word_phonemic_final.txt", "r", encoding="utf8")
    wordsDict = {}
    # test = f.read().split()
    with open("./files/dict/own_dic_p.txt", "r", encoding='utf8') as myfile:
        data = myfile.read().splitlines()
        for i in data:
            # print(i.split(' ',1)[1])
            khmer_w = i.split(' ', 1)[0]
            khmer_p = i.split(' ', 1)[1]
            # wordsDict[khmer_w+khmer_p] = 1
            wordsDict[khmer_w] = str(khmer_p)
            # print(khmer_p)
        # wordsDict.append(data)

    f.close()
    newV = []
    k = []
    for kIf, v in wordsDict.items():
        if string.strip() == kIf:
            newVIf = v.split('1', 1)[0]
            timeCounter()
            newV.append(newVIf)

    for ks, v in wordsDict.items():
        for i in newV:
            if i == v.split('1', 1)[0]:
                k.append(ks)
                # print(k + ' : '+ newV)
    print(k)
    if len(newV) == 0:
        return string
    else:
        # print(newV)
        return str(k), str(newV)

# 
def improveWordsToPho(string):
    f = open("./files/dict/test1.json", "r", encoding="utf8")
    wordsDict = {}
    # test = f.read().split()
    with open("./files/dict/own_dic_p.txt", "r", encoding='utf8') as myfile:
        data = myfile.read().splitlines()
        for i in data:
            # print(i.split(' ',1)[1])
            khmer_w = i.split(' ', 1)[0]
            khmer_p = i.split(' ', 1)[1]
            # wordsDict[khmer_w+khmer_p] = 1
            wordsDict[khmer_w] = str(khmer_p)
            # print(khmer_p)
        # wordsDict.append(data)

    f.close()
    newV = []
    k = []
    for kIf, v in wordsDict.items():
        if string.strip() == kIf:
            newVIf = v.split('1', 1)[0]
            timeCounter()
            newV.append(newVIf)

    for ks, v in wordsDict.items():
        for i in newV:
            if i == v.split('1', 1)[0]:
                k.append(ks)
                # print(k + ' : '+ newV)
    # print(k)
    if len(newV) == 0:
        return string
    else:
        # print(newV)
        return str(k), str(newV)
    

@app.get("/words_correct_sp/{str}")
def read_item(str: str):
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = './files/dict/own_dic_v2.txt'

    sym_spell.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    result = sym_spell.lookup(str, Verbosity.CLOSEST,
                              max_edit_distance=2,)

    results = []

    list_k_p = {}
    for suggestion in result:
        results.append(suggestion)
    for i in results:
        a = check_to_pho(i.term)
        # print((a))
        kh, ph = a
        list_k_p[kh] = ph
    return {"str": list_k_p, 'each word': 'word'}

# word correction in hunspell


@app.get("/words_correct_h/{str}")
def read_item(str: str):
    # ignore for check correction.
    ignore_txts = ('៛', '០', '១', '២', '៣', '៤', '៥' , '៦', '៧', '៨', '៩')

    # segment the input.
    # result = sym_spell_s.word_segmentation('ខ្ញុំ​ស្រលាអ្នក')
    result = segment('ខ្ញុំ​ស្រលាអ្នក')
    # words = result[0].replace(SPACE, ' ')
    # raw_words = tuple(set(words.split()))
    raw_words = result

    suggested_words = {}
    for raw_word in raw_words:
        if raw_word not in ignore_txts and not hunspell.spell(raw_word):
            look_similars = hunspell.suggest(raw_word)
            sound_similars = []
            for look_similar in look_similars:
                sound_similar = kh_to_ph_dict.get(look_similar)
                if sound_similar != None:
                    for ph in sound_similar:
                        kh_txts = ph_to_kh_dict.get(ph)
                        if kh_txts != None:
                            sound_similars.extend(kh_txts)

        suggested_words[raw_word] = list(set(look_similars + tuple(sound_similars)))

    return {'suggested_word': suggested_words}


# words seg + correction
@app.get("/words_sc/{str}")
def read_item(str: str, q: Optional[str] = None):
    timer  = timeCounter()
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
    # print("{}, {}, {}".format(result.corrected_string, result.distance_sum,
    #                           result.log_prob_sum))
    # print(type(words))
    segmentation_split = words.split()
    segmentation_split_res = []
    res_arr = []
    kh_pho_arr = {}
    for i in segmentation_split:
        segmentation_split_res.append(i)
        # print(i)
    for i in range(len(segmentation_split_res)):
        # print(arr[i])
        result = sym_spell_c.lookup(segmentation_split_res[i], Verbosity.CLOSEST,
                                    max_edit_distance=2)
        for suggestion in result:
            res_arr.append(suggestion.term)
        # res.append(result)
    for i in res_arr:
        a = improveWordsToPho(i)
        # print(a)
        kh, ph = a
        kh_pho_arr[kh] = ph

    return {"sentence : ": words, "words in segment correction : ": kh_pho_arr, "timer : " : timer}


# Sambath Works start Here

@app.get("/spell-check/{input}")
def read_item(input: str):
    timer  = timeCounter()
    sym_spell_s = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
    sym_spell_c = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = './files/dict/own_dic_v2.txt'
    sym_spell_s.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    sym_spell_c.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    result = sym_spell_s.word_segmentation(input)
    words = result[0]
    raw_words_splited = words.split()
    # return raw_words_splited
    words_splited = []

    for se in raw_words_splited:
        if se != "​​" and se != "​" and se != "។​" and se != "៛": 
            words_splited.append(se)

    toReturn = []

    wordsDict = {}
    with open("./files/dict/own_dic_p.txt", "r", encoding='utf8') as myfile:
        data = myfile.read().splitlines()
        for i in data:
            khmer_w = i.split(' ', 1)[0]
            khmer_p = i.split(' ', 1)[1]
            wordsDict[khmer_w] = str(khmer_p)
    key_list = list(wordsDict.keys())
    val_list = list(wordsDict.values())

    for word in words_splited:
        result = sym_spell_c.lookup(word, Verbosity.CLOSEST, max_edit_distance=2,)
        # correct
        if(len(result) == 1 and result[0]._distance == 0):
            toPush = {
                "segment": word,
                "isCorrect": True
            }
            toReturn.append(toPush)
            continue
        # incorrect
        toPush = {
            "segment": word,
            "isCorrect": False,
        }
        allSuggestions = []
        for i in result:
            wordsListWithTheSamePhonetic = []
            khmerWord = i._term
            print("khmerWord")
            phonetic = wordsDict[khmerWord]
            all_indexes = [] 
            for phoneticIndex in range(0, len(val_list)) : 
                if val_list[phoneticIndex] == phonetic : 
                    all_indexes.append(phoneticIndex)
            for rightIndex in all_indexes:
                wordsListWithTheSamePhonetic.append(key_list[rightIndex])
            
            for sug in wordsListWithTheSamePhonetic:
                allSuggestions.append(sug)
        
        toPush["suggestions"] = allSuggestions
        toReturn.append(toPush)
    
    return {"segementsWithSuggestions": toReturn, "segments": words_splited, "vl": val_list}
