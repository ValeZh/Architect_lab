
from abc import ABC, abstractmethod


# Целевой интерфейс — изменять его нельзя
class Notification(ABC):

    @abstractmethod
    def send(self, title: str, message: str) -> None:
        pass


# Система відправки Email-сповіщень
class EmailNotification(Notification):

    def __init__(self, admin_email: str):
        self.admin_email = admin_email

    def send(self, title: str, message: str) -> None:
        print(
            f"Email: '{title}' -> {self.admin_email}. "
            f"Повідомлення: '{message}'"
        )


# Сторонній клас для роботи зі Slack
class SlackService:

    def login(self, login: str, api_key: str) -> None:
        pass

    def send_message(self, chat_id: str, text: str) -> None:
        pass


# Адаптер для Slack
class SlackNotificationAdapter(Notification):

    def __init__(self, login: str, api_key: str, chat_id: str):
        self.slack = SlackService()
        self.slack.login(login, api_key)
        self.chat_id = chat_id

    def send(self, title: str, message: str) -> None:
        text = f"{title}: {message}"
        self.slack.send_message(self.chat_id, text)
        print(f"Slack: чат {self.chat_id}. Повідомлення: '{text}'")


# Сторонній клас для відправки SMS
class SMSService:

    def send_sms(self, phone: str, sender: str, text: str) -> None:
        pass


# Адаптер для SMS
class SMSNotificationAdapter(Notification):

    def __init__(self, phone: str, sender: str):
        self.sms = SMSService()
        self.phone = phone
        self.sender = sender

    def send(self, title: str, message: str) -> None:
        text = f"{title}: {message}"
        self.sms.send_sms(self.phone, self.sender, text)
        print(
            f"SMS: відправник {self.sender}, номер {self.phone}. "
            f"Повідомлення: '{text}'"
        )


# Клієнтський код
def send_notification(notification: Notification,
                      title: str,
                      message: str) -> None:
    notification.send(title, message)


if __name__ == "__main__":

    # Email
    email = EmailNotification("admin@example.com")
    send_notification(
        email,
        "Системне повідомлення",
        "Система працює нормально"
    )

    # Slack
    slack = SlackNotificationAdapter(
        login="my_login",
        api_key="my_api_key",
        chat_id="C12345678"
    )
    send_notification(
        slack,
        "Попередження",
        "Виявлено помилку в системі"
    )

    # SMS
    sms = SMSNotificationAdapter(
        phone="+380991234567",
        sender="MySystem"
    )
    send_notification(
        sms,
        "Сповіщення",
        "Ваш код підтвердження: 1234"
    )
