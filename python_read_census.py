fin = open('db_csv/PERSONA_BDP.csv','r')

n = 0
for line in fin:
    n = n + 1
    print(line)
    if n > 5:
        break

fin.close()
