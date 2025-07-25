import cv2
import numpy as np
import csv

# 1) Load the top-down image and convert it to greyscale. 
img = cv2.imread('/Users/alessioborgi/Documents/GitHub/Tohoku_TESP/img/moon_environment_orig.png')
if img is None:
    raise ValueError("Image not found. Check the file path.")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2) Threshold to segment rocks.
threshold_value = 120   
_, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

# 3) Detect contours (rocks).
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 4) Generate an occupancy grid (white=free, black=obstacle). 
occupancy_grid = np.ones_like(gray) * 255  
cv2.drawContours(occupancy_grid, contours, -1, (0), thickness=cv2.FILLED)  

# 5) Apply median filter to remove Salt and Pepper noise.
filtered = cv2.medianBlur(cv2.medianBlur(occupancy_grid, 5), 5)  # 5 is kernel size; use 3, 5, or 7

# 6) Overlay grid for visualization. 
cell_size = 40  
grid_img = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)
for x in range(0, filtered.shape[1], cell_size):
    cv2.line(grid_img, (x, 0), (x, filtered.shape[0]), (0, 255, 0), 1)
for y in range(0, filtered.shape[0], cell_size):
    cv2.line(grid_img, (0, y), (filtered.shape[1], y), (0, 255, 0), 1)
cv2.imwrite('/Users/alessioborgi/Documents/GitHub/Tohoku_TESP/img/occupancy_grid_with_gridlines.png', grid_img)

# 7) Export the occupancy grid as PNG.
cv2.imwrite('/Users/alessioborgi/Documents/GitHub/Tohoku_TESP/img/occupancy_grid.png', filtered)
