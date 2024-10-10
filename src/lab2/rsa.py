"""
Модуль для реализации алгоритма RSA шифрования и дешифрования.
"""

import random
import typing as tp


def is_prime(number: int) -> bool:
    """
    Проверяет, является ли число простым.

    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if number <= 1:
        return False
    if number <= 3:
        return True
    # Исключаем кратные 2 и 3
    if number % 2 == 0 or number % 3 == 0:
        return False
    divisor = 5
    # Проверяем делители до квадратного корня из числа
    while divisor * divisor <= number:
        if number % divisor == 0 or number % (divisor + 2) == 0:
            return False
        divisor += 6
    return True


def compute_gcd(value_a: int, value_b: int) -> int:
    """
    Алгоритм Евклида для нахождения наибольшего общего делителя (НОД).

    >>> compute_gcd(12, 15)
    3
    >>> compute_gcd(3, 7)
    1
    """
    while value_b != 0:
        value_a, value_b = value_b, value_a % value_b
    return value_a


def multiplicative_inverse(exponent: int, phi: int) -> int:
    """
    Расширенный алгоритм Евклида для нахождения мультипликативного обратного.

    >>> multiplicative_inverse(7, 40)
    23
    """
    def extended_gcd(value_a, value_b):
        if value_a == 0:
            return value_b, 0, 1
        gcd_value, x_coef1, y_coef1 = extended_gcd(value_b % value_a, value_a)
        x_coef = y_coef1 - (value_b // value_a) * x_coef1
        y_coef = x_coef1
        return gcd_value, x_coef, y_coef

    gcd_value, x_coef, _ = extended_gcd(exponent, phi)
    if gcd_value != 1:
        raise Exception('Мультипликативного обратного не существует.')
    return x_coef % phi


def generate_keypair(prime_p: int, prime_q: int) -> tp.Tuple[tp.Tuple[int, int],
                    tp.Tuple[int, int]]:
    """
    Генерирует пару ключей (публичный и приватный) для RSA шифрования.

    :param prime_p: первое простое число
    :param prime_q: второе простое число
    :return: кортеж с публичным и приватным ключами
    """
    if not (is_prime(prime_p) and is_prime(prime_q)):
        raise ValueError("Оба числа должны быть простыми.")
    if prime_p == prime_q:
        raise ValueError("p и q не должны быть равны")

    # Вычисляем n = p * q
    modulus_n = prime_p * prime_q

    # Вычисляем функцию Эйлера phi(n) = (p - 1) * (q - 1)
    phi = (prime_p - 1) * (prime_q - 1)

    # Выбираем e так, чтобы 1 < e < phi и НОД(e, phi) = 1
    exponent_e = random.randrange(2, phi)
    gcd_value = compute_gcd(exponent_e, phi)
    while gcd_value != 1:
        exponent_e = random.randrange(2, phi)
        gcd_value = compute_gcd(exponent_e, phi)

    # Вычисляем d, мультипликативное обратное к e по модулю phi
    exponent_d = multiplicative_inverse(exponent_e, phi)

    # Публичный ключ (e, n), приватный ключ (d, n)
    return ((exponent_e, modulus_n), (exponent_d, modulus_n))


def encrypt(public_key: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    """
    Шифрует сообщение с использованием публичного ключа.

    :param public_key: публичный ключ (e, n)
    :param plaintext: исходное сообщение
    :return: зашифрованное сообщение в виде списка чисел
    """
    exponent_e, modulus_n = public_key
    cipher = [pow(ord(char), exponent_e, modulus_n) for char in plaintext]
    return cipher


def decrypt(private_key: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    """
    Расшифровывает сообщение с использованием приватного ключа.

    :param private_key: приватный ключ (d, n)
    :param ciphertext: зашифрованное сообщение в виде списка чисел
    :return: расшифрованное сообщение
    """
    exponent_d, modulus_n = private_key
    plain = [chr(pow(char, exponent_d, modulus_n)) for char in ciphertext]
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Шифратор/Дешифратор")
    PRIME_P = int(input("Введите простое число (например, 17, 19, 23 и т.д.): "))
    PRIME_Q = int(input("Введите другое простое число (отличное от предыдущего): "))
    print("Генерируем ваши публичный и приватный ключи...")
    PUBLIC_KEY, PRIVATE_KEY = generate_keypair(PRIME_P, PRIME_Q)
    print("Ваш публичный ключ: ", PUBLIC_KEY, " и ваш приватный ключ: ", PRIVATE_KEY)
    MESSAGE = input("Введите сообщение для шифрования приватным ключом: ")
    ENCRYPTED_MSG = encrypt(PRIVATE_KEY, MESSAGE)
    print("Ваше зашифрованное сообщение: ")
    print(" ".join(map(str, ENCRYPTED_MSG)))
    print("Расшифровываем сообщение с помощью публичного ключа ", PUBLIC_KEY, "...")
    print("Ваше сообщение:")
    print(decrypt(PUBLIC_KEY, ENCRYPTED_MSG))
