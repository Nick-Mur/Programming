from calculator import Calculator


def input_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Пожалуйста, введите корректное число.")


def input_operation():
    while True:
        choice = input("Введите номер операции: ")
        if choice in map(str, range(1, 8)):
            return choice
        else:
            print("Неверный выбор, попробуйте снова.")


def main():
    calc = Calculator()
    print("Добро пожаловать в Калькулятор!")
    while True:
        print("\nВыберите операцию:")
        print("1. Сложение чисел")
        print("2. Вычитание чисел")
        print("3. Умножение чисел")
        print("4. Деление чисел")
        print("5. Возведение в степень")
        print("6. Решение квадратного уравнения")
        print("7. Выход")

        choice = input_operation()

        if choice == '1':
            a = input_number("Введите первое число: ")
            b = input_number("Введите второе число: ")
            result = calc.add(a, b)
            print(f"\nРезультат: {result}")
        elif choice == '2':
            a = input_number("Введите уменьшаемое: ")
            b = input_number("Введите вычитаемое: ")
            result = calc.subtract(a, b)
            print(f"\nРезультат: {result}")
        elif choice == '3':
            a = input_number("Введите первый множитель: ")
            b = input_number("Введите второй множитель: ")
            result = calc.multiply(a, b)
            print(f"\nРезультат: {result}")
        elif choice == '4':
            a = input_number("Введите делимое: ")
            b = input_number("Введите делитель: ")
            if b == 0:
                print("\nДеление на ноль невозможно. Попробуйте снова.")
            else:
                result = calc.divide(a, b)
                print(f"\nРезультат: {result}")
        elif choice == '5':
            a = input_number("Введите основание: ")
            n = input_number("Введите показатель степени: ")
            result = calc.power(a, n)
            print(f"\nРезультат: {result}")
        elif choice == '6':
            print("Форма уравнения: ax^2 + bx + c = 0")
            a = input_number("Введите a: ")
            b = input_number("Введите b: ")
            c = input_number("Введите c: ")
            discriminant, roots = calc.solve_quadratic(a, b, c)
            print(f"\nДискриминант: {discriminant}")
            if roots is None:
                print("Действительных корней нет.")
            elif isinstance(roots, tuple):
                print(f"Корни уравнения: x1 = {roots[0]}, x2 = {roots[1]}")
            else:
                print(f"Корень уравнения: x = {roots}")
        elif choice == '7':
            break

        next_action = input('\nВведите "1", чтобы завершить работу. Любой иной ответ — продолжить: ')
        if next_action == '1':
            break
    print("Программа завершила работу")


if __name__ == "__main__":
    main()
