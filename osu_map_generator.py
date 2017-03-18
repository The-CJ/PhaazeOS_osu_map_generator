from tkinter import filedialog
import math, time, os, sys, random, threading
import tkinter as tk

note_format_after_x_y_and_time = _nft_ = ",1,0,0:0:0:0:"
note_format_after_x_y_and_time_with_new_combo = _nftnc_ = ",5,0,0:0:0:0:"

New_combo_or_not = [_nft_, _nftnc_, _nft_, _nft_, _nft_, _nftnc_,  _nft_, _nft_]

_t1 = "Welcome to the PhaazeOS osu!map generator. This generator can generate simple hitcircle only maps for jump training and fun."
x = input(_t1+"\nPress Enter to continue.\n")

_t2 = "Make sure you have the base map prepared.\nAt LEAST 2 circles at the beginning to get the time distance between them\nand one at the very last to know where to stop.\nMake sure the distance between the notes is the same and remove breaks.\n"
x = input(_t2)

x = input("WARNING: This program will not take BPM changes or any timing points in calculations\nMAKE SURE: YOU PLACED THE NOTES ON FULL BEATS (WHITE TIMING POINTS)\n\nPlease press enter once again to start and choose a file.")

print("----------------------------------------------------------------------------")

def is_out_of_calc_time(info):
	time.sleep(180)
	if info.successfull_generated == True: return
	else:
		print("It seems like the generator is taking to long... thats most liky because you made stupid settings")
		print("The Programm will exit itself now, please try again with better settings.")
		time.sleep(3)
		info.error = True
		sys.exit()

