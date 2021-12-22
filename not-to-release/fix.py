from depedit import DepEdit
 
infile = open("../pa_puntb-ud-test.conllu")
d = DepEdit()
d.add_transformation("func=/compound:lvc/;func=/nmod/;func=/.*/\t#1>#2;#3>#1\t#3>#2;#2:func=obj")
result = d.run_depedit(infile)
with open('pa_puntb-ud-test.conllu', 'w') as fout:
    fout.write(result)