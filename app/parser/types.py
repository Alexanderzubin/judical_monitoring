import datetime
from typing import TypedDict


class ParsedCaseTableData(TypedDict):
    unique_identifier: str
    judge: str
    date_of_receipt: datetime.date
    court: str
    categories: list[str]


class ParsedCaseData(TypedDict):
    number: str
    unique_identifier: str
    judge: str
    date_of_receipt: datetime.date
    court: str
    categories: list[str]


class ParsedCaseEventData(TypedDict):
    date: datetime.date
    time: datetime.time
    event_name: str
    location: str | None
    result: str | None
    reason: str | None
    note: str | None
    placement_date: datetime.date
