import datetime
list_of_platforms = []
list_of_trains = []

class schedule(object):
	def __init__(self, from_time, to_time):
		t = datetime.datetime.now().replace(microsecond=0, second=0)
		dt = datetime.timedelta(seconds=60)

		generated_schedule = { t + n*dt for n in range(from_time - 1, to_time) }

		self.slot = generated_schedule
		self.busy = set()

	def __repr__(self):
		string = ' The schedule is free in ' + str(sorted(self.slot)) + ' and occupied in ' + str(sorted(self.busy))
		return(string)

	def find_first_slot_available(self, activity_from_time, activity_to_time):
		slot_found = False
		wait_time = 0
		while slot_found == False:
			#print(self.busy) 
			activity = schedule(activity_from_time + wait_time, activity_to_time + wait_time)
			clash = self.busy.intersection(activity.slot)
			#print(clash)
			if clash:

				wait_time += 1
			else:
				slot_found = True
		return(wait_time)

	def add_activity(self, activity_from_time, activity_to_time):
		wait_time = self.find_first_slot_available(activity_from_time, activity_to_time)
		activity = schedule(activity_from_time + wait_time, activity_to_time + wait_time)
		self.busy = self.busy.union(activity.slot)
		self.slot = self.slot.difference(self.busy)
		
	def free_up_slot(self, activity_from_time, activity_to_time):
		activity = schedule(activity_from_time, activity_to_time)
		self.slot = self.slot.union(activity.slot)
		self.busy = self.busy.difference(self.busy)

class platform(object):
	def __init__(self, pf_number, pf_schedule, minimum_discharge_time = 5):
		self.number = pf_number
		self.schedule = pf_schedule
		self.minimum_discharge_time = minimum_discharge_time
		list_of_platforms.append(self)
		list_of_platforms.sort(key=lambda x: x.minimum_discharge_time)

	def __repr__(self):
		string = ' The Platform Number is ' + str(self.number) #+ ' and ' + str(self.schedule)
		return(string)

	def assign(self, from_time, to_time, tr_no=False):
		self.schedule.add_activity(from_time, to_time)

class train(object):
	def __init__(self, train_no, ETA, stoppage_time, pfs_nos_usable, precedence_rank = 0):
		self.number = train_no
		self.ETA = ETA
		self.stoppage_time = stoppage_time
		self.pfs_nos_usable = pfs_nos_usable
		self.platform_assigned = False
		self.precedence_rank = precedence_rank
		list_of_trains.append(self)
		list_of_trains.sort(key=lambda x: (x.precedence_rank, x.stoppage_time, x.ETA))

	def __repr__(self):
		string = ' The Train Number is ' + str(self.ETA) #+ ' and ' + str(self.schedule)
		return(string)

	def find_best_pf(self):
		dictionary_of_op_times = {}	

		for platform in list_of_platforms:

			from_time = self.ETA
			to_time = self.ETA + self.stoppage_time + platform.minimum_discharge_time			
			wait_time = platform.schedule.find_first_slot_available(from_time, to_time)
			
			operational_time = wait_time + to_time - from_time
			print(operational_time)
			dictionary_of_op_times[platform] = operational_time
			if wait_time == 0:
				break
		best_pf = min(dictionary_of_op_times, key=dictionary_of_op_times.get)
		wait_time = best_pf.schedule.find_first_slot_available(from_time, to_time)
			
		best_pf.assign(self.ETA + wait_time, self.ETA + self.stoppage_time + best_pf.minimum_discharge_time + wait_time)
		return best_pf.number






a = platform(1, schedule(40, 55), 4)
b = platform(2, schedule(40, 55), 2)
c = platform(3, schedule(40, 55), 8)



test_train_1 = train(11, 48, 2, 1)
test_train_2 = train(12, 43, 4, 1)
print(test_train_1.find_best_pf())
print('----')
print(test_train_2.find_best_pf())

"""
 The schedule is free in {datetime.datetime(2018, 4, 15, 11, 35), datetime.datetime(2018, 4, 15, 11, 38), datetime.datetime(2018, 4, 15, 11, 36), datetime.datetime(2018, 4, 15, 11, 37), datetime.datetime(2018, 4, 15, 11, 39)} and occupied in set()
 The schedule is free in {datetime.datetime(2018, 4, 15, 11, 35), datetime.datetime(2018, 4, 15, 11, 38), datetime.datetime(2018, 4, 15, 11, 39)} and occupied in {datetime.datetime(2018, 4, 15, 11, 36), datetime.datetime(2018, 4, 15, 11, 37)}
"""