import shapefile
import re

sf = shapefile.Reader("gtm_adm_ocha_conred_2019_shp/gtm_adm_ocha_conred_2019_SHP/gtm_admbnda_adm2_ocha_conred_20190207.shp")
w = shapefile.Writer('shapefile_modified')
stats = open("asesinados_en_municipio.csv",'r',encoding = "UTF-8")

w.field('Municipality', 'C')
w.field('Asesinados', 'N')
#w.fields = sf.fields[1:] # skip first deletion field

stat_array = []
stats.readline()
for line in stats:
    #print(line.replace("\"",""))
    ls = line.replace("\"","").strip().split(",")
    stat_array.append(ls)

print(stat_array)


##print(sf.shapeType)
##
##shapes = sf.shapes()
##
##print(len(shapes))
##
##records = sf.records()
##
##
##sf.field()
##fields = sf.fields
##for x in fields:
##    print(x)
##
##for y in records:
##    print(y[2])

num_found = 0
is_found = 0
for shaperec in sf.iterShapeRecords():
    is_found = 0
    munic = shaperec.record[2]
    for x in stat_array:
        if x[0] == munic:
            #print("match found")
            w.record(Municipality=munic,Asesinados=x[1])
            is_found = 1
            num_found = num_found + 1
            break
##        else:
##            w.record(Municipality=munic,Asesinados=0)
    if is_found == 0:
        w.record(Municipality=munic,Asesinados=null)
        print(munic)
    else:
        print("FOUND",munic)
    w.shape(shaperec.shape)

##is_found = 0  
##for x in stat_array:
##    is_found = 0
##    for shaperec in sf.iterShapeRecords():
##        munic = shaperec.record[2]
##        if x[0] == munic:
##            print(x[0], munic, x[1])
##            w.record(Municipality=munic,Asesinados=x[1]) 
##            is_found = 1
##            break
##        else:
##            w.record(Municipality=munic,Asesinados=0)
##            #print("NOT FOUND",x[0], munic, x[1])
##    if is_found == 1:
           
    
print("num_found: ",num_found)
stats.close()
w.close()









