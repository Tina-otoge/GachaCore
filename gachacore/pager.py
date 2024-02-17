from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class Pager:
    """
    A pagination helper.

    p = Pager(page=1, results=10, offset=2)
    query = session.query(Table).filter(Table.field == "value")

    >>> p(query)
    {
        "results": [Table, Table, Table],
        "info": {
            "page": 1,
            "pages": 10,
            "count": 10,
            "total": 100,
            "offset": 2,
        },
    }
    """

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
                    "results": list[schema],
                    "info": cls.PageInfoSchema,
                },
            },
        )
        return result

    def update(self, query):
        offset = (self.page - 1) * self.results
        offset += self.offset
        return query.offset(offset).limit(self.results)

    def __call__(self, query):
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
