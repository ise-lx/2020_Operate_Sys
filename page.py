# class Page():
#     def __init__(self,p1,p2):
#         self.p1 = p1
#         self.p2 = p2
#
# P1 = Page(2,2)
# l = []
# l.append(P1)
# pp1 = l[0]
# P2 = Page(3,3)
# print("before:")
# print(P2.p1)
# print("after:")
# P2 = P1
# print(P2.p1)
#

def findindex(list,value):
    for i in range(len(list)):
        temp = list[i]
        if temp == value:
            return i,True
    return -1,True
ls = [1,2,4,6,1,2]


index = findindex(ls,0)
index1,flag1 = findindex(ls,50)
print(index)


