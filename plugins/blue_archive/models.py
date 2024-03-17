import enum
import typing as t

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped as Column
from sqlalchemy.orm import mapped_column as column
from sqlalchemy.orm import relationship

from gachacore.database import Database
from gachacore.types import EnumStr

db = Database("blue_archive")

# https://github.com/SchaleDB/SchaleDB/blob/main/data/en/localization.json


class Student(db.Base):
    class Type(EnumStr):
        STRIKER = enum.auto()
        SPECIAL = enum.auto()

        @classmethod
        def from_data(cls, data: str):
            return {
                "Main": cls.STRIKER,
                "Support": cls.SPECIAL,
            }[data]

    class Role(EnumStr):
        DAMAGE_DEALER = "Damage Dealer"
        SUPPORTER = enum.auto()
        TANKER = enum.auto()
        VEHICLE = enum.auto()
        HEALER = enum.auto()

    class Position(EnumStr):
        FRONT = enum.auto()
        MIDDLE = enum.auto()
        BACK = enum.auto()

    class Bullet(EnumStr):
        EXPLOSIVE = enum.auto()
        SONIC = enum.auto()
        PIERCING = enum.auto()
        MYSTIC = enum.auto()

        @classmethod
        def from_data(cls, data: str):
            tr = {
                "Explosion": cls.EXPLOSIVE,
                "Pierce": cls.PIERCING,
            }
            return tr.get(data) or cls(data)

    class Armor(EnumStr):
        LIGHT = enum.auto()
        HEAVY = enum.auto()
        ELASTIC = enum.auto()
        SPECIAL = enum.auto()

        @classmethod
        def from_data(cls, data: str):
            return {
                "LightArmor": cls.LIGHT,
                "HeavyArmor": cls.HEAVY,
                "ElasticArmor": cls.ELASTIC,
                "Unarmed": cls.SPECIAL,
            }

    WEAPON = t.Literal[
        "HG", "RL", "FT", "RG", "SG", "GL", "SMG", "AR", "SR", "MT", "MG"
    ]

    CLUB = {
        "Kohshinjo68": "Problem Solver 68",
        "Justice": "Justice Task Force",
        "CleanNClearing": "Cleaning & Clearing",
        "BookClub": "Library Committee",
        "Countermeasure": "Foreclosure Task Force",
        "Engineer": "Engineering Department",
        "FoodService": "School Lunch Club",
        "Fuuki": "Prefect Team",
        "GourmetClub": "Gourmet Research Society",
        "HoukagoDessert": "After-School Sweets Club",
        "KnightsHospitaller": "Remedial Knights",
        "MatsuriOffice": "Festival Operations Department",
        "Meihuayuan": "Plum Blossom Garden",
        "Onmyobu": "Yin-Yang Club",
        "RemedialClass": "Make-Up Work Club",
        "SPTF": "Super Phenomenon Task Force",
        "Shugyobu": "Inner Discipline Club",
        "Endanbou": "Eastern Alchemy Society",
        "TheSeminar": "Seminar",
        "TrainingClub": "Athletics Training Club",
        "TrinityVigilance": "Trinity's Vigilante Crew",
        "Veritas": "Veritas",
        "NinpoKenkyubu": "Ninjutsu Research Club",
        "GameDev": "Game Development Department",
        "RedwinterSecretary": "Red Winter Office",
        "anzenkyoku": "Public Safety Bureau",
        "SisterHood": "The Sisterhood",
        "Class227": "Spec Ops No. 227",
        "Emergentology": "Medical Emergency Club",
        "RabbitPlatoon": "RABBIT Squad",
        "PandemoniumSociety": "Pandemonium Society",
        "AriusSqud": "Arius Squad",
        "HotSpringsDepartment": "Hot Springs Department",
        "TeaParty": "Tea Party",
        "PublicPeaceBureau": "Public Peace Bureau",
        "BlackTortoisePromenade": "Black Tortoise Promenade",
        "Genryumon": "Genryumon",
        "LaborParty": "Labor Party",
        "KnowledgeLiberationFront": "Knowledge Liberation Front",
        "Hyakkayouran": "Hyakkayouran Resolution Council",
        "EmptyClub": None,
    }

    id: Column[int] = column(primary_key=True)
    name: Column[str]
    family_name: Column[str]
    age: Column[str]
    schale_page: Column[str]
    game_id: Column[str]
    year: Column[str] = column(nullable=True)
    background: Column[str]
    intro: Column[str]
    hobby: Column[str]
    birthday: Column[str]
    height: Column[str]

    @property
    def portrait_url(self):
        return f"https://schale.gg/images/student/portrait/{self.id}.webp"

    @property
    def thumb_url(self):
        return f"https://schale.gg/images/student/collection/{self.id}.webp"

    @property
    def background_url(self):
        return f"https://schale.gg/images/background/{self.background}.jpg"

    @property
    def schale_url(self):
        return f"https://schale.gg/?chara={self.schale_page}"
