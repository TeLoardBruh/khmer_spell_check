

def getSuggestionByPhonetic(word):
    phonetic = ""
    wordsListWithTheSamePhonetic = []

    f = open("./files/dict/word_phonemic_final.txt", "r",encoding="utf8")
    with open ("./files/dict/own_dic_p.txt", "r",encoding='utf8') as myfile:
        lines = myfile.read().splitlines()
        for i in lines:
            khmerWordInLine = i.split(' ',1)[0]
            phoneticInLine = i.split(' ',1)[1]
            if(word == khmerWordInLine):
                phonetic = phoneticInLine
                break
        for i in lines:
            khmerWordInLine = i.split(' ',1)[0]
            phoneticInLine = i.split(' ',1)[1]
            if(phonetic == phoneticInLine):
                wordsListWithTheSamePhonetic.append(khmerWordInLine)
    f.close()
    return wordsListWithTheSamePhonetic

def getSuggestionBySymSpell(word):
    sym_spell = SymSpell(max_dictionary_edit_distance = 2, prefix_length=7)
    dictionary_path = './files/dict/own_dic_v2.txt'
    sym_spell.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    results = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2,)
    return results


@app.get("/spell-check/{input}")
def read_item(input: str):
    sym_spell_s = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
    sym_spell_c = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = './files/dict/own_dic_v2.txt'
    sym_spell_s.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    sym_spell_c.load_dictionary(dictionary_path, 0, 1, encoding="utf8")
    result = sym_spell_s.word_segmentation(input)
    words = result[0]
    words_splited = words.split()

    toReturn = []
    for word in words_splited:
        result = getSuggestionBySymSpell(word)
        # correct
        if(len(result) == 1):
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
            suggestionsByPhonetic = getSuggestionByPhonetic(i._term)
            for sug in suggestionsByPhonetic:
                allSuggestions.append(sug)
        toPush["suggestions"] = allSuggestions
        toReturn.append(toPush)

    return {"str": toReturn}