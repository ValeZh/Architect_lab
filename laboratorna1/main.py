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
        pass

    def upload_file(self, file_path):
        pass

    def download_file(self, file_name):
        pass

    def delete_file(self, file_name):
        pass


# Amazon S3
class AmazonS3Storage(Storage):

    def connect(self):
        pass

    def upload_file(self, file_path):
        pass

    def download_file(self, file_name):
        pass

    def delete_file(self, file_name):
        pass


# Одинак — менеджер файлов
class FileManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
            cls._instance.storage = None
        return cls._instance

    def set_storage(self, storage: Storage):
        pass

    def get_storage(self) -> Storage:
        pass

    def upload_file(self, file_path):
        pass

    def download_file(self, file_name):
        pass

    def delete_file(self, file_name):
        pass


# Пользователь
class User:

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.storage = None

    def set_storage(self, storage: Storage):
        pass

    def get_storage(self) -> Storage:
        pass