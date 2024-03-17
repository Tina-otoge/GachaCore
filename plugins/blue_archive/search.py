from dataclasses import dataclass

from gachacore import TableFilter

from .models import Student


@dataclass
class StudentFilters(TableFilter):
    model = Student

    name: str = None
