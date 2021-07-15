source = open('files/dict/word_phonemic_final.txt', 'r')
kh_texts = open('files/split/kh_texts.txt', 'w')
phonemic_texts = open('files/split/phonemic_texts.txt', 'w')

lines = source.readlines()

for line in lines:
  split_line = line.split()
  kh_text = split_line[0]
  phonemic_text = ''.join((''.join(split_line[1:])).split('.'))
  kh_texts.write(kh_text+'\n')
  phonemic_texts.write(phonemic_text+'\n')

source.close()
kh_texts.close()
phonemic_texts.close()
