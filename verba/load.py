import csv
import itertools
from importlib.resources import files
from verba.word.noun import Noun
from verba.word.word_key import WordKey as WK

def line_product(line):
    line = {k: v.split() for k, v in line.items()}
    line = {k: v for k, v in line.items() if v}
    for p in itertools.product(*line.values()):
        yield dict(zip(line.keys(), p))

def load_keys(library_name):
    keys = {}
    with files('verba.data').joinpath(library_name).joinpath('keys.tsv').open(encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            chapter = int(line['chapter'])
            pofs = line['part_of_speech']
            keys.setdefault(pofs, [])
            for lp in line_product(line):
                key = WK(*[v for k,v in lp.items() 
                           if k != 'chapter' and k != 'part_of_speech']) 
                keys[pofs].append((chapter, key))

    # add default key for words that don't decline
    for pofs in keys.keys():
        keys[pofs].append((0, WK('default')))

    return keys

def load_words(library_name):
    words = []

    with files('verba.data').joinpath(library_name).joinpath('words.tsv').open(encoding='utf-16') as file:
        tsv_file = csv.DictReader(file, delimiter='\t')
        for line in tsv_file:
            if line['part_of_speech'] == 'noun':
                words.append(Noun(line))

    return words