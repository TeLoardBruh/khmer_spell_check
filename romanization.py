import json
import pkg_resources
from symspellpy import SymSpell, Verbosity


def create_ditc():
    sym_spell = SymSpell()
    corpus_path = './files/dict/km_KH.txt'
    sym_spell.create_dictionary(corpus_path,encoding='utf8')


    # creating file 
    with open('own_dic.txt', 'w', encoding='utf-8') as file:
        for key, value in sym_spell.words.items(): 
            file.write('%s %s \n' % (key, value)) # use `json.loads` to do the reverse


    print((sym_spell.words.items()))

def create_mydic():
    f = open("./files/dict/km_KH.txt", "r",encoding='utf8')
    lines = []
    linesDict = {}
    

    with open ("./files/dict/km_KH.txt", "r",encoding='utf8') as myfile:
        data = myfile.read().splitlines()
        # print(data)
        lines.append(data)
        for i in data:
            linesDict[i] = 1
    f.close()
    print(linesDict)
    with open('own_dic.txt', 'w', encoding='utf-8') as file:
        for k, v in linesDict.items():
            num = 1
            line = "{} {} \n".format(k,v)
            file.write(line) # use `json.loads` to do the reverse


def check_up():
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = './files/dict/own_dic_p.txt'
    # term_index is the column of the term and count_index is the
    # column of the term frequency
    sym_spell.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    # print(sym_spell.words.items())
    # lookup suggestions for single-word input strings
    input_term = "ចង់"  # misspelling of "members"
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_dictionary_edit_distance)
    suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST,
                               max_edit_distance=2,include_unknown=True)
    # display suggestion term, term frequency, and edit distance
    # display suggestion term, term frequency, and edit distance
    print("in here")
    for suggestion in suggestions:
        print(suggestion)
    # result = sym_spell.word_segmentation(input_term)
    # print("{}, {}, {}".format(result.corrected_string, result.distance_sum,
    #                       result.log_prob_sum))




# phoni

def check_pho():
    f = open("./files/dict/word_phonemic_final.txt", "r",encoding="utf8")
    wordsDict = {}
    # test = f.read().split()
    with open ("./files/dict/word_phonemic_final.txt", "r",encoding='utf8') as myfile:
        data = myfile.read().splitlines()
        
        for i in data:
            # print(i.split(' ',1)[1])
            khmer_w = i.split(' ',1)[0]
            khmer_p = i.split(' ',1)[1].replace(' ','')
            # wordsDict[khmer_w+khmer_p] = 1
            wordsDict[khmer_w+' 1\n'+khmer_p] = str("1")
            # print(khmer_p)
        # wordsDict.append(data)

    f.close()
    # print(wordsDict)
    with open('own_dic_p.txt', 'w', encoding='utf-8') as file:
        for k, v in wordsDict.items():
            num = 1
            line = "{} {} \n".format(k,v)
            file.write(line) # use `json.loads` to do the reverse
    # print(test)
    

def check_to_pho(string):
    f = open("./files/dict/word_phonemic_final.txt", "r",encoding="utf8")
    wordsDict = {}
    # test = f.read().split()
    with open ("./files/dict/word_phonemic_final.txt", "r",encoding='utf8') as myfile:
        data = myfile.read().splitlines()
        
        for i in data:
            # print(i.split(' ',1)[1])
            khmer_w = i.split(' ',1)[0]
            khmer_p = i.split(' ',1)[1].replace(' ','')
            # wordsDict[khmer_w+khmer_p] = 1
            wordsDict[khmer_w] = str(khmer_p+"/1")
            # print(khmer_p)
        # wordsDict.append(data)

    f.close()
    for k,v in wordsDict.items():
        if string == k:
            return v
    return "key doesn't exist"
    print('')

# create function convert files to json 

def convert_to_json():
    fIn = open("./files/dict/word_phonemic_final.txt", "r",encoding="utf8")
    wordsDict = {}
    with open ("./files/dict/word_phonemic_final.txt", "r",encoding='utf8') as myfile:
        data = myfile.read().splitlines()
        
        for i in data:
            # print(i.split(' ',1)[1])
            khmer_w = i.split(' ',1)[0]
            khmer_p = i.split(' ',1)[1].replace(' ','')
            # wordsDict[khmer_w+khmer_p] = 1
            wordsDict[khmer_w] = str(khmer_p)
            # print(khmer_p)
        # wordsDict.append(data)

    fIn.close()
    # print(wordsDict)
    fOut = open("test1.json", "w",encoding="utf8")
    json.dump(wordsDict, fOut, indent = 4,ensure_ascii=False)
    fOut.close()
    # print(wordsDict)
    # pass
# check_pho()
convert_to_json()
# print(check_to_pho("ស្រឡាញ់"))