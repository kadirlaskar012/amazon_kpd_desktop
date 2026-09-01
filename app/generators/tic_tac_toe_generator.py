"""
Tic-Tac-Toe Game Page Layout Generator Engine.
Generates multi-game printable layouts with customizable grids, game numbering, player tags, and score blocks.
Supports 1, 2, 4, and 6 games per page.
"""

from typing import List, Dict, Any, Optional


class TicTacToeGenerator:
    @staticmethod
    def generate_game_item(
        game_num: int,
        grid_size: int = 3,
        show_player_labels: bool = True,
        show_winner_box: bool = True,
        show_date: bool = False
    ) -> Dict[str, Any]:
        """Generates metadata and structure for an individual Tic-Tac-Toe game item."""
        game_id = f"ttt_{game_num:04d}"
        return {
            "id": game_id,
            "game_number": game_num,
            "title": f"Game #{game_num:03d}",
            "grid_size": grid_size,
            "player_x_label": "Player X: ____________________",
            "player_o_label": "Player O: ____________________",
            "winner_label": "Winner: [ X ]  [ O ]  [ Tie ]",
            "date_label": "Date: ____________",
            "show_player_labels": show_player_labels,
            "show_winner_box": show_winner_box,
            "show_date": show_date
        }

    @classmethod
    def generate_page_layout(
        cls,
        start_game_num: int = 1,
        games_per_page: int = 4,
        grid_size: int = 3,
        page_w_pt: float = 612.0,
        page_h_pt: float = 792.0,
        margin_in: float = 0.5
    ) -> Dict[str, Any]:
        """
        Calculates precise coordinate boxes for games on a single page.
        """
        margin_pt = margin_in * 72.0
        usable_w = page_w_pt - (margin_pt * 2)
        usable_h = page_h_pt - (margin_pt * 2)

        games = []
        if games_per_page == 1:
            # 1 big game
            box_w = usable_w * 0.85
            box_h = usable_h * 0.85
            box_x = margin_pt + (usable_w - box_w) / 2.0
            box_y = margin_pt + (usable_h - box_h) / 2.0
            game_data = cls.generate_game_item(start_game_num, grid_size)
            game_data["bounds"] = {"x": box_x, "y": box_y, "w": box_w, "h": box_h}
            games.append(game_data)

        elif games_per_page == 2:
            # 2 games stacked vertically
            box_w = usable_w * 0.85
            box_h = (usable_h - 40) / 2.0
            for i in range(2):
                box_x = margin_pt + (usable_w - box_w) / 2.0
                box_y = margin_pt + (i * (box_h + 40))
                game_data = cls.generate_game_item(start_game_num + i, grid_size)
                game_data["bounds"] = {"x": box_x, "y": box_y, "w": box_w, "h": box_h}
                games.append(game_data)

        elif games_per_page == 6:
            # 3 rows x 2 columns
            cols, rows = 2, 3
            spacing_x = 24.0
            spacing_y = 30.0
            box_w = (usable_w - ((cols - 1) * spacing_x)) / cols
            box_h = (usable_h - ((rows - 1) * spacing_y)) / rows
            for r in range(rows):
                for c in range(cols):
                    idx = (r * cols) + c
                    box_x = margin_pt + (c * (box_w + spacing_x))
                    box_y = margin_pt + (r * (box_h + spacing_y))
                    game_data = cls.generate_game_item(start_game_num + idx, grid_size)
                    game_data["bounds"] = {"x": box_x, "y": box_y, "w": box_w, "h": box_h}
                    games.append(game_data)

        else:
            # Default: 4 games per page (2x2 grid)
            cols, rows = 2, 2
            spacing_x = 30.0
            spacing_y = 36.0
            box_w = (usable_w - ((cols - 1) * spacing_x)) / cols
            box_h = (usable_h - ((rows - 1) * spacing_y)) / rows
            for r in range(rows):
                for c in range(cols):
                    idx = (r * cols) + c
                    box_x = margin_pt + (c * (box_w + spacing_x))
                    box_y = margin_pt + (r * (box_h + spacing_y))
                    game_data = cls.generate_game_item(start_game_num + idx, grid_size)
                    game_data["bounds"] = {"x": box_x, "y": box_y, "w": box_w, "h": box_h}
                    games.append(game_data)

        return {
            "games_per_page": games_per_page,
            "games": games
        }

    @classmethod
    def generate_bulk(
        cls,
        total_games: int = 100,
        games_per_page: int = 4,
        grid_size: int = 3
    ) -> List[Dict[str, Any]]:
        """Generates a sequence of pages covering the requested number of total games."""
        pages = []
        current_game_num = 1
        page_index = 1

        while current_game_num <= total_games:
            games_on_this_page = min(games_per_page, total_games - current_game_num + 1)
            page_data = cls.generate_page_layout(
                start_game_num=current_game_num,
                games_per_page=games_per_page,
                grid_size=grid_size
            )
            page_data["page_number"] = page_index
            pages.append(page_data)
            current_game_num += games_per_page
            page_index += 1

        return pages
