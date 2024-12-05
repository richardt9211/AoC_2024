# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:11:13 2024

@author: Richard.Smith
"""

--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?

#%%

import re
import pandas as pd

# Import Day 4 .txt file
file_path = 'C:/Users/Richard.Smith/Downloads/day_04.txt'

# Read the file content
with open(file_path, 'r') as file:
    grid = [line.strip() for line in file.readlines() if line.strip()]

grid[:5]  # Show the first 5 rows to understand the data structure
    
def find_word_in_grid(grid, word):
    rows = len(grid)  # Number of rows in the grid
    cols = len(grid[0])  # Number of columns in the grid
    word_length = len(word)  # Length of the word to search
    total_count = 0  # Initialize count of word occurrences

    # Directions: right, down, diagonal right-down, diagonal left-down
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check each direction for the word
            for dr, dc in directions:
                # Check both forward and reverse word in each direction
                for reverse in (1, -1):
                    current_word = ''
                    # Construct the word from the grid
                    for i in range(word_length):
                        rr = r + i * dr * reverse
                        cc = c + i * dc * reverse
                        if 0 <= rr < rows and 0 <= cc < cols:
                            current_word += grid[rr][cc]
                        else:
                            break
                    # If the constructed word matches, increase the count
                    if current_word == word:
                        total_count += 1

    return total_count

# Define the word to find
word_to_find = "XMAS"

# Call the function and print the number of occurrences
print(find_word_in_grid(grid, word_to_find))

#%%

--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

#%%

def check_xmas(grid, r, c):
    # Check the central character is 'A'
    if grid[r][c] != 'A':
        return False

    # Helper function to safely retrieve characters and avoid IndexError
    def grid_char(x, y):
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            return grid[x][y]
        return None  # Return None if indices are out of range

    # Check diagonal pairs for 'MAS' or 'SAM'
    # First pair (top-left to bottom-right)
    word1 = grid_char(r - 1, c - 1) + grid_char(r + 1, c + 1)
    if word1 not in ['MS', 'SM']:
        return False

    # Second pair (bottom-left to top-right)
    word2 = grid_char(r + 1, c - 1) + grid_char(r - 1, c + 1)
    return word2 in ['MS', 'SM']

def count_x_mas_patterns(grid):
    # Count valid X-MAS patterns
    count = 0
    # Iterate through grid, avoiding the borders
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if check_xmas(grid, r, c):
                count += 1
    return count

# Calculate the total count of valid X-MAS patterns
total_x_mas_count = count_x_mas_patterns(grid)
print('Part 2:', total_x_mas_count)

#%%
import plotly.io as pio
pio.renderers.default = 'browser'
import plotly.graph_objects as go
from manim import *
from typing import List


class SearchVisualization(Scene):
    def construct(self):
        # Input data
        raw_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

        # Prepare the data
        data = [list(row) for row in raw_data.splitlines()]

        grid = self.create_grid(data)

        grid.center()

        # Scale to fit screen, with a bit of padding
        grid.scale(
            min(config.frame_width / grid.width, config.frame_height / grid.height)
            * 0.8
        )

        self.add(grid)

        # Create text for tracking search progress
        search_text = Text("Searching...", font_size=24).to_edge(UP).to_edge(LEFT)
        self.add(search_text)

        # Create text for total matches
        matches = Text("Matches: ", font_size=24).next_to(search_text, DOWN)
        self.add(matches)

        match_num = Integer(0, font_size=24).next_to(matches, RIGHT)
        self.add(match_num)

        xmas_count = self.find_xmas_patterns(
            data, grid, search_text, matches, match_num
        )

        final_count_text = Text(
            f"Total XMAS Patterns Found: {xmas_count}", font_size=24
        ).to_edge(DOWN)
        self.play(FadeOut(search_text), Create(final_count_text))
        self.wait(0.5)

    def create_grid(self, data: List[List[str]]) -> VGroup:
        """Create a grid of squares with letters."""
        grid = VGroup()
        for i, row in enumerate(data):
            for j, letter in enumerate(row):
                square = Square(side_length=0.8).move_to(
                    RIGHT * j + UP * i  # Uses UP * i for correct orientation
                )
                text = Text(letter, font_size=24).move_to(square)
                grid.add(square, text)
        return grid

    def find_xmas_patterns(
        self,
        data: List[List[str]],
        grid: VGroup,
        search_text: Text,
        matches: Text,
        matches_num: Text,
    ) -> int:
        """Find and highlight all XMAS patterns."""
        grid_size = len(data)
        xmas_count = 0

        directions = [
            # (delta row, delta col)
            (0, 1),  # horizontal
            (1, 0),  # vertical
            (1, 1),  # diagonal down-right
            (1, -1),  # diagonal down-left
        ]

        # Words to search for (both forward and backward)
        target_words = ["XMAS", "SAMX"]
        highlight = SurroundingRectangle(grid[0], color=YELLOW, buff=0.05)

        for word_index, word in enumerate(target_words):
            # Update search text for current word
            search_text.become(
                Text(f"Searching for: {word}", font_size=24).to_edge(LEFT).to_edge(UP)
            )
            for i in range(grid_size):
                for j in range(grid_size):
                    current_cell_index = (i * grid_size + j) * 2
                    current_square = grid[current_cell_index]
                    self.play(
                        highlight.animate.move_to(current_square.get_center()),
                        run_time=0.18,
                    )

                    for dr, dc in directions:
                        # Check if pattern fits within grid
                        if 0 <= i + dr * 3 < grid_size and 0 <= j + dc * 3 < grid_size:
                            # Check if current position matches pattern
                            if self.check_pattern(data, i, j, dr, dc, word):
                                # Highlight the pattern with a polygon (surrounding the squares)
                                pattern_squares = self.get_pattern_squares(
                                    grid, i, j, dr, dc, grid_size
                                )

                                # Get the corner points of the surrounding rectangles in the correct order
                                pattern_vertices = self.get_pattern_vertices(
                                    dr, dc, pattern_squares
                                )

                                # Create the polygon
                                pattern_polygon = Polygon(
                                    *pattern_vertices,
                                    color=GREEN,
                                    fill_opacity=0.2,
                                    stroke_width=3,
                                )

                                xmas_count += 1
                                self.play(
                                    Create(pattern_polygon),
                                    matches_num.animate.set_value(xmas_count),
                                )

                                pattern_polygon.set_opacity(0.3)

        return xmas_count

    def check_pattern(
        self,
        data: List[List[str]],
        start_row: int,
        start_col: int,
        delta_row: int,
        delta_col: int,
        target_word: str,
    ) -> bool:
        """Check if a specific pattern exists."""
        for k in range(4):
            row = start_row + k * delta_row
            col = start_col + k * delta_col
            if data[row][col] != target_word[k]:
                return False
        return True

    def get_pattern_squares(
        self,
        grid: VGroup,
        start_row: int,
        start_col: int,
        delta_row: int,
        delta_col: int,
        grid_size: int,
    ) -> VGroup:
        """Get the VGroup of squares for a specific pattern."""
        pattern_squares = VGroup()
        for k in range(4):
            row = start_row + k * delta_row
            col = start_col + k * delta_col
            grid_index = (row * grid_size + col) * 2
            pattern_squares.add(grid[grid_index])
        return pattern_squares

    def get_pattern_vertices(
        self, delta_row: int, delta_col: int, pattern_squares: List[Square]
    ) -> List[np.ndarray]:
        """Get the corner points of the surrounding rectangles in the correct order."""
        pattern_vertices = []

        if delta_row == 0:  # Horizontal
            pattern_vertices.extend(
                [
                    pattern_squares[0].get_corner(UL),
                    pattern_squares[3].get_corner(UR),
                    pattern_squares[3].get_corner(DR),
                    pattern_squares[0].get_corner(DL),
                ]
            )
        elif delta_col == 0:  # Vertical
            pattern_vertices.extend(
                [
                    pattern_squares[0].get_corner(DL),
                    pattern_squares[0].get_corner(DR),
                    pattern_squares[3].get_corner(UR),
                    pattern_squares[3].get_corner(UL),
                ]
            )
        # check if diaonally going right to left
        elif delta_col == -1:  # Diagonal left to right
            pattern_vertices.extend(
                [
                    pattern_squares[0].get_corner(UR),
                    pattern_squares[0].get_corner(DR),
                    pattern_squares[0].get_corner(DL),
                    pattern_squares[-1].get_corner(DL),
                    pattern_squares[-1].get_corner(UL),
                    pattern_squares[-1].get_corner(UR),
                ]
            )
        else:  # Diagonal Left to Right
            pattern_vertices.extend(
                [
                    pattern_squares[0].get_corner(DR),
                    pattern_squares[0].get_corner(DL),
                    pattern_squares[0].get_corner(UL),
                    pattern_squares[-1].get_corner(UL),
                    pattern_squares[-1].get_corner(UR),
                    pattern_squares[-1].get_corner(DR),
                ]
            )

        return pattern_vertices