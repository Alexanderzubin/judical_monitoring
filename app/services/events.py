from typing import Self

from app.database.models import CaseEvent
from app.database.repositories.case_event import CaseEventRepository
from app.database.session import Session
from app.services.exceptions import CaseEventNotFoundError


class CaseEventService:
    def __init__(
        self,
        case_event_repository: CaseEventRepository,
    ):
        self._case_event_repository = case_event_repository

    @classmethod
    def get_service(cls, session: Session) -> Self:
        return cls(
            case_event_repository=CaseEventRepository(session),
        )

    def find_event_by_id(self, event_id) -> CaseEvent:
        case_event = self._case_event_repository.get_by_id(event_id)
        if not case_event:
            raise CaseEventNotFoundError()

        return case_event
