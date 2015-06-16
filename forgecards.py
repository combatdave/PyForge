from forgeessences import *


class Card:
	name = None

	taint = None
	taintStrength = 0


	def __init__(self, item):
		self.item = item


	def __repr__(self):
		if self.name is not None:
			return self.name
		else:
			return self.__class__.__name__


	def OnCreated(self):
		pass


	def ActivateInSlot(self, cardSlot):
		pass


	def ActivateDestroyed(self):
		pass


	def ApplyTemporaryEffects(self):
		pass


class Card_None(Card):
	name = "--"

	def __init__(self):
		pass


class Card_Wisp(Card):
	def OnCreated(self):
		if self.taint is not None:
			essence = self.item.GetEssenceByType(self.taint)
			essence.taint += 1


class Card_LightWisp(Card_Wisp):
	name = "Light Wisp"
	taint = EssenceType.Light
	taintStrength = 1


class Card_ShadeWisp(Card_Wisp):
	name = "Shade Wisp"
	taint = EssenceType.Shade
	taintStrength = 1


class Card_Nymph(Card):
	name = "Nymph"

	def ActivateDestroyed(self):
		self.item.AddEnergy(192, self, "CardDestroyed")


class Card_CracklingSpark(Card):
	name = "Crackling Spark"

	def ApplyTemporaryEffects(self):
		self.item.AddTemporaryResistance(EssenceType.Light, 5)
		self.item.AddTemporaryResistance(EssenceType.Shade, 5)