
from abc import ABC, abstractmethod


# Интерфейс загрузчика
class Downloader(ABC):

    @abstractmethod
    def download(self, url: str) -> bytes:
        pass


# Реальный загрузчик
class SimpleDownloader(Downloader):

    def download(self, url: str) -> bytes:
        pass


# Заместитель с механизмом кеширования
class CachedDownloader(Downloader):

    def __init__(self, downloader: Downloader):
        self.downloader = downloader
        self.cache: dict[str, bytes] = {}

    def download(self, url: str) -> bytes:
        if url not in self.cache:
            self.cache[url] = self.downloader.download(url)

        return self.cache[url]


# Клиентский код
if __name__ == "__main__":

    simple_downloader = SimpleDownloader()

    # Оборачиваем загрузчик в заместитель
    downloader = CachedDownloader(simple_downloader)

    # Первый вызов — данные загружаются
    data1 = downloader.download("https://example.com/file1")

    # Второй вызов — данные берутся из кеша
    data2 = downloader.download("https://example.com/file1")

    # Другой URL — отдельная загрузка
    data3 = downloader.download("https://example.com/file2")
