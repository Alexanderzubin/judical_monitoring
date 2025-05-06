from typing import TypedDict
from app.database.repositories.user import UserRepository
from app.database.repositories.case import CaseRepository
from app.database.repositories.subscription import SubscriptionRepository
from app.database.repositories.judge import JudgeRepository
from app.database.repositories.court import Courtepository
from app.database.repositories.category import CategoryRepository

class Repos(TypedDict):
	user: UserRepository
	case: CaseRepository
	subscription: SubscriptionRepository
	judge: JudgeRepository
	court: Courtepository
	category: CategoryRepository

