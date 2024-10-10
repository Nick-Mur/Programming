"""Модуль содержит функции, реализующие шифр Цезаря"""


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Шифрует текст с использованием шифра Цезаря.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
        if "A" <= char <= "Z":
            # Сдвиг для заглавных букв
            ciphertext += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
        elif "a" <= char <= "z":
            # Сдвиг для строчных букв
            ciphertext += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        else:
            # Непечатаемые символы остаются без изменений
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Расшифровывает текст, зашифрованный шифром Цезаря.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
        if "A" <= char <= "Z":
            # Обратный сдвиг для заглавных букв
            plaintext += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
        elif "a" <= char <= "z":
            # Обратный сдвиг для строчных букв
            plaintext += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
        else:
            # Непечатаемые символы остаются без изменений
            plaintext += char
    return plaintext
