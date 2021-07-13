from hunspell import Hunspell
import json
import time

from util.rnn import segment

start_time = time.time()

SPACE = '\u200b'

# call symspell for spliting the input
# sym_spell_s = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = './files/dict/own_dic_v2.txt'

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

print(suggested_words)
end_time = time.time()
print(end_time - start_time)
