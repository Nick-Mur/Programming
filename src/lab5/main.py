import re
from typing import List, Tuple

def read_orders(file_path: str) -> List[List[str]]:
    """
    Читает заказы из указанного файла.

    :param file_path: Путь к файлу с заказами.
    :return: Список заказов, каждый из которых является списком атрибутов.
    """
    orders = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                orders.append(line.strip().split(';'))
    return orders

def validate_order(order: List[str]) -> Tuple[bool, List[Tuple[str, str, str]]]:
    """
    Проверяет заказ на соответствие правилам.

    :param order: Список атрибутов заказа.
    :return: Кортеж, содержащий флаг валидности и список ошибок.
    """
    errors = []
    order_number, _, _, address, phone_number, _ = order

    # Проверка адреса доставки
    if not address or len(address.strip().split('. ')) != 4:
        error_value = address if address else "no data"
        errors.append((order_number, '1', error_value))

    # Проверка номера телефона
    if not phone_number:
        errors.append((order_number, '2', "no data"))
    else:
        pattern = r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, phone_number):
            errors.append((order_number, '2', phone_number))

    return len(errors) == 0, errors


def process_orders(orders: List[List[str]]) -> Tuple[List[List[str]], List[Tuple[str, str, str]]]:
    """
    Обрабатывает и проверяет все заказы.

    :param orders: Список заказов.
    :return: Кортеж, содержащий список валидных заказов и список ошибок.
    """
    valid_orders = []
    error_list = []

    for order in orders:
        is_valid, errors = validate_order(order)
        if is_valid:
            valid_orders.append(order)
        else:
            error_list.extend(errors)

    return valid_orders, error_list

def write_non_valid_orders(errors: List[Tuple[str, str, str]], file_path: str) -> None:
    """
    Записывает невалидные заказы в файл.

    :param errors: Список ошибок.
    :param file_path: Путь к выходному файлу.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for error in errors:
            file.write(f"{error[0]};{error[1]};{error[2]}\n")

def sort_orders(orders: List[List[str]]) -> List[List[str]]:
    """
    Сортирует заказы по стране и приоритету доставки.

    :param orders: Список валидных заказов.
    :return: Отсортированный список заказов.
    """
    priority_mapping = {'MAX': 1, 'MIDDLE': 2, 'LOW': 3}

    def sort_key(order: List[str]) -> Tuple[str, int]:
        address_parts = order[3].split('. ')
        country = address_parts[0] if address_parts else ''
        priority = priority_mapping.get(order[5], 4)
        return country, priority

    return sorted(orders, key=sort_key)

def format_products(products: str) -> str:
    """
    Форматирует строку с продуктами.

    :param products: Исходная строка продуктов.
    :return: Отформатированная строка продуктов.
    """
    product_list = [p.strip() for p in products.split(',')]
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

def format_address(address: str) -> str:
    """
    Форматирует строку с адресом.

    :param address: Исходная строка адреса.
    :return: Отформатированная строка адреса.
    """
    address_parts = address.split('. ')
    return '. '.join(address_parts[1:])

def write_valid_orders(orders: List[List[str]], file_path: str) -> None:
    """
    Записывает валидные заказы в файл после форматирования.

    :param orders: Список валидных заказов.
    :param file_path: Путь к выходному файлу.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for order in orders:
            order_number, products, customer_name, address, phone_number, priority = order
            formatted_products = format_products(products)
            formatted_address = format_address(address)
            file.write(f"{order_number};{formatted_products};{customer_name};"
                       f"{formatted_address};{phone_number};{priority}\n")

def main() -> None:
    """
    Главная функция для обработки заказов.
    """
    orders = read_orders('txt_files/orders.txt')
    valid_orders, errors = process_orders(orders)
    write_non_valid_orders(errors, 'txt_files/non_valid_orders.txt')
    sorted_orders = sort_orders(valid_orders)
    write_valid_orders(sorted_orders, 'txt_files/order_country.txt')

if __name__ == "__main__":
    main()
