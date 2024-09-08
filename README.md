# Sudoku Solver with OCR

This project uses Optical Character Recognition (OCR) to read and solve Sudoku puzzles from images. It employs the `TrOCR` model from the `transformers` library to extract numbers from each cell in a Sudoku grid, then solves the puzzle using a backtracking algorithm.

## Overview

The main components of the project include:

1. **Image Splitting**: Splits the Sudoku grid image into individual cell images.
2. **OCR Processing**: Uses `TrOCR` to read numbers from each cell image.
3. **Sudoku Solver**: Uses a backtracking algorithm to solve the Sudoku puzzle.
4. **Output**: Prints both the unsolved and solved Sudoku grids.

## Requirements

- Python 3.x
- PyTorch
- Transformers
- Pillow

You can install the required libraries using pip:

```bash
pip install torch transformers pillow
```

## Files

- `sudoku_solver.py`: The main script that splits the image, performs OCR, solves the puzzle, and cleans up.
- Sample images (`1.png`, `443.png`, `462.png`, `587.png`): Example Sudoku puzzles used for testing.

## Usage

1. **Place the Sudoku Image**: Place your Sudoku puzzle image in the same directory as `sudoku_solver.py` and update the `image_path` variable in the script accordingly.

2. **Run the Script**: Execute the script to process the image and solve the Sudoku puzzle.

    ```bash
    python sudoku_solver.py
    ```

3. **Output**: The script will print the unsolved and solved Sudoku grids to the console. It will also create an output directory for cell images and clean it up after processing.

## Known Limitations

- The script has been tested specifically on images from [sudoku-puzzles.net](https://sudoku-puzzles.net/sudoku-easy/) which have thin line borders between cells. Performance on images with different formats or borders may vary.
- The script was tested on the following sample puzzles: `1.png`, `443.png`, `462.png`, and `587.png`.

## Example

Here is a brief example of how the script processes an image:

1. **Input Sudoku Image**:
   
    ![input image](https://raw.githubusercontent.com/savirsingh/ocr-sudoku-solver/main/examples/587.png)

3. **Output Sudoku Grid**:
    ```
    sudoku board (unsolved):
    3 7 5 . 2 . . 4 9
    . 9 . 5 4 . . . 1
    6 4 . 8 . . 3 2 5
    7 . 3 1 . 5 . 9 4
    . 8 . . 6 . . 3 .
    . 1 6 3 9 7 5 8 .
    . 5 4 7 . 6 2 . 8
    . . . 2 5 4 9 . 6
    2 . 7 9 1 8 4 5 3
    
    solved sudoku grid:
    3 7 5 6 2 1 8 4 9
    8 9 2 5 4 3 7 6 1
    6 4 1 8 7 9 3 2 5
    7 2 3 1 8 5 6 9 4
    5 8 9 4 6 2 1 3 7
    4 1 6 3 9 7 5 8 2
    9 5 4 7 3 6 2 1 8
    1 3 8 2 5 4 9 7 6
    2 6 7 9 1 8 4 5 3
    ```
