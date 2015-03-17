#!/usr/bin/env python

class Circuit():	
	def __init__(self, data):
		#print(data)
		name = data[0]
		stats_list = data[1:]
		stats_dict = {}
		# Convert stats raw list to dictionary
		for stat in stats_list:
			k,v = stat.split(":")
			stats_dict[k] = int(v)

		print(name)
		print(stats_dict)


class Juggler():
	def __init__(self, data):
		#print(data)
		name = data[0]
		stats_list = data[1:4]
		circuits_wanted = data[4:]
		stats_dict = {}
		# Convert stats raw list to dictionary
		for stat in stats_list:
			k,v = stat.split(":")
			stats_dict[k] = int(v)

		print(name)
		print(stats_dict)
		print(circuits_wanted)

def file_to_list(file_name):
	juggfest_data = open(file_name, "r")

	line = juggfest_data.readline()
	jugglers = []
	circuits = []
	
	while line:
		info = line.split()
		#print(info)
		if len(info) > 0:	
			#print(info[0])

			if info[0] == "C":
				#print(info[1:])

				temp = Circuit(info[1:])
				circuits.append(temp)

			if info[0] == "J":
				#print(info[1:])

				temp = Juggler(info[1:])
				jugglers.append(temp)


		"""
		if info[0] == "C":
			Temp = Circuit()
			circuits.append(Tem

		if info[0] == "J":
			tempo = Juggler()
			circuits.append(Temp)
		"""
		#print(circuits)
		#print(jugglers)


		line = juggfest_data.readline()

	return 0

file_to_list("JUGGLE_TEST.txt")