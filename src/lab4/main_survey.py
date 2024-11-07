# main_survey.py

from py_files.survey_processor import SurveyProcessor, Respondent
from py_files.consts import MAX_AGE
import sys


def main():
    """
    Основная функция приложения для разбивки респондентов по возрастным группам.
    """
    # Проверяем наличие аргументов командной строки
    if len(sys.argv) < 2:
        print("Необходимо указать границы возрастных групп в качестве аргументов командной строки.")
        sys.exit(1)

    try:
        # Парсим границы возрастных групп из аргументов командной строки
        boundaries = [int(arg) for arg in sys.argv[1:]]
    except ValueError:
        print("Все границы возрастных групп должны быть целыми числами.")
        sys.exit(1)

    # Создаем обработчик опроса
    try:
        processor = SurveyProcessor(boundaries)
    except ValueError as ve:
        print(f"Ошибка: {ve}")
        sys.exit(1)

    # Читаем респондентов из стандартного ввода
    print("Введите список респондентов в формате <ФИО>,<возраст>. Для завершения введите 'END':")
    respondents = []
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break  # EOF
            line = line.strip()
            if line.upper() == "END":
                break
            if not line:
                continue  # Пропускаем пустые строки
            parts = line.split(',', 1)
            if len(parts) != 2:
                print(f"Некорректная строка: '{line}'. Ожидается формат <ФИО>,<возраст>.")
                continue
            full_name = parts[0].strip()
            age_str = parts[1].strip()
            age = int(age_str)
            if not (0 <= age <= MAX_AGE):
                print(f"Некорректный возраст для респондента '{full_name}': {age}. Должен быть от 0 до {MAX_AGE}.")
                continue
            respondent = Respondent(full_name, age)
            respondents.append(respondent)
        except ValueError:
            print(f"Некорректный возраст в строке: '{line}'. Должен быть целым числом.")
            continue
        except Exception as e:
            print(f"Ошибка при обработке строки '{line}': {e}")
            continue

    # Обрабатываем респондентов
    processor.process_respondents(respondents)

    # Выводим результаты
    processor.display_groups()


if __name__ == "__main__":
    main()
