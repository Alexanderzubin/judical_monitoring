import logging
from typing import Dict
from app.database.models.user import User
from app.database.models.case_event import CaseEvent
from app.database.repositories.user import UserRepository
from app.database.repositories.case import CaseRepository
from app.database.repositories.case_event import CaseEventRepository
from app.database.repositories.subscription import SubscriptionRepository
from app.database.repositories.notification import NotificationRepository
from app.database.session import Session
from app.parser.parser import CasePageParser

logger = logging.getLogger(__name__)


def create_case_from_url(session: Session, case_url: str, parser: CasePageParser) -> Dict:

    try:
        parsed_data = parser.get_case_data()
        if not parsed_data:
            return {'status': 'error', 'message': 'Не удалось распарсить данные дела'}

        case_repo = CaseRepository(session, logger)

        existing_case = case_repo.get_by_url(case_url)
        if existing_case:
            return {
                'status': 'exists',
                'case_id': existing_case.id,
                'message': 'Дело уже существует в системе'
            }

        new_case = case_repo.create(
            number=parsed_data['number'],
            unique_identifier=parsed_data['unique_identifier'],
            judge=parsed_data['judge'],
            date_of_receipt=parsed_data['date_of_receipt'],
            url=case_url,
            court=parsed_data['court'],
            categories=parsed_data['categories']
        )

        return {
            'status': 'success',
            'case_id': new_case.id,
            'data': parsed_data
        }

    except Exception as exc:
        logger.error(f'Ошибка при создании дела: {str(exc)}')
        return {
            'status': 'error',
            'message': f'Ошибка при создании дела: {str(exc)}'
        }


def get_case_updates(session: Session, case_id: int, parser: CasePageParser) -> Dict:

    try:
        case_repo = CaseRepository(session, logger)
        event_repo = CaseEventRepository(session, logger)

        case = case_repo.get_by_id(case_id)
        if not case:
            return {'status': 'error', 'message': 'Дело не найдено'}

        current_data = parser.get_case_data()
        current_events = parser.get_event_data()

        changes = {}

        if case.number != current_data['number']:
            changes['number'] = {'old': case.number, 'new': current_data['number']}

        if case.judge != current_data['judge']:
            changes['judge'] = {'old': case.judge, 'new': current_data['judge']}

        existing_events = [e.name for e in case.events]
        new_events = [
            e for e in current_events
            if e['name'] not in existing_events
        ]

        if new_events:
            changes['new_events'] = new_events
            for event in new_events:
                event_repo.create(
                    name=event['name'],
                    date=event['date'],
                    time=event['time'],
                    result=event['result'],
                    the_basic_for_the_selected_result=event['the_basic_for_the_selected_result'],
                    date_of_placement=event['date_of_placement'],
                    case=case
                )

        if changes:
            case_repo.update(case)

        return {
            'status': 'success',
            'case_id': case_id,
            'changes': changes,
            'has_changes': bool(changes)
        }

    except Exception as exc:
        logger.error(f'Ошибка при проверке обновлений: {str(exc)}')
        return {
            'status': 'error',
            'message': f'Ошибка при проверке обновлений: {str(exc)}'
        }


def subscribe_user_to_case(session: Session, user_id: int, case_url: str, parser: CasePageParser) -> Dict:

    try:
        case_repo = CaseRepository(session, logger)
        sub_repo = SubscriptionRepository(session, logger)

        case = case_repo.get_by_url(case_url)

        if not case:
            case_data = create_case_from_url(session, case_url, parser)
            if case_data['status'] != 'success':
                return case_data
            case_id = case_data['case_id']
        else:
            case_id = case.id

        existing_sub = sub_repo.get_by_user_and_case(user_id, case_id)
        if existing_sub:
            return {
                'status': 'exists',
                'subscription_id': existing_sub.id,
                'message': 'Подписка уже существует'
            }

        subscription = sub_repo.create(user_id=user_id, case_id=case_id)

        return {
            'status': 'success',
            'subscription_id': subscription.id,
            'case_id': case_id
        }

    except Exception as exc:
        logger.error(f'Ошибка при подписке пользователя: {str(exc)}')
        return {
            'status': 'error',
            'message': f'Ошибка при подписке пользователя: {str(exc)}'
        }


def get_user_subscriptions(session: Session, user_id: int) -> Dict:

    try:
        sub_repo = SubscriptionRepository(session, logger)
        subscriptions = sub_repo.get_user_subscriptions(user_id)

        return {
            'status': 'success',
            'subscriptions': [
                {
                    'id': sub.id,
                    'case_id': sub.case_id,
                    'created_at': sub.created_at
                }
                for sub in subscriptions
            ]
        }

    except Exception as exc:
        logger.error(f'Ошибка при получении подписок: {str(exc)}')
        return {
            'status': 'error',
            'message': f'Ошибка при получении подписок: {str(exc)}'
        }


def create_notification_for_event(session: Session, user_id: int, event_id: int) -> Dict:

    try:
        user_repo = UserRepository(session, logger)
        event_repo = CaseEventRepository(session, logger)
        notif_repo = NotificationRepository(session, logger)

        user = user_repo.get_by_tg_id(user_id)
        if not user:
            raise ValueError('Пользователь не найден')

        event = event_repo.get_by_id(event_id)
        if not event:
            raise ValueError("Событие не найдено")

        notification = notif_repo.create(user=user, event=event)

        return {
            'status': 'success',
            'notification_id': notification.id,
            'event_id': event_id,
            'user_id': user_id
        }

    except Exception as exc:
        logger.error(f'Ошибка при создании уведомления: {str(exc)}')
        return {
            'status': 'error',
            'message': f'Ошибка при создании уведомления: {str(exc)}',
            'user_id': user_id,
            'event_id': event_id
        }


def check_all_active_cases(session: Session, parser: CasePageParser) -> Dict:

    try:
        sub_repo = SubscriptionRepository(session, logger)
        case_repo = CaseRepository(session, logger)

        subscriptions = sub_repo.get_user_subscriptions(user_id=id(session))

        results = []

        for sub in subscriptions:
            case_updates = get_case_updates(session, sub.case_id, parser)

            if case_updates['status'] == 'success' and case_updates['has_changes']:
                for event in case_updates.get('new_events', []):
                    create_notification_for_event(
                        session,
                        sub.user_id,
                        event['id']
                    )

            results.append({
                'case_id': sub.case_id,
                'user_id': sub.user_id,
                'has_changes': case_updates.get('has_changes', False)
            })

        return {
            'status': 'success',
            'checked_cases': len(results),
            'updated_cases': len([r for r in results if r['has_changes']]),
            'details': results
        }

    except Exception as exc:
        logger.error(f'Ошибка при массовой проверке дел: {str(exc)}')
        return {
            'status': 'error',
            'message': f'Ошибка при массовой проверке дел: {str(exc)}'
        }

