"""Основной модуль для запуска калькулятора."""

from lab1.calculator import Calculator


def input_number(prompt: str) -> float:
    """Запрашивает у пользователя число с обработкой исключений.

    Args:
        prompt (str): Текст запроса для ввода.

    Returns:
        float: Введенное пользователем число.
    """
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Пожалуйста, введите корректное число.")


def input_operation() -> str:
    """Запрашивает у пользователя выбор операции.

    Returns:
        str: Номер выбранной операции.
    """
    while True:
        choice = input("Введите номер операции: ")
        if choice in map(str, range(1, 8)):
            return choice
        print("Неверный выбор, попробуйте снова.")


def perform_addition(calc: Calculator) -> None:
    """Выполняет операцию сложения."""
    num1 = input_number("Введите первое число: ")
    num2 = input_number("Введите второе число: ")
    result = calc.add(num1, num2)
    print(f"\nРезультат: {result}")


def perform_subtraction(calc: Calculator) -> None:
    """Выполняет операцию вычитания."""
    minuend = input_number("Введите уменьшаемое: ")
    subtrahend = input_number("Введите вычитаемое: ")
    result = calc.subtract(minuend, subtrahend)
    print(f"\nРезультат: {result}")


def perform_multiplication(calc: Calculator) -> None:
    """Выполняет операцию умножения."""
    factor1 = input_number("Введите первый множитель: ")
    factor2 = input_number("Введите второй множитель: ")
    result = calc.multiply(factor1, factor2)
    print(f"\nРезультат: {result}")


def perform_division(calc: Calculator) -> None:
    """Выполняет операцию деления."""
    dividend = input_number("Введите делимое: ")
    divisor = input_number("Введите делитель: ")
    if divisor == 0:
        print("\nДеление на ноль невозможно. Попробуйте снова.")
    else:
        result = calc.divide(dividend, divisor)
        print(f"\nРезультат: {result}")


def perform_power(calc: Calculator) -> None:
    """Выполняет возведение в степень."""
    base = input_number("Введите основание: ")
    exponent = input_number("Введите показатель степени: ")
    result = calc.power(base, exponent)
    print(f"\nРезультат: {result}")


def perform_quadratic_solution(calc: Calculator) -> None:
    """Решает квадратное уравнение."""
    print("Форма уравнения: ax^2 + bx + c = 0")
    coef_a = input_number("Введите a: ")
    if coef_a == 0:
        print("Коэффициент 'a' не может быть нулём в квадратном уравнении.")
        return
    coef_b = input_number("Введите b: ")
    coef_c = input_number("Введите c: ")
    discriminant, roots = calc.solve_quadratic(coef_a, coef_b, coef_c)
    print(f"\nДискриминант: {discriminant}")
    if roots is None:
        print("Действительных корней нет.")
    elif isinstance(roots, tuple):
        print(f"Корни уравнения: x1 = {roots[0]}, x2 = {roots[1]}")
    else:
        print(f"Корень уравнения: x = {roots}")


def main() -> None:
    """Основная функция программы, реализующая интерфейс калькулятора."""
    calc = Calculator()
    print("Добро пожаловать в Калькулятор!")
    while True:
        print(
            "\nВыберите операцию:\n"
            "1. Сложение чисел\n"
            "2. Вычитание чисел\n"
            "3. Умножение чисел\n"
            "4. Деление чисел\n"
            "5. Возведение в степень\n"
            "6. Решение квадратного уравнения\n"
            "7. Выход"
        )

        choice = input_operation()

        if choice == '1':
            perform_addition(calc)
        elif choice == '2':
            perform_subtraction(calc)
        elif choice == '3':
            perform_multiplication(calc)
        elif choice == '4':
            perform_division(calc)
        elif choice == '5':
            perform_power(calc)
        elif choice == '6':
            perform_quadratic_solution(calc)
        elif choice == '7':
            break

        next_action = input('\nВведите "1", чтобы завершить работу. '
                            'Любой иной ответ — продолжить: ')
        if next_action == '1':
            break
    print("Программа завершила работу")


if __name__ == "__main__":
    main()
