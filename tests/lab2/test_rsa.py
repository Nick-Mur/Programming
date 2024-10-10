"""
Модуль для тестирования функций шифрования и дешифрования RSA.
"""

import unittest
from src.lab2.rsa import is_prime, compute_gcd, multiplicative_inverse, generate_keypair, encrypt, decrypt


class TestRSAEncryption(unittest.TestCase):
    """
    Класс для тестирования функций шифрования и дешифрования RSA.
    """

    def test_is_prime(self):
        """Тест функции проверки числа на простоту."""
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertFalse(is_prime(4))
        self.assertTrue(is_prime(5))
        self.assertFalse(is_prime(9))
        self.assertTrue(is_prime(13))
        self.assertFalse(is_prime(15))
        self.assertTrue(is_prime(17))
        self.assertTrue(is_prime(19))

    def test_gcd(self):
        """Тест функции для нахождения наибольшего общего делителя (НОД)."""
        self.assertEqual(compute_gcd(48, 18), 6)
        self.assertEqual(compute_gcd(18, 48), 6)
        self.assertEqual(compute_gcd(101, 10), 1)
        self.assertEqual(compute_gcd(54, 24), 6)
        self.assertEqual(compute_gcd(17, 31), 1)

    def test_multiplicative_inverse(self):
        """Тест функции для нахождения мультипликативного обратного."""
        self.assertEqual(multiplicative_inverse(7, 40), 23)
        self.assertEqual(multiplicative_inverse(3, 26), 9)
        with self.assertRaises(Exception):
            multiplicative_inverse(6, 12)

    def test_generate_keypair(self):
        """Тест генерации ключевой пары RSA."""
        public_key, private_key = generate_keypair(17, 19)
        self.assertEqual(public_key[1], 17 * 19)
        self.assertEqual(private_key[1], 17 * 19)
        self.assertNotEqual(public_key[0], private_key[0])

        with self.assertRaises(ValueError):
            generate_keypair(15, 19)  # 15 не простое число

        with self.assertRaises(ValueError):
            generate_keypair(17, 17)  # p и q не должны быть равны

    def test_encrypt_decrypt(self):
        """Тест шифрования и дешифрования сообщения с использованием ключей RSA."""
        prime_p, prime_q = 61, 53
        public_key, private_key = generate_keypair(prime_p, prime_q)
        message = "HELLO RSA"
        encrypted_msg = encrypt(public_key, message)
        decrypted_msg = decrypt(private_key, encrypted_msg)
        self.assertEqual(message, decrypted_msg)

    def test_encrypt_decrypt_with_special_characters(self):
        """Тест шифрования и дешифрования сообщения с неалфавитными символами."""
        prime_p, prime_q = 61, 53
        public_key, private_key = generate_keypair(prime_p, prime_q)
        message = "Hello, World! 123"
        encrypted_msg = encrypt(public_key, message)
        decrypted_msg = decrypt(private_key, encrypted_msg)
        self.assertEqual(message, decrypted_msg)

    def test_large_primes(self):
        """Тест шифрования и дешифрования сообщения с большими простыми числами."""
        prime_p, prime_q = 337, 331
        public_key, private_key = generate_keypair(prime_p, prime_q)
        message = "RSA ENCRYPTION TEST"
        encrypted_msg = encrypt(public_key, message)
        decrypted_msg = decrypt(private_key, encrypted_msg)
        self.assertEqual(message, decrypted_msg)


if __name__ == "__main__":
    unittest.main()
