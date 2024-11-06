# test_recommender.py

import unittest
from src.lab4.py_files.objects import MovieRecommender


class TestMovieRecommender(unittest.TestCase):
    """Тестовый класс для проверки MovieRecommender"""

    def setUp(self):
        """Устанавливает данные для тестов."""
        # Данные фильмов
        self.movies = {
            1: 'Мстители: Финал',
            2: 'Хатико',
            3: 'Дюна',
            4: 'Унесенные призраками'
        }

        # История просмотров пользователей
        self.histories = [
            [2, 1, 3],
            [1, 4, 3],
            [2, 2, 2, 2, 2, 3]
        ]

        # Создаем экземпляр MovieRecommender с тестовыми данными
        self.recommender = MovieRecommender(movies=self.movies, histories=self.histories)

    def test_recommendation(self):
        """Тестирует работу функции recommend."""
        # Пример из задания
        user_movies = [2, 4]
        recommended_movie = self.recommender.recommend(user_movies)
        self.assertEqual(recommended_movie, 'Дюна')

    def test_no_recommendation(self):
        """Тестирует случай, когда нет рекомендаций."""
        # Пользователь уже посмотрел все фильмы
        user_movies = [1, 2, 3, 4]
        recommended_movie = self.recommender.recommend(user_movies)
        self.assertIsNone(recommended_movie)

    def test_edge_case_half_movies(self):
        """Тестирует случай, когда совпадает ровно половина фильмов."""
        user_movies = [1, 2]
        recommended_movie = self.recommender.recommend(user_movies)
        # Ожидаем, что рекомендация будет среди оставшихся фильмов
        self.assertEqual(recommended_movie, 'Дюна')

    def test_error_handling_invalid_input(self):
        """Тестирует обработку неверного ввода."""
        # Передаем некорректный список фильмов
        user_movies = ['a', None, 5]
        with self.assertRaises(ValueError):
            self.recommender.recommend(user_movies)

    def test_empty_user_movies(self):
        """Тестирует случай, когда пользователь не смотрел ни одного фильма."""
        user_movies = list()
        recommended_movie = self.recommender.recommend(user_movies)
        self.assertIsNone(recommended_movie)

    def test_recommendation_with_weights(self):
        """Тестирует, что вес рекомендаций учитывается правильно."""
        user_movies = [1, 3]
        recommended_movie = self.recommender.recommend(user_movies)
        # Проверяем, что рекомендован фильм с максимальным суммарным весом
        self.assertEqual(recommended_movie, 'Хатико')

if __name__ == '__main__':
    unittest.main()
