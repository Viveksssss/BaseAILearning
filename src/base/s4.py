# print(list(zip([1,3,5],[2,4,6])))

# p = zip([1,3,5],[2,4,6])

# k, l = next(p)
# print(k,l)
# for i,j in p:
#     print(i,j)



def transpose(field):
    '''矩阵转置'''
    return [list(row) for row in zip(*field)]

def invert(field):
    '''左右逆置'''
    return [row[::-1] for row in field]
field = [[1,3,5],[2,4,6],[7,8,9]]
print(transpose(field))
print(invert(field))