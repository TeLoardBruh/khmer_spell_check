import json
source = open('files/dict/word_phonemic_final.txt', 'r')

lines = source.readlines()

json_dict = {}
for line in lines:
  split_line = line.split()
  kh_text = split_line[0]
  if len(kh_text) == 1:
    char_type = 'consonant'
    json_dict[kh_text] = {
      'rep': ''.join((''.join(split_line[1:])).split('.')),
      'type': char_type,
      'family': 'a'
    }
  # if len(kh_text) == 2 and kh_text[0] == 'អ' and json_dict.get(kh_text[1]) == None:
  #   kh_text = kh_text[1]
  #   char_type = 'vowel'
  #   json_dict[kh_text] = {
  #     'rep': ''.join((''.join(split_line[1:])).split('.')),
  #     'type': char_type,
  #     'family': 'a'
  #   }
  

with open("files/split/dict.json", "w") as outfile: 
      json.dump(json_dict, outfile)


source.close()
