from depedit import DepEdit
import unicodedata
import conllu
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
from tqdm import tqdm

nominal = {
    's': {'Number': 'Sing'},
    'p': {'Number': 'Plur'},
    'm': {'Gender': 'Masc'},
    'f': {'Gender': 'Fem'},
    'n': {'Case': 'Nom'},
    'o': {'Case': 'Acc'},
    'v': {'Case': 'Voc'},
    'a': {'Case': 'Abl'},
    '1': {'Person': '1'},
    '2': {'Person': '2'},
    '3': {'Person': '3'}
}
verbal = {
    'in': {'VerbForm': 'Inf'},
    'c': {'VerbForm': 'Conv'},
    'pr': {'VerbForm': 'Fin', 'Mood': 'Ind', 'Aspect': 'Prosp'},
    's': {'VerbForm': 'Fin', 'Mood': 'Sub'},
    'f': {'VerbForm': 'Fin', 'Mood': 'Ind', 'Tense': 'Fut'},
    'im': {'VerbForm': 'Fin', 'Mood': 'Imp'},
    'p': {'VerbForm': 'Fin', 'Mood': 'Ind', 'Aspect': 'Perf'},
    'i': {'VerbForm': 'Fin', 'Mood': 'Ind', 'Aspect': 'Imp'},
    'pp': {'VerbForm': 'Part', 'Mood': 'Ind', 'Aspect': 'Perf'},
    'ii': {'VerbForm': 'Part', 'Mood': 'Ind', 'Aspect': 'Imp'}
}

def feats(xpos):
    if not xpos:
        return None
    parts = xpos.split('_')
    res = {}
    if parts[0] == 'v':
        if len(parts) > 1:
            res = {**res, **verbal[parts[1]]}
        if len(parts) == 3:
            for i in parts[2]:
                res = {**res, **nominal[i]}
    elif len(parts) == 2:
        for i in parts[1]:
            res = {**res, **nominal[i]}
    return res if res != {} else None

 
infile = open("../pa_puntb-ud-test.conllu")
d = DepEdit()

# RULES
# any that have been commented out have been already run and are unnecessary now

## fix genitive objects of compound:lvc constructions
# d.add_transformation("func=/compound:lvc/;func=/nmod/;func=/.*/\t#1>#2;#3>#1\t#3>#2;#2:func=obj")

## fix passives
# d.add_transformation("func=/aux:pass/;func=/nsubj:pass/;func=/.*/\t#3>#1;#3>#2\t#2:func=obl:agent")
# d.add_transformation("func=/nsubj:pass/\tnone\t#1:func=obl:agent")
# d.add_transformation("func=/aux:pass/;func=/obj/;func=/.*/\t#3>#1;#3>#2\t#2:func=nsubj:pass")

result = d.run_depedit(infile)
result = unicodedata.normalize('NFD', result)
result = unicodedata.normalize('NFC', result)
result = result.replace('ਸ਼', 'ਸ਼')
result = result.replace('ਜ਼', 'ਜ਼')

con = conllu.parse(result)
for i in tqdm(range(len(con))):
    for j in range(len(con[i])):
        f = feats(con[i][j]['xpos'])
        if f:
            f = dict(sorted(f.items(), key=lambda x: x[0]))
        con[i][j]['feats'] = f
        # if not con[i][j]['misc']:
        #     con[i][j]['misc'] = {}
        # translit = transliterate(con[i][j]['form'], sanscript.GURMUKHI, sanscript.IAST)
        # con[i][j]['misc']['Translit'] = translit

result = ''.join([x.serialize() for x in con])
result = result.replace('ਫ਼', 'ਫ਼')


with open('pa_puntb-ud-test.conllu', 'w') as fout:
    fout.write(result)

infile.close()