from dataclasses import dataclass


@dataclass
class Notification:
    notification_id: str
    alert_id: str
    level_id: str
    sent_at: int
