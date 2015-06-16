from forgecards import *
from forgeworld import *


class WorldItem:
	name = None

	def __init__(self, world):
		self.world = world

	def Use(self):
		raise Exception("Unimplemented")

	def __repr__(self):
		if self.name is not None:
			return self.name
		else:
			return self.__class__.__name__


class MagicItem(WorldItem):
	def Use(self, forgedItem):
		raise Exception("Unimplemented")


class MI_Glowstone(MagicItem):
	name = "Glowstone"

	def Use(self, forgedItem):
		forgedItem.PushCard(Card_Nymph)


class MI_Sparkstone(MagicItem):
	name = "Sparkstone"

	def Use(self, forgedItem):
		forgedItem.PushLastToLoop()
		forgedItem.PushCard(Card_CracklingSpark)


class MI_FocusCrystal(MagicItem):
	name = "Focus Crystal"

	def Use(self, forgedItem):
		forgedItem.AddEnergy(8, self, "ItemUse")
		time = self.world.GetTime()
		if time == World.Day:
			forgedItem.PushCard(Card_LightWisp)
		elif time == World.Night:
			forgedItem.PushCard(Card_ShadeWisp)


class WI_Clock(WorldItem):
	name = "Clock"

	def Use(self):
		self.world.IncreaseTime()