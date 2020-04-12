import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#PCP21 = open("municpio_edu_no_attend_PCP21.csv",'r',encoding = "UTF-8")

#for line in PCP21:
#    print(line)

#PCP21.close()

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)

########################################################
#####  LITERACY
########################################################

PCP22 = pd.read_csv("municpio_literacy_PCP22.csv")

grp = PCP22.groupby(['dept_name','munic_code','response'])
#print(grp.head())
#grp.info()
#print(grp.count())

PCP22.drop(columns=['PCP22'], inplace=True)
test = PCP22.set_index(keys=['dept_name','dept_code','munic_name','munic_code','response'])

#print(test.head())

test2 = test.unstack()

#test2.info()
#print(test2.head())


test2.columns = test2.columns.droplevel()

#print(test2.head())

test2['perc_illiterate'] = test2['No']/(test2['Sí']+test2['No'])*100

#print(test2.head(1000))

########################################################
#####  EDUCATION
########################################################

PCP17 = pd.read_csv("municpio_highest_edu_PCP17_A.csv").drop(columns=['PCP17_A'])


PCP17i = PCP17.set_index(keys=['dept_name','dept_code','munic_name','munic_code','response'])

PCP17iu = PCP17i.unstack()

#print(PCP17iu.head())

#print(PCP17i.head(100))

PCP17is = PCP17i.sum(level = 'response')
#print(PCP17is.head())

PCP17s = PCP17.groupby(['dept_name','response']).sum().drop(columns=['munic_code','dept_code'])

PCP17s2 = PCP17s.groupby('dept_name').sum()

max_val = PCP17s2.max()
facts = PCP17s2.div(max_val)

PCP17s_norm = PCP17s.divide(max_val).div(facts, axis='rows')

#print(PCP17s.head(100))

PCP17iu.columns = PCP17iu.columns.droplevel()

#PCP17iu['Doctorado'].fillnan(value=0)

PCP17_filt = PCP17iu.filter(items=['Doctorado', 'Licenciatura','Ninguno','Nivel medio (básico y diversificado)','Preprimaria','Primaria','Maestría'])
PCP17_filt.fillna(value=0, inplace=True)

totals = PCP17_filt['Doctorado'] + PCP17_filt['Licenciatura'] + PCP17_filt['Ninguno'] + PCP17_filt['Nivel medio (básico y diversificado)'] + PCP17_filt['Preprimaria'] + PCP17_filt['Primaria'] + PCP17_filt['Maestría'] 

PCP17iu['perc_doctorado'] = (PCP17_filt['Doctorado']/totals)*100
PCP17iu['perc_maestria'] = (PCP17_filt['Maestría']/totals)*100
PCP17iu['perc_licenciatura'] = (PCP17_filt['Licenciatura']/totals)*100
PCP17iu['perc_preprimaria'] = (PCP17_filt['Preprimaria']/totals)*100
PCP17iu['perc_primaria'] = (PCP17_filt['Primaria']/totals)*100
PCP17iu['perc_medio'] = (PCP17_filt['Nivel medio (básico y diversificado)']/totals)*100
PCP17iu['perc_ninguno'] = (PCP17_filt['Ninguno']/totals)*100
PCP17iu['perc_higher'] = ((PCP17_filt['Licenciatura']+PCP17_filt['Maestría']+PCP17_filt['Doctorado'])/totals)*100

#PCP17s_norm.columns = PCP17s_norm.columns.droplevel()



#PCP17s_norm_u = PCP17s_norm.stack

PCP17p = PCP17s_norm.unstack()

PCP17p.columns = PCP17p.columns.droplevel()

PCP17p.rename(columns = {"Nivel medio (básico y diversificado)" : "Nivel medio"}, inplace=True)

PCP17p = PCP17p[['Ninguno',
                 'Primaria',
                 'Nivel medio',
                 'Preprimaria',
                 'Licenciatura',
                 'Maestría',
                 'Doctorado']]


PCP17p.plot(kind='bar', stacked=True)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

plt.show()

########################################################
#####  UNEMPLOYMENT
########################################################

PCP27 = pd.read_csv("municpio_trabajo_unemployment_PCP27.csv").drop(columns=['PCP27'])
PCP27i = PCP27.set_index(keys=['dept_name','dept_code','munic_name','munic_code','response'])

PCP27i = PCP27i.unstack()
PCP27i.columns = PCP27i.columns.droplevel()

#print(test2.head())

PCP27i['perc_unemp'] = PCP27i['No']/(PCP27i['Sí']+PCP27i['No'])*100

########################################################
#####  TRABAJO
########################################################

PCP32 = pd.read_csv("municpio_trabajo_PCP32_1D.csv").drop(columns=['PCP32_1D'])

trans = PCP32.groupby(['munic_code'])['count'].transform(max)

idx = trans == PCP32['count']

PCP32r = PCP32[idx].rename(columns={'response':'top_empl'})

########################################################
#####  LANGUAGE
########################################################

# impoty data using Pandas csv reader
PCP15 = pd.read_csv("municpio_idioma_PCP15.csv").drop(columns=['PCP15'])

