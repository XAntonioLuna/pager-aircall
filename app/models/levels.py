from dataclasses import dataclass
from typing import List, Union

from app.models.target import TargetSms, TargetEmail, TargetSlack


@dataclass
class Level:
    level_id: str
    name: str
    targets: List[Union[TargetSms, TargetEmail, TargetSlack]]
