from gachacore.gacha import GachaItem, PluginGacha

from .models import Student
from .search import StudentFilters


class BlueArchiveGacha(PluginGacha):
    SLUG = "ba"
    ITEM_TYPE = Student
    SEARCH = StudentFilters
    GRID_SIZE = PluginGacha.Size.SMALL
    THUMB_HEIGHT = PluginGacha.Size.SMALL

    @classmethod
    def build_gacha_item(cls, item: Student):
        return GachaItem(
            id=item.id,
            name=item.name,
            rarity=None,
            img_url=item.portrait_url,
            thumb_url=item.thumb_url,
            bg_url=item.background_url,
        )
