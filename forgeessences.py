class EssenceType:
	Fire = "Fire"
	Water = "Water"
	Light = "Light"
	Shade = "Shade"
	Mecha = "Mecha"
	Nature = "Nature"


def CreateEssences(owner):
	essences = {}

	essences[EssenceType.Fire] = Essence_Consumer(EssenceType.Fire, owner)
	essences[EssenceType.Water] = Essence_Consumer(EssenceType.Water, owner)

	m = essences[EssenceType.Mecha] = Essence_Circular(EssenceType.Mecha, owner)
	n = essences[EssenceType.Nature] = Essence_Circular(EssenceType.Nature, owner)
	l = essences[EssenceType.Light] = Essence_Circular(EssenceType.Light, owner)
	s = essences[EssenceType.Shade] = Essence_Circular(EssenceType.Shade, owner)

	essences[EssenceType.Fire].SetConsumableEssence(essences[EssenceType.Water])
	essences[EssenceType.Water].SetConsumableEssence(essences[EssenceType.Fire])

	m.SetClockwiseEssence(l)
	m.SetCounterclockwiseEssence(s)

	l.SetClockwiseEssence(n)
	l.SetCounterclockwiseEssence(m)

	n.SetClockwiseEssence(s)
	n.SetCounterclockwiseEssence(l)

	s.SetClockwiseEssence(m)
	s.SetCounterclockwiseEssence(n)

	return essences


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
		return self.essenceType + " essence (" + str(self.level) + ")"#" - contains " + str(self.GetEnergyContained()) + " energy"


	def EnergyRequiredToLevelUp(self):
		baseEnergyRequired = self._GetEnergyForLevel(self.level + 1)

		resistance = self.item.GetTemporaryResistance(self.essenceType) + self.resistance
		if resistance >= 10:
			resistance = 10
		elif resistance <= -10:
			resistance = -10

		multiplier = 1.0 + (resistance / 20.0)	# 0.5 to 1.5
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
		print self.essenceType, "trying to level from", self.level, "to", self.level+1, "... Needs", self.EnergyRequiredToLevelUp(), "energy."
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
		print self.essenceType, "trying to level from", self.level, "to", self.level+1, "... Needs", self.EnergyRequiredToLevelUp(), "energy."
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


class Essence_Circular(Essence):
	def SetClockwiseEssence(self, essence):
		self.clockwise = essence

	def SetCounterclockwiseEssence(self, essence):
		self.counterclockwise = essence