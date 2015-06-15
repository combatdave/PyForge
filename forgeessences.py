class EssenceType:
	Light = "Light"
	Shade = "Shade"


class Essence:
	def __init__(self, essenceType, item):
		self.essenceType = essenceType
		self.item = item
		self.resistance = 0

		self.level = 0
		self.taint = 0


	def ResetForTurn(self):
		self.taint = 0


	def __repr__(self):
		return self.essenceType + " essence (" + str(self.level) + ") - contains " + str(self.GetEnergyContained()) + " energy"


	def EnergyRequiredToLevelUp(self):
		baseEnergyRequired = self._GetEnergyForLevel(self.level + 1)
		multiplier = 1.0 + (self.resistance / 20.0)	# 0.5 to 1.5
		return baseEnergyRequired * multiplier


	def _GetEnergyForLevel(self, level):
		return pow(2, level + 2)


	def GetEnergyContained(self):
		energy = 0
		for i in xrange(self.level, 0, -1):
			energyForLevel = self._GetEnergyForLevel(i)
			energy += energyForLevel
		return energy


	def TryToLevelUp(self):
		if self.item.energy >= self.EnergyRequiredToLevelUp():
			self.item.energy -= self.EnergyRequiredToLevelUp()
			self.level += 1
			return True
		else:
			return False


class Essence_Consumer(Essence):
	def SetConsumableEssence(self, consumable):
		self.consumable = consumable


	def TryToLevelUp(self):
		#print self.essenceType, "trying to level from", self.level, "to", self.level+1, "... Needs", self.EnergyRequiredToLevelUp(), "energy."
		if self.item.energy >= self.EnergyRequiredToLevelUp():
			self.item.energy -= self.EnergyRequiredToLevelUp()
			self.level += 1

			if self.consumable is not None:
				energyToConsume = self.consumable.GetEnergyContained()
				if energyToConsume > 0:
					self.item.AddEnergy(energyToConsume, self.consumable, "Consume")
					self.consumable.level = 0

			return True
		else:
			return False