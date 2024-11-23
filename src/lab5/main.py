import re
from typing import List, Tuple, Optional


class Order:
    def __init__(self, order_data: List[str]):
        """
        Инициализирует объект заказа на основе списка атрибутов.

        :param order_data: Список атрибутов заказа.
        """
        self.order_number = order_data[0]
        self.products = order_data[1]
        self.customer_name = order_data[2]
        self.address = order_data[3]
        self.phone_number = order_data[4]
        self.priority = order_data[5]

        self.errors: List[Tuple[str, str]] = []  # Список ошибок для данного заказа

    def validate(self) -> None:
        """
        Проверяет заказ на соответствие правилам и заполняет список ошибок.
        """
        # Проверка адреса доставки
        if not self.address or len(self.address.strip().split('. ')) != 4:
            error_value = self.address if self.address else "no data"
            self.errors.append(('1', error_value))

        # Проверка номера телефона
        if not self.phone_number:
            self.errors.append(('2', "no data"))
        else:
            pattern = r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$'
            if not re.match(pattern, self.phone_number):
                self.errors.append(('2', self.phone_number))

    def is_valid(self) -> bool:
        """
        Проверяет, является ли заказ валидным.

        :return: True, если заказ валиден, иначе False.
        """
        return len(self.errors) == 0

    def format_products(self) -> str:
        """
        Форматирует строку с продуктами.

        :return: Отформатированная строка продуктов.
        """
        product_list = [p.strip() for p in self.products.split(',')]
        product_count = {}
        for product in product_list:
            product_count[product] = product_count.get(product, 0) + 1

        formatted_products = []
        for product, count in product_count.items():
            if count > 1:
                formatted_products.append(f"{product} x{count}")
            else:
                formatted_products.append(product)
        return ', '.join(formatted_products)

    def format_address(self) -> str:
        """
        Форматирует строку с адресом.

        :return: Отформатированная строка адреса.
        """
        address_parts = self.address.split('. ')
        return '. '.join(address_parts[1:]) if len(address_parts) > 1 else self.address

    def get_country(self) -> str:
        """
        Извлекает страну из адреса.

        :return: Название страны.
        """
        address_parts = self.address.split('. ')
        return address_parts[0] if address_parts else ''

    def get_priority_value(self) -> int:
        """
        Возвращает числовое значение приоритета для сортировки.

        :return: Числовое значение приоритета.
        """
        priority_mapping = {'MAX': 1, 'MIDDLE': 2, 'LOW': 3}
        return priority_mapping.get(self.priority, 4)


class OrderProcessor:
    def __init__(self, orders_data: Optional[List[List[str]]] = None, input_file: Optional[str] = None):
        """
        Инициализирует объект для обработки заказов.

        :param orders_data: Список заказов, каждый из которых является списком атрибутов.
        :param input_file: Путь к файлу с заказами.
        """
        self.orders: List[Order] = []
        self.errors: List[Tuple[str, str, str]] = []

        if orders_data:
            self.orders = [Order(order_data) for order_data in orders_data]
        elif input_file:
            self.read_orders_from_file(input_file)
        else:
            raise ValueError("Необходимо предоставить либо orders_data, либо input_file")

    def read_orders_from_file(self, input_file: str) -> None:
        """
        Читает заказы из файла и создает объекты Order.

        :param input_file: Путь к файлу с заказами.
        """
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    order_data = line.strip().split(';')
                    order = Order(order_data)
                    self.orders.append(order)

    def validate_orders(self) -> None:
        """
        Проверяет все заказы и собирает ошибки.
        """
        for order in self.orders:
            order.validate()
            if not order.is_valid():
                for error_type, error_value in order.errors:
                    self.errors.append((order.order_number, error_type, error_value))

    def write_non_valid_orders(self, file_path: str) -> None:
        """
        Записывает невалидные заказы в файл.

        :param file_path: Путь к выходному файлу.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            for error in self.errors:
                file.write(f"{error[0]};{error[1]};{error[2]}\n")

    def get_valid_orders(self) -> List[Order]:
        """
        Возвращает список валидных заказов.

        :return: Список объектов Order.
        """
        return [order for order in self.orders if order.is_valid()]

    def sort_orders(self, orders: List[Order]) -> List[Order]:
        """
        Сортирует заказы по стране и приоритету доставки.

        :param orders: Список заказов для сортировки.
        :return: Отсортированный список заказов.
        """
        return sorted(orders, key=lambda o: (o.get_country(), o.get_priority_value()))

    def write_valid_orders(self, orders: List[Order], file_path: str) -> None:
        """
        Записывает валидные заказы в файл после форматирования.

        :param orders: Список валидных заказов.
        :param file_path: Путь к выходному файлу.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            for order in orders:
                formatted_products = order.format_products()
                formatted_address = order.format_address()
                file.write(f"{order.order_number};{formatted_products};{order.customer_name};"
                           f"{formatted_address};{order.phone_number};{order.priority}\n")

    def process(self, non_valid_orders_file: Optional[str] = None, valid_orders_file: Optional[str] = None) -> None:
        """
        Выполняет полный цикл обработки заказов.

        :param non_valid_orders_file: Путь к файлу для записи невалидных заказов.
        :param valid_orders_file: Путь к файлу для записи валидных заказов.
        """
        self.validate_orders()
        if non_valid_orders_file:
            self.write_non_valid_orders(non_valid_orders_file)
        valid_orders = self.get_valid_orders()
        sorted_orders = self.sort_orders(valid_orders)
        if valid_orders_file:
            self.write_valid_orders(sorted_orders, valid_orders_file)


def main() -> None:
    """
    Главная функция для запуска обработки заказов.
    """
    processor = OrderProcessor(input_file='txt_files/orders.txt')
    processor.process(non_valid_orders_file='txt_files/non_valid_orders.txt',
                      valid_orders_file='txt_files/order_country.txt')


if __name__ == "__main__":
    main()
