#!/usr/bin/env python

def file_to_list(file_name):
	tri_data = open(file_name, "r")

	line = tri_data.readline()
	triangle = []
	
	while line:
		numbers = [int(i) for i in line.split()]
		triangle.append(numbers)		
		
		line = tri_data.readline()

	return triangle

def find_max_sum(tri_list):
	for i in reversed(range(len(tri_list)-1)):
		for j in range(len(tri_list[i])):
			bigger_number = max(tri_list[i+1][j], tri_list[i+1][j+1])
			tri_list[i][j] += bigger_number

	return tri_list[0][0]


#data = file_to_list("tritest.txt")
data = file_to_list("triangle.txt")

ans = find_max_sum(data)
print(ans)