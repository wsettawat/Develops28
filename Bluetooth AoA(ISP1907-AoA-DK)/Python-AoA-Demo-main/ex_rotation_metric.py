import math
import numpy as np



# Program to multiply two matrices using list comprehension

# 3x3 matrix
theta = math.pi
a=math.cos(theta*0.32)
b=math.sin(theta*0.32)
A = [[a,b],
    [-b,a]]
c=685
d=-1601
B = [[c],
     [d]]
# 3x4 matrix



# result is 3x4

result = np.dot(A,B)

print(result[0],result[1]) 
translation_x = 685
translation_y = -1601
result[0] += translation_x
result[1] += translation_y
print(result[0],result[1]) 

print(int(result[0]),int(result[1])) 