class generator(object):
	def __init__(self):
		self.ingnore_files = []
		self.alternate_beat_option = [1,1,1, 2,2,2,2,2,2,2,2,2,2, 4,4,4,4]
		self.hit_ammount = 0
		self.real_hit_ammount = 0

		self.object_or_so = []
		self.new_combo_d = 0
		self.min_distance = 0
		self.max_distance = 800
		self.min_x = 0
		self.min_y = 0
		self.max_x = 512
		self.max_y = 384

		self.only_beats = True
		self.can_have_sliders = False
		self.only_sliders = False

		self.beat_type = "1"

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
			check = input("\nChange the minimum distance between FULL 2 circles?   Just press enter to keep it 0.\n(e.g. a cummon 1/4 Stream is like 30 and normal Monstrata jumps around 100)\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) <= math.sqrt((self.max_x-self.min_x)**2 + (self.max_y-self.min_y)**2):
						print(check + " is to big or small, it has to be in range 0-" + str(round(math.sqrt((self.max_x-self.min_x)**2 + (self.max_y-self.min_y)**2))))
					else:
						self.min_distance = int(check)
						print("Min Distance set to: " + check)
						break

				else:
					print("You can only enter a digital number.")

		while True: # max distance
			check = input("\nChange the maximum distance between FULL 2 circles?   Just press enter to keep it unlimited.\n(e.g. a cummon 1/4 Stream is like 30 and normal Monstrata jumps around 100)\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) <= math.sqrt((self.max_x-self.min_x)**2 + (self.max_y-self.min_y)**2):
						print(check + " is to big or small, it has to be in range 1-" + str(round(math.sqrt((self.max_x-self.min_x)**2 + (self.max_y-self.min_y)**2))))
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

		while True: #sliders?
			check = input("\nDo you wanna have:\n\nOnly Beats : 1\nOnly Sliders : 2\nBoth : 3\n   Just press enter to keep it only Beats.\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) < 4:
						print(check + " is to smallor high, it can only be from 1-3")
					else:
						if int(check) == 1:
							self.only_beats = True
							self.can_have_sliders = False
							self.only_sliders = False
							print("Only Beats enabled")
							break

						if int(check) == 2 and "" == "P":
							self.only_beats = False
							self.can_have_sliders = False
							self.only_sliders = True
							print("Only Sliders enabled")
							break

						if int(check) == 3 and "" == "P":
							self.only_beats = False
							self.can_have_sliders = True
							self.only_sliders = False
							print("Beats and Sliders enabled")
							break

				else:
					print("You can only enter a digital number.")

		while True: #beat type?
			check = input("\nDo you wanna have:\n\nOnly Full Beats : 1\nOnly Half Beats : 2\nFull and Half : 3\n1/4 Tripple : 4\nFull and Tripple : 5\nHalf and Tripple : 6\nAll Types : 7\n\nJust press enter to keep it only Full Beats.\n>>> ")
			if check == "":
				break
			else:
				if check.isdigit():
					if not 0 < int(check) < 8:
						print(check + " is to smallor high, it can only be from 1-7")
					else:
						if int(check) == 1:
							self.beat_type = "1"
							print("Only Full Beats enabled")
							break

						if int(check) == 2:
							self.beat_type = "2"
							print("Only Half Beats enabled")
							break

						if int(check) == 3:
							self.beat_type = "12"
							print("Full and Half Beats enabled")
							break

						if int(check) == 4:
							self.beat_type = "4"
							print("Streams enabled")
							break

						if int(check) == 5:
							self.beat_type = "14"
							print("Full and Streams enabled")
							break

						if int(check) == 6:
							self.beat_type = "24"
							print("Half and Streams enabled")
							break

						if int(check) == 7:
							self.beat_type = "124"
							print("All types enabled")
							break

				else:
					print("You can only enter a digital number.")

	def get_a_file(self):
		o_file = None
		root = tk.Tk()
		root.withdraw()
		while True:
			o_file = filedialog.askopenfilename()

			if o_file == "" or o_file == " ":
				return ""

			if not o_file.endswith(".osu"):
				print("Thats not a '.osu' file, please select a '.osu' file")
				time.sleep(2)

			else: break

		if o_file == None:
			print("No \".osu\" file found. Please place the Programm in a osu folder (Best: In a extra folder with only 1 \".osu\" file)")
			return self.exit_programm()

		return o_file

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

	def beginn_settings(self):
		while True:
			_input = input(">>> ").lower()

			if _input == "a": #Beginner
				self.min_x = self.min_x + 50
				self.max_x = self.max_x - 50
				self.min_y = self.min_y + 50
				self.max_y = self.max_y - 50
				self.min_distance = 50
				self.max_distance = 100
				self.new_combo_d = 4
				break

			elif _input == "b": #Medium
				self.min_x = self.min_x + 20
				self.max_x = self.max_x - 20
				self.min_y = self.min_y + 20
				self.max_y = self.max_y - 20
				self.min_distance = 100
				self.max_distance = 150
				self.new_combo_d = 4
				break

			elif _input == "c": #Pro
				self.min_x = self.min_x + 5
				self.max_x = self.max_x - 5
				self.min_y = self.min_y + 5
				self.max_y = self.max_y - 5
				self.min_distance = 150
				self.max_distance = 200
				self.new_combo_d = 4
				break

			elif _input == "d": #Master
				self.min_x = self.min_x
				self.max_x = self.max_x
				self.min_y = self.min_y
				self.max_y = self.max_y
				self.min_distance = 250
				self.max_distance = self.max_distance
				self.new_combo_d = 4
				break

			elif _input == "e": #S: 2 beats
				self.min_x = self.min_x
				self.max_x = self.max_x
				self.min_y = self.min_y
				self.max_y = self.max_y
				self.min_distance = 175
				self.max_distance = 180
				self.new_combo_d = 4

				self.beat_type = "12"
				self.only_beats = True
				self.can_have_sliders = False
				self.only_sliders = False
				break

			elif _input == "f": #random
				self.min_x = self.min_x
				self.max_x = self.max_x
				self.min_y = self.min_y
				self.max_y = self.max_y
				self.min_distance = self.min_distance
				self.max_distance = self.max_distance
				self.new_combo_d = 0
				self.beat_type = "124"
				self.can_have_sliders = True
				self.only_beats = False
				self.only_sliders = False
				break
				#

			elif _input == "1": #Strange streams
				self.min_x = self.min_x
				self.max_x = self.max_x
				self.min_y = self.min_y
				self.max_y = self.max_y
				self.min_distance = 20
				self.max_distance = 21
				self.new_combo_d = 8
				self.beat_type = "4"
				break

			elif _input == "2": #Only left window site
				self.min_x = self.min_x
				self.max_x = int(self.max_x / 2)
				self.min_y = self.min_y
				self.max_y = self.max_y
				self.min_distance = self.min_distance
				self.max_distance = self.max_distance
				self.new_combo_d = 4
				break

			elif _input == "3": #Only right window site
				self.min_x = int(self.max_x / 2)
				self.max_x = self.max_x
				self.min_y = self.min_y
				self.max_y = self.max_y
				self.min_distance = self.min_distance
				self.max_distance = self.max_distance
				self.new_combo_d = 4
				break

			elif _input == "4": #Small middle window
				self.min_x = int((self.max_x / 3))
				self.max_x = int((self.max_x / 3) * 2)
				self.min_y = int((self.max_y / 3))
				self.max_y = int((self.max_y / 3) * 2)
				self.min_distance = self.min_distance
				self.max_distance = self.max_distance
				self.new_combo_d = 4
				break

			elif _input == "5": #All in one line
				self.min_x = self.min_x
				self.max_x = self.max_x
				self.min_y = int((self.max_y / 2) - 1)
				self.max_y = int((self.max_y / 2) + 1)
				self.min_distance = 150
				self.max_distance = self.max_distance
				self.new_combo_d = 2
				break

			elif _input == "6": #Monstrata
				self.min_x = self.min_x
				self.max_x = self.max_x
				self.min_y = self.min_y
				self.max_y = self.max_y
				self.min_distance = 175
				self.max_distance = 176
				self.new_combo_d = 3
				break

			elif _input == "" :
				self.change_settings()
				break

			else:
				print("Option not available, try again.")

	def make_me_a_new_map(self):
		#get a ".osu" file
		file_ = self.get_a_file()

		if file_ == "" or file_ == " ":
			self.exit_programm()

		print("\nContinue using: " + file_.split("/")[-1])
		print("----------------------------------------------------------------------------")

		print("\nWanna use pre-settings? Or do you wanna set everything by yourself?\n")

		print("A - Beginner")
		print("B - Medium")
		print("C - Pro")
		print("D - Master")
		print("E - Advanced with Half Beats (long generate time)")
		print("F - |Random|")
		print("")
		print("1 - Strange streams")
		print("2 - Only left window site")
		print("3 - Only right window site")
		print("4 - Small middle window")
		print("5 - All on a line")
		print("6 - Monstra... eee.. Triangle Edition")
		print("")
		print("Just Enter = Continue Custom Settings")

		self.beginn_settings()

		#open file
		try:
			map_file = open(file_, "r", encoding="UTF-8").read()
			splited_map = map_file.split("[HitObjects]\n")

			rest_map = splited_map[0]
			hit_objects = splited_map[1]
		except:
			print("Your map could not be parsed successfull. :c")
			return self.exit_programm()

		class single_hit_Onion(object):
			def __init__(self, objec):
				parses = objec.split(",")
				self.x = parses[0]
				self.y = parses[1]
				self.time = parses[2]

		list_of_all_objects = [single_hit_Onion(h) for h in hit_objects.splitlines()]

		if len(list_of_all_objects) < 3:
			print("You need at least 3 objects, 2 at the beginning and on at the very end")
			return self.exit_programm()

		self.first_hit_object = list_of_all_objects[0]
		self.last_hit_object = list_of_all_objects[-1]

		def set_delay_time(list_):
			total_delay = 0
			ob1 = 0
			ob2 = 1
			calcavle_objects = 0

			while True:
				try:
					_O1 = list_[ob1]
					_O2 = list_[ob2]
					if int(_O2.time) - int(_O1.time) != 0:
						total_delay = total_delay + (int(_O2.time) - int(_O1.time))
						calcavle_objects = calcavle_objects + 1

					ob1 = ob1 + 1
					ob2 = ob2 + 1
				except:
					break

			delay = total_delay / calcavle_objects
			return delay

		self.delay_time = set_delay_time(list_of_all_objects[:-1])

		confirm_text = 	"\n\nYour map starts at: {start} and ends at: {end} - Length: {length}m ({obj} Objects).\n"\
						"The delay between 2 FULL BEAT circles whould be: {delay}ms ~ {bpm} BPM.\n"\
						"Wanna create it now?  Y/N\n>>> ". format	(
																		start = self.get_time_from_delay(int(self.first_hit_object.time)),
																		end = self.get_time_from_delay(int(self.last_hit_object.time)),
																		length = self.get_time_from_delay(int(self.last_hit_object.time) - int(self.first_hit_object.time)),
																		delay = str(self.delay_time),
																		bpm = self.get_bpm_from_delay(),
																		obj = self.calc_objects()
																	)

		calc_acc = "Low ( |--------- )"
		if len(list_of_all_objects[:-1]) > 5:
			calc_acc = "Medium ( |||------- )"

		if len(list_of_all_objects[:-1]) > 15:
			calc_acc = "Normal ( |||||----- )"

		if len(list_of_all_objects[:-1]) > 30:
			calc_acc = "High ( |||||||--- )"

		if len(list_of_all_objects[:-1]) > 60:
			calc_acc = "High ( |||||||||| )"

		print("\nHitpoint timing accuracy:\n\n{0} Objects found to calculate\n{1}".format(str(len(list_of_all_objects[:-1])), calc_acc))
		print("If the accuracy is very low, it could be possile that later Hitpoint are offbeat,\ntry placing more objects to get the acc. higher.")

		c = input("\nDo you wanna enter a map seed? It can be everything.  Enter = Full Random\n>>> ")
		if c != None and c != "" and c != " ":
			random.seed(a=c)


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

		#main generate
		print("\nYour map will now be generated, based on you settings (especially distance or preset) that could take a while...")
		print("----------------------------------------------------------------------------")
		time.sleep(2)
		self.starting_time = time.time()
		self.successfull_generated = False
		self.error = False
		#beat or slider
		beat_or_slider_ = [0,0, 0,0, 0,0, 0,1, 1,1] #7/10
		while int(self.current_note_time) < int(self.last_hit_object.time) and not self.error:

			n_or_s = random.choice(beat_or_slider_)

			#generate a new one
			if self.can_have_sliders:
				if n_or_s == 0:
					new_hit_object = new_note(self)
				else:
					new_hit_object = new_slider(self)

			if self.only_beats:
					new_hit_object = new_note(self)

			if self.only_sliders:
					new_hit_object = new_slider(self)

			maxdi = self.max_distance
			mindi = self.min_distance

			#check new object
			if self.only_beats or (self.can_have_sliders and n_or_s == 0):
				#calc for beats
				dis = self.get_distanse(self.last_x, self.last_y, new_hit_object.x, new_hit_object.y)
				if not mindi < dis < maxdi:
					continue

				self.last_x = new_hit_object.x
				self.last_y = new_hit_object.y

			elif self.only_sliders or (self.can_have_sliders and n_or_s == 1):
				#calc for sliders
				dis = self.get_distanse(self.last_x, self.last_y, new_hit_object.x, new_hit_object.y)
				if not mindi < dis < maxdi:
					continue

				self.last_x = new_hit_object.end_x
				self.last_y = new_hit_object.end_y

			self.current_note_time = int(self.first_hit_object.time) + round(self.hit_ammount * self.delay_time)
			self.hit_ammount = self.hit_ammount + 1
			self.real_hit_ammount = self.real_hit_ammount + new_hit_object.note_type_ammount
			self.object_or_so.append(new_hit_object.text)

			g = (100 * int(self.current_note_time)) / int(self.last_hit_object.time)

			print("  {0}%    ".format(str(round(g, 5))), end='\r')

		self.generated_map = "\n".join(o for o in self.object_or_so[1:])

		#finished mapping
		#replace some stuff

		print("100% - Your Map is finished")
		self.successfull_generated = True
		self.exit_time = time.time()
		process_time = round(self.exit_time - self.starting_time, 3)
		print("Process time: " + str(process_time) + "s  -  {0} Objects generatred".format(str(self.real_hit_ammount)))
		print("You can now change some settings.")
		_hhhh = []
		hhhh = rest_map.splitlines()
		for line_ in hhhh:
			if line_.startswith("StackLeniency"):
				while True:
					check = input("\nChange StackLeniency?  [0-7]  Enter = No Change\n>>> ")
					if check == "":
						break
					else:
						if check.isdigit():
							if not 0 <= int(check) <= 7:
								print(check + " is to big or small, it has to be in range 0-7")
							else:
								print("StackLeniency set to: " + check)
								line_ = "StackLeniency: "+ check
								break

						else:
							print("You can only enter a digital number.")

			if line_.startswith("ApproachRate"):
				while True:
					check = input("\nChange ApproachRate?  [0-10]  Enter = No Change\n>>> ")
					if check == "":
						break
					else:
						if check.isdigit():
							if not 0 <= int(check) <= 10:
								print(check + " is to big or small, it has to be in range 0-10")
							else:
								print("ApproachRate set to: " + check)
								line_ = "ApproachRate: "+ check
								break

						else:
							print("You can only enter a digital number.")

			if line_.startswith("Mode"):
				line_ = "Mode: 0"

			if line_.startswith("Version"):
				line_ = "Version:Phaazerized"

			if line_.startswith("Tags"):
				line_ = "Tags:autogenerated,phaaze,python"

			if line_.startswith("HPDrainRate"):
				while True:
					check = input("\nChange HPDrainRate?  [0-10]  Enter = No Change\n>>> ")
					if check == "":
						break
					else:
						if check.isdigit():
							if not 0 <= int(check) <= 10:
								print(check + " is to big or small, it has to be in range 0-10")
							else:
								print("HPDrainRate set to: " + check)
								line_ = "HPDrainRate: " + check
								break

						else:
							print("You can only enter a digital number.")

			if line_.startswith("CircleSize"):
				while True:
					check = input("\nChange CircleSize?  [0-10]  Enter = No Change\n>>> ")
					if check == "":
						break
					else:
						if check.isdigit():
							if not 0 <= int(check) <= 10:
								print(check + " is to big or small, it has to be in range 0-10")
							else:
								print("CircleSize set to: " + check)
								line_ = "CircleSize: " + check
								break

						else:
							print("You can only enter a digital number.")

			if line_.startswith("OverallDifficulty"):
				while True:
					check = input("\nChange OverallDifficulty?  [0-10]  Enter = No Change\n>>> ")
					if check == "":
						break
					else:
						if check.isdigit():
							if not 0 <= int(check) <= 10:
								print(check + " is to big or small, it has to be in range 0-10")
							else:
								print("OverallDifficulty set to: " + check)
								line_ = "OverallDifficulty: " + check
								break

						else:
							print("You can only enter a digital number.")

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

			if line_.startswith("Creator"):
				line_ = "Creator:Phaaze osu!map generator"

			if line_.startswith("[Colours]"):
				line_ = "\n[Colours]"


			_hhhh.append(line_)

		rest_map = "\n".join(x for x in _hhhh if x != "")

		finished_map = rest_map + "\n\n[HitObjects]\n" + self.generated_map

		x = input("\nThats it. Press Enter to save and finish your map.")

		fin = open(file_, "w", encoding="UTF-8")
		fin.write(finished_map)
		fin.close()
		return self.success_exit()

	def exit_programm(self):
		print("\nProgramm will exit itself in 10s")
		time.sleep(10)
		sys.exit()

	def success_exit(self):
		print("\n\n---FINISHED---")
		print("Thanks for using the PhaazeOS osu!map generator :3\nAnd please... enjoy game.")
		print(	" _____  _                          ____   _____\n"\
				"|  __ \| |                        / __ \ / ____|\n"\
				"| |__) | |__   __ _  __ _ _______| |  | | (___\n"\
				"|  ___/| '_ \ / _` |/ _` |_  / _ \ |  | |\___ \\\n"\
				"| |    | | | | (_| | (_| |/ /  __/ |__| |____) |\n"\
				"|_|    |_| |_|\__,_|\__,_/___\___|\____/|_____/")
		print("\n----------------------------------------------------------------------------")
		print("| - - - - - - - - - -", end='\r'),
		time.sleep(0.5)
		print("| | - - - - - - - - -", end='\r'),
		time.sleep(0.5)
		print("| | | - - - - - - - -", end='\r'),
		time.sleep(0.5)
		print("| | | | - - - - - - -", end='\r'),
		time.sleep(0.5)
		print("| | | | | - - - - - -", end='\r'),
		time.sleep(0.5)
		print("| | | | | | - - - - -", end='\r'),
		time.sleep(0.5)
		print("| | | | | | | - - - -", end='\r'),
		time.sleep(0.5)
		print("| | | | | | | | - - -", end='\r'),
		time.sleep(0.5)
		print("| | | | | | | | | - -", end='\r'),
		time.sleep(0.5)
		print("| | | | | | | | | | -", end='\r'),
		time.sleep(0.5)
		print("| | | | | | | | | | | ", end='\r'),
		time.sleep(0.5)
		sys.exit()

class new_note(object):
	def __init__(self, info):
		self.found_nothing = True
		while self.found_nothing:
			self.found_nothing = False
			alternate = random.choice(info.alternate_beat_option)

			if info.beat_type == "1" or ("1" in info.beat_type and alternate == 1):
				self.note_type_ammount = 1
				self.x = random.randint(info.min_x, info.max_x)
				self.y = random.randint(info.min_y, info.max_y)
				self.new_c = info.need_new_combo()
				self.text = "{x},{y},{time}{rest}".format	(
																x = str(self.x),
																y = str(self.y),
																time = str(int(info.current_note_time)),
																#time = str(int(info.current_note_time + round(info.delay_time))),
																rest = str(self.new_c)
															)

			elif info.beat_type == "2" or ("2" in info.beat_type and alternate == 2):

				maxdi = info.max_distance
				mindi = info.min_distance

				self.first_x = random.randint(info.min_x, info.max_x)
				self.first_y = random.randint(info.min_y, info.max_y)

				while True:

					self.x = random.randint(info.min_x, info.max_x)
					self.y = random.randint(info.min_y, info.max_y)

					dis = info.get_distanse(self.first_x, self.first_y, self.x, self.y)

					if (mindi/2) < dis < (maxdi/2):
						break
				self.note_type_ammount = 2
				self.text = "{first_x},{first_y},{time_h}{rest}\n"\
							"{x},{y},{time}{rest_1}".format	(
															first_x = self.first_x,
															first_y = self.first_y,
															#time_h = str(int((info.current_note_time + round(info.delay_time) / 2))),
															time_h = str(int(info.current_note_time)),

															x = self.x,
															y = self.y,
															#time = str(int(info.current_note_time + round(info.delay_time))),
															time = str(int(info.current_note_time + round(info.delay_time / 2))),

															rest = info.need_new_combo(),
															rest_1 = _nft_
															)

			elif info.beat_type == "4" or ("4" in info.beat_type and alternate == 4):
				maxdi = info.max_distance
				mindi = info.min_distance

				self.note_type_ammount = 3
				self.x = random.randint(info.min_x, info.max_x)
				self.y = random.randint(info.min_y, info.max_y)
				self.text = "{first_x},{first_y},{time_4}{rest}\n"\
							"{second_x},{second_y},{time_3}{rest1}\n"\
							"{x},{y},{time}{rest3}".format	(
															first_x = self.x,
															first_y = self.y,
															time_4 = str(int(info.current_note_time)),

															second_x = self.x,
															second_y = self.y,
															time_3 = str(
																			int(
																				info.current_note_time + round((info.delay_time / 4))
																				)
																		),

															x = self.x,
															y = self.y,
															time = str(int(info.current_note_time + round(info.delay_time / 2))),

															rest = info.need_new_combo(),
															rest1 = _nft_,
															rest3 = _nft_
															)

			else:
				self.found_nothing = True

class new_slider(object):
	def __init__(self, info):
		self.x = random.randint(info.min_x, info.max_x)
		self.y = random.randint(info.min_y, info.max_y)
		self.time = info.current_note_time
		self.new_c = info.need_new_combo()
		self.text = "{x},{y},{time}{sliderpoints}{nc}{length_and_repeats}".format	(
														x = str(self.x),
														y = str(self.y),
														time = str(self.time),
														sliderpoints = "",
														nc="",
														length_and_repeats = ""
													)

generator().make_me_a_new_map()

#The_CJ 2017

# TODO: AR Komma stellen
