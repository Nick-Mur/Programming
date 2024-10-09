import unittest
from src.lab1.calculator import Calculator


class CalculatorTestCase(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_numbers(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract_numbers(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_multiply_numbers(self):
        self.assertEqual(self.calc.multiply(2, 3), 6)

    def test_divide_numbers(self):
        self.assertEqual(self.calc.divide(6, 3), 2)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(5, 0)

    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8)

    def test_solve_quadratic_two_roots(self):
        roots = self.calc.solve_quadratic(1, -3, 2)
        self.assertEqual(roots, (1.0, (2.0, 1.0)))

    def test_solve_quadratic_one_root(self):
        root = self.calc.solve_quadratic(1, -2, 1)
        self.assertEqual(root, (0.0, 1.0))

    def test_solve_quadratic_no_real_roots(self):
        roots = self.calc.solve_quadratic(1, 0, 1)
        self.assertEqual(roots, (-4.0, None))

if __name__ == '__main__':
    unittest.main()
