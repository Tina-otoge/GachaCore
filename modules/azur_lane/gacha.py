from dataclasses import dataclass

from .models import Ship


@dataclass
class GachaRarity:
    name: str
    color: str
    bg_color: str = None
    rate: float = 1.0


@dataclass
class GachaBag:
    name: str
    items: list["GachaItem"]


@dataclass
class GachaItem:
    id: str
    name: str
    rarity: GachaRarity
    img_url: str
    rate: float = None
    thumb_url: str = None
    small_url: str = None
    bg_url: str = None
    extra: dict[str, str] = None

    variants: list["GachaVariant"] = None


@dataclass
class GachaVariant:
    name: str
    img_url: str
    thumb_url: str


def get_gacha_bags():
    return [GachaBag("all", get_gacha_items())]


def get_gacha_rarity(rarity: Ship.Rarity):
    return {
        Ship.Rarity.NORMAL: GachaRarity("Normal", "white"),
        Ship.Rarity.RARE: GachaRarity("Rare", "blue"),
        Ship.Rarity.ELITE: GachaRarity("Elite", "purple"),
        Ship.Rarity.SUPER_RARE: GachaRarity("Super Rare", "gold"),
        Ship.Rarity.ULTRA_RARE: GachaRarity("Ultra Rare", "pink"),
    }[rarity]


def get_gacha_items(page=1):
    from common.api import Pager

    pager = Pager(page)
    with Ship.db.create_session() as session:
        items = [
            GachaItem(
                id=ship.id,
                name=ship.name,
                rarity=get_gacha_rarity(ship.rarity),
                img_url=ship.default_skin.default_variant.img_url,
                thumb_url=ship.default_skin.default_variant.thumb_url,
                bg_url=ship.default_skin.bg_url,
                extra={
                    "chibi_url": ship.default_skin.chibi_url,
                    "type": ship.type.name,
                    "affiliation": ship.affiliation.name,
                },
                variants=[
                    GachaVariant(
                        name=skin.name,
                        img_url=skin.default_variant.img_url,
                        thumb_url=skin.default_variant.thumb_url,
                    )
                    for skin in ship.skins
                ],
            )
            for ship in pager.update(session.query(Ship)).all()
        ]
    return items
