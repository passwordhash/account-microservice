from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Account:
    uuid: str
    email: str
    hashed_password: str
    is_verified: Optional[bool] = None
    created_at: Optional[datetime] = None


@dataclass
class AccountCreate:
    email: str
    password: str


@dataclass
class JWTTokenPayload:
    uuid: str