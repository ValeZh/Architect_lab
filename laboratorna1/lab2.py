# Абстрактный продукт
class SocialNetwork:
    def connect(self):
        pass

    def publish(self, message):
        pass


class Facebook(SocialNetwork):
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def connect(self):
        print(f"Выполнено подключение к Facebook как {self.login}")

    def publish(self, message):
        print(f"Facebook: опубликовано сообщение: {message}")


class LinkedIn(SocialNetwork):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def connect(self):
        print(f"Выполнено подключение к LinkedIn как {self.email}")

    def publish(self, message):
        print(f"LinkedIn: опубликовано сообщение: {message}")
# Абстрактная фабрика
class SocialNetworkFactory:
    def create_network(self):
        pass


# Фабрика Facebook
class FacebookFactory(SocialNetworkFactory):
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def create_network(self):
        return Facebook(self.login, self.password)


# Фабрика LinkedIn
class LinkedInFactory(SocialNetworkFactory):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def create_network(self):
        return LinkedIn(self.email, self.password)

# Facebook
facebook_factory = FacebookFactory(
    "my_login",
    "my_password"
)

facebook = facebook_factory.create_network()

facebook.connect()
facebook.publish("Привет! Это мое сообщение в Facebook.")


print()


# LinkedIn
linkedin_factory = LinkedInFactory(
    "my_email@example.com",
    "my_password"
)

linkedin = linkedin_factory.create_network()

linkedin.connect()
linkedin.publish("Привет! Это мое сообщение в LinkedIn.")