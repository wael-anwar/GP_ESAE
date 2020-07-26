studentlist=[[1.44,2.56],[1.11,1.67]]
listnew=[]
listouter=[]
for grade in studentlist:
    listnew=[]
    for g in grade:
        listnew.append(round(g,1))
    listouter.append(listnew)
print(listouter)