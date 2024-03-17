import dataclasses
import enum
from dataclasses import dataclass

from gachacore import TableFilter
from gachacore.pager import Pager


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
    extra: dict[str, str] = dataclasses.field(default_factory=dict)

    variants: list["GachaVariant"] = None


@dataclass
class GachaVariant:
    name: str
    img_url: str
    thumb_url: str


class PluginGacha:
    class Size(enum.Enum):
        SMALL = enum.auto()
        MEDIUM = enum.auto()
        LARGE = enum.auto()

    ITEM_TYPE: type = None
    SLUG = None
    SEARCH = None  # TODO: Need a more solid interface approach, this fails later if not filled with a TableFilters subclass
    GRID_SIZE = Size.LARGE
    THUMB_HEIGHT = Size.LARGE

    @classmethod
    def get_gacha_bags(cls) -> list[GachaBag]:
        return [GachaBag("all", cls.get_gacha_items())]

    @classmethod
    def build_gacha_item(cls, item) -> GachaItem:
        """Build a GachaItem from the given lower-level plugin-specific item."""
        raise NotImplementedError

    @classmethod
    def build_gacha_rarity(cls, rarity) -> GachaRarity:
        """Build a GachaRarity from the given lower-level plugin-specific rarity."""
        raise NotImplementedError

    @classmethod
    def get_gacha_item(cls, id: str) -> GachaItem:
        if cls.ITEM_TYPE is None:
            raise NotImplementedError
        with cls.ITEM_TYPE.db.create_session() as session:
            item = session.query(cls.ITEM_TYPE).get(id)
            if item is None:
                return None
            result = cls.build_gacha_item(item)
        return result

    @classmethod
    def get_gacha_items(cls, filters: TableFilter, page=1) -> list[GachaItem]:
        pager = Pager(page)
        filters.before()
        paged = pager(filters.query)
        paged["results"] = [
            cls.build_gacha_item(item) for item in paged["results"]
        ]
        return paged
