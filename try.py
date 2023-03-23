list=[1,2,3,4,5,6,7,8,9,1]

for i in range(0,12):
    if i not in list:
        list.append(i)

print(list)