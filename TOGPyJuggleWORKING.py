#!/usr/bin/env python
from multiprocessing import Pool


class Circuit():	

	def __init__(self, data):

		self.name = data[0]
		self.stats_list = data[1:]
		self.stats_dict = {}
		self.performances = {}
		
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
		self.assignment = -1
		
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


def file_to_list(file_name):

	juggfest_data = open(file_name, "r")
	line = juggfest_data.readline()
	info = line.split()

	global Circuits
	global Jugglers
	global choice_prefs

	# Create new objects for all Circuits and Jugglers
	# Put objects in dictionaries with names as keys
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


def print_schedule():
	file_out = open("output.txt", "w")
	if len(Circuits) < 5:		
		print("CORRECT")
		print("C2: J6, J3, J10, J0")
		print("C1: J9, J8, J7, J1")
		print("C0: J5, J11, J2, J4")
		print("MINE")
		for circ_key in Circuits:
			output = []		
			for key in Circuits[circ_key].performances:
				output.append(key)
			to_write = circ_key,output
			print(to_write)
			file_out.write(str(to_write))
			file_out.write("\n")
	else:
		output = []		
		for key in Circuits["C1970"].performances:
			output.append(key)
		to_write = ("C1970",output)
		print(to_write)
		file_out.write(str(to_write))
		file_out.write("\n")


def build_schedule(juggler, circuit, choice):

	if juggler.assignment < 0:
		if len(circuit.performances) < jugg_per_circ:
			# print("Filling ", circuit.name, " with ",juggler.name)
			circuit.performances[juggler.name] = juggler.perf_stats[circuit.name]
			juggler.assignment = choice

			return True
		
		elif any(juggler.perf_stats[circuit.name] > circuit.performances[key] for key in circuit.performances):
			# print(juggler.name, " is unassigned and bigger")
			circuit.performances[juggler.name] = juggler.perf_stats[circuit.name]
			juggler.assignment = choice

			# # smaller_keys = []
			# for key in circuit.performances:
			# 	if circuit.performances[key] < circuit.performances[juggler.name]:
			# 		smaller_keys.append(key)

			# # print(juggler.name," is better at ", circuit.name, " than ", smaller_keys)

			# for key in smaller_keys:
			# 	circuit.performances.pop(key)
			# 	Jugglers[key].assignment = "unassigned"

			min_key = min(circuit.performances, key=circuit.performances.get)
			circuit.performances.pop(min_key)
			Jugglers[min_key].assignment = -1

			return True
	
	elif choice < juggler.assignment:
		if any(juggler.perf_stats[circuit.name] > circuit.performances[key] for key in circuit.performances):
			# print("ERROR: Found preferred circuit I'm better at")
			
			# Remove from already assigned circuit
			Circuits[juggler.circuits_wanted[juggler.assignment]].performances.pop(juggler.name)

			# Assign to new circuit
			circuit.performances[juggler.name] = juggler.perf_stats[circuit.name]
			juggler.assignment = choice

			# Remove all lesser performances for further consideration
			smaller_keys = []
			for key in circuit.performances:
				if circuit.performances[key] < circuit.performances[juggler.name]:
					smaller_keys.append(key)

			# print(juggler.name," is better at ", circuit.name, " than ", smaller_keys)

			for key in smaller_keys:
				circuit.performances.pop(key)
				Jugglers[key].assignment = -1

			return True
	else:
		return False

if __name__ == '__main__':
	
	Circuits = {}
	Jugglers = {}
	choice_prefs = 0

	file_to_list("JUGGLE_TEST.txt")
	# file_to_list("JUGGLE_FEST.txt")

	# Set number of picks each juggler makes and number of jugglers per circuit
	choice_prefs = len(list(Jugglers.values())[0].circuits_wanted)
	jugg_per_circ = len(Jugglers) / len(Circuits)

	i = 0
	change_count = 1

	# Runs schedule builder until schedule is finished
	while change_count != 0:
		change_count = 0

		i += 1
		print("Run",i, end=": ")

		# Break loop if stuck
		if i > 10:
			print("INF LOOP?")
			break

		# Try to build a working schedule
		for choice in (range(choice_prefs)):
			# print("Choice: ",choice + 1)
			for key in Jugglers:
				juggler = Jugglers[key]
				circuit = Circuits[Jugglers[key].circuits_wanted[choice]]
				if build_schedule(juggler, circuit, choice):
					#changed_schedule = True
					change_count += 1
		
		if change_count == 0:
			print("Schedule is finished")
		else:
			print(change_count," changes made")

	print()
	print_schedule()







	

