import math, time, os, sys, random

note_format_after_x_y_and_time = _nft_ = ",1,0,0:0:0:0:"
note_format_after_x_y_and_time_with_new_combo = _nftnc_ = ",5,0,0:0:0:0:"

New_combo_or_not = [_nft_, _nftnc_, _nft_, _nft_, _nft_, _nftnc_,  _nft_, _nft_]

_t1 = "Welcome to the PhaazeOS osu!map generator. This generator can generate simple hitcircle only maps for jump training and fun."
x = input(_t1+"\nPress Enter to continue.\n")

_t2 = "Make sure you have the base map prepared.\n2 circles at the beginning to get the time distance between them and one at the very last to know where to stop.\n"
x = input(_t2)

x = input("Make also sure the '.osu' file and this programm are in the same folder.\n")

x = input("Please press enter once again to start an choose a file in the folder.")

print("----------------------------------------------------------------------------")

class generator(object):
	def __init__(self):
		self.ingnore_files = []

		self.new_combo_d = 0
		self.min_distance = 0
		self.max_distance = 800
		self.min_x = 0
		self.min_y = 0
		self.max_x = 512
		self.max_y = 384

	def change_settings(self):
		while True: #min x
			check = input("\nChange the minimum x (left) window distance?  [0-512]  Just press enter to keep it 0\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) < self.max_x:
						print(check + " is to big or small, it has to be in range 0-" + str(self.max_x))
					else:
						self.min_x = int(check)
						print("Minimum X set to: " + check)
						break

				else:
					print("You can only enter a digital number.")

		while True: #max x
			check = input("\nChange the maximum x (right) window distance?  [0-512]  Just press enter to keep it 512\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) < self.max_x:
						print(check + " is to big or small, it has to be in range 0-" + str(self.max_x))
					else:
						self.max_x = int(check)
						print("Maximum X set to: " + check)
						break

				else:
					print("You can only enter a digital number.")

		if self.min_x > self.max_x:
			print("\n\nWait... it seems your Min X is bigger than your Max X... thats not possible to map")
			self.exit_programm()

		while True: #min y
			check = input("\nChange the minimum y (top) window distance?  [0-384]  Just press enter to keep it 0\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) < self.max_y:
						print(check + " is to big or small, it has to be in range 0-" + str(self.max_y))
					else:
						self.min_y = int(check)
						print("Minimum Y set to: " + check)
						break

				else:
					print("You can only enter a digital number.")

		while True: # max y
			check = input("\nChange the maximum y (buttom) window distance?  [0-384]  Just press enter to keep it 384\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) < self.max_y:
						print(check + " is to big or small, it has to be in range 0-" + str(self.max_y))
					else:
						self.max_y = int(check)
						print("Maximum Y set to: " + check)
						break

				else:
					print("You can only enter a digital number.")

		if self.min_y > self.max_y:
			print("\n\nWait... it seems your Min Y is bigger than your Max Y... thats not possible to map")
			self.exit_programm()

		while True: # min distance
			check = input("\nChange the minimum distance between 2 circles?   Just press enter to keep it 0.\n(e.g. a cummon 1/4 Stream is like 30 and normal Monstrata jumps around 100)\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) <= 600:
						print(check + " is to big or small, it has to be in range 0-600")
					else:
						self.min_distance = int(check)
						print("Min Distance set to: " + check)
						break

				else:
					print("You can only enter a digital number.")

		while True: # max distance
			check = input("\nChange the maximum distance between 2 circles?   Just press enter to keep it unlimited.\n(e.g. a cummon 1/4 Stream is like 30 and normal Monstrata jumps around 100)\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) <= 600:
						print(check + " is to big or small, it has to be in range 1-600")
					else:
						self.max_distance = int(check)
						print("Max Distance set to: " + check)
						break

				else:
					print("You can only enter a digital number.")

		if self.min_distance > self.max_distance:
			print("\n\nWait... it seems your Min distance is bigger than your Max distance... thats not possible to map")
			self.exit_programm()

		while True: #new combo distance
			check = input("\nChange the distance between new combos?   Just press enter to keep it random.\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check):
						print(check + " is to small, it has to be at least 1")
					else:
						self.new_combo_d = int(check)
						print("New Combo interval set to: " + check)
						break

				else:
					print("You can only enter a digital number.")

	def get_a_file(self):
		o_file = None
		for file_ in os.listdir():
			if str(file_).endswith(".osu") and not file_ in self.ingnore_files:
				return file_

		if o_file == None:
			print("No \".osu\" file found. Please place the Programm in a osu folder (Best: In a extra folder with only 1 \".osu\" file)")
			return self.exit_programm()

	def get_time_from_delay(self, delay_time_):
		s, ms = divmod(delay_time_, 1000)
		m, s = divmod(s, 60)
		return "{m}:{s}:{ms}".format(m=str(m), s=str(s), ms=str(ms))

	def need_new_combo(self):
		if self.new_combo_d == 0:
			return random.choice(New_combo_or_not)
		else:
			_g_, _e_ = divmod(self.hit_ammount, self.new_combo_d)
			if _e_ == 0:
				return note_format_after_x_y_and_time_with_new_combo
			else:
				return note_format_after_x_y_and_time

	def calc_objects(self):
		l = int(self.last_hit_object.time) - int(self.first_hit_object.time)
		return str(round(l / self.delay_time))

	def get_bpm_from_delay(self):
		return str(60000 / self.delay_time)

	def get_distanse(self, _last_x_, _last_y_, _new_x_, _new_y_):
		comp_x = [int(_last_x_), int(_new_x_)]
		comp_y = [int(_last_y_), int(_new_y_)]

		calc_smaller_x = min(comp_x)
		calc_bigger_x = max(comp_x)

		calc_smaller_y = min(comp_y)
		calc_bigger_y = max(comp_y)

		distance_x = calc_bigger_x - calc_smaller_x
		distance_y = calc_bigger_y - calc_smaller_y

		#one of the distances is 0
		if distance_x == 0: return distance_y
		if distance_y == 0: return distance_x

		#calculating distance with the sentance of Monstrat.... ee i mean Pythagoras
		c = math.sqrt(distance_x**2 + distance_y**2)
		return c

	def make_me_a_new_map(self):
		while True:
			#get a ".osu" file
			file_ = self.get_a_file()

			sure = input("\nUsing: " + file_ + " ?\n\nEnter: \"Y\" to start or press enter to switch throw all .osu files in the folder\n>>> ")
			if not "y" == sure.lower():
				self.ingnore_files.append(file_)
				continue

			break
		print("\nContinue using: " + file_)
		print("----------------------------------------------------------------------------")

		#ask if settings should be changed
		self.change_settings()

		#open file
		map_file = open(file_, "r", encoding="UTF-8").read()
		try:
			splited_map = map_file.split("[HitObjects]\n")

			rest_map = splited_map[0]
			hit_objects = splited_map[1]
		except:
			print("Your map could not be parsed successfull. :c")
			return self.exit_programm()

		class single_hit_onject(object):
			def __init__(self, objec):
				parses = objec.split(",")
				self.x = parses[0]
				self.y = parses[1]
				self.time = parses[2]

		list_of_all_objects = [single_hit_onject(h) for h in hit_objects.splitlines()]

		if len(list_of_all_objects) != 3:
			print("\nERROR: Only 2 objects and 1 Endpoint is allowed")
			return self.exit_programm()

		self.first_hit_object = list_of_all_objects[0]
		self.last_hit_object = list_of_all_objects[-1]

		self.delay_time = int(list_of_all_objects[1].time) - int(list_of_all_objects[0].time)

		confirm_text = 	"\n\nYour map starts at: {start} and ends at: {end} - Length: {length}m ({obj} Objects).\n"\
						"The delay between 2 circles whould be: {delay}ms ~ {bpm} BPM.\n"\
						"Wanna create it now?  Y/N\n>>> ". format	(
																		start = self.get_time_from_delay(int(self.first_hit_object.time)),
																		end = self.get_time_from_delay(int(self.last_hit_object.time)),
																		length = self.get_time_from_delay(int(self.last_hit_object.time) - int(self.first_hit_object.time)),
																		delay = str(self.delay_time),
																		bpm = self.get_bpm_from_delay(),
																		obj = self.calc_objects()
																	)

		while True:
			sure = input(confirm_text)

			if "y" == sure.lower():
				break

			elif "n" == sure.lower():
				return self.exit_programm()

			else:
				pass

		#beginn generating
		self.generated_map = ""

		self.current_note_time = int(self.first_hit_object.time)
		self.hit_ammount = 0

		self.last_x = 0
		self.last_y = 0

		class new_note(object):
			def __init__(self, info):
				self.x = random.randint(info.min_x, info.max_x)
				self.y = random.randint(info.min_y, info.max_y)
				self.time = info.current_note_time
				self.new_c = info.need_new_combo()
				self.text = "{x},{y},{time}{rest}".format	(
																x = str(self.x),
																y = str(self.y),
																time = str(self.time),
																rest = str(self.new_c)
															)

		#main generate
		print("\nYour map will now be generated, based on you settings (especially distance) that could take a while...")
		print("----------------------------------------------------------------------------")
		self.starting_time = time.time()
		while int(self.current_note_time) < int(self.last_hit_object.time) + self.delay_time:

			new_hit_object = new_note(self)

			maxdi = self.max_distance
			mindi = self.min_distance

			dis = self.get_distanse(self.last_x, self.last_y, new_hit_object.x, new_hit_object.y)
			if not mindi < dis < maxdi:
				continue

			self.last_x = new_hit_object.x
			self.last_y = new_hit_object.y
			self.generated_map = self.generated_map + new_hit_object.text + "\n"
			self.current_note_time = int(self.first_hit_object.time) + (int(self.delay_time) * int(self.hit_ammount))
			self.hit_ammount = self.hit_ammount + 1

		#finished mapping
		#replace some stuff
		_hhhh = []
		hhhh = rest_map.splitlines()
		for line_ in hhhh:
			if line_.startswith("StackLeniency"):
				line_ = "StackLeniency: 0"

			if line_.startswith("Mode"):
				line_ = "Mode: 0"

			if line_.startswith("Version"):
				line_ = "Version:Phaazerized"

			if line_.startswith("Tags"):
				line_ = "Tags:autogenerated,phaaze,cj,os.python"

			if line_.startswith("HPDrainRate"):
				line_ = "HPDrainRate:4"

			if line_.startswith("CircleSize"):
				line_ = "CircleSize:4"

			if line_.startswith("OverallDifficulty"):
				line_ = "OverallDifficulty:4"

			if line_.startswith("SliderMultiplier"):
				line_ = "SliderMultiplier:1"

			if line_.startswith("SliderTickRate"):
				line_ = "SliderTickRate:1"

			#debug
			if line_.startswith("[General]"):
				line_ = "\n[General]"

			if line_.startswith("[Editor]"):
				line_ = "\n[Editor]"

			if line_.startswith("[Metadata]"):
				line_ = "\n[Metadata]"

			if line_.startswith("[Difficulty]"):
				line_ = "\n[Difficulty]"

			if line_.startswith("[Events]"):
				line_ = "\n[Events]"

			if line_.startswith("[TimingPoints]"):
				line_ = "\n[TimingPoints]"

			if line_.startswith("[Colours]"):
				line_ = "\n[Colours]"

			_hhhh.append(line_)

		rest_map = "\n".join(x for x in _hhhh if x != "")

		finished_map = rest_map + "\n[HitObjects]\n" + self.generated_map

		fin = open(file_, "w", encoding="UTF-8")
		fin.write(finished_map)
		fin.close()
		return self.success_exit()

	def exit_programm(self):
		print("\nProgramm will exit itself in 10s")
		time.sleep(10)
		sys.exit()

	def success_exit(self):
		self.exit_time = time.time()
		process_time = round(self.exit_time - self.starting_time, 3)
		print("\n\n---FINISHED---")
		print("Process time: " + str(process_time) + "s")
		print("Thanks for using the PhaazeOS osu!map generator :3\nAnd please... enjoy game.")
		print(	" _____  _                          ____   _____\n"\
				"|  __ \| |                        / __ \ / ____|\n"\
				"| |__) | |__   __ _  __ _ _______| |  | | (___\n"\
				"|  ___/| '_ \ / _` |/ _` |_  / _ \ |  | |\___ \\\n"\
				"| |    | | | | (_| | (_| |/ /  __/ |__| |____) |\n"\
				"|_|    |_| |_|\__,_|\__,_/___\___|\____/|_____/")
		print("----------------------------------------------------------------------------")
		time.sleep(5)
		sys.exit()

generator().make_me_a_new_map()

#The_CJ 2017
