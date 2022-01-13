from depedit import DepEdit
import unicodedata
 
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
with open('pa_puntb-ud-test.conllu', 'w') as fout:
    fout.write(unicodedata.normalize('NFD', result))