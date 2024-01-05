
file_path = r'C:\Users\Byung Mu Kang\Desktop\rtd_addon\2023-12-31_23-56-21.png'
ultrarisk_path = r'C:\Users\Byung Mu Kang\Desktop\rtd_addon\ultra.jpg'
# Let's execute the Python code provided by the user to perform ultrarisk matching on the uploaded image.
# We will simulate the ultrarisk image by cropping a portion of the uploaded image.

import cv2
import numpy as np

# Step 1: Load the images
# The file paths are adjusted to the current file system
scene_image_path = file_path
ultralisk_image_path = ultrarisk_path

scene_image = cv2.imread(scene_image_path)
ultralisk_image = cv2.imread(ultralisk_image_path)

# Step 2: Convert both images to grayscale
scene_gray = cv2.cvtColor(scene_image, cv2.COLOR_BGR2GRAY)
ultralisk_gray = cv2.cvtColor(ultralisk_image, cv2.COLOR_BGR2GRAY)

# Step 3: Apply template matching
# Use the method TM_CCOEFF_NORMED for template matching
result = cv2.matchTemplate(scene_gray, ultralisk_gray, cv2.TM_CCOEFF_NORMED)

# Step 4: Use a threshold to determine matches
threshold = 0.7  # This threshold might need adjustment
locations = np.where(result >= threshold)
locations = list(zip(*locations[::-1]))  # Switch x and y coordinates to (x, y)

# Step 5: Draw rectangles on the original scene image
# Assuming Ultralisk size is consistent, get the width and height of the Ultralisk template
ultralisk_w = ultralisk_gray.shape[1]
ultralisk_h = ultralisk_gray.shape[0]

# Create a copy of the scene to draw rectangles on
scene_copy = scene_image.copy()
rectangles = []

# Loop over all the locations where matches were found
for loc in locations:
    rect = [int(loc[0]), int(loc[1]), ultralisk_w, ultralisk_h]
    # Add all the rectangles to the list
    rectangles.append(rect)
    rectangles.append(rect)  # We add each rectangle twice to ensure we can find the group later

# Group rectangles to avoid multiple counts for the same Ultralisk
rectangles, _ = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

# Draw the rectangles on the image
for (x, y, w, h) in rectangles:
    cv2.rectangle(scene_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Step 6: Count the number of rectangles drawn
ultralisk_count = len(rectangles)

# Step 7: Display the count and the annotated scene image
# Since we can't open a window to display the image, we will save it to the file system
annotated_image_path = r'C:\Users\Byung Mu Kang\Desktop\rtd_addon\answer.jpg'
cv2.imwrite(annotated_image_path, scene_copy)

# Return the count and the path to the annotated image
ultralisk_count, annotated_image_path
