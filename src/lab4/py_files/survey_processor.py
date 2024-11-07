# py_files/survey_processor.py

from typing import List, Optional
from .consts import MAX_AGE


class Respondent:
    """
    Класс Respondent представляет респондента с ФИО и возрастом.
    """

    def __init__(self, full_name: str, age: int):
        """
        Инициализирует респондента.

        :param full_name: Полное имя респондента.
        :param age: Возраст респондента.
        """
        self.full_name = full_name
        self.age = age

    def __repr__(self):
        """
        Возвращает строковое представление респондента.
        """
        return f"{self.full_name} ({self.age})"


class AgeGroup:
    """
    Класс AgeGroup представляет возрастную группу с границами и списком респондентов.
    """

    def __init__(self, label: str, lower: int, upper: Optional[int]):
        """
        Инициализирует возрастную группу.

        :param label: Метка группы (например, "81-100").
        :param lower: Нижняя граница возраста (включительно).
        :param upper: Верхняя граница возраста (включительно). Если верхняя граница None, значит без верхнего предела.
        """
        self.label = label
        self.lower = lower
        self.upper = upper
        self.respondents: List[Respondent] = []

    def add_respondent(self, respondent: Respondent):
        """
        Добавляет респондента в группу.

        :param respondent: Объект Respondent.
        """
        self.respondents.append(respondent)

    def has_respondents(self) -> bool:
        """
        Проверяет, есть ли респонденты в группе.

        :return: True, если есть респонденты, иначе False.
        """
        return len(self.respondents) > 0

    def sort_respondents(self):
        """
        Сортирует респондентов в группе по возрасту убывания и по ФИО возрастания при одинаковом возрасте.
        """
        self.respondents.sort(key=lambda r: (-r.age, r.full_name))

    def __repr__(self):
        """
        Возвращает строковое представление группы с респондентами.
        """
        respondents_str = ', '.join([f"{r.full_name} ({r.age})" for r in self.respondents])
        return f"{self.label}: {respondents_str}"


class SurveyProcessor:
    """
    Класс SurveyProcessor обрабатывает список респондентов и разбивает их на возрастные группы.
    """

    def __init__(self, boundaries: List[int]):
        """
        Инициализирует обработчик опроса с заданными границами возрастных групп.

        :param boundaries: Список целых чисел, определяющих верхние границы возрастных групп.
        """
        if not self._validate_boundaries(boundaries):
            raise ValueError("Границы возрастных групп должны быть возрастающими числами в диапазоне от 1 до 123.")
        self.boundaries = sorted(boundaries)
        self.age_groups: List[AgeGroup] = self._create_age_groups()

    def _validate_boundaries(self, boundaries: List[int]) -> bool:
        """
        Проверяет корректность границ возрастных групп.

        :param boundaries: Список границ.
        :return: True, если границы корректны, иначе False.
        """
        previous = -1
        for boundary in boundaries:
            if not (0 < boundary <= MAX_AGE):
                return False
            if boundary <= previous:
                return False
            previous = boundary
        return True

    def _create_age_groups(self) -> List[AgeGroup]:
        """
        Создает список возрастных групп на основе границ.

        :return: Список объектов AgeGroup, отсортированных от старшей к младшей группе.
        """
        groups = []
        lower = 0
        for boundary in self.boundaries:
            label = f"{lower}-{boundary}"
            groups.append(AgeGroup(label, lower, boundary))
            lower = boundary + 1
        # Добавляем последнюю группу без верхней границы
        label = f"{lower}+"  # Например, "101+"
        groups.append(AgeGroup(label, lower, None))
        # Сортируем группы от старшей к младшей
        groups.sort(key=lambda g: g.lower, reverse=True)
        return groups

    def add_respondent(self, respondent: Respondent):
        """
        Добавляет респондента в соответствующую возрастную группу.

        :param respondent: Объект Respondent.
        """
        age = respondent.age
        for group in self.age_groups:
            if group.upper is not None:
                if group.lower <= age <= group.upper:
                    group.add_respondent(respondent)
                    return
            else:
                if age >= group.lower:
                    group.add_respondent(respondent)
                    return

    def process_respondents(self, respondents: List[Respondent]):
        """
        Обрабатывает список респондентов, распределяя их по возрастным группам.

        :param respondents: Список объектов Respondent.
        """
        for respondent in respondents:
            self.add_respondent(respondent)
        # После распределения сортируем респондентов в каждой группе
        for group in self.age_groups:
            if group.has_respondents():
                group.sort_respondents()

    def get_sorted_groups(self) -> List[AgeGroup]:
        """
        Возвращает список возрастных групп с респондентами, отсортированных от старшей к младшей.

        :return: Список AgeGroup.
        """
        return [group for group in self.age_groups if group.has_respondents()]

    def display_groups(self):
        """
        Выводит разбивку по возрастным группам в требуемом формате.
        """
        sorted_groups = self.get_sorted_groups()
        for group in sorted_groups:
            print(group)
