import pandas as pd
import matplotlib.pyplot as plt

#PCP21 = open("municpio_edu_no_attend_PCP21.csv",'r',encoding = "UTF-8")

#for line in PCP21:
#    print(line)

#PCP21.close()

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

PCP21 = pd.read_csv("municpio_edu_no_attend_PCP21_with_dept.csv")

#print(PCP21)

print(PCP21.head())

#print(PCP21.tail(20))

#PCP21.info()

#print(PCP21.describe())

#print(PCP21.definition.1.unique())

##PCP21.rename(columns={'question':'MUNICIPIO_NAME',
##                          'definition':'MUNICIPIO_code',
##                          'code.1':'CENSUS_CODE'}, 
##                 inplace=True)

PCP21.drop(columns=['question','code_1', 'code','question.1','question_1','code.1'], inplace=True)
PCP21.rename(columns={'definition':'PCP21_desc', 'definition.1':'DEPT_value','defs_1':'MUNIC_VALUE'}, inplace=True)

print(PCP21.head(1000))

filt = PCP21.PCP21_desc != "No declarado"

PCP21 = PCP21[filt]

group1 = PCP21.groupby('PCP21_desc').agg({'count': ['sum']})#.sort_values(columns={['count, sum']})
group1.info()
#group.rename(columns={'(count, sum)':'TIM'}, inplace=True)
group1.columns = ['Totals']
group1.sort_values('Totals', ascending=False, inplace=True)

#print(PCP21.head())
print(group1.head(100))

from textwrap import wrap
labels=group1.index
labels = [ '\n'.join(wrap(l, 20)) for l in labels ]

print(labels)



fig = plt.figure()
ax=fig.add_subplot(111)
plt.bar(group1.index,group1['Totals'])
#group1.plot(kind='bar')
plt.setp(ax.set_xticklabels(labels))
plt.xticks(rotation='vertical')

group2 = PCP21.groupby(['DEPT_value','PCP21_desc']).agg({'count': ['sum']})
print(group2.head(10))

group2.unstack().plot(kind='bar', stacked=True)

group2u = group2.unstack()
print(group2u.head(5))
group2u.info()

sums = group2u.sum(axis=1)
#print(sums.head())
max_sum = sums.max()
#print(sums)
#sums.info()
facts = sums.div(max_sum)

g2ur = group2u.reindex(group2u.mean().sort_values(ascending=False).index, axis=1)
g2us = g2ur.divide(max_sum).divide(facts, axis='rows')
g2us.columns = g2us.columns.droplevel()
g2us.columns = g2us.columns.droplevel()
g2us.plot(kind='bar', stacked=True)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))



#group2.plot.bar(stacked=True)


plt.show()
#group.plot.bar(x='PCP21_desc', y='count sum', rot=0)




