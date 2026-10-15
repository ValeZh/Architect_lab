
from abc import ABC, abstractmethod
from dataclasses import dataclass


# Клас Product — информация о товаре
@dataclass
class Product:
    id: int
    name: str
    description: str
    image: str


# Интерфейс рендерера
class Renderer(ABC):

    @abstractmethod
    def render(self, title: str, content: str) -> str:
        pass


# HTML-рендерер
class HTMLRenderer(Renderer):

    def render(self, title: str, content: str) -> str:
        pass


# JSON-рендерер
class JsonRenderer(Renderer):

    def render(self, title: str, content: str) -> str:
        pass


# XML-рендерер
class XmlRenderer(Renderer):

    def render(self, title: str, content: str) -> str:
        pass


# Базовый класс Page
class Page(ABC):

    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    @abstractmethod
    def render(self) -> str:
        pass


# Простая страница
class SimplePage(Page):

    def __init__(self, title: str, content: str, renderer: Renderer):
        super().__init__(renderer)
        self.title = title
        self.content = content

    def render(self) -> str:
        return self.renderer.render(self.title, self.content)


# Страница товара
class ProductPage(Page):

    def __init__(self, product: Product, renderer: Renderer):
        super().__init__(renderer)
        self.product = product

    def render(self) -> str:
        content = (
            f"ID: {self.product.id}; "
            f"Название: {self.product.name}; "
            f"Описание: {self.product.description}; "
            f"Изображение: {self.product.image}"
        )
        return self.renderer.render(self.product.name, content)


# Клиентский код
if __name__ == "__main__":

    product = Product(
        id=101,
        name="Ноутбук",
        description="Ноутбук для работы и учебы",
        image="laptop.jpg"
    )

    renderers = [
        HTMLRenderer(),
        JsonRenderer(),
        XmlRenderer()
    ]

    for renderer in renderers:
        print(f"\n--- {renderer.__class__.__name__} ---")

        simple_page = SimplePage(
            title="Главная страница",
            content="Добро пожаловать на сайт!",
            renderer=renderer
        )
        print(simple_page.render())

        product_page = ProductPage(
            product=product,
            renderer=renderer
        )
        print(product_page.render())
