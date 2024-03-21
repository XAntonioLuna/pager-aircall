from typing import Optional

from app.models.escalation_policy import EscalationPolicy
from app.models.levels import Level
from app.models.target import TargetSlack, TargetEmail, TargetSms


MOCK_ESCALATION_POLICIES = {
    'ep1': EscalationPolicy(
            escalation_id='ep1',
            name='Escalation Policy 1',
            levels=[
                Level(
                    level_id='lev1',
                    name='Level 1',
                    targets=[
                        TargetSms(
                            target_id='targ1',
                            name='Oncall eng',
                            phone_number='+1234567890',
                        ),
                        TargetEmail(
                            target_id='targ2',
                            name='Secondary oncall',
                            email='test@testwlio.com'
                        )
                    ]
                ),
                Level(
                    level_id='lev2',
                    name='Level 2',
                    targets=[
                        TargetSlack(
                            target_id='targ21',
                            name='Engineering manager',
                            slack_id='@manager',
                            channel_id='engineering'
                        ),
                    ]
                )
            ]
        )
}


class EscalationPolicyAdapter:
    def __init__(self, response: Optional[dict] = MOCK_ESCALATION_POLICIES):
        self.response = response

    def get(self, escalation_policy_id) -> Optional[EscalationPolicy]:
        return self.response.get(escalation_policy_id, None)
