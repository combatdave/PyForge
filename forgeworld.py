class World:
	Dawn = "Dawn"
	Day = "Day"
	Dusk = "Dusk"
	Night = "Night"

	TimeLoop = [Dawn, Day, Dusk, Night]

	def __init__(self):
		self.time = 1

	def GetTime(self):
		return World.TimeLoop[self.time % len(World.TimeLoop)]

	def IncreaseTime(self):
		self.time += 1