# apply filter to exclude Español
filt = PCP15.response != "Español"
PCP15f = PCP15[filt]

# select language per each municipality that has the highest number of speakers
trans = PCP15f.groupby(['munic_code'])['count'].transform(max)
idx = trans == PCP15f['count']

# rename "reponse" column to "top_language"
PCP15r = PCP15f[idx].rename(columns={'response' : 'top_language'})

########################################################
#####  AGE/SEX COUNTRY LEVEL
########################################################

PCP6 = pd.read_csv("county_age_sex_PCP6_PCP7.csv")
PCP6.set_index(['PCP7','PCP6'], inplace=True)
PCP6u = PCP6.unstack()
PCP6u.columns = PCP6u.columns.droplevel()
PCP6u.plot(kind='bar')

PCP6u['binned'] = pd.cut(PCP6u.index, np.arange(0, 100, 2))

PCP6b = PCP6u.groupby('binned').sum()

PCP6b['age'] = np.arange(2,100,2)

PCP6b.set_index(['age'], inplace=True)

PCP6b.columns = ['Men','Women']

PCP6b.plot(kind='bar')

#plt.show()

########################################################
#####  AGE MUNIC LEVEL
########################################################

PCP7 = pd.read_csv("municipio_age_PCP7.csv")

PCP7['above_60'] = np.where(PCP7['PCP7']>=60, 'yes', 'no')

PCP7g = PCP7.groupby(['munic_code','above_60'])['count'].sum()

PCP7gu = PCP7g.unstack()

PCP7gu['percent_abv_60'] = PCP7gu['yes']/(PCP7gu['yes']+PCP7gu['no'])*100

#PCP7.groupby()

########################################################
#####  TOTAL POPULATION
########################################################

pop = pd.read_csv("municipio_population.csv").rename(columns={'count':'pop'})

m1 = pd.merge(test2,PCP17iu,on='munic_code')
m2 = pd.merge(m1,PCP27i,on='munic_code')
m3 = pd.merge(m2,PCP32r,on='munic_code')
m4 = pd.merge(m3,PCP15r,on='munic_code')
m5 = pd.merge(m4,PCP7gu,on='munic_code')
m6 = pd.merge(m5,pop,on='munic_code')

areas = pd.read_csv("munic_area.csv")

m7 = pd.merge(m6,areas,on='munic_code',how='left')

m8 = m7.filter(['munic_code',
                'perc_illiterate',
                'perc_doctorado',
                'perc_maestria',
                'perc_licenciatura',
                'perc_preprimaria',
                'perc_primaria',
                'perc_medio',
                'perc_ninguno',
                'perc_unemp',
                'dept_code_x',
                'munic_name_x',
                'dept_name_x',
                'percent_abv_60',
                'top_language',
                'pop',
                'top_empl',
                'area_km',
                'perc_higher'])

m8['pop_dens'] = m8['pop'] / m8['area_km']

m8.to_csv('demographic_data.csv')



#m7.set_index('munic_name_x', inplace=True)
#print(m7.loc['El Adelanto',:])





#print(PCP32r.head(100))

#print(test2.head())

#grp2 = grp.unstack()
#print(grp2.head())

#group.apply(lambda row : add(row['A'],row['B'], row['C']), axis = 1) 



#print(PCP21.tail(20))

#PCP21.info()

#print(PCP21.describe())

#print(PCP21.definition.1.unique())

##PCP21.rename(columns={'question':'MUNICIPIO_NAME',
##                          'definition':'MUNICIPIO_code',
##                          'code.1':'CENSUS_CODE'}, 
##                 inplace=True)

####PCP21.drop(columns=['question','code_1', 'code','question.1','question_1','code.1'], inplace=True)
####PCP21.rename(columns={'definition':'PCP21_desc', 'definition.1':'DEPT_value','defs_1':'MUNIC_VALUE'}, inplace=True)
####
####print(PCP21.head(1000))
####
####group1 = PCP21.groupby('PCP21_desc').agg({'count': ['sum']})#.sort_values(columns={['count, sum']})
####group1.info()
#####group.rename(columns={'(count, sum)':'TIM'}, inplace=True)
####group1.columns = ['Totals']
####group1.sort_values('Totals', ascending=False, inplace=True)
####
#####print(PCP21.head())
####print(group1.head(100))
####group1.plot(kind='bar')
####
####group2 = PCP21.groupby(['DEPT_value','PCP21_desc']).agg({'count': ['sum']})
####print(group2.head(10))
####
####group2.unstack().plot(kind='bar', stacked=True)
####
####group2u = group2.unstack()
####print(group2u.head(5))
####group2u.info()
####
####sums = group2u.sum(axis=1)
#####print(sums.head())
####max_sum = sums.max()
#####print(sums)
#####sums.info()
####facts = sums.div(max_sum)
####
####g2ur = group2u.reindex(group2u.mean().sort_values().index, axis=1)
####g2us = g2ur.divide(max_sum).divide(facts, axis='rows')
####g2us.plot(kind='bar', stacked=True, legend=False)



#group2.plot.bar(stacked=True)



#group.plot.bar(x='PCP21_desc', y='count sum', rot=0)




