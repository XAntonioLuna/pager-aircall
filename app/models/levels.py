from dataclasses import dataclass
from typing import List

from app.models.target import Target


@dataclass
class Level:
    level_id: str
    name: str
    targets: List[Target]
