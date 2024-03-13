from typing import Optional

from app.models.escalation_policy import EscalationPolicy
from app.models.levels import Level
from app.models.target import Target, TargetType


MOCK_ESCALATION_POLICIES = {
    'ep1': EscalationPolicy(
            escalation_id='ep1',
            name='Escalation Policy 1',
            levels=[
                Level(
                    level_id='lev1',
                    name='Level 1',
                    targets=[
                        Target(
                            target_id='targ1',
                            name='Oncall eng',
                            type=TargetType.SMS,
                            contact_info='lunagantonio@aircall.com'
                        ),
                        Target(
                            target_id='targ2',
                            name='Secondary oncall',
                            type=TargetType.EMAIL,
                            contact_info='robert@aircall.com'
                        )
                    ]
                ),
                Level(
                    level_id='lev2',
                    name='Level 2',
                    targets=[
                        Target(
                            target_id='targ21',
                            name='Engineering manager',
                            type=TargetType.SMS,
                            contact_info='alan@aircall.com'
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
