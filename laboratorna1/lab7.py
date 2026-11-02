
from abc import ABC, abstractmethod


# --------------------------------------------------
# Strategy interface
# --------------------------------------------------

class DeliveryStrategy(ABC):
    """Base interface for all delivery strategies."""

    @abstractmethod
    def calculate_cost(self, order_amount: float, distance: float) -> float:
        """
        Calculate delivery cost.

        Parameters:
            order_amount: Total price of the order.
            distance: Delivery distance in kilometers.

        Returns:
            Delivery cost.
        """
        pass


# --------------------------------------------------
# Concrete Strategy 1: Pickup
# --------------------------------------------------

class PickupStrategy(DeliveryStrategy):
    """Customer picks up the order personally."""

    def calculate_cost(self, order_amount: float, distance: float) -> float:
        return 0.0


# --------------------------------------------------
# Concrete Strategy 2: External delivery service
# --------------------------------------------------

class ExternalDeliveryStrategy(DeliveryStrategy):
    """Delivery is performed by an external company."""

    def calculate_cost(self, order_amount: float, distance: float) -> float:
        return 50.0 + distance * 15.0


# --------------------------------------------------
# Concrete Strategy 3: Own delivery service
# --------------------------------------------------

class OwnDeliveryStrategy(DeliveryStrategy):
    """Delivery is performed by the restaurant's own couriers."""

    def calculate_cost(self, order_amount: float, distance: float) -> float:
        return 30.0 + distance * 10.0


# --------------------------------------------------
# Context
# --------------------------------------------------

class FoodDelivery:
    """Food delivery application that uses a delivery strategy."""

    def __init__(self, strategy: DeliveryStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DeliveryStrategy) -> None:
        """Change the current delivery strategy."""
        self._strategy = strategy

    def calculate_delivery_cost(
        self, order_amount: float, distance: float
    ) -> float:
        """Calculate cost using the selected strategy."""
        return self._strategy.calculate_cost(order_amount, distance)


# --------------------------------------------------
# Main program
# --------------------------------------------------

def main():
    order_amount = 500.0
    distance = 5.0

    strategies = {
        "1": ("Pickup", PickupStrategy()),
        "2": ("External delivery", ExternalDeliveryStrategy()),
        "3": ("Own delivery", OwnDeliveryStrategy())
    }

    print("=== FOOD DELIVERY APPLICATION ===")
    print(f"Order amount: {order_amount:.2f} UAH")
    print(f"Delivery distance: {distance:.1f} km")

    print("\nChoose delivery method:")
    print("1. Pickup")
    print("2. External delivery service")
    print("3. Own delivery service")

    choice = input("\nYour choice: ")

    if choice not in strategies:
        print("Invalid choice!")
        return

    name, strategy = strategies[choice]

    app = FoodDelivery(strategy)
    cost = app.calculate_delivery_cost(order_amount, distance)

    print("\n=== DELIVERY INFORMATION ===")
    print(f"Selected method: {name}")
    print(f"Delivery cost: {cost:.2f} UAH")
    print(f"Total amount: {order_amount + cost:.2f} UAH")


if __name__ == "__main__":
    main()
