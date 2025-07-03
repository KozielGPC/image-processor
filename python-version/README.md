# Python Version - Image Processing

This directory contains a Python application for image processing and coin detection, complementing the main Java project.

## Application Overview
This application provides a graphical interface (GUI) for:
- Detecting and classifying Brazilian Real coins in images, calculating their total value.
- Applying various image processing operations, including grayscale conversion, noise addition, filtering, and edge detection.

## Features & Functionalities

### 1. Coin Detection and Classification
- **Detects coins** in an input image using contour analysis and size heuristics.
- **Classifies coins** by size into: 1 real, 50 centavos, 25 centavos, 10 centavos, 5 centavos.
- **Annotates** each coin with its value and color code.
- **Calculates and displays** the total monetary value of all detected coins.

### 2. Image Processing Operations
Accessible from the "Image Processing" menu:
- **Grayscale Conversion**: Converts the image to grayscale using a weighted sum of RGB channels.
- **Salt & Pepper Noise**: Randomly corrupts 5% of pixels, setting them to black or white based on intensity.
- **Mean Filter**: Applies a 3x3 mean filter to reduce noise (implemented manually, not using OpenCV's built-in functions).
- **Median Filter**: Applies a 3x3 median filter to reduce impulsive noise (also implemented manually).
- **Roberts Edge Detection**: Detects edges using the Roberts cross operator (manual implementation).

### 3. GUI Features
- **Open Image**: Load JPG or PNG images for processing.
- **Display**: Shows the original and processed images with annotations.
- **Menu-driven**: All functionalities are accessible via the menu bar.

## File Structure
- `main.py`: Main application with all functionalities and GUI.
- `requirements.txt`: Python dependencies.
- `README.md`: This documentation.

## How to Use

1. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
2. **Run the application**
   ```powershell
   python main.py
   ```
3. **Load an image** using the "File > Open Image" menu.
4. **Apply operations** using the "Detect" or "Image Processing" menus.

## Requirements
- Python 3.7+
- See `requirements.txt` for required packages

## Implementation Notes
- All filters and edge detection are implemented from scratch (not using OpenCV's ready-made functions), as required by the assignment.
- The coin detection logic uses contour area and bounding box size to classify coins.
- The GUI is built with Tkinter and uses OpenCV and Pillow for image handling.

## Extending the Application
- Add new filters or processing functions in `main.py`.
- Update the GUI menu to include new features.

## Contact
For questions or contributions, please contact the project maintainer.
