# Python Spell checker



## Installation

```bash
# for installing the lib to use
pip install symspellpy
pip install cyhunspell

# setting up api
pip install fastapi
pip install uvicorn[standard]
```

## Py files
```files 

app.py contain Tuple stuff

romanization.py contain some functions that helps convert normal dict files into sys_spell dict

jamspell.py contain extra info on another libs 

```

## Usage

```python
# window
env\Scripts\activate

# mac or linux
source env/bin/activate


# to run fastapi
uvicorn main:app --reload # allows to auto refresh 
uvicorn main:app # normal luanch

# use fastapi to test
# after luanch can access this link for friendly UI to test
http://127.0.0.1:8000/docs

# or you can 
http://127.0.0.1:8000/words_correct_h/yours_khmer_words #hunspell

http://127.0.0.1:8000/words_correct_s/yours_khmer_words #sys_spell

both will return in json format


# files dictionary are in 
./files/dict/*

# feedback and comments files
./files/feedback

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
