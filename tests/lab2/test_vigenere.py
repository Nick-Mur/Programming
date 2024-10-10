"""
Модуль для тестирования функций шифрования и дешифрования шифра Виженера.
"""

import unittest
from src.lab2.vigenere import encrypt_vigenere, decrypt_vigenere


class TestVigenereCipher(unittest.TestCase):
    """
    Класс для тестирования функций шифрования и дешифрования шифра Виженера.
    """

    def test_encrypt_simple(self):
        """Тест простого шифрования с использованием ключа."""
        self.assertEqual(encrypt_vigenere("HELLO", "KEY"), "RIJVS")

    def test_encrypt_with_spaces(self):
        """Тест шифрования текста с пробелами."""
        self.assertEqual(encrypt_vigenere("HELLO WORLD", "KEY"), "RIJVS UYVJN")

    def test_encrypt_mixed_case(self):
        """Тест шифрования текста со смешанным регистром."""
        self.assertEqual(encrypt_vigenere("HelloWorld", "key"), "RijvsUyvjn")

    def test_encrypt_non_alpha(self):
        """Тест шифрования текста с неалфавитными символами."""
        self.assertEqual(encrypt_vigenere("Hello, World!", "key"), "Rijvs, Uyvjn!")

    def test_decrypt_simple(self):
        """Тест простого дешифрования с использованием ключа."""
        self.assertEqual(decrypt_vigenere("RIJVS", "KEY"), "HELLO")

    def test_decrypt_with_spaces(self):
        """Тест дешифрования текста с пробелами."""
        self.assertEqual(decrypt_vigenere("RIJVS UYVJN", "KEY"), "HELLO WORLD")

    def test_decrypt_mixed_case(self):
        """Тест дешифрования текста со смешанным регистром."""
        self.assertEqual(decrypt_vigenere("RijvsUyvjn", "key"), "HelloWorld")

    def test_decrypt_non_alpha(self):
        """Тест дешифрования текста с неалфавитными символами."""
        self.assertEqual(decrypt_vigenere("Rijvs, Uyvjn!", "key"), "Hello, World!")

    def test_encrypt_empty(self):
        """Тест шифрования пустой строки."""
        self.assertEqual(encrypt_vigenere("", "key"), "")

    def test_decrypt_empty(self):
        """Тест дешифрования пустой строки."""
        self.assertEqual(decrypt_vigenere("", "key"), "")

    def test_encrypt_keyword_a(self):
        """Тест шифрования с ключом 'A'."""
        self.assertEqual(encrypt_vigenere("HELLO", "A"), "HELLO")

    def test_decrypt_keyword_a(self):
        """Тест дешифрования с ключом 'A'."""
        self.assertEqual(decrypt_vigenere("HELLO", "A"), "HELLO")

    def test_encrypt_long_keyword(self):
        """Тест шифрования с длинным ключом."""
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "LEMONLEMONLE"), "LXFOPVEFRNHR")

    def test_decrypt_long_keyword(self):
        """Тест дешифрования с длинным ключом."""
        self.assertEqual(decrypt_vigenere("LXFOPVEFRNHR", "LEMONLEMONLE"), "ATTACKATDAWN")


if __name__ == "__main__":
    unittest.main()
