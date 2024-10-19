"""Тесты для sudoku.py."""


import unittest

from src.lab3.sudoku import (
    check_solution,
    create_grid,
    find_empty_positions,
    find_possible_values,
    generate_sudoku,
    get_block,
    get_col,
    get_row,
    group_values,
    solve,
)


class TestSudoku(unittest.TestCase):
    """Класс с юнит-тестами для функций модуля sudoku.py"""

    def test_group(self):
        """Тестирование функции group"""
        # Стандартные случаи
        self.assertEqual(group_values([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(group_values([1, 2, 3, 4, 5, 6, 7, 8, 9], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        # Пустой список
        self.assertEqual(group_values([], 3), [])
        # n = 1
        self.assertEqual(group_values([1, 2, 3], 1), [[1], [2], [3]])
        # Неполные группы
        self.assertEqual(group_values([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])
        # Ошибочные значения n
        with self.assertRaises(ValueError):
            group_values([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            group_values([1, 2, 3], -1)
        with self.assertRaises(ValueError):
            group_values([1, 2, 3], 2.5)

    def test_create_grid(self):
        """Тестирование функции create_grid"""
        # Стандартные случаи
        puzzle = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
        grid = create_grid(puzzle)
        self.assertEqual(len(grid), 9)
        self.assertEqual(len(grid[0]), 9)
        self.assertEqual(grid[0], ["5", "3", ".", ".", "7", ".", ".", ".", "."])
        self.assertEqual(grid[1], ["6", ".", ".", "1", "9", "5", ".", ".", "."])

        # Проверка длины пазла
        with self.assertRaises(ValueError):
            create_grid("123")  # Меньше 81 символа

        with self.assertRaises(ValueError):
            create_grid("1" * 82)  # Больше 81 символа

        with self.assertRaises(ValueError):
            create_grid("1" * 80 + "x")  # Неправильный символ

    def test_get_row(self):
        """Тестирование функции get_row"""
        grid = [
            ["1", "2", ".", "4", "5", "6", "7", "8", "9"],
            ["4", "5", "6", "7", "8", "9", "1", "2", "3"],
            ["7", "8", "9", "1", "2", "3", "4", "5", "6"],
            ["2", "3", "4", "5", "6", "7", "8", "9", "1"],
            ["5", "6", "7", "8", "9", "1", "2", "3", "4"],
            ["8", "9", "1", "2", "3", "4", "5", "6", "7"],
            ["3", "4", "5", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "8", "9", "1", "2", "3", "4", "5"],
            ["9", "1", "2", "3", "4", "5", "6", "7", "8"],
        ]
        # Стандартные случаи
        self.assertEqual(get_row(grid, (0, 0)), ["1", "2", ".", "4", "5", "6", "7", "8", "9"])
        self.assertEqual(get_row(grid, (4, 4)), ["5", "6", "7", "8", "9", "1", "2", "3", "4"])
        # Граничные случаи
        self.assertEqual(get_row(grid, (8, 8)), ["9", "1", "2", "3", "4", "5", "6", "7", "8"])
        # Ошибочные индексы
        with self.assertRaises(IndexError):
            get_row(grid, (-1, 0))
        with self.assertRaises(IndexError):
            get_row(grid, (9, 0))

    def test_get_col(self):
        """Тестирование функции get_col"""
        grid = [
            ["1", "2", ".", "4", "5", "6", "7", "8", "9"],
            ["4", "5", "6", "7", "8", "9", "1", "2", "3"],
            ["7", "8", "9", "1", "2", "3", "4", "5", "6"],
            ["2", "3", "4", "5", "6", "7", "8", "9", "1"],
            ["5", "6", "7", "8", "9", "1", "2", "3", "4"],
            ["8", "9", "1", "2", "3", "4", "5", "6", "7"],
            ["3", "4", "5", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "8", "9", "1", "2", "3", "4", "5"],
            ["9", "1", "2", "3", "4", "5", "6", "7", "8"],
        ]
        # Стандартные случаи
        self.assertEqual(get_col(grid, (0, 0)), ["1", "4", "7", "2", "5", "8", "3", "6", "9"])
        self.assertEqual(get_col(grid, (0, 4)), ["5", "8", "2", "6", "9", "3", "7", "1", "4"])
        # Граничные случаи
        self.assertEqual(get_col(grid, (8, 8)), ["9", "3", "6", "1", "4", "7", "2", "5", "8"])
        # Ошибочные индексы
        with self.assertRaises(IndexError):
            get_col(grid, (0, -1))
        with self.assertRaises(IndexError):
            get_col(grid, (0, 9))

    def test_get_block(self):
        """Тестирование функции get_block"""
        grid = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
        ]
        self.assertEqual(get_block(grid, (0, 1)), ["5", "3", ".", "6", ".", ".", ".", "9", "8"])
        self.assertEqual(get_block(grid, (4, 7)), [".", ".", "3", ".", ".", "1", ".", ".", "6"])
        self.assertEqual(get_block(grid, (8, 8)), ["2", "8", ".", ".", ".", "5", ".", "7", "9"])
        # Граничные случаи
        self.assertEqual(get_block(grid, (2, 2)), ["5", "3", ".", "6", ".", ".", ".", "9", "8"])
        self.assertEqual(get_block(grid, (6, 0)), [".", "6", ".", ".", ".", ".", ".", ".", "."])
        # Ошибочные индексы
        with self.assertRaises(IndexError):
            get_block(grid, (-1, 0))
        with self.assertRaises(IndexError):
            get_block(grid, (0, 9))

    def test_find_empty_positions(self):
        """Тестирование функции find_empty_positions"""
        # Пазл без пустых позиций
        grid = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.assertIsNone(find_empty_positions(grid))
        # Пазл с одной пустой позицией
        grid = [["1", "2", "."], ["4", "5", "6"], ["7", "8", "9"]]
        self.assertEqual(find_empty_positions(grid), (0, 2))
        # Пазл с несколькими пустыми позициями
        grid = [["1", ".", "3"], ["4", ".", "6"], ["7", "8", "9"]]
        self.assertEqual(find_empty_positions(grid), (0, 1))
        # Пустой пазл
        grid = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        self.assertEqual(find_empty_positions(grid), (0, 0))

    def test_find_possible_values(self):
        """Тестирование функции find_possible_values"""
        grid = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
        ]
        # Позиция (0,2)
        self.assertEqual(find_possible_values(grid, (0, 2)), {"1", "2", "4"})
        # Позиция (4,7)
        self.assertEqual(find_possible_values(grid, (4, 7)), {"2", "5", "9"})
        # Позиция (8,0)
        self.assertEqual(find_possible_values(grid, (8, 0)), {"1", "2", "3"})

    def test_solve(self):
        """Тестирование функции solve"""
        grid = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"],
        ]
        expected_solution = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertEqual(solution, expected_solution)
        self.assertTrue(check_solution(solution))

    def test_check_solution(self):
        """Тестирование функции check_solution"""
        correct_solution = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        self.assertTrue(check_solution(correct_solution))

        # Неверное решение (повторение в строке)
        incorrect_solution_row = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "5"],  # Повтор '5' в последней строке
        ]
        self.assertFalse(check_solution(incorrect_solution_row))

        # Неверное решение (повторение в столбце)
        incorrect_solution_col = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        # Повтор '9' в первом столбце
        incorrect_solution_col[8][0] = "9"
        self.assertFalse(check_solution(incorrect_solution_col))

        # Неверное решение (повторение в блоке)
        incorrect_solution_block = [
            ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
            ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
            ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
            ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
            ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
            ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
            ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
            ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
            ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
        ]
        # Добавляем дубликат '5' в нижнем левом блоке (например, заменяем (7,0) на '5')
        incorrect_solution_block[7][0] = "5"
        self.assertFalse(check_solution(incorrect_solution_block))

    def test_generate_sudoku(self):
        """Тестирование функции generate_sudoku"""
        # Генерация с 40 заполненными клетками
        grid = generate_sudoku(40)
        num_filled = sum(1 for row in grid for e in row if e != ".")
        self.assertEqual(num_filled, 40)
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))

        # Генерация с 0 заполненными клетками (полностью пустой)
        grid = generate_sudoku(0)
        num_filled = sum(1 for row in grid for e in row if e != ".")
        self.assertEqual(num_filled, 0)
        solution = solve(grid)
        self.assertIsNotNone(solution)
        self.assertTrue(check_solution(solution))

        # Генерация с максимальным количеством заполненных клеток (81)
        grid = generate_sudoku(81)
        num_filled = sum(1 for row in grid for e in row if e != ".")
        self.assertEqual(num_filled, 81)
        self.assertTrue(check_solution(grid))

        # Генерация с количеством, превышающим 81 (должно быть ограничено)
        grid = generate_sudoku(1000)
        num_filled = sum(1 for row in grid for e in row if e != ".")
        self.assertEqual(num_filled, 81)
        self.assertTrue(check_solution(grid))


if __name__ == "__main__":
    # Запуск юнит-тестов
    unittest.main()
