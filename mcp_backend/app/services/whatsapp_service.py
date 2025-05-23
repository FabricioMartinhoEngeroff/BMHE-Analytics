from twilio.rest import Client

class WhatsAppService:
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send_welcome_message(self, to_number: str, user_name: str):
        message_body = f"Olá {user_name}, seja bem-vindo ao BMHE Analytics! 👋🚀"
        self.client.messages.create(
            body=message_body,
            from_=self.from_number,
            to=f"whatsapp:{to_number}"
        )
