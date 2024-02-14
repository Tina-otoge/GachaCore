import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped as Column
from sqlalchemy.orm import mapped_column as column
from sqlalchemy.orm import relationship

from database import Database

db = Database("azur_lane")


class EnumStr(enum.StrEnum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> str:
        return name.lower().replace("_", " ").title()


class Ship(db.Base):
    class Rarity(EnumStr):
        NORMAL = enum.auto()
        RARE = enum.auto()
        ELITE = enum.auto()
        SUPER_RARE = enum.auto()
        ULTRA_RARE = enum.auto()

        def next(self):
            # Return the next rarity in the enum for a StrEnum
            return Ship.Rarity(self.value + 1)

    class Type(EnumStr):
        # ref: https://azurlane.koumakan.jp/wiki/Category:Ship_types

        AIRCRAFT_CARRIER = enum.auto()
        AIRCRAFT_BATTLESHIP = enum.auto()
        BATTLECRUISER = enum.auto()
        BATTLESHIP = enum.auto()
        DESTROYER = enum.auto()
        GUIDED_MISSILE_DESTROYER = "Guided-Missile Destroyer"
        HEAVY_CRUISER = enum.auto()
        LARGE_CRUISER = enum.auto()
        LIGHT_AIRCRAFT_CARRIER = enum.auto()
        LIGHT_CRUISER = enum.auto()
        MONITOR = enum.auto()
        MUNITION_SHIP = enum.auto()
        REPAIR_SHIP = enum.auto()
        SUBMARINE = enum.auto()
        SUBMARINE_CARRIER = enum.auto()

        # Pirates
        PIRATE_MAIN = "Sailing Frigate (Main)"
        PIRATE_SUBMARINE = "Sailing Frigate (Submarine)"
        PIRATE_VANGUARD = "Sailing Frigate (Vanguard)"

        # Collabs only
        AVIATION_BATTLESHIP = enum.auto()

    class Affiliation(EnumStr):
        # ref: https://azurlane.koumakan.jp/wiki/Nations

        # Major Nations
        EAGLE_UNION = enum.auto()
        ROYAL_NAVY = enum.auto()
        SAKURA_EMPIRE = enum.auto()
        IRON_BLOOD = enum.auto()
        DRAGON_EMPERY = enum.auto()
        NORTHERN_PARLIAMENT = enum.auto()
        IRIS_ORTHODOXY = enum.auto()
        IRIS_LIBRE = enum.auto()
        VICHYA_DOMINION = enum.auto()
        SARDEGNA_EMPIRE = enum.auto()

        UNIVERSAL = enum.auto()

        # Sirens
        META = "META"

        # Pirates
        TEMPESTA = enum.auto()

        # Collabs
        NEPTUNIA = enum.auto()
        BILIBILI = enum.auto()
        UTAWARERUMONO = enum.auto()
        KIZUNA_AI = "KizunaAI"
        HOLOLIVE = enum.auto()
        VENUS_VACATION = enum.auto()
        THE_IDOLMASTER = enum.auto()
        SSSS = "SSSS"
        ATELIER_RYZA = enum.auto()
        SENRAN_KAGURA = enum.auto()

    id: Column[str] = column(primary_key=True)
    name: Column[str]
    rarity: Column[Rarity]
    type: Column[Type]
    affiliation: Column[Affiliation]

    skins = relationship("Skin", backref="ship")


class Skin(db.Base):
    ship_id: Column[str] = column(ForeignKey("ships.id"), primary_key=True)
    name: Column[str] = column(primary_key=True)
    bg_url: Column[str]
    chibi_url: Column[str] = column(nullable=True)

    variants = relationship(
        "SkinVariant",
        backref="skin",
        lazy="joined",
        primaryjoin="and_(Skin.ship_id == SkinVariant.skin_ship_id, Skin.name == SkinVariant.skin_name)",
    )


class SkinVariant(db.Base):
    skin_ship_id: Column[str] = column(
        ForeignKey("skins.ship_id"), primary_key=True
    )
    skin_name: Column[str] = column(ForeignKey("skins.name"), primary_key=True)
    name: Column[str] = column(primary_key=True)
    img_url: Column[str]
    thumb_url: Column[str]
