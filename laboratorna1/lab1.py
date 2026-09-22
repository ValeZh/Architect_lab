from abc import ABC, abstractmethod


# Интерфейс хранилища
class Storage(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def upload_file(self, file_path):
        pass

    @abstractmethod
    def download_file(self, file_name):
        pass

    @abstractmethod
    def delete_file(self, file_name):
        pass


# Локальное хранилище
class LocalStorage(Storage):

    def connect(self):
        print("Подключение к локальному хранилищу")

    def upload_file(self, file_path):
        print(f"Файл {file_path} загружен в локальное хранилище")

    def download_file(self, file_name):
        print(f"Файл {file_name} скачан из локального хранилища")

    def delete_file(self, file_name):
        print(f"Файл {file_name} удалён из локального хранилища")


# Amazon S3
class AmazonS3Storage(Storage):

    def connect(self):
        print("Подключение к Amazon S3")

    def upload_file(self, file_path):
        print(f"Файл {file_path} загружен в Amazon S3")

    def download_file(self, file_name):
        print(f"Файл {file_name} скачан из Amazon S3")

    def delete_file(self, file_name):
        print(f"Файл {file_name} удалён из Amazon S3")


# Одинак — менеджер файлов
class FileManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
            cls._instance.storage = None
        return cls._instance

    def set_storage(self, storage: Storage):
        self.storage = storage

    def get_storage(self) -> Storage:
        return self.storage

    def upload_file(self, file_path):
        self.storage.upload_file(file_path)

    def download_file(self, file_name):
        self.storage.download_file(file_name)

    def delete_file(self, file_name):
        self.storage.delete_file(file_name)


# Пользователь
class User:

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.storage = None

    def set_storage(self, storage: Storage):
        self.storage = storage

    def get_storage(self) -> Storage:
        return self.storage



# Пример использования

# Создаём двух пользователей
user1 = User(1, "Алиса")
user2 = User(2, "Боб")

# Создаём хранилища
local_storage = LocalStorage()
amazon_storage = AmazonS3Storage()

# Каждый пользователь выбирает своё хранилище
user1.set_storage(local_storage)
user2.set_storage(amazon_storage)

# Создаём менеджеры файлов
manager1 = FileManager()
manager2 = FileManager()

# Проверяем Singleton
print("manager1 и manager2 — один объект:", manager1 is manager2)

# Алиса использует локальное хранилище
manager1.set_storage(user1.get_storage())

print("\n--- Работа Алисы ---")
manager1.get_storage().connect()
manager1.upload_file("document.txt")
manager1.download_file("document.txt")
manager1.delete_file("document.txt")

# Боб использует Amazon S3
manager2.set_storage(user2.get_storage())

print("\n--- Работа Боба ---")
manager2.get_storage().connect()
manager2.upload_file("photo.jpg")
manager2.download_file("photo.jpg")
manager2.delete_file("photo.jpg")