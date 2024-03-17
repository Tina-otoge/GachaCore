from gachacore.gacha import GachaItem, GachaRarity, GachaVariant, PluginGacha

from .models import Ship
from .search import ShipFilters


class AzurLaneGacha(PluginGacha):
    SLUG = "al"
    ITEM_TYPE = Ship
    SEARCH = ShipFilters

    @classmethod
    def build_gacha_rarity(cls, rarity: Ship.Rarity):
        return {
            Ship.Rarity.NORMAL: GachaRarity("Normal", "white"),
            Ship.Rarity.RARE: GachaRarity("Rare", "blue"),
            Ship.Rarity.ELITE: GachaRarity("Elite", "purple"),
            Ship.Rarity.SUPER_RARE: GachaRarity("Super Rare", "gold"),
            Ship.Rarity.ULTRA_RARE: GachaRarity("Ultra Rare", "pink"),
        }[rarity]

    @classmethod
    def build_gacha_item(cls, item: Ship):
        return GachaItem(
            id=item.id,
            name=item.name,
            rarity=cls.build_gacha_rarity(item.rarity),
            img_url=item.default_skin.default_variant.img_url,
            thumb_url=item.default_skin.default_variant.thumb_url,
            bg_url=item.default_skin.bg_url,
            extra={
                "chibi_url": item.default_skin.chibi_url,
                "type": item.type,
                "affiliation": item.affiliation,
            },
            variants=[
                GachaVariant(
                    name=skin.name,
                    img_url=skin.default_variant.img_url,
                    thumb_url=skin.default_variant.thumb_url,
                )
                for skin in item.skins
            ],
        )
