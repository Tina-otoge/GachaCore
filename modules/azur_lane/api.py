from dataclasses import dataclass

from fastapi import APIRouter
from pydantic import BaseModel

from .models import Ship, Skin, SkinVariant, db

router = APIRouter()


class ShipSchema(BaseModel):
    id: str
    name: str
    rarity: Ship.Rarity
    type: Ship.Type
    affiliation: Ship.Affiliation


@dataclass
class Filter:
    type: type
    partial: bool = False


filters = {
    "name": Filter(str, partial=True),
    "rarity": Filter(Ship.Rarity),
    "affiliation": Filter(Ship.Affiliation),
    "type": Filter(Ship.Type),
}


@router.get("/ships/", response_model=list[ShipSchema])
async def get_ships(
    name: str = None,
    rarity: Ship.Rarity = None,
    affiliation: Ship.Affiliation = None,
    type: Ship.Type = None,
):
    with db.create_session() as session:
        query = session.query(Ship)
        if name:
            query = query.filter(Ship.name.ilike(f"%{name}%"))
        if rarity:
            query = query.filter(Ship.rarity == rarity)
        if affiliation:
            query = query.filter(Ship.affiliation == affiliation)
        if type:
            query = query.filter(Ship.type == type)
        return query.all()
