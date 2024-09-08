from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os
import shutil
import re

def splitImage(image_path, output_dir):
    # open the sudoku image
    img = Image.open(image_path)
    
    # get image dimensions, assume it's a square
    img_width, img_height = img.size
    
    # size of each cell is 1/9th of the image
    cell_width = img_width // 9
    cell_height = img_height // 9
    
    # make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # loop through each cell and crop/save
    for row in range(9):
        for col in range(9):
            # calculate cell coordinates
            left = col * cell_width
            top = row * cell_height
            right = left + cell_width
            bottom = top + cell_height
            
            # crop the cell from the image
            cell_img = img.crop((left, top, right, bottom))
            
            # save the cell image
            cell_img.save(os.path.join(output_dir, f"cell_{row}_{col}.png"))
    
    print(f"successfully split the sudoku grid into 81 sub-images in {output_dir}")

def printGrid(grid):
    # print the sudoku grid in a readable format
    for row in grid:
        print(' '.join(str(num) if num != 0 else '.' for num in row))
    print()

def isValid(grid, row, col, num):
    # check if num can be placed at (row, col)
    if num in grid[row]:  # check row
        return False
    
    for r in range(9):  # check column
        if grid[r][col] == num:
            return False
    
    # check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == num:
                return False
    
    return True

def findEmpty(grid):
    # find an empty spot in the grid
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None

def solve(grid):
    # solve the sudoku puzzle with backtracking
    empty_location = findEmpty(grid) # find next empty cell
    if not empty_location:
        return True  # solved
    
    row, col = empty_location
    
    for num in range(1, 10):  # numbers 1 to 9, just brute force
        if isValid(grid, row, col, num):
            grid[row][col] = num
            if solve(grid):
                return True
            grid[row][col] = 0  # backtrack bc this doesn't work
    
    return False  # no sol, need to backtrack

# create a 9x9 grid initialized with zeros
grid = [[0 for j in range(9)] for i in range(9)]
#print(grid) # to check if grid is initialized as a proper 2d array

# load OCR model and processor
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
processor.tokenizer.add_tokens(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
processor.tokenizer.model_max_length = 1  # predicting one character
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# path to the sudoku image and output directory
image_path = "587.png" #change this path for a new image
output_dir = "sudoku_cells"
splitImage(image_path, output_dir)

# process each cell image and update the grid
for i in range(9):
    for j in range(9):
        image_source = f"sudoku_cells/cell_{i}_{j}.png"

        try:
            # open and process the image
            image = Image.open(image_source).convert("RGB")
            pixel_values = processor(image, return_tensors="pt").pixel_values
            generated_ids = model.generate(pixel_values)
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # extract and clean text
            cleaned_text = re.sub(r'[^\d\s]', '', generated_text)
            num = int(cleaned_text.split()[0])
            if num <= 9:
                grid[i][j] = num
                #print(i, j, "done") # for debugging

        except Exception as e:
            # usually this is just if string is empty, which generally implies that the cell is empty
            #print(f"an error occurred: {e}") # for debugging
            pass

print("sudoku board (unsolved):")
printGrid(grid)

# solve and print the solved sudoku grid
if solve(grid):
    print("solved sudoku grid:")
    printGrid(grid)
else:
    print("no solution exists.")
    
# clean up the output directory
shutil.rmtree('sudoku_cells')
