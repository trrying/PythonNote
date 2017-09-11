import time

# python 3.x 开始 print() 是一个方法， 2.x之前 print ""  直接输入
print("Hello word!")


# python可以直接复制，不用指定数据类型
counter = 100
miles = 1000.0
name = "John"

print(counter)
print(miles)
print(name)

# 字符串可以用类似数组的形式来时直接输出里面的元素，下标从0开始，
# 也可以用 name[1:3] 来截取 第二个到第三个来形成新的字符串
print(name[1:3])

# 也可以用 name[1:] 来截取从下标为一的元素直到最后一个元素的字符串
print(name[1:])


# List
# python 可以直接定义不同数据类型的列表
user = {'Trry', 123, 3.14, 'ocean'}
# python 可以使用print() 直接输出列表的内容，但是不是按照顺序的
print(user)
# 使用 user[0] 可以使用下标来获取对应的元素
# print(user[0])

list = ['abc', 789, 2.34, 'round']
tinyList = [123, 'run']

print(list[0])
print(list[-3:-1])

print(list + tinyList)
print(list * 2)

# 循环list
print("循环")
for str in list:
    print(str)


student = {'tom', 'jim', 'mary', 'jack', 'tom'}
print(student)
print('tom' in student)

a = set('abcdefocean')
b = {'bdfopq'}
print(a-b)  #差集
print(a|b)  #并集
print(a&b)  #交集
print(a^b)  #a和b中不同时存在的元素

dict = {}
dict['one'] = "1-第一题"
dict[2] = "第二题"
print(dict)
tinyDict = {'name':'rouoob', "tian":456}
print("tinyDict : ")
print(tinyDict)


result = "\u667a\u80fd\u6392\u5e8f"
print(result.encode())

intString = "123"
print(int(intString))


print(int(time.time()))








