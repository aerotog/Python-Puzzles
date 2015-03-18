#!/usr/bin/env python

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
		self.assignment = "unassigned"
		
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

	def get_perf(self, circ_name):
		return self.perf_stats[circ_name]

def file_to_list(file_name):

	juggfest_data = open(file_name, "r")
	line = juggfest_data.readline()
	info = line.split()

	global Circuits
	global Jugglers
	global choice_prefs

	choice_prefs = len(info[4])
		
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
	#correct_output = {C2: ["J6", "J3", "J10", "J0"], C1: ["J9", "J8", "J7", "J1"], C0: ["J5", "J11", "J2", "J4"]}
	print("CORRECT")
	print("C2: J6, J3, J10, J0")
	print("C1: J9, J8, J7, J1")
	print("C0: J5, J11, J2, J4")
	print("MINE")
	for circ_key in Circuits:
		output = []		
		for key in Circuits[circ_key].performances:
			output.append(key)
		print(circ_key,output)


Circuits = {}
Jugglers = {}
choice_prefs = 0

file_to_list("JUGGLE_TEST.txt")
#print(Jugglers["J0"].get_perf("C0"))
jugg_per_circ = len(Jugglers) / len(Circuits)

def schedule_perf(juggler, circuit, choice):

	if juggler.assignment == "unassigned":
		if len(circuit.performances) < jugg_per_circ:
			print("Filling ", circuit.name, " with ",juggler.name)
			circuit.performances[juggler.name] = juggler.perf_stats[circuit.name]
			juggler.assignment = choice

			return True
		
		elif any(juggler.perf_stats[circuit.name] > circuit.performances[key] for key in circuit.performances):
			print(juggler.name, " is unassigned and bigger")
			circuit.performances[juggler.name] = juggler.perf_stats[circuit.name]
			juggler.assignment = choice

			smaller_keys = []
			for key in circuit.performances:
				if circuit.performances[key] < circuit.performances[juggler.name]:
					smaller_keys.append(key)

			print(juggler.name," is better at ", circuit.name, " than ", smaller_keys)

			for key in smaller_keys:
				circuit.performances.pop(key)
				Jugglers[key].assignment = "unassigned"

			return True
	
	elif choice < juggler.assignment:
		if any(juggler.perf_stats[circuit.name] > circuit.performances[key] for key in circuit.performances):
			print("ERROR: Found choice circuit I'm better at")
			
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

			print(juggler.name," is better at ", circuit.name, " than ", smaller_keys)

			for key in smaller_keys:
				circuit.performances.pop(key)
				Jugglers[key].assignment = "unassigned"

			return True
	# elif choice >= juggler.assignment:
	# 	print("Happy with my assignment")
	# 	return False
	else:
		print("Everything checks out")
		return False



			

	# else:
	# 	if choice > juggler.assigned:
	# 		if any(juggler.perf_stats[circuit.name] > circuit.performances(key) for key in circuit.performances):
	# 			circuit.performances[juggler.name] = juggler.perf_stats[circuit.name]
	# 			juggler.assigned = choice

	# 			min_key = min(circuit.performances, key=circuit.performances.get)
	# 			circuit.performances.pop[min_key]
	# 			return

i = 0
changed_schedule = True
#while any(len(Circuits[key].performances) < jugg_per_circ for key in Circuits):
while changed_schedule:
	changed_schedule = False
	i += 1
	print("i is ",i)
	#[print(len(Circuits[key].performances)) for key in Circuits]
	if i > 100:
		print("TOO MANY!")
		break

	for choice in (range(choice_prefs-1)):
		print(choice)
		for key in Jugglers:
			juggler = Jugglers[key]
			circuit = Circuits[Jugglers[key].circuits_wanted[choice]]
			if schedule_perf(juggler, circuit, choice):
				changed_schedule = True

	print_schedule()







	

