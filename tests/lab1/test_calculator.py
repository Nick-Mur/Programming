"""Модуль содержит юнит-тесты для класса Calculator."""

import unittest

from src.lab1.calculator import Calculator


class CalculatorTestCase(unittest.TestCase):
    """Тестовый класс для проверки методов Calculator."""

    def setUp(self):
        """Настройка тестового окружения."""
        self.calc = Calculator()

    def test_add_numbers(self):
        """Тестирование метода add."""
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract_numbers(self):
        """Тестирование метода subtract."""
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_multiply_numbers(self):
        """Тестирование метода multiply."""
        self.assertEqual(self.calc.multiply(2, 3), 6)

    def test_divide_numbers(self):
        """Тестирование метода divide."""
        self.assertEqual(self.calc.divide(6, 3), 2)

    def test_divide_by_zero(self):
        """Тестирование метода divide при делении на ноль."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(5, 0)

    def test_power(self):
        """Тестирование метода power."""
        self.assertEqual(self.calc.power(2, 3), 8)

    def test_solve_quadratic_two_roots(self):
        """Тестирование метода solve_quadratic с двумя корнями."""
        discriminant, roots = self.calc.solve_quadratic(1, -3, 2)
        self.assertEqual(discriminant, 1.0)
        self.assertEqual(roots, (2.0, 1.0))

    def test_solve_quadratic_one_root(self):
        """Тестирование метода solve_quadratic с одним корнем."""
        discriminant, root = self.calc.solve_quadratic(1, -2, 1)
        self.assertEqual(discriminant, 0.0)
        self.assertEqual(root, 1.0)

    def test_solve_quadratic_no_real_roots(self):
        """Тестирование метода solve_quadratic без действительных корней."""
        discriminant, roots = self.calc.solve_quadratic(1, 0, 1)
        self.assertEqual(discriminant, -4.0)
        self.assertIsNone(roots)


if __name__ == '__main__':
    unittest.main()
