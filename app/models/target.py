from dataclasses import dataclass
from app.adapters.messaging_adapters import SmsAdapter, SlackAdapter, EmailAdapter


@dataclass
class Target:
    target_id: str
    name: str


@dataclass
class TargetSlack(Target):
    slack_id: str
    channel_id: str
    adapter: SlackAdapter = SlackAdapter()

    def __dict__(self):
        return {
            'slack_id': self.slack_id,
            'channel_id': self.channel_id
        }


@dataclass
class TargetEmail(Target):
    email: str
    adapter: EmailAdapter = EmailAdapter()

    def __dict__(self):
        return {
            'email': self.email
        }


@dataclass
class TargetSms(Target):
    phone_number: str
    adapter: SmsAdapter = SmsAdapter()

    def __dict__(self):
        return {
            'phone_number': self.phone_number
        }
