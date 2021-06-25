import json

kh_files = open('files/split/kh_texts.txt', 'r')
phonemic_files = open('files/split/phonemic_texts.txt', 'r')

kh_texts = kh_files.readlines()
phonemic_texts = phonemic_files.readlines()

ph_to_kh_dict = {}
kh_to_ph_dict = {}
for i, phonemic_text in enumerate(phonemic_texts):
  if ph_to_kh_dict.get(phonemic_text) == None:
    ph_to_kh_dict[phonemic_text.replace('\n', '')] = [kh_texts[i].replace('\n', '')]
    kh_to_ph_dict[kh_texts[i].replace('\n', '')] = [phonemic_text.replace('\n', '')]
  else:
    ph_to_kh_dict[phonemic_text.replace('\n', '')].append(kh_texts[i].replace('\n', ''))
    kh_to_ph_dict[kh_texts[i].replace('\n', '')].append(phonemic_text.replace('\n', ''))

with open("files/split/ph_to_kh_dict.json", "w") as outfile: 
  json.dump(ph_to_kh_dict, outfile)

with open("files/split/kh_to_ph_dict.json", "w") as outfile: 
  json.dump(kh_to_ph_dict, outfile)

kh_files.close()
phonemic_files.close()
