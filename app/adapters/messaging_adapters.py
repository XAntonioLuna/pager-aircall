class MessagingAdapter:
    def send(self, message: str, *args, **kwargs) -> None:
        raise NotImplementedError("send() must be implemented in a subclass")


class SlackAdapter(MessagingAdapter):
    def send(self, message: str, *args, **kwargs) -> None:
        slack_id = kwargs.get('slack_id')
        channel_id = kwargs.get('channel_id')
        print(f'Sending slack message to {slack_id} in channel {channel_id}. Message: {message}')


class SmsAdapter(MessagingAdapter):
    def send(self, message: str, *args, **kwargs) -> None:
        phone_number = kwargs.get('phone_number')
        print(f"Sending SMS to {phone_number}. Message:  {message}")


class EmailAdapter(MessagingAdapter):
    def send(self, message: str, *args, **kwargs) -> None:
        subject = 'Alert!'
        email = kwargs.get('email')
        print(f"Sending email to {email} with subject {subject}. Message: {message}")
