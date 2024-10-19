"""
Модуль для работы с пазлами Судоку: чтение, отображение, решение и генерация новых пазлов.
"""

import multiprocessing
import pathlib
import random
import time
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """
    Прочитать Судоку из указанного файла.

    Args:
        path (Union[str, Path]): Путь к файлу с пазлом.

    Returns:
        List[List[str]]: Двумерный список, представляющий пазл Судоку.
    """
    path = pathlib.Path(path)
    with path.open(encoding="utf-8") as file_handle:
        puzzle = file_handle.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    """
    Преобразовать строку пазла в двумерный список.

    Args:
        puzzle (str): Строковое представление пазла.

    Returns:
        List[List[str]]: Двумерный список, представляющий сетку Судоку.

    Raises:
        ValueError: Если пазл не содержит ровно 81 символ.
    """
    digits = [c for c in puzzle if c in "123456789."]
    if len(digits) != 81:
        raise ValueError(
            "Пазл должен содержать ровно 81 символ "
            "(цифры от 1 до 9 или точки)."
        )
    grid = group_values(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """
    Вывести Судоку на экран.

    Args:
        grid (List[List[str]]): Двумерный список, представляющий сетку Судоку.
    """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        row_display = ""
        for col in range(9):
            cell = grid[row][col].center(width)
            row_display += cell
            if col in [2, 5]:
                row_display += "|"
        print(row_display)
        if row in [2, 5]:
            print(line)
    print()


def group_values(values: tp.List[T], group_size: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по group_size элементов.

    Args:
        values (List[T]): Список значений для группировки.
        group_size (int): Размер каждой группы.

    Returns:
        List[List[T]]: Список сгруппированных значений.

    Raises:
        ValueError: Если group_size не является положительным целым числом.
    """
    if not isinstance(group_size, int) or group_size <= 0:
        raise ValueError(
            "Размер группы group_size должен быть положительным целым числом."
        )
    return [
        values[i: i + group_size] for i in range(0, len(values), group_size)
    ]


def get_row(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """
    Получить все значения из строки, указанной позицией pos.

    Args:
        grid (List[List[str]]): Сетка Судоку.
        pos (Tuple[int, int]): Позиция в сетке.

    Returns:
        List[str]: Список значений из указанной строки.

    Raises:
        IndexError: Если индекс строки выходит за пределы.
    """
    row, _ = pos
    if row < 0 or row >= len(grid):
        raise IndexError("Индекс строки выходит за пределы.")
    return grid[row]


def get_col(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """
    Получить все значения из столбца, указанного позицией pos.

    Args:
        grid (List[List[str]]): Сетка Судоку.
        pos (Tuple[int, int]): Позиция в сетке.

    Returns:
        List[str]: Список значений из указанного столбца.

    Raises:
        IndexError: Если индекс столбца выходит за пределы.
    """
    _, col = pos
    if col < 0 or col >= len(grid[0]):
        raise IndexError("Индекс столбца выходит за пределы.")
    return [grid[row][col] for row in range(len(grid))]


def get_block(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """
    Получить все значения из 3x3 блока, в который входит позиция pos.

    Args:
        grid (List[List[str]]): Сетка Судоку.
        pos (Tuple[int, int]): Позиция в сетке.

    Returns:
        List[str]: Список значений из указанного блока.

    Raises:
        IndexError: Если индекс строки или столбца выходит за пределы.
    """
    row, col = pos
    if not (0 <= row < 9 and 0 <= col < 9):
        raise IndexError(
            "Индекс строки или столбца выходит за пределы."
        )
    block_row = 3 * (row // 3)
    block_col = 3 * (col // 3)
    return [
        grid[r][c]
        for r in range(block_row, block_row + 3)
        for c in range(block_col, block_col + 3)
    ]


def find_empty_positions(
    grid: tp.List[tp.List[str]]
) -> tp.Optional[tp.Tuple[int, int]]:
    """
    Найти первую пустую позицию (с точкой) в пазле.

    Args:
        grid (List[List[str]]): Сетка Судоку.

    Returns:
        Optional[Tuple[int, int]]: Позиция пустой клетки или None, если нет пустых.
    """
    for row, row_content in enumerate(grid):
        for col, cell in enumerate(row_content):
            if cell == ".":
                return (row, col)
    return None


def find_possible_values(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    """
    Найти возможные значения для указанной позиции.

    Args:
        grid (List[List[str]]): Сетка Судоку.
        pos (Tuple[int, int]): Позиция в сетке.

    Returns:
        Set[str]: Множество возможных значений.
    """
    possible_values = set("123456789")
    row_values = set(get_row(grid, pos))
    col_values = set(get_col(grid, pos))
    block_values = set(get_block(grid, pos))
    used_values = row_values | col_values | block_values
    return possible_values - used_values


def solve(
    grid: tp.List[tp.List[str]]
) -> tp.Optional[tp.List[tp.List[str]]]:
    """
    Решить пазл Судоку с помощью рекурсивного перебора.

    Args:
        grid (List[List[str]]): Сетка Судоку.

    Returns:
        Optional[List[List[str]]]: Решенная сетка Судоку или None, если решения нет.
    """
    pos = find_empty_positions(grid)
    if not pos:
        return grid  # Все позиции заполнены
    row, col = pos
    for value in find_possible_values(grid, pos):
        grid[row][col] = value
        solution = solve(grid)
        if solution:
            return solution
        grid[row][col] = "."  # Откат изменений
    return None  # Нет решения


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """
    Проверить корректность решения Судоку.

    Args:
        solution (List[List[str]]): Решенная сетка Судоку.

    Returns:
        bool: True, если решение верно, иначе False.
    """

    def is_valid_group(group: tp.List[str]) -> bool:
        elements = [x for x in group if x != "."]  # Игнорируем пустые клетки
        return (
            len(elements) == len(set(elements))
            and all(e in "123456789" for e in elements)
        )

    # Проверка строк
    for row in solution:
        if not is_valid_group(row):
            return False

    # Проверка столбцов
    for col in range(9):
        column = [solution[row][col] for row in range(9)]
        if not is_valid_group(column):
            return False

    # Проверка блоков 3x3
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block = [
                solution[r][c]
                for r in range(block_row, block_row + 3)
                for c in range(block_col, block_col + 3)
            ]
            if not is_valid_group(block):
                return False

    return True


def generate_sudoku(filled_cells: int) -> tp.List[tp.List[str]]:
    """
    Сгенерировать новый пазл Судоку с заполненными filled_cells клетками.

    Args:
        filled_cells (int): Количество заполненных клеток в пазле.

    Returns:
        List[List[str]]: Сгенерированная сетка Судоку.
    """
    # Создаем пустую сетку
    grid = [["." for _ in range(9)] for _ in range(9)]
    # Находим решение для пустой сетки (полный Судоку)
    solution = solve(grid)
    if not solution:
        return grid  # Если решение не найдено, возвращаем пустую сетку
    # Копируем решение
    grid = [row[:] for row in solution]
    # Ограничиваем filled_cells допустимыми значениями
    filled_cells = max(0, min(filled_cells, 81))
    # Генерируем список всех позиций и перемешиваем их
    positions = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(positions)
    # Удаляем клетки, оставляя filled_cells заполненных
    for i in range(81 - filled_cells):
        row, col = positions[i]
        grid[row][col] = "."
    return grid


def process_puzzle(file_name: str) -> None:
    """
    Прочитать пазл из файла, решить его и вывести результат.

    Args:
        file_name (str): Имя файла с пазлом.
    """
    try:
        grid = read_sudoku(file_name)
        print(f"Исходный пазл из файла {file_name}:")
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Пазл из файла {file_name} не может быть решен.\n")
        else:
            print(f"Решение для файла {file_name}:")
            display(solution)
            if check_solution(solution):
                print("Решение верно.\n")
            else:
                print("Решение неверно.\n")
    except FileNotFoundError:
        print(f"Файл {file_name} не найден.\n")
    except ValueError as error:
        print(f"Ошибка в файле {file_name}: {error}\n")


def run_solve(file_name: str) -> None:
    """
    Решить пазл и вывести время выполнения.

    Args:
        file_name (str): Имя файла с пазлом.
    """
    grid = read_sudoku(file_name)
    start_time = time.time()
    solution = solve(grid)
    end_time = time.time()
    if solution:
        print(f"{file_name}: {end_time - start_time:.6f} секунд")
    else:
        print(f"{file_name}: Решение не найдено")


if __name__ == "__main__":
    puzzle_files = ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]
    processes = []
    for file in puzzle_files:
        process = multiprocessing.Process(target=run_solve, args=(file,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
