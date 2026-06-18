mp={}
mp["key"]=2
print(mp)
get=mp.get("key",1)
print(get)
for key,value in mp.items():
    print(key,value)
