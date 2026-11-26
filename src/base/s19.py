import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='38324',
    database='py_adv_db',
    charset='utf8mb4',
    init_command="SET time_zone='+8:00'"
)

cursor = conn.cursor()


# with conn.cursor(pymysql.cursors.DictCursor) as cursor:
#     sql = "SELECT * FROM user"
#     cursor.execute(sql)
#     p = cursor.fetchall()
#     print(p[0].keys())
#     for row in p:
#         for i in row.values():
#             print(i,end='\t')

#         print()

# # # INSERT INTO user(name,age,email)
# # # VALUES (%s,%s,%s)
# # # sql = """
# # # UPDATE user set age = %s where id = %s
# # # """

# # sql = '''
# #     SELECT * FROM user
# # '''

# # sql2 = '''
# #     UPDATE user SET money = 100 where id = 4;
# #     INSERT INTO user(id,name ,age,email)
# #     VALUES(1,%s,%s,%s)
# # '''
# # cursor.execute(sql2,("aaa",22,"vqq@163.com"))
# # data = ('张三',22,'zhansgan@163.com')

# # # cursor.execute(sql,(222,4))
# # cursor.execute(sql)
# # # conn.commit()
# # print(cursor.fetchall())
# # print(cursor.rowcount)

# # cursor.close()
# # conn.close()


# try:
#     sql1 = "UPDATE user SET age = age - 100 where id = 1"
#     sql2 = "UPDATE user SET age = age + 100 where id = 4"
#     cursor.execute(sql1)
#     cursor.execute(sql2)
#     conn.commit()
#     print("转账成功")
# except Exception as e:
#     conn.rollback()
#     print(e)
# finally:
#     cursor.close()
#     conn.close()


sql = "INSERT INTO user(name,age) VALUES (%s,%s)"
data_list = [("李四", 20), ("王五", 24), ("赵六", 29)]

cursor.executemany(sql, data_list)
conn.commit()
print("批量插入行数", cursor.rowcount)
print(cursor.lastrowid)
cursor.close()
conn.close()
