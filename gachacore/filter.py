from dataclasses import dataclass
from enum import Enum


@dataclass
class TableFilter:
    def __post_init__(self):
        with self.model.db.create_session() as session:
            query = session.query(self.model)
            for field in self.__dataclass_fields__:
                value = getattr(self, field)
                if not value:
                    continue
                if isinstance(value, str) and not issubclass(type(value), Enum):
                    query = query.filter(
                        getattr(self.model, field).ilike(f"%{value}%")
                    )
                else:
                    query = query.filter(getattr(self.model, field) == value)
            self.query = query

    def before(self):
        pass
