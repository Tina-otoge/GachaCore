from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class Pager:
    page: int = 1
    results: int = 100
    offset: int = 0

    class PageInfoSchema(BaseModel):
        page: int
        pages: int
        count: int
        total: int
        offset: int

    @classmethod
    def schema(cls, schema):
        result = type(
            schema.__name__,
            (BaseModel,),
            {
                "__annotations__": {
                    "items": list[schema],
                    "page_info": cls.PageInfoSchema,
                },
            },
        )
        return result

    def update(self, query):
        offset = (self.page - 1) * self.results
        offset += self.offset
        return query.offset(offset).limit(self.results)

    def __call__(self, filters):
        query = filters.query
        total = query.count()
        query = self.update(query)
        items = query.all()
        return {
            "results": items,
            "info": self.PageInfoSchema(
                page=self.page,
                pages=(total + self.results - 1) // self.results,
                count=len(items),
                total=total,
                offset=self.offset,
            ),
        }


@dataclass
class TableFilter:
    def __post_init__(self):
        with self.model.db.create_session() as session:
            query = session.query(self.model)
            for field in self.__dataclass_fields__:
                value = getattr(self, field)
                if not value:
                    continue
                if isinstance(value, str):
                    query = query.filter(
                        getattr(self.model, field).ilike(f"%{value}%")
                    )
                else:
                    query = query.filter(getattr(self.model, field) == value)
            self.query = query
