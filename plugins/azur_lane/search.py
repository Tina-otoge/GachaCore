from dataclasses import dataclass

from gachacore import TableFilter

from .models import Ship


@dataclass
class ShipFilters(TableFilter):
    model = Ship

    id: str = None
    name: str = None
    rarity: Ship.Rarity = None
    affiliation: Ship.Affiliation = None
    type: Ship.Type = None

    def before(self):
        self.query = self.query.order_by(self.model.id.asc())

    # TODO: Allow filtering by skin name
