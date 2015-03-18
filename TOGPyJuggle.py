#!/usr/bin/env python

class Circuit():	

	def __init__(self, data):

		self.name = data[0]
		self.stats_list = data[1:]
		self.stats_dict = {}

		# Convert stats raw list to dictionary
		for stat in self.stats_list:
			k,v = stat.split(":")
			self.stats_dict[k] = int(v)


class Juggler():

	def __init__(self, data, circuits):

		self.name = data[0]
		self.stats_list = data[1:4]
		self.circuits_wanted = data[4].split(",")
		self.perf_stats = {}

		# Convert stats raw list to dictionary
		self.stats_dict = {}		
		for stat in self.stats_list:
			k,v = stat.split(":")
			self.stats_dict[k] = int(v)

		# Populate performance values for desired circuits
		for cw_key in self.circuits_wanted:
			value = 0
			for sd_key in self.stats_dict:
				value += circuits[cw_key].stats_dict[sd_key] * self.stats_dict[sd_key]

			self.perf_stats[cw_key] = value

		print(self.perf_stats)

	def performance(self, circuits):

		for cw_key in self.circuits_wanted:
			value = 0

			for sd_key in self.stats_dict:
				value += circuits[cw_key].stats_dict[sd_key] * self.stats_dict[sd_key]

			self.perf_stats[cw_key] = value

		print(self.perf_stats)


def file_to_list(file_name):

	juggfest_data = open(file_name, "r")
	line = juggfest_data.readline()
	
	global Circuits
	global Jugglers
	
	while line:
		info = line.split()
		if len(info) > 0:	

			if info[0] == "C":
				temp = Circuit(info[1:])
				Circuits[temp.name] = temp

			elif info[0] == "J":
				temp = Juggler(info[1:], Circuits)
				Jugglers[temp.name] = temp

		line = juggfest_data.readline()


Circuits = {}
Jugglers = {}

file_to_list("JUGGLE_TEST.txt")

