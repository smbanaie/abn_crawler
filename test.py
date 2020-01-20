
f = open('BUSINESS_NAMES_202001.csv','r')
f2 = open('BUSINESS_NAMES_202001_ABN.csv','w')
next(f)
for line in f : 
    k = line.split('\t')[-1].strip()
    if len(k) > 0 :
        print(k)
        f2.write(f"{k}\n")
f2.close()

# s = 'BUSINESS NAMES	   Nourishing Your World	Registered	13/03/2017		13/03/2020			23850847348'
# k = s.split("\t")[-1]
# print(k)
