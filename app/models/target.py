from dataclasses import dataclass
from enum import Enum


class TargetType(Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"


@dataclass
class Target:
    target_id: str
    name: str
    type: TargetType
    contact_info: str
