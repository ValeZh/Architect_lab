from abc import ABC, abstractmethod


# Общий интерфейс строителя
class QueryBuilder(ABC):

    @abstractmethod
    def select(self, columns):
        pass

    @abstractmethod
    def where(self, condition):
        pass

    @abstractmethod
    def limit(self, value):
        pass

    @abstractmethod
    def getSQL(self):
        pass


# Строитель для PostgreSQL
class PostgreSQLQueryBuilder(QueryBuilder):

    def select(self, columns):
        pass

    def where(self, condition):
        pass

    def limit(self, value):
        pass

    def getSQL(self):
        pass


# Строитель для MySQL
class MySQLQueryBuilder(QueryBuilder):

    def select(self, columns):
        pass

    def where(self, condition):
        pass

    def limit(self, value):
        pass

    def getSQL(self):
        pass


# Клиентский код
def create_query(builder):
    builder.select(["id", "name"])
    builder.where("age > 18")
    builder.limit(10)

    return builder.getSQL()


# Использование PostgreSQL
postgres_builder = PostgreSQLQueryBuilder()
postgres_query = create_query(postgres_builder)

print("PostgreSQL:")
print(postgres_query)


# Использование MySQL
mysql_builder = MySQLQueryBuilder()
mysql_query = create_query(mysql_builder)

print("MySQL:")
print(mysql_query)