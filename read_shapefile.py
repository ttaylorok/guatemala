import shapefile

sf = shapefile.Reader("gtm_adm_ocha_conred_2019_shp/gtm_adm_ocha_conred_2019_SHP/gtm_admbnda_adm2_ocha_conred_20190207.shp")

print(sf.shapeType)

shapes = sf.shapes()

print(len(shapes))

records = sf.records()

fields = sf.fields
for x in fields:
    print(x)

for y in records:
    print(y[2])








