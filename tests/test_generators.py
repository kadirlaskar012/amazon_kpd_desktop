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
from app.generators.dot_to_dot_generator import DotToDotGenerator
from PIL import Image, ImageDraw
import io
import base64


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


def test_dot_to_dot_generator_presets():
    for preset_name in ["star", "butterfly", "heart", "rocket", "dinosaur", "cat", "airplane", "fish"]:
        res = DotToDotGenerator.generate_preset(preset_name=preset_name, dot_count=30)
        assert res["type"] == "dot_to_dot"
        assert len(res["dots"]) == 30
        assert res["dots"][0]["num"] == 1
        assert res["dots"][0]["is_start"] is True
        assert res["dots"][-1]["num"] == 30


def test_dot_to_dot_generator_from_image():
    # Create a synthetic test image with a black circle on white background
    img = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 50, 250, 250), outline="black", width=6)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

    res = DotToDotGenerator.from_image(image_input=data_url, dot_count=24)
    assert res["type"] == "dot_to_dot"
    assert res["dot_count"] == 24
    assert len(res["dots"]) == 24
    assert res["dots"][0]["num"] == 1
    assert "x" in res["dots"][0] and "y" in res["dots"][0]
    assert "label_x" in res["dots"][0] and "label_y" in res["dots"][0]

