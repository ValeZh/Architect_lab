
from abc import ABC, abstractmethod


# ============================================================
# 1. ІНТЕРФЕЙС ВІДВІДУВАЧА
# ============================================================

class Visitor(ABC):

    @abstractmethod
    def visit_company(self, company):
        pass

    @abstractmethod
    def visit_department(self, department):
        pass

    @abstractmethod
    def visit_employee(self, employee):
        pass


# ============================================================
# 2. КЛАС СПІВРОБІТНИКА
# ============================================================

class Employee:

    def __init__(self, position: str, salary: float):
        self.position = position
        self.salary = salary

    def accept(self, visitor: Visitor):
        return visitor.visit_employee(self)


# ============================================================
# 3. КЛАС ДЕПАРТАМЕНТУ
# ============================================================

class Department:

    def __init__(self, name: str, employees: list):
        self.name = name
        self.employees = employees

    def accept(self, visitor: Visitor):
        return visitor.visit_department(self)


# ============================================================
# 4. КЛАС КОМПАНІЇ
# ============================================================

class Company:

    def __init__(self, name: str, departments: list):
        self.name = name
        self.departments = departments

    def accept(self, visitor: Visitor):
        return visitor.visit_company(self)


# ============================================================
# 5. ВІДВІДУВАЧ ДЛЯ ФОРМУВАННЯ ЗАРПЛАТНОЇ ВІДОМОСТІ
# ============================================================

class SalaryReportVisitor(Visitor):

    def __init__(self):
        self.report = []

    def visit_company(self, company: Company):

        self.report = []

        for department in company.departments:
            department.accept(self)

        return self.report

    def visit_department(self, department: Department):

        for employee in department.employees:
            employee.accept(self)

        return self.report

    def visit_employee(self, employee: Employee):

        self.report.append({
            "position": employee.position,
            "salary": employee.salary
        })

        return self.report

    # Формування текстового звіту
    def generate_report(self, title: str):

        print("\n================================")
        print("ЗАРПЛАТНА ВІДОМІСТЬ")
        print(title)
        print("================================")

        total = 0

        for employee in self.report:

            print(
                f"Посада: {employee['position']} | "
                f"Зарплата: {employee['salary']} грн"
            )

            total += employee["salary"]

        print("--------------------------------")
        print(f"Загальна сума: {total} грн")
        print(f"Кількість співробітників: {len(self.report)}")
        print("================================")


# ============================================================
# 6. КЛІЄНТСЬКИЙ КОД
# ============================================================

if __name__ == "__main__":

    # Створення співробітників
    employees_it = [
        Employee("Програміст", 40000),
        Employee("Тестувальник", 30000),
        Employee("Системний адміністратор", 28000)
    ]

    employees_hr = [
        Employee("HR-менеджер", 25000),
        Employee("Рекрутер", 22000)
    ]

    employees_finance = [
        Employee("Бухгалтер", 27000),
        Employee("Фінансовий аналітик", 35000)
    ]

    # Створення департаментів
    it_department = Department("IT", employees_it)
    hr_department = Department("HR", employees_hr)
    finance_department = Department("Фінансовий", employees_finance)

    # Створення компанії
    company = Company(
        "Tech Company",
        [
            it_department,
            hr_department,
            finance_department
        ]
    )

    # Створення відвідувача
    visitor = SalaryReportVisitor()

    # Отримання зарплатної відомості всієї компанії
    company.accept(visitor)

    visitor.generate_report("Компанія Tech Company")

    # Отримання зарплатної відомості окремого департаменту
    visitor.report = []

    it_department.accept(visitor)

    visitor.generate_report("Департамент IT")
