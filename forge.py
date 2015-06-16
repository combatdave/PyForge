from forgecards import *
from forgeitems import *
from forgeessences import *
from forgeworld import *


class Material:
	def __init__(self, name):
		self.name = name
		self.resistances = {}

	def __repr__(self):
		return self.name


class ForgedItem:
	def __init__(self, world, name, material, sequence=None):
		self.world = world
		self.name = name

		self.essences = CreateEssences(self)

		self.energy = 0

		self.enteringCard = Card_None()
		self.cards = [Card_None()] * 3
		self.destroyedCard = Card_None()

		self.loop = [None] * 3

		self.material = material
		self.temporaryResistances = {}
		self.SetResistancesFromMaterial()

		self.lastMagicItem = None

		self._EvaluateSequence(sequence)


	def __repr__(self):
		return str(self.material) + " " + self.name


	def SetResistancesFromMaterial(self):
		for essence in self.essences.itervalues():
			if essence.essenceType in self.material.resistances:
				essence.resistance = self.material.resistances[essence.essenceType]
			else:
				essence.resistance = 0


	def PushCard(self, cardType):
		if isinstance(self.enteringCard, Card_None):
			card = cardType(self)
			card.OnCreated()
			self.enteringCard = card
			print self.enteringCard, "was added."
		else:
			raise Exception("Can't push a card when one already exists: " + str(self.enteringCard))


	def AddEnergy(self, energy, source, reason):
		self.energy += energy
		print "Added", energy, "energy from", source, "(" + reason + ")"


	def GetEssenceByType(self, essenceType):
		if essenceType in self.essences:
			return self.essences[essenceType]
		return None


	def PushLastToLoop(self):
		if not isinstance(self.cards[-1], Card_None):
			self.loop[0] = self.cards[-1]
			self.cards[-1] = Card_None()


	def GetTemporaryResistance(self, essenceType):
		if essenceType in self.temporaryResistances:
			return self.temporaryResistances[essenceType]

		return 0


	def AddTemporaryResistance(self, essenceType, resistance):
		if essenceType not in self.temporaryResistances:
			self.temporaryResistances[essenceType] = 0

		self.temporaryResistances[essenceType] += resistance


	def RotateLoop(self):
		self.loop = [self.loop[-1]] + self.loop[:-1]


	def _EvaluateSequence(self, sequence):
		for itemType in sequence:
			item = itemType(self.world)

			if isinstance(item, MagicItem):
				self._EvaluateMagicItem(item)
			elif isinstance(item, WorldItem):
				self._EvaluateWorldItem(item)

			print ""


	def _EvaluateMagicItem(self, item):
		print "Applying", item, "to", self, "during", self.world.GetTime()

		self._ResetForTurn()

		item.Use(self)

		self._PushCards()

		self._ApplyTaintStrengths()

		self._ApplyCardEffects()

		self._ActivateCards()

		self._EvaluateEssences()

		print "Status:"
		self._PrintEssences()
		self._PrintStack()
		self._PrintLoop()

		self.lastMagicItem = item


	def _EvaluateWorldItem(self, item):
		print "Activating", item, "during", self.world.GetTime()
		item.Use()


	def _ResetForTurn(self):
		self.energy = 0
		self.destroyedCard = Card_None()
		self.temporaryResistances = {}

		for essence in self.essences.itervalues():
			essence.ResetForTurn()


	def _PushCards(self):
		if self.enteringCard is not None and not isinstance(self.enteringCard, Card_None):
			self.destroyedCard = self.cards[-1]
			self.cards = [self.enteringCard] + self.cards[:-1]
			self.enteringCard = Card_None()


	def _ApplyTaintStrengths(self):
		for card in self.cards:
			if card.taint is not None:
				essence = self.GetEssenceByType(card.taint)
				essence.taint += card.taintStrength


	def _ApplyCardEffects(self):
		for card in self.cards:
			card.ApplyTemporaryEffects()


	def _ActivateCards(self):
		self.destroyedCard.ActivateDestroyed()
		for i, card in enumerate(self.cards):
			card.ActivateInSlot(i)


	def _EvaluateEssences(self):
		print "Improving essences with", self.energy, "energy..."
		essencesByTaint = sorted(self.essences.values(), key=lambda essence: essence.taint, reverse=True)
		essenceToLevel = essencesByTaint[0]
		while essenceToLevel.TryToLevelUp():
			pass


	def _PrintStack(self):
		for i, card in enumerate(self.cards):
			print str(i+1) + ":", card


	def _PrintEssences(self):
		for essence in self.essences.itervalues():
			print essence


	def _PrintLoop(self):
		print "\t\t<\t 2:", self.loop[2]
		print "0:", self.loop[0], "\t\t^"
		print "\t\t>\t 1:", self.loop[1]


sequence = [
	MI_Glowstone,
	MI_FocusCrystal,
	WI_Clock,
	WI_Clock,
	MI_FocusCrystal,
	MI_FocusCrystal,
]

world = World()

wood = Material("Wood")
wood.resistances[EssenceType.Shade] = 10

#i = ForgedItem(world, "Sword", wood, sequence)
