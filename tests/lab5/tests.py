import unittest
from src.lab5.main import *


class TestOrderProcessing(unittest.TestCase):
    def test_validate_order_valid(self):
        """
        Тестирование валидного заказа.
        """
        order = ['12345', 'Product1, Product2', 'John Doe', 'Country. Region. City. Street', '+1-123-456-78-90', 'MAX']
        is_valid, errors = validate_order(order)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])

    def test_validate_order_invalid_address(self):
        """
        Тестирование заказа с невалидным адресом.
        """
        order = ['12345', 'Product1, Product2', 'John Doe', '', '+1-123-456-78-90', 'MAX']
        is_valid, errors = validate_order(order)
        self.assertFalse(is_valid)
        self.assertEqual(errors, [('12345', '1', 'no data')])

    def test_validate_order_invalid_phone(self):
        """
        Тестирование заказа с пустым номером телефона.
        """
        order = ['12345', 'Product1, Product2', 'John Doe', 'Country. Region. City. Street', '', 'MAX']
        is_valid, errors = validate_order(order)
        self.assertFalse(is_valid)
        self.assertEqual(errors, [('12345', '2', 'no data')])

    def test_validate_order_invalid_phone_format(self):
        """
        Тестирование заказа с неверным форматом номера телефона.
        """
        order = ['12345', 'Product1, Product2', 'John Doe', 'Country. Region. City. Street', '+1-123-4567-890', 'MAX']
        is_valid, errors = validate_order(order)
        self.assertFalse(is_valid)
        self.assertEqual(errors, [('12345', '2', '+1-123-4567-890')])

    def test_validate_order_multiple_errors(self):
        """
        Тестирование заказа с несколькими ошибками.
        """
        order = ['12345', 'Product1, Product2', 'John Doe', '', '', 'MAX']
        is_valid, errors = validate_order(order)
        self.assertFalse(is_valid)
        self.assertEqual(errors, [('12345', '1', 'no data'), ('12345', '2', 'no data')])

    def test_process_orders(self):
        """
        Тестирование обработки заказов.
        """
        orders = [
            ['12345', 'Product1, Product2', 'John Doe', 'Country. Region. City. Street', '+1-123-456-78-90', 'MAX'],
            ['12346', 'Product3, Product4', 'Jane Smith', '', '+1-123-456-78-90', 'LOW']
        ]
        valid_orders, errors = process_orders(orders)
        self.assertEqual(len(valid_orders), 1)
        self.assertEqual(len(errors), 1)

    def test_sort_orders(self):
        """
        Тестирование сортировки заказов.
        """
        orders = [
            ['12345', '', '', 'CountryA. Region. City. Street', '', 'MAX'],
            ['12346', '', '', 'CountryB. Region. City. Street', '', 'LOW'],
            ['12347', '', '', 'CountryA. Region. City. Street', '', 'MIDDLE']
        ]
        sorted_orders = sort_orders(orders)
        self.assertEqual(sorted_orders[0][0], '12345')  # MAX приоритет в CountryA
        self.assertEqual(sorted_orders[1][0], '12347')  # MIDDLE приоритет в CountryA
        self.assertEqual(sorted_orders[2][0], '12346')  # LOW приоритет в CountryB

    def test_format_products(self):
        """
        Тестирование форматирования продуктов.
        """
        products = 'Apple, Banana, Apple, Orange, Banana, Banana'
        formatted = format_products(products)
        expected = 'Apple x2, Banana x3, Orange'
        self.assertEqual(formatted, expected)

    def test_format_address(self):
        """
        Тестирование форматирования адреса.
        """
        address = 'Country. Region. City. Street'
        formatted = format_address(address)
        expected = 'Region. City. Street'
        self.assertEqual(formatted, expected)

if __name__ == '__main__':
    unittest.main()
