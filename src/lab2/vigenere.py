"""
Модуль, реализующий шифр Виженера.
"""


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Шифрует текст с использованием шифра Виженера.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword_length = len(keyword)
    keyword_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(keyword[keyword_index % keyword_length].lower()) - ord("a")
            if char.isupper():
                ciphertext += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            else:
                ciphertext += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            keyword_index += 1
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Расшифровывает текст, зашифрованный шифром Виженера.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword_length = len(keyword)
    keyword_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(keyword[keyword_index % keyword_length].lower()) - ord("a")
            if char.isupper():
                plaintext += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            else:
                plaintext += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            keyword_index += 1
        else:
            plaintext += char
    return plaintext
