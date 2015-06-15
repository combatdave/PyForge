from forgecards import *

class MagicItem_Base:
	name = None

	def Use(self, forgedItem):
		pass

	def __repr__(self):
		if self.name is not None:
			return self.name
		else:
			return self.__class__.__name__


class MagicItem_LightCoin(MagicItem_Base):
	name = "Light Coin"


	def Use(self, forgedItem):
		forgedItem.AddEnergy(8, self, "ItemUse")
		forgedItem.PushCard(Card_LightWisp())


class MagicItem_ShadeCoin(MagicItem_Base):
	name = "Shade Coin"


	def Use(self, forgedItem):
		forgedItem.AddEnergy(8, self, "ItemUse")
		forgedItem.PushCard(Card_ShadeWisp())


class MagicItem_Glowstone(MagicItem_Base):
	name = "Glowstone"


	def Use(self, forgedItem):
		forgedItem.PushCard(Card_Nymph())