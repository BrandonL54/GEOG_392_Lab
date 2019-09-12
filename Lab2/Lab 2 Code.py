#Part 1
def multiplylist(mylist):
    result = 1
    for x in mylist:
        result = result * x
    return result

part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
print(multiplylist(part1))


#Part 2
def addlist(parameter_list):
    result = 0
    for i in parameter_list:
        result = result + i
    return result

part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]
print(addlist(part2))

#Part 3
def addeven(parameter_list):
    result = 0
    for i in parameter_list:
        if i %2==0:
            result = result + i
    return result

part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21]
print(addeven(part3))

print(multiplylist(part1))