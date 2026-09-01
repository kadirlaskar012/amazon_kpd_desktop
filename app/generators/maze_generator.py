"""
Maze Generation & Solver Engine.
Generates rectangular mazes using Depth-First Search with backtracking.
Guarantees a solvable path from Start to Finish with solution path coordinates.
"""

import random
from typing import List, Tuple, Dict, Any, Optional


class MazeGenerator:
    # Wall bitmasks: Top=1, Right=2, Bottom=4, Left=8
    N, E, S, W = 1, 2, 4, 8
    DX = {E: 1, W: -1, N: 0, S: 0}
    DY = {E: 0, W: 0, N: -1, S: 1}
    OPPOSITE = {E: W, W: E, N: S, S: N}

    @classmethod
    def generate_maze(
        cls, 
        width: int = 15, 
        height: int = 20, 
        maze_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a perfect maze of width x height cells.
        Returns grid walls, start/finish coords, and solution path.
        """
        grid = [[0 for _ in range(width)] for _ in range(height)]
        visited = [[False for _ in range(width)] for _ in range(height)]

        def walk(cx: int, cy: int):
            visited[cy][cx] = True
            directions = [cls.N, cls.E, cls.S, cls.W]
            random.shuffle(directions)

            for d in directions:
                nx, ny = cx + cls.DX[d], cy + cls.DY[d]
                if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                    grid[cy][cx] |= d
                    grid[ny][nx] |= cls.OPPOSITE[d]
                    walk(nx, ny)

        # Generate from top-left (0,0)
        walk(0, 0)

        start_pos = (0, 0)
        finish_pos = (width - 1, height - 1)

        # Find solution path using BFS
        solution_path = cls._solve_maze(grid, width, height, start_pos, finish_pos)

        m_id = maze_id or f"maze_{random.randint(1000, 9999)}"

        return {
            "id": m_id,
            "width": width,
            "height": height,
            "start": start_pos,
            "finish": finish_pos,
            "grid": grid,
            "solution_path": solution_path
        }

    @classmethod
    def _solve_maze(
        cls, 
        grid: List[List[int]], 
        width: int, 
        height: int, 
        start: Tuple[int, int], 
        finish: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """Finds the shortest path from start to finish in the maze."""
        queue = [[start]]
        seen = {start}

        while queue:
            path = queue.pop(0)
            cx, cy = path[-1]

            if (cx, cy) == finish:
                return path

            for d in (cls.N, cls.E, cls.S, cls.W):
                if grid[cy][cx] & d:
                    nx, ny = cx + cls.DX[d], cy + cls.DY[d]
                    if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        queue.append(path + [(nx, ny)])
        return []

    @classmethod
    def generate_bulk(
        cls,
        count: int = 10,
        width: int = 15,
        height: int = 20
    ) -> List[Dict[str, Any]]:
        """Generates a batch of unique mazes with sequential IDs."""
        mazes = []
        for i in range(count):
            m_id = f"maze_{i + 1:04d}"
            m = cls.generate_maze(width=width, height=height, maze_id=m_id)
            mazes.append(m)
        return mazes
