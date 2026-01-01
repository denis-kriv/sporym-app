from enum import Enum


class SportType(str, Enum):
    FOOTBALL = "FOOTBALL"


class EventStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    LIVE = "LIVE"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"
    POSTPONED = "POSTPONED"


class MarketType(str, Enum):
    MATCH_RESULT = "MATCH_RESULT"


class MarketStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class OutcomeCode(str, Enum):
    W1 = "W1"
    W2 = "W2"
    X = "X"


class ChallengeType(str, Enum):
    PVP = "PVP"


class PayoutRule(str, Enum):
    PVP_FIXED = "PVP_FIXED"
    PVP_PERCENT = "PVP_PERCENT"


class ChallengeStatus(str, Enum):
    OPEN = "OPEN"
    LOCKED = "LOCKED"
    WAIT_SETTLING = "WAIT_SETTLING"
    SETTLED = "SETTLED"
    CANCELED = "CANCELED"


class ParticipationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    WON = "WON"
    LOST = "LOST"
    REFUNDED = "REFUNDED"


class TransactionType(str, Enum):
    BET = "BET"
    WIN = "WIN"
    REFUND = "REFUND"
    FEE = "FEE"
