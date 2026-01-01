import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import BigInteger, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, SQLModel

from app.enums import (
    ChallengeStatus,
    ChallengeType,
    EventStatus,
    MarketStatus,
    MarketType,
    OutcomeCode,
    ParticipationStatus,
    PayoutRule,
    SportType,
    TransactionType,
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# =====================
# DATABASE MODELS
# =====================


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    telegram_id: int = Field(unique=True, sa_type=BigInteger)

    username: str | None = Field(default=None, max_length=255)
    first_name: str = Field(max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    photo_url: str | None = Field(default=None, max_length=1024)

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sport: SportType = Field(sa_column=Column(Text, nullable=False))
    name: str = Field(max_length=255)
    starts_at: datetime

    status: EventStatus = Field(
        default=EventStatus.SCHEDULED,
        sa_column=Column(Text, nullable=False, server_default="SCHEDULED"),
    )

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Market(SQLModel, table=True):
    __tablename__ = "markets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event_id: uuid.UUID
    type: MarketType = Field(sa_column=Column(Text, nullable=False))
    params: dict | None = Field(default=None, sa_column=Column(JSONB))

    status: MarketStatus = Field(
        default=MarketStatus.OPEN,
        sa_column=Column(Text, nullable=False, server_default="OPEN"),
    )
    winning_outcome_id: uuid.UUID | None = Field(default=None)

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Outcome(SQLModel, table=True):
    __tablename__ = "outcomes"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    market_id: uuid.UUID
    code: OutcomeCode = Field(sa_column=Column(Text, nullable=False))

    odds: Decimal = Field(max_digits=6, decimal_places=3)

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Challenge(SQLModel, table=True):
    __tablename__ = "challenges"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    market_id: uuid.UUID
    type: ChallengeType = Field(sa_column=Column(Text, nullable=False))
    payout_rule: PayoutRule = Field(sa_column=Column(Text, nullable=False))
    fee: Decimal = Field(max_digits=6, decimal_places=3)
    max_participants: int
    min_bet: int | None = Field(default=None)
    max_bet: int | None = Field(default=None)

    status: ChallengeStatus = Field(
        default=ChallengeStatus.OPEN,
        sa_column=Column(Text, nullable=False, server_default="OPEN"),
    )

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Participation(SQLModel, table=True):
    __tablename__ = "participations"
    __table_args__ = (
        UniqueConstraint(
            "challenge_id", "user_id", name="participations_unique_user_per_challenge"
        ),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    challenge_id: uuid.UUID
    user_id: uuid.UUID
    outcome_id: uuid.UUID
    amount: int
    odds: Decimal = Field(max_digits=6, decimal_places=3)
    potential_payout: int

    status: ParticipationStatus = Field(
        default=ParticipationStatus.ACTIVE,
        sa_column=Column(Text, nullable=False, server_default="ACTIVE"),
    )

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    participation_id: uuid.UUID
    amount: int  # (+): we get money / (-): we give money
    type: TransactionType = Field(sa_column=Column(Text, nullable=False))

    created_at: datetime = Field(default_factory=utc_now)


# =====================
# PYDANTIC SCHEMAS (for API)
# =====================


class Message(SQLModel):
    message: str
