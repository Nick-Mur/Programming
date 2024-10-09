class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно.")
        return a / b

    def power(self, a, n):
        return a ** n

    def solve_quadratic(self, a, b, c):
        from math import sqrt


        discriminant = b**2 - 4*a*c
        if discriminant > 0:
            x1 = (-b + sqrt(discriminant)) / (2*a)
            x2 = (-b - sqrt(discriminant)) / (2*a)
            return discriminant, (x1, x2)
        elif discriminant == 0:
            x = -b / (2*a)
            return discriminant, x
        else:
            return discriminant, None
