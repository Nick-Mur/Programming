"""
Модуль для тестирования функций шифрования и дешифрования шифра Цезаря.
"""

import unittest
from src.lab2.caesar import encrypt_caesar, decrypt_caesar


class TestCaesarCipher(unittest.TestCase):
    """
    Класс для тестирования функций шифрования и дешифрования шифра Цезаря.
    """

    def test_encrypt_uppercase(self):
        """Тест шифрования заглавных букв."""
        self.assertEqual(encrypt_caesar("HELLO"), "KHOOR")

    def test_encrypt_lowercase(self):
        """Тест шифрования строчных букв."""
        self.assertEqual(encrypt_caesar("hello"), "khoor")

    def test_encrypt_mixedcase(self):
        """Тест шифрования текста со смешанным регистром."""
        self.assertEqual(encrypt_caesar("HelloWorld"), "KhoorZruog")

    def test_encrypt_with_non_alpha(self):
        """Тест шифрования текста с неалфавитными символами."""
        self.assertEqual(encrypt_caesar("Hello, World!"), "Khoor, Zruog!")

    def test_encrypt_empty(self):
        """Тест шифрования пустой строки."""
        self.assertEqual(encrypt_caesar(""), "")

    def test_decrypt_uppercase(self):
        """Тест дешифрования заглавных букв."""
        self.assertEqual(decrypt_caesar("KHOOR"), "HELLO")

    def test_decrypt_lowercase(self):
        """Тест дешифрования строчных букв."""
        self.assertEqual(decrypt_caesar("khoor"), "hello")

    def test_decrypt_mixedcase(self):
        """Тест дешифрования текста со смешанным регистром."""
        self.assertEqual(decrypt_caesar("KhoorZruog"), "HelloWorld")

    def test_decrypt_with_non_alpha(self):
        """Тест дешифрования текста с неалфавитными символами."""
        self.assertEqual(decrypt_caesar("Khoor, Zruog!"), "Hello, World!")

    def test_decrypt_empty(self):
        """Тест дешифрования пустой строки."""
        self.assertEqual(decrypt_caesar(""), "")

    def test_custom_shift_encrypt(self):
        """Тест шифрования с использованием пользовательского сдвига."""
        self.assertEqual(encrypt_caesar("abc", shift=1), "bcd")

    def test_custom_shift_decrypt(self):
        """Тест дешифрования с использованием пользовательского сдвига."""
        self.assertEqual(decrypt_caesar("bcd", shift=1), "abc")

    def test_negative_shift_encrypt(self):
        """Тест шифрования с отрицательным сдвигом."""
        self.assertEqual(encrypt_caesar("def", shift=-1), "cde")

    def test_negative_shift_decrypt(self):
        """Тест дешифрования с отрицательным сдвигом."""
        self.assertEqual(decrypt_caesar("cde", shift=-1), "def")


if __name__ == "__main__":
    unittest.main()
