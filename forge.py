from forgecards import *
from forgeitems import *
from forgeessences import *


class Material:
	def __init__(self, name):
		self.name = name
		self.resistances = {}


	def __repr__(self):
		return self.name


class ForgedItem:
	def __init__(self, name, material, sequence=None):
		self.name = name

		self.essences = {}
		self.essences[EssenceType.Light] = Essence_Consumer(EssenceType.Light, self)
		self.essences[EssenceType.Shade] = Essence_Consumer(EssenceType.Shade, self)

		self.essences[EssenceType.Light].SetConsumableEssence(self.essences[EssenceType.Shade])
		self.essences[EssenceType.Shade].SetConsumableEssence(self.essences[EssenceType.Light])

		self.energy = 0

		self.enteringCard = Card_None()
		self.cards = [Card_None()] * 3
		self.destroyedCard = Card_None()

		self.material = material
		self.SetResistancesFromMaterial()

		self._EvaluateSequence(sequence)


	def __repr__(self):
		return str(self.material) + " " + self.name


	def SetResistancesFromMaterial(self):
		for essence in self.essences.itervalues():
			if essence.essenceType in self.material.resistances:
				essence.resistance = self.material.resistances[essence.essenceType]
			else:
				essence.resistance = 0


	def PushCard(self, card):
		if isinstance(self.enteringCard, Card_None):
			self.enteringCard = card
		else:
			raise Exception("Can't push a card when one already exists: " + str(self.enteringCard))


	def AddEnergy(self, energy, source, reason):
		self.energy += energy
		print "Added", energy, "energy from", source, "(" + reason + ")"


	def GetEssenceByType(self, essenceType):
		if essenceType in self.essences:
			return self.essences[essenceType]
		return None


	def _EvaluateSequence(self, sequence):
		for item in sequence:
			print "Applying", item, "to", self

			self._ResetForTurn()

			self._UseItem(item)

			self._PushCards()

			self._ApplySpiritEssenceStrengths()

			self._ApplyCardEffects()

			self._ActivateCards()

			self._EvaluateEssences()

			print "Turn complete:"
			self._PrintEssences()
			self._PrintStack()
			print ""


	def _ResetForTurn(self):
		self.energy = 0
		self.destroyedCard = Card_None

		for essence in self.essences.itervalues():
			essence.ResetForTurn()


	def _UseItem(self, item):
		item.Use(self)


	def _PushCards(self):
		self.destroyedCard = self.cards[-1]
		self.cards = [self.enteringCard] + self.cards[:-1]
		self.enteringCard = Card_None()


	def _ApplySpiritEssenceStrengths(self):
		for card in self.cards:
			if card.spiritEssence is not None:
				essence = self.GetEssenceByType(card.spiritEssence)
				essence.taint += card.spiritEssenceStrength


	def _ApplyCardEffects(self):
		for card in self.cards:
			card.ApplyTemporaryEffects(self)


	def _ActivateCards(self):
		self.destroyedCard.ActivateDestroyed(self)
		for i, card in enumerate(self.cards):
			card.ActivateInSlot(self, i)


	def _EvaluateEssences(self):
		print "Improving essences with", self.energy, "energy..."
		essenceToLevel = sorted(self.essences.values(), key=lambda essence: essence.taint, reverse=True)[0]
		while essenceToLevel.TryToLevelUp():
			pass


	def _PrintStack(self):
		for i, card in enumerate(self.cards):
			print str(i+1) + ":", card


	def _PrintEssences(self):
		for essence in self.essences.itervalues():
			print essence


sequence = [
	MagicItem_Glowstone(),
	MagicItem_LightCoin(),
	MagicItem_LightCoin(),
	MagicItem_LightCoin(),
]


sequence = [
	MagicItem_Glowstone(),
	MagicItem_ShadeCoin(),
	MagicItem_ShadeCoin(),
	MagicItem_ShadeCoin(),
]


wood = Material("Wood")
wood.resistances[EssenceType.Shade] = 10

i = ForgedItem("Sword", wood, sequence)
