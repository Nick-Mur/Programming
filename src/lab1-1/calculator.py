"""Модуль содержит класс Calculator для выполнения основных математических операций."""

from math import sqrt
from typing import Optional, Tuple, Union


class Calculator:
    """
    Калькулятор для выполнения основных арифметических операций и решения
    квадратных уравнений.
    """

    def add(self, num1: float, num2: float) -> float:
        """
        Возвращает сумму num1 и num2.

        Args:
            num1 (float): Первое слагаемое.
            num2 (float): Второе слагаемое.

        Returns:
            float: Сумма num1 и num2.
        """
        return num1 + num2

    def subtract(self, num1: float, num2: float) -> float:
        """
        Возвращает разность num1 и num2.

        Args:
            num1 (float): Уменьшаемое.
            num2 (float): Вычитаемое.

        Returns:
            float: Разность num1 и num2.
        """
        return num1 - num2

    def multiply(self, num1: float, num2: float) -> float:
        """
        Возвращает произведение num1 и num2.

        Args:
            num1 (float): Первый множитель.
            num2 (float): Второй множитель.

        Returns:
            float: Произведение num1 и num2.
        """
        return num1 * num2

    def divide(self, num1: float, num2: float) -> float:
        """
        Возвращает результат деления num1 на num2.

        Args:
            num1 (float): Делимое.
            num2 (float): Делитель.

        Raises:
            ZeroDivisionError: Если num2 равен нулю.

        Returns:
            float: Частное от деления num1 на num2.
        """
        if num2 == 0:
            raise ZeroDivisionError("Деление на ноль невозможно.")
        return num1 / num2

    def power(self, base: float, exponent: float) -> float:
        """
        Возводит число base в степень exponent.

        Args:
            base (float): Основание степени.
            exponent (float): Показатель степени.

        Returns:
            float: Результат возведения base в степень exponent.
        """
        return base ** exponent

    def solve_quadratic(
        self, coef_a: float, coef_b: float, coef_c: float
    ) -> Tuple[float, Optional[Union[float, Tuple[float, float]]]]:
        """
        Решает квадратное уравнение вида ax^2 + bx + c = 0.

        Args:
            coef_a (float): Коэффициент при x^2.
            coef_b (float): Коэффициент при x.
            coef_c (float): Свободный член.

        Returns:
            tuple: Кортеж из дискриминанта и корней уравнения.
        """
        discriminant = coef_b ** 2 - 4 * coef_a * coef_c
        if discriminant > 0:
            root1 = (-coef_b + sqrt(discriminant)) / (2 * coef_a)
            root2 = (-coef_b - sqrt(discriminant)) / (2 * coef_a)
            return discriminant, (root1, root2)
        if discriminant == 0:
            root = -coef_b / (2 * coef_a)
            return discriminant, root
        return discriminant, None
