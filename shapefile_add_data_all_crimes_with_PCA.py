import shapefile
import re
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

##
sf = shapefile.Reader("municipios_gtm/municipios_GTM.shp",encoding = "latin1")
w = shapefile.Writer('shapefile_modified_all_crime_PCA_new')
#stats = open("all_crimes_by_municipio.csv",'r',encoding = "UTF-8")
stats = open("all_crimes_by_municipio_v2.csv",'r',encoding = "UTF-8")
pca = pd.read_csv("pca_output.csv")
pca2 = pca['0'] - pca['0'].min()
pca3 = pd.DataFrame((pca2 / pca2.max())*10)
pca3.columns = ['PCA1']
pca3['munic_code'] = pca['munic_code']

dem = pd.read_csv('demographic_data.csv')

#print(dem.loc[dem['munic_name_x'] == 'El Adelanto'])

dem['munic_name_c'] = dem['munic_name_x']



##stats.readline()
##stat_array = []
##for line in stats:
##    ls = line.replace("\"","").strip().split(";")
##    stat_array.append(ls)
##    #print(ls)
##    if len(ls) != 5:
##        print(ls)

#df = pd.DataFrame(stat_array, columns = ['Munic', 'Crime', 'Code', 'Count', 'Crime_Total'])
df = pd.read_csv(stats)

#print(df)

df2 = df.pivot(index='munic_code', columns='crime_desc', values='count')

df3 = pd.merge(df2,dem,on='munic_code',how='left')

dfp = pd.merge(df3,pca3,on='munic_code',how='left')
dfp['PCA1'].fillna(value=0)

df3.to_csv('merged_data_GTM.csv')
df3.to_excel('merged_data_GTM.xlsx')

df3 = dfp

def fit_exp(x, a, b, c):
    return a * np.exp(-b * x) + c

def fit_lin(x, a, b):
    return a * x + b

def fit_pow(x, a, b):
    return a * np.power(x, b)

def fit_poly2(x, a, b, c):
    return a * np.power(x, 2) + b * x + c
 
figure, axes = plt.subplots(3, 2, figsize=(7, 8))
#plt.figure(num=None, figsize=(8, 10))

plt.subplot(321, xlabel="% Pop. >60 yrs")
plt.scatter(df3['percent_abv_60'],df3['PCA1'],s=5)
dfxx = df3.dropna(subset=['percent_abv_60','PCA1']).sort_values(by=['percent_abv_60'])
popt, pcov = curve_fit(fit_lin, dfxx['percent_abv_60'], dfxx['PCA1'])
plt.plot(dfxx['percent_abv_60'], fit_lin(dfxx['percent_abv_60'],*popt),'r-')


plt.subplot(322, xlabel="% Pop. without Eduction")
plt.scatter(df3['perc_ninguno'],df3['PCA1'],s=5)
dfxx = df3.dropna(subset=['perc_ninguno','PCA1']).sort_values(by=['perc_ninguno'])
popt, pcov = curve_fit(fit_exp, dfxx['perc_ninguno'], dfxx['PCA1'])
plt.plot(dfxx['perc_ninguno'], fit_exp(dfxx['perc_ninguno'],*popt),'r-')

plt.subplot(323, xlabel="% Pop. with Higher Education")
plt.scatter(df3['perc_higher'],df3['PCA1'],s=5)
dfxx = df3.dropna(subset=['perc_higher','PCA1']).sort_values(by=['perc_higher'])
popt, pcov = curve_fit(fit_lin, dfxx['perc_higher'], dfxx['PCA1'])
plt.plot(dfxx['perc_higher'], fit_lin(dfxx['perc_higher'],*popt),'r-')

plt.subplot(324, xlabel="% Pop. Unemployed")
plt.scatter(df3['perc_unemp'],df3['PCA1'],s=5)
dfxx = df3.dropna(subset=['perc_unemp','PCA1']).sort_values(by=['perc_unemp'])
popt, pcov = curve_fit(fit_pow, dfxx['perc_unemp'], dfxx['PCA1'])
plt.plot(dfxx['perc_unemp'], fit_pow(dfxx['perc_unemp'],*popt),'r-')

plt.subplot(325, xlabel="Population Density")
plt.scatter(df3['pop_dens'],df3['PCA1'],s=5)
dfxx = df3.dropna(subset=['pop_dens','PCA1']).sort_values(by=['pop_dens'])
popt, pcov = curve_fit(fit_lin, dfxx['pop_dens'], dfxx['PCA1'])
plt.plot(dfxx['pop_dens'], fit_lin(dfxx['pop_dens'],*popt),'r-')

plt.subplot(326, xlabel="% Pop. Illiterate")
plt.scatter(df3['perc_illiterate'],df3['PCA1'],s=5)
dfxx = df3.dropna(subset=['perc_illiterate','PCA1']).sort_values(by=['perc_illiterate'])
popt, pcov = curve_fit(fit_exp, dfxx['perc_illiterate'], dfxx['PCA1'])
plt.plot(dfxx['perc_illiterate'], fit_exp(dfxx['perc_illiterate'],*popt),'r-')

figure.suptitle("Crime Index vs. Demographic Factors", fontsize=12)
figure.tight_layout()
figure.subplots_adjust(top=0.93)
figure.savefig("correlations_new.png") 

plt.show()


#print(df3.info())      

#print(df2)

w.field('Municipality', 'C')
for col in df3.columns:
    #print(col)
    #print(df3[0,col])
    #print(type(df3[0,col]))
    if type(df3[col][0]) == str:
        w.field(col, 'C')
    elif "perc" in col:
        w.field(col, 'F', decimal=4)
    elif col == 'PCA1':
        w.field(col, 'F', decimal=4)
    else:
        w.field(col,'N')

##w.field('Municipality', 'C')
##w.field('Test', 'N')

#print(df2["Homicidio"])
#print(df2.loc[:,"Homicidio"])

fields = w.fields
##for x in fields:
##    print(x)

num_fields = len(fields)

num_found = 0
is_found = 0
for shaperec in sf.iterShapeRecords():
    is_found = 0
    munic = shaperec.record[1]
    #print(munic)
    for i in range(len(df3)) : 
    #for x in df3.index.values:
        x = df3.loc[i,'munic_code']
        #print(x)
        #if type(x) == str:
        if x == munic:        

            t = tuple([x] + df3.loc[i,:].fillna(0).to_list())
            #print(len(t))
            
            w.record(*t)
            is_found = 1
            num_found = num_found + 1
            break
    if is_found == 0:
        print("NOT FOUND", munic)
        w.record(*tuple([munic]+([0]*num_fields)))
        
    else:
        #print("FOUND",munic)
        pass
    w.shape(shaperec.shape)




#print(stat_array)

##
##w.field('Municipality', 'C')
##w.field('Asesinados', 'N')
##
##stat_array = []
##stats.readline()
##for line in stats:
##    ls = line.replace("\"","").strip().split(",")
##    stat_array.append(ls)
##
##print(stat_array)
##
##num_found = 0
##is_found = 0
##for shaperec in sf.iterShapeRecords():
##    is_found = 0
##    munic = shaperec.record[2]
##    for x in stat_array:
##        if x[0] == munic:
##            #print("match found")
##            w.record(Municipality=munic,Asesinados=x[1])
##            is_found = 1
##            num_found = num_found + 1
##            break
##    if is_found == 0:
##        w.record(Municipality=munic,Asesinados=null)
##        print(munic)
##    else:
##        print("FOUND",munic)
##    w.shape(shaperec.shape)
##
##    
##print("num_found: ",num_found)
stats.close()
w.close()









