from forgeessences import *


class Card:
	name = None

	spiritEssence = None
	spiritEssenceStrength = 0

	def __repr__(self):
		if self.name is not None:
			return self.name
		else:
			return self.__class__.__name__


	def ActivateInSlot(self, item, cardSlot):
		pass


	def ActivateDestroyed(self, item):
		pass


	def ApplyTemporaryEffects(self, item):
		pass


class Card_None(Card):
	name = "--"


class Card_LightWisp(Card):
	name = "Light Wisp"
	spiritEssence = EssenceType.Light
	spiritEssenceStrength = 1

	def ApplyTemporaryEffects(self, item):
		pass
		#item.essence_light.taint += 1


class Card_ShadeWisp(Card):
	name = "Shade Wisp"
	spiritEssence = EssenceType.Shade
	spiritEssenceStrength = 1

	def ApplyTemporaryEffects(self, item):
		pass
		#item.essence_shade.taint += 1


class Card_Nymph(Card):
	name = "Nymph"

	def ActivateDestroyed(self, item):
		item.AddEnergy(192, self, "CardDestroyed")