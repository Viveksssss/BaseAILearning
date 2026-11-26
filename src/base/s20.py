import numpy as np

arr1 = np.array([1, 2, 3, 4], dtype=np.int64)
print(arr1)


arr2 = np.full((2, 2), fill_value=9)  # 填充指定值
print(arr2)

arr3 = np.empty((2,2))
print(arr3)

arr4 = np.eye(3)  # 单位矩阵
print(arr4)

arr5 = np.arange(0, 10, 2)  # [0,2,4,6,8]，左闭右开
print(arr5)

arr6 = np.linspace(0, 1, 5)  # 0~1均匀生成5个点
print(arr6)

np.random.seed(42)  # 设置随机种子，结果可复现
print(np.random.rand(2, 3))  # [0,1)均匀分布
print(np.random.randn(3, 3))  # 标准正态分布
print(np.random.randint(0, 10, size=(2, 2)))  # 整数随机


arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr[0])  # 第0行
print(arr[0, 1])  # 第0行第1列
print(arr[0][1])  # 等价写法

print(arr[0:2, 1:])    # 行0~1，列1到末尾
print(arr[:, 0])       # 所有行，第0列

mask = arr>5 
print(arr[mask])
print(np.where(arr>5,arr,0))
print(arr[[0,2],[1,0]])


a = np.array([1,2,3])
b = np.array([4,5,6])

# 逐个元素计算
print(f'a + b: {a + b}')
print(f'a * b: {a * b}')
print(f'a / b: {a / b}')
print(f'a // b: {a // b}')
print(f'a - b: {a - b}')
print(f'a ** 2: {a ** 2}')
print(f"a @ b: {a @ b}")
print(np.dot(a,b))
print(np.sum(a*b))

c = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(c.reshape(1,9))
print(np.array([[[1,2,3],[2,3,4]]]).flatten())
print(arr1.ravel())
print(arr1)

arr7 = np.array([[1,2,3],[4,5,6]])
print(arr7.ravel())
print(arr7)
print(arr7.T)
print(np.transpose(arr7))

print(np.concatenate((arr2, arr3),axis=1))
print(np.vstack((arr2,arr3)))
print(np.hstack((arr2,arr3)))

h = np.split(arr,3)
print(f'h: {h}')
print(f'np.std(arr):{np.std(arr)}')  # 标准差
print(f'np.var(arr):{np.var(arr)}')
print(np.mean(np.array([1,2,3])))
print(np.argmax(np.array([1,2,3])))


np.savetxt("data.txt", arr)
