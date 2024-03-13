class EmailAdapter:
    def send(self, email: str, subject: str, body: str) -> None:
        print(f"Sending email to {email} with subject {subject} and body {body}")
