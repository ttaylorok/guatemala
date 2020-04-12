import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)


stats = open("all_crimes_by_municipio_v2.csv",'r',encoding = "UTF-8")

dem = pd.read_csv('demographic_data.csv')
dem['munic_name_c'] = dem['munic_name_x']


df = pd.read_csv(stats)
df2 = df.pivot(index='munic_code', columns='crime_desc', values='count')
df3 = pd.merge(df2,dem,on='munic_code',how='left')
df3.to_csv('merged_data_GTM.csv')

##for a,b in enumerate(df3.columns):
##    print(a, b)

df4 = df3.iloc[:,0:340]
df4.rename(columns={"Robo de equipo terminal movil": "Robo celular"}, inplace=True)

df3['pop_density'] = df3['pop'] / df3['area_km']

#df[['B','C']].div(df.A, axis=0)

df3.set_index('munic_code', inplace=True)
df4.set_index('munic_code', inplace=True)

df_norm = df4.div(df3['pop'], axis=0) * 100000
df4 = df_norm

#df4.columns.values

sums = df4.sum()

filt_val = sums.sort_values(ascending=False)[11]

sums2 = sums >= filt_val

##sums.plot(kind='bar')
##plt.show()

df5 = df4.loc[:,sums2]
#df5['munic_code']=df4.index.tolist
#df5.set_index('munic_code', inplace=True)



#df6 = df5[df5['Hurto']<300]
#df7 = df6[df6['Robo celular']<200]
df7 = df5

#df7.set_index('munic_code', inplace=True)
df8 = df7.drop(columns=['Otros', 'No es delito'])

sns.set(style="ticks")

##do not delete!
g = sns.PairGrid(df8)
g.map_diag(plt.hist)
g.map_offdiag(plt.scatter, s=6)
plt.subplots_adjust(left=0.1)
plt.subplots_adjust(bottom=0.05)

fig = g.fig
fig.savefig("scatter_matrix.png") 


s8 = df8.sum(axis = 1, skipna = False)
filt = pd.isnull(s8) == False

df9 = df8.loc[filt,:]
df10 = StandardScaler().fit_transform(df9)

pca = PCA()
pca_comps = pca.fit(df10)
expl_var = pca.explained_variance_ratio_
sing_values = pca.singular_values_
print(expl_var)
print(sing_values)
print(pca_comps.components_)
v = pd.DataFrame(pca_comps.components_).transpose()
v['crime'] = df9.columns
v.set_index('crime', inplace=True)
print(v)

scores = pca.fit_transform(df10)
sc = pd.DataFrame(scores)
sc['munic_code'] = df9.index
sc.set_index('munic_code', inplace=True)

sc.to_csv("pca_output.csv")



print(pca.score(df10))

cum_var = expl_var.cumsum()
#plt.scatter(np.arange(1,len(cum_var)+1,1), cum_var)
#plt.show()
#plt.scatter(np.arange(1,len(sing_values)+1,1), sing_values)
#https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

figure, axes = plt.subplots(1, 2)

plt.subplot(121, title="Scree Plot")

ax_titles = []
for x in np.arange(1,len(sing_values)+1,1):
    ax_titles.append("PC" + str(x))

plt.plot(ax_titles,sing_values, c='red',marker='o',linestyle='--')
plt.subplot(122, title="Cumulative Variance")
cum_var2 = pd.concat([pd.Series([0]), pd.Series(cum_var)])
plt.plot([""] + ax_titles, cum_var2, c='blue',marker='o',linestyle='--')

plt.show()



stats.close()

