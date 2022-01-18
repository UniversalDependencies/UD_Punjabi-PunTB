import conllu
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import *

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
})

pos = Counter()
tot = 0

with open('../pa_puntb-ud-test.conllu', 'r') as fin:
    for tokenlist in conllu.parse_incr(fin):
        for token in tokenlist.filter(id=lambda x: type(x) is int):
            pos[token['upos']] += 1
            tot += 1

for i, j in pos.most_common():
    print(i, pos[i], f'{(pos[i] / tot) * 100:.1f}\%', sep=' & ', end=' \\\\\n')
input()

print(pos)
df = pd.DataFrame.from_dict(pos, orient='index').reset_index()
df.columns = ['Deprel', 'count']
df = df.sort_values(by=['count'], ascending=False)
print(df)

graph = (ggplot(df, aes('Deprel', 'count'))
    + geom_bar(stat='identity')
    # + geom_text(
    # aes(label='count'),
    # stat='identity',
    # nudge_y=0.125,
    # va='bottom'
    # #  format_string='{:.1f}% '
    # )
    # + labs(title='POS tag distribution in UD Punjabi')
    + theme(legend_key_width=2, legend_key_height=10, axis_text_x=element_text(rotation=90, hjust=0.5), legend_position='none')
)
graph.save('figures/deprel.pdf', width=7, height=2)
# graph.draw()
# plt.show()