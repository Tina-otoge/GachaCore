from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from common.api import Pager, TableFilter
from common.errors import NotFound

from .models import Ship

router = APIRouter()


class VariantSchema(BaseModel):
    name: str
    img_url: str
    thumb_url: str


class SkinSchema(BaseModel):
    name: str
    bg_url: str
    chibi_url: str | None

    variants: list[VariantSchema]


class ShipSchema(BaseModel):
    id: str
    name: str
    rarity: Ship.Rarity
    type: Ship.Type
    affiliation: Ship.Affiliation


class DetailedShipSchema(ShipSchema):
    skins: list[SkinSchema]


@dataclass
class ShipFilters(TableFilter):
    model = Ship

    id: str = None
    name: str = None
    rarity: Ship.Rarity = None
    affiliation: Ship.Affiliation = None
    type: Ship.Type = None

    # TODO: Allow filtering by skin name


@router.get("/ships/", response_model=Pager.schema(ShipSchema))
async def get_ships(
    filters: Annotated[ShipFilters, Depends()],
    pager: Annotated[Pager, Depends()],
):
    return pager(filters)


@router.get("/ships/{ship_id_or_name}", response_model=DetailedShipSchema)
async def get_ship(ship_id_or_name: str):
    with Ship.db.create_session() as session:
        result = (
            session.query(Ship).filter(Ship.name == ship_id_or_name).first()
            or session.query(Ship).filter(Ship.id == ship_id_or_name).first()
        )
        if not result:
            raise NotFound(Ship, ship_id_or_name)
        # Needed to lazy load the relationships from within the session context
        return DetailedShipSchema.model_validate(result, from_attributes=True)
