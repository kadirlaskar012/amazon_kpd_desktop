"""
Unit tests for all puzzle & game generator engines:
- Sudoku Generator
- Tic-Tac-Toe Generator
- Maze Generator
- Word Search Generator
"""

import pytest
from app.generators.sudoku_generator import SudokuGenerator
from app.generators.tic_tac_toe_generator import TicTacToeGenerator
from app.generators.maze_generator import MazeGenerator
from app.generators.word_search_generator import WordSearchGenerator


def test_sudoku_generation_and_uniqueness():
    puzzle = SudokuGenerator.generate_puzzle(difficulty="easy", puzzle_id="sudoku_test_1")
    assert puzzle["id"] == "sudoku_test_1"
    assert len(puzzle["puzzle_grid"]) == 9
    assert len(puzzle["solution_grid"]) == 9
    assert 30 <= puzzle["clues_count"] <= 45

    # Verify that solution grid has no zeroes and satisfies Sudoku constraints
    solution = puzzle["solution_grid"]
    for row in solution:
        assert len(row) == 9
        assert set(row) == set(range(1, 10))

    for col_idx in range(9):
        col = [solution[r][col_idx] for r in range(9)]
        assert set(col) == set(range(1, 10))


def test_tic_tac_toe_generator():
    pages = TicTacToeGenerator.generate_bulk(total_games=12, games_per_page=4, grid_size=3)
    assert len(pages) == 3
    assert len(pages[0]["games"]) == 4
    assert pages[0]["games"][0]["game_number"] == 1
    assert "bounds" in pages[0]["games"][0]


def test_maze_generator():
    maze = MazeGenerator.generate_maze(width=10, height=10, maze_id="maze_test_1")
    assert maze["id"] == "maze_test_1"
    assert len(maze["grid"]) == 10
    assert len(maze["grid"][0]) == 10
    assert len(maze["solution_path"]) > 0
    assert maze["solution_path"][0] == (0, 0)
    assert maze["solution_path"][-1] == (9, 9)


def test_word_search_generator():
    words = ["APPLE", "BANANA", "ORANGE", "MANGO", "GRAPES"]
    ws = WordSearchGenerator.generate_puzzle(words=words, grid_size=12, puzzle_id="ws_test_1")
    assert ws["id"] == "ws_test_1"
    assert len(ws["grid"]) == 12
    assert len(ws["grid"][0]) == 12
    assert len(ws["words"]) == 5
    for placed in ws["placed_details"]:
        assert placed["word"] in words
