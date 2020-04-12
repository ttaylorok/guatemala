import shapefile
import re
import pandas as pd 
##
sf = shapefile.Reader("gtm_adm_ocha_conred_2019_shp/gtm_adm_ocha_conred_2019_SHP/gtm_admbnda_adm2_ocha_conred_20190207.shp")
w = shapefile.Writer('shapefile_modified_all_crime')
#stats = open("all_crimes_by_municipio.csv",'r',encoding = "UTF-8")
stats = open("all_crimes_by_municipio_v2.csv",'r',encoding = "UTF-8")

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

df3.to_csv('merged_data_GTM.csv')


#df3.set_index('munic_name_c', inplace=True)

##temp = df3.loc['El Adelanto',:].iloc[0,:]
##df3.drop(index='El Adelanto', inplace=True)
##df3.drop(index='La Democracia', inplace=True)
##df3.drop(index='La Libertad', inplace=True)
##df3.drop(index='Pasaco', inplace=True)
##df3.drop(index='San Lorenzo', inplace=True)
##df3.drop(index='San José', inplace=True)
##df3.drop(index='San Pedro Sacatepéquez', inplace=True)
##df3.drop(index='Santa Bárbara', inplace=True)

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
    munic = shaperec.record[2]
    for i in range(len(df3)) : 
    #for x in df3.index.values:
        x = df3.loc[i,'munic_name_x']
        #print(x)
        if type(x) == str:
            if(x.lower() in munic.lower()) or (munic.lower() in x.lower()):
                #print("match found")
                #print(munic)
                #print(x)
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









