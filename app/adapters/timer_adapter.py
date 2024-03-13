TIMEOUT = 15 * 60 * 1000  # 15 minutes in milliseconds


class TimerAdapter:
    def send_task(self,alert_id: str) -> None:
        payload = {
            'alert_id': alert_id,
            'callback_url': 'fakeserver/callback'
        }
        print(f'Sending task with payload {payload} to timer service with timeout {TIMEOUT}')
        pass
