class SmsAdapter:
    def send(self, message: str, phone_number: str) -> None:
        print(f"Sending SMS to {phone_number}: {message}")
