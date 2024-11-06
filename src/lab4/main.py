# Основная часть программы
from py_files.objects import MovieRecommender
from py_files.consts import *


if __name__ == '__main__':
    # Создаем экземпляр MovieRecommender
    recommender = MovieRecommender(movies_file=MOVIES_FILE, histories_file=HISTORIES_FILE)

    # Запрашиваем у пользователя список просмотренных фильмов
    user_input = input("Введите список идентификаторов просмотренных фильмов, разделенных запятыми:\n")
    user_movies_list = [int(movie_id_str.strip()) for movie_id_str in user_input.split(',') if movie_id_str.strip().isdigit()]

    # Получаем рекомендацию
    recommendation = recommender.recommend(user_movies_list)

    # Выводим результат
    if recommendation:
        print(recommendation)
    else:
        print("Нет доступных рекомендаций.")
