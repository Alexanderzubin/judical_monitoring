import logging
from datetime import datetime
from typing import Self

from app.database.models import Case, CaseEvent
from app.database.repositories.case import CaseRepository
from app.database.repositories.case_event import CaseEventRepository
from app.database.repositories.category import CategoryRepository
from app.database.repositories.court import CourtRepository
from app.database.repositories.judge import JudgeRepository
from app.database.session import Session
from app.parser.parser import CasePageParser
from app.parser.types import ParsedCaseEventData
from app.services.exceptions import CasePageParsingError, CaseNotFoundError
from app.settings import settings

logger = logging.getLogger(__name__)


class CaseService:
    def __init__(
        self,
        case_repository: CaseRepository,
        case_event_repository: CaseEventRepository,
        judge_repository: JudgeRepository,
        court_repository: CourtRepository,
        category_repository: CategoryRepository,
        session: Session,
        case_page_request_timeout_seconds: int = settings.case_page_request_timeout_seconds,
    ):
        self._case_repository = case_repository
        self._case_event_repository = case_event_repository
        self._judge_repository = judge_repository
        self._court_repository = court_repository
        self._category_repository = category_repository
        self._session = session
        self._case_page_request_timeout_seconds = case_page_request_timeout_seconds

    @classmethod
    def get_service(cls, session: Session) -> Self:
        return cls(
            case_repository=CaseRepository(session),
            case_event_repository=CaseEventRepository(session),
            judge_repository=JudgeRepository(session),
            court_repository=CourtRepository(session),
            category_repository=CategoryRepository(session),
            session=session,
        )

    def get_case_by_url(self, url: str) -> Case | None:
        return self._case_repository.get_by_url(url)

    def find_case_by_id(self, case_id: int) -> Case:
        case = self._case_repository.get_by_id(case_id)
        if not case:
            raise CaseNotFoundError()

        return case

    def get_or_create_case(self, url: str) -> tuple[Case, bool]:
        parser = self._get_case_page_parser(url)
        case_data = parser.get_case_data()
        created = True

        if not case_data:
            raise CasePageParsingError()

        case = self._case_repository.get_by_unique_identifier(
            identifier=case_data['unique_identifier']
        )
        if case:
            created = False
            return case, created

        judge = self._judge_repository.get_or_create(case_data['judge'])
        court = self._court_repository.get_or_create(case_data['court'])

        categories = []
        for category_name in case_data['categories']:
            category = self._category_repository.get_or_create(category_name)
            categories.append(category)

        case = self._case_repository.create(
            number=case_data['number'],
            unique_identifier=case_data['unique_identifier'],
            date_of_receipt=case_data['date_of_receipt'],
            url=url,
            judge=judge,
            court=court,
            categories=categories,
        )

        return case, created

    def check_case_for_updates(self, case: Case) -> list[CaseEvent]:
        """
        Проверяет дело на наличие обновлений. Возвращает сохранённые новые события по делу.
        """
        parser = self._get_case_page_parser(case.url)
        case_data = parser.get_case_data()
        parsed_events = parser.get_case_events()

        if not case_data:
            raise CasePageParsingError()

        changes = {}

        if case.number != case_data['number']:
            case.number = case_data['number']

        if case.judge.name != case_data['judge']:
            changes['judge'] = {'old': case.judge.name, 'new': case_data['judge']}
            new_judge = self._judge_repository.get_or_create(case_data['judge'])
            case.judge = new_judge

        new_parsed_events = self._get_new_parsed_events(case, parsed_events)
        new_events = []

        if new_parsed_events:
            logger.info(f'Got {len(new_parsed_events)} new events for {case.id}')
            for event in new_parsed_events:
                new_event = self._case_event_repository.create(case, event)
                new_events.append(new_event)

        if changes:
            self._case_repository.update(case)
            # TODO: создать задачу, которая будет уведомлять всех юзеров об изменении судьи

        return new_events

    def get_cases_for_sync(self) -> list[Case]:
        return self._case_repository.get_cases_for_sync()

    def _get_case_page_parser(self, url: str) -> CasePageParser:
        return CasePageParser(
            url=url,
            timeout=self._case_page_request_timeout_seconds,
        )

    def _get_new_parsed_events(
        self,
        case: Case, parsed_events: list[ParsedCaseEventData]
    ) -> list[ParsedCaseEventData]:
        existing_events: list[CaseEvent] = case.events

        existing_events_map = {
            (event.name, event.occurred_at): event for event in existing_events
        }

        new_parsed_events = []

        for parsed_event in parsed_events:
            event_occurred_at = datetime.combine(parsed_event['date'], parsed_event['time'])
            event_key = (parsed_event['event_name'], event_occurred_at)

            if event_key not in existing_events_map:
                new_parsed_events.append(parsed_event)

        return new_parsed_events