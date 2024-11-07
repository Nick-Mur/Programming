# main_movie_recommender.py

from py_files.movie_recommender import MovieRecommender
from py_files.consts import MOVIES_FILE, HISTORIES_FILE


def main():
    """
    Основная функция для MovieRecommender.
    """
    # Создаем экземпляр MovieRecommender
    recommender = MovieRecommender(movies_file=MOVIES_FILE, histories_file=HISTORIES_FILE)

    # Запрашиваем у пользователя список просмотренных фильмов
    user_input = input("Введите список идентификаторов просмотренных фильмов, разделенных запятыми:\n")
    try:
        user_movies_list = [int(movie_id_str.strip()) for movie_id_str in user_input.split(',') if movie_id_str.strip().isdigit()]
    except ValueError:
        print("Некорректный ввод. Убедитесь, что вы вводите только целые числа, разделенные запятыми.")
        user_movies_list = []

    # Получаем рекомендацию
    recommendation = recommender.recommend(user_movies_list)

    # Выводим результат
    if recommendation:
        print(recommendation)
    else:
        print("Нет доступных рекомендаций.")


if __name__ == "__main__":
    main()
