"""
Sudoku Puzzle & Solution Generator Engine.
Generates 100% mathematically valid 9x9 Sudoku puzzles with guaranteed unique solutions.
Supports Easy, Medium, Hard, and Expert difficulty levels.
"""

import random
from typing import List, Tuple, Optional, Dict, Any


class SudokuGenerator:
    @staticmethod
    def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Checks if placing num at board[row][col] is valid according to Sudoku rules."""
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    @staticmethod
    def solve_board(board: List[List[int]]) -> bool:
        """Solves the Sudoku board using randomized backtracking."""
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if SudokuGenerator.is_valid(board, r, c, num):
                            board[r][c] = num
                            if SudokuGenerator.solve_board(board):
                                return True
                            board[r][c] = 0
                    return False
        return True

    @staticmethod
    def count_solutions(board: List[List[int]], count_limit: int = 2) -> int:
        """Counts how many solutions a given Sudoku board has (up to count_limit)."""
        empty = None
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    empty = (r, c)
                    break
            if empty:
                break

        if not empty:
            return 1

        r, c = empty
        solutions = 0
        for num in range(1, 10):
            if SudokuGenerator.is_valid(board, r, c, num):
                board[r][c] = num
                solutions += SudokuGenerator.count_solutions(board, count_limit)
                board[r][c] = 0
                if solutions >= count_limit:
                    break
        return solutions

    @classmethod
    def generate_full_solution(cls) -> List[List[int]]:
        """Generates a complete, valid, randomly filled 9x9 Sudoku board."""
        board = [[0] * 9 for _ in range(9)]
        cls.solve_board(board)
        return board

    @classmethod
    def generate_puzzle(
        cls, 
        difficulty: str = "medium", 
        puzzle_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a Sudoku puzzle and paired solution with a guaranteed unique solution.
        Difficulty targets:
          - easy: 38 - 42 clues
          - medium: 30 - 34 clues
          - hard: 26 - 29 clues
          - expert: 22 - 25 clues
        """
        difficulty = difficulty.lower()
        if difficulty == "easy":
            target_clues = random.randint(38, 42)
        elif difficulty == "hard":
            target_clues = random.randint(26, 29)
        elif difficulty == "expert":
            target_clues = random.randint(22, 25)
        else:  # medium
            target_clues = random.randint(30, 34)

        solution = cls.generate_full_solution()
        puzzle = [row[:] for row in solution]

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        current_clues = 81
        for r, c in cells:
            if current_clues <= target_clues:
                break

            removed_val = puzzle[r][c]
            puzzle[r][c] = 0

            # Verify uniqueness
            test_board = [row[:] for row in puzzle]
            if cls.count_solutions(test_board) != 1:
                # Restoring cell because removing it causes multiple solutions
                puzzle[r][c] = removed_val
            else:
                current_clues -= 1

        p_id = puzzle_id or f"sudoku_{random.randint(1000, 9999)}"

        return {
            "id": p_id,
            "difficulty": difficulty.capitalize(),
            "clues_count": current_clues,
            "puzzle_grid": puzzle,
            "solution_grid": solution
        }

    @classmethod
    def generate_bulk(
        cls, 
        count: int = 100, 
        difficulty: str = "medium"
    ) -> List[Dict[str, Any]]:
        """Generates a batch of sequential Sudoku puzzles with paired solutions."""
        puzzles = []
        for i in range(count):
            p_id = f"sudoku_{i + 1:04d}"
            puzzle_data = cls.generate_puzzle(difficulty=difficulty, puzzle_id=p_id)
            puzzles.append(puzzle_data)
        return puzzles
