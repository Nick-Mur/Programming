# recommender.py

class MovieRecommender:
    """
    Класс MovieRecommender отвечает за загрузку данных о фильмах и истории просмотров,
    а также за предоставление рекомендаций на основе истории пользователя.
    """

    def __init__(self, movies_file=None, histories_file=None, movies=None, histories=None):
        """
        Инициализирует класс, загружает данные о фильмах и истории просмотров.
        Можно передать списки movies и histories напрямую для тестирования.
        """
        if movies:
            # Используем переданные данные напрямую
            self.movies = movies  # Словарь с фильмами {идентификатор: название}
        else:
            self.movies_file = movies_file
            self.movies = dict()
            self.load_movies()
        if histories:
            self.histories = histories  # Список историй просмотров
        else:
            # Загружаем данные из файлов
            self.histories_file = histories_file
            self.histories = list()
            self.load_user_histories()

    def load_movies(self):
        """Загружает список фильмов из файла."""
        try:
            with open(self.movies_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        movie_id_str, movie_name = line.split(',', 1)
                        movie_id = int(movie_id_str)
                        self.movies[movie_id] = movie_name
        except FileNotFoundError:
            print(f"Файл {self.movies_file} не найден.")
        except Exception as e:
            print(f"Ошибка при загрузке фильмов: {e}")

    def load_user_histories(self):
        """Загружает историю просмотров пользователей из файла."""
        try:
            with open(self.histories_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        movie_ids = [int(movie_id_str) for movie_id_str in line.split(',')]
                        self.histories.append(movie_ids)
        except FileNotFoundError:
            print(f"Файл {self.histories_file} не найден.")
        except Exception as e:
            print(f"Ошибка при загрузке истории просмотров: {e}")

    def recommend(self, user_movies_list):
        """
        Рекомендует фильм на основе истории просмотров пользователя.

        :param user_movies_list: Список идентификаторов фильмов, просмотренных пользователем.
        :return: Название рекомендованного фильма или None, если рекомендаций нет.
        """
        if not isinstance(user_movies_list, list) or not all(isinstance(mid, int) for mid in user_movies_list):
            raise ValueError("Список фильмов должен быть списком целых чисел.")

        if not user_movies_list:
            return None  # Пользователь не смотрел ни одного фильма

        user_movies_set = set(user_movies_list)
        matching_histories = list()

        # Шаг 1: Отбираем истории, где совпадает хотя бы половина фильмов
        for history in self.histories:
            history_set = set(history)
            common_movies = user_movies_set.intersection(history_set)
            overlap_ratio = len(common_movies) / len(user_movies_set)
            if overlap_ratio >= 0.5:
                matching_histories.append((history, overlap_ratio))

        # Шаг 2: Собираем фильмы, которые пользователь еще не смотрел, с учетом веса
        recommended_movies = dict()
        for history, weight in matching_histories:
            for movie_id in history:
                if movie_id not in user_movies_set:
                    if movie_id in recommended_movies:
                        recommended_movies[movie_id] += weight
                    else:
                        recommended_movies[movie_id] = weight

        if not recommended_movies:
            return None  # Нет рекомендаций

        # Шаг 3: Находим фильм с максимальным суммарным весом
        max_weight = max(recommended_movies.values())
        top_movies = [movie_id for movie_id, weight in recommended_movies.items() if weight == max_weight]

        # Возвращаем название любого из фильмов с максимальным весом
        recommended_movie_id = top_movies[0]
        return self.movies.get(recommended_movie_id, None)
