from hunspell import Hunspell
h = Hunspell(disk_cache_dir='km_KH.dic')

a = h.spell('កក') # True
print(a)
