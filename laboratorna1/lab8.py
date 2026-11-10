
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any
import json


# ============================================================
# 1. КЛАС ВІДПОВІДІ REST API
# ============================================================

@dataclass
class APIResponse:
    code: int
    status: str
    data: dict | None = None


# ============================================================
# 2. АБСТРАКТНИЙ БАЗОВИЙ КЛАС
# ============================================================

class EntityUpdater(ABC):

    def __init__(self, entity_id, api_client):
        self.entity_id = entity_id
        self.api_client = api_client

    # Шаблонний метод: визначає загальний алгоритм оновлення
    def update(self, new_data: dict) -> APIResponse:

        entity = self.get_entity()

        if not self.validate_data(new_data, entity):
            self.on_validation_error(new_data)
            return self.create_response(400, "Validation Error")

        self.before_save(new_data)

        request = self.build_request(new_data, entity)

        result = self.save_entity(request)

        self.after_save(result)

        return self.create_response(
            result["code"],
            result["status"],
            result
        )

    # Отримання сутності
    @abstractmethod
    def get_entity(self) -> dict:
        pass

    # Базова валідація даних
    def validate_data(self, new_data: dict, entity: dict) -> bool:

        for field, value in new_data.items():

            if field not in entity:
                return False

            if not self.is_field_allowed(field):
                return False

        return self.validate_hook(new_data, entity)

    # Перевірка дозволених полів
    @abstractmethod
    def is_field_allowed(self, field: str) -> bool:
        pass

    # Формування запиту
    def build_request(self, new_data: dict, entity: dict) -> dict:

        updated_entity = entity.copy()
        updated_entity.update(new_data)

        return updated_entity

    # Збереження через REST API
    def save_entity(self, request: dict) -> dict:
        return self.api_client.put(
            self.entity_id,
            request
        )

    # Формування відповіді
    def create_response(
        self,
        code: int,
        status: str,
        result: dict | None = None
    ) -> APIResponse:

        return APIResponse(code, status)

    # ========================================================
    # ХУКИ — ДОДАТКОВІ ТОЧКИ РОЗШИРЕННЯ
    # ========================================================

    def validate_hook(self, new_data: dict, entity: dict) -> bool:
        return True

    def on_validation_error(self, new_data: dict) -> None:
        pass

    def before_save(self, new_data: dict) -> None:
        pass

    def after_save(self, result: dict) -> None:
        pass


# ============================================================
# 3. КЛАС ТОВАРУ
# ============================================================

class ProductUpdater(EntityUpdater):

    ALLOWED_FIELDS = {
        "name", "price", "description", "quantity"
    }

    def get_entity(self) -> dict:
        return self.api_client.get("products", self.entity_id)

    def is_field_allowed(self, field: str) -> bool:
        return field in self.ALLOWED_FIELDS

    # Хук: повідомлення адміністратора при помилці
    def on_validation_error(self, new_data: dict) -> None:
        self.api_client.notify_admin(
            "Помилка валідації товару",
            new_data
        )


# ============================================================
# 4. КЛАС КОРИСТУВАЧА
# ============================================================

class UserUpdater(EntityUpdater):

    ALLOWED_FIELDS = {
        "name", "email", "phone", "address"
    }

    def get_entity(self) -> dict:
        return self.api_client.get("users", self.entity_id)

    def is_field_allowed(self, field: str) -> bool:
        return field in self.ALLOWED_FIELDS

    # Хук: заборона зміни email
    def validate_hook(self, new_data: dict, entity: dict) -> bool:
        if "email" in new_data:
            return False

        return True


# ============================================================
# 5. КЛАС ЗАМОВЛЕННЯ
# ============================================================

class OrderUpdater(EntityUpdater):

    ALLOWED_FIELDS = {
        "status", "quantity", "total_price", "delivery_address"
    }

    def get_entity(self) -> dict:
        return self.api_client.get("orders", self.entity_id)

    def is_field_allowed(self, field: str) -> bool:
        return field in self.ALLOWED_FIELDS

    # Хук: додавання JSON-подання замовлення у відповідь
    def create_response(
        self,
        code: int,
        status: str,
        result: dict | None = None
    ) -> APIResponse:

        return APIResponse(
            code,
            status,
            result.get("entity") if result else None
        )

    # Формування запиту з додатковим JSON-поданням
    def build_request(self, new_data: dict, entity: dict) -> dict:

        updated_entity = super().build_request(new_data, entity)

        return {
            "entity": updated_entity
        }


# ============================================================
# 6. УМОВНИЙ REST API КЛІЄНТ
# ============================================================

class RESTClient:

    def __init__(self):
        self.database = {
            "products": {
                1: {
                    "name": "Laptop",
                    "price": 25000,
                    "description": "Gaming laptop",
                    "quantity": 5
                }
            },
            "users": {
                1: {
                    "name": "Valeria",
                    "email": "user@example.com",
                    "phone": "123456789",
                    "address": "Kharkiv"
                }
            },
            "orders": {
                1: {
                    "status": "New",
                    "quantity": 2,
                    "total_price": 50000,
                    "delivery_address": "Kharkiv"
                }
            }
        }

    def get(self, entity_type: str, entity_id: int) -> dict:
        return self.database[entity_type][entity_id].copy()

    def put(self, entity_id: int, data: dict) -> dict:
        # Визначення сутності за структурою запиту
        # У реальному API адреса ресурсу задається окремо.
        for entity_type, records in self.database.items():
            if entity_id in records:
                if entity_type == "orders":
                    records[entity_id] = data["entity"]
                    return {
                        "code": 200,
                        "status": "OK",
                        "entity": data["entity"]
                    }

                records[entity_id] = data
                return {
                    "code": 200,
                    "status": "OK"
                }

        return {
            "code": 404,
            "status": "Not Found"
        }

    def notify_admin(self, message: str, data: dict) -> None:
        print(f"Повідомлення адміністратору: {message}")
        print(f"Дані: {data}")


# ============================================================
# 7. ПЕРЕВІРКА РОБОТИ ПРОГРАМИ
# ============================================================

if __name__ == "__main__":

    api = RESTClient()

    # Оновлення товару
    product = ProductUpdater(1, api)
    product_response = product.update({
        "price": 27000
    })

    print("Товар:", product_response)

    # Оновлення користувача
    user = UserUpdater(1, api)
    user_response = user.update({
        "name": "New Name"
    })

    print("Користувач:", user_response)

    # Спроба змінити email
    email_response = user.update({
        "email": "new@example.com"
    })

    print("Зміна email:", email_response)

    # Оновлення замовлення
    order = OrderUpdater(1, api)
    order_response = order.update({
        "status": "Completed"
    })

    print("Замовлення:", order_response)

    print(
        "JSON замовлення:",
        json.dumps(order_response.data, ensure_ascii=False, indent=4)
    )
