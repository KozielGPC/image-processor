# Image Processing Application

This project is a Java-based desktop application for performing various image processing tasks. It provides a graphical user interface (GUI) to load, manipulate, and save images with different effects and transformations.

## Features

- **Open and Save Images**: Load images in various formats (BMP, JPG, PNG, GIF) and save them after processing.
- **Image Effects**:
  - Negative Effect
  - Grayscale Effect
  - Transparency Gradient
  - Color Segmentation
- **Image Transformations**:
  - Rotate Clockwise and Counter-Clockwise (90°)
  - Flip Vertically and Horizontally
- **Transparency with Two Images**: Blend two images with adjustable transparency.

## How to Run

1. Open the project in a Java IDE (e.g., NetBeans, IntelliJ IDEA, Eclipse).
2. Build the project using the provided `build.xml` file or your IDE's build tools.
3. Run the `NewJFrame` class to launch the application.

## Folder Structure

- **src/**: Contains the source code of the application.
  - `NewJFrame.java`: Main class for the GUI and image processing logic.
- **images/**: Sample images for testing the application.
- **build/**: Compiled classes and build artifacts.
- **nbproject/**: NetBeans project configuration files.

## Requirements

- Java Development Kit (JDK) 8 or higher
- A Java IDE or build tool (e.g., Apache Ant)

## Usage

1. Launch the application.
2. Use the "File" menu to open an image.
3. Apply effects or transformations using the "Image" menu.
4. Save the processed image using the "File" menu.

## Method Implementations

### `applyNegativeEffect`
This method iterates through each pixel of the image, inverts the RGB values, and updates the image with the negative effect. The inversion is calculated as:
```
Red = 255 - Red
Green = 255 - Green
Blue = 255 - Blue
```
This creates a photographic negative effect.

### `applyGrayscaleEffect`
This method converts each pixel of the image to grayscale by calculating the luminance using the formula:
```
Gray = 0.299 * Red + 0.587 * Green + 0.114 * Blue
```
The resulting grayscale value is applied to all three RGB channels, creating a monochrome image.

### `applyTransparencyEffect`
This method applies a transparency gradient to the image by adjusting the alpha channel of each pixel. The alpha value is calculated based on a slider input, where 0 represents full transparency and 100 represents full opacity. The transparency effect is applied as:
```
Alpha = (1.0 - sliderValue / 100) * 255
```

### `applyTransparencyEffectWithTwoImages`
This method blends two images of the same dimensions by adjusting the alpha value. The blending formula is:
```
R' = R1 * (1 - α) + R2 * α
G' = G1 * (1 - α) + G2 * α
B' = B1 * (1 - α) + B2 * α
```
Where `α` is the transparency level controlled by a slider. This creates a smooth transition between the two images.

### `applyColorSegmentation`
This method segments the image by isolating pixels close to a user-selected target color. The closeness is determined by a threshold value. Pixels within the threshold retain their original color, while others are set to black. The segmentation logic checks if:
```
|Red - TargetRed| <= Threshold
|Green - TargetGreen| <= Threshold
|Blue - TargetBlue| <= Threshold
```
If all conditions are met, the pixel is kept; otherwise, it is set to black.

### `rotateImage90Degrees`
This method rotates the image 90 degrees clockwise or counter-clockwise by rearranging the pixel positions. For clockwise rotation:
```
NewX = Height - OldY - 1
NewY = OldX
```
For counter-clockwise rotation:
```
NewX = OldY
NewY = Width - OldX - 1
```

### `flipImage`
This method flips the image horizontally, vertically, or both. For horizontal flipping:
```
NewX = Width - OldX - 1
NewY = OldY
```
For vertical flipping:
```
NewX = OldX
NewY = Height - OldY - 1
```

### `openPPMImage`
This method allows the user to open and display PPM (Portable Pixmap) images. It reads the PPM file format, extracts pixel data, and converts it into a BufferedImage for display in the application.

### `openPGMImage`
This method allows the user to open and display PGM (Portable Graymap) images. It reads the PGM file format, extracts grayscale pixel data, and converts it into a BufferedImage for display in the application.

## Screenshots

### Main Interface
![image](https://github.com/user-attachments/assets/6b0e6639-6002-406a-8f76-7e00fe557306)

![image](https://github.com/user-attachments/assets/73beb53a-fa5e-4ca4-b793-04c9975b3296)

![image](https://github.com/user-attachments/assets/09a314b5-9b31-44da-a0f2-066429cb533f)

![image](https://github.com/user-attachments/assets/a9f5d2c9-a757-4b31-8d51-4c1591fb652c)

![image](https://github.com/user-attachments/assets/f1595251-eac5-4fd1-88bf-ebb3572f20bc)

### Negative Effect
![image](https://github.com/user-attachments/assets/5698a383-7c82-420f-8e68-c368de3a4291)

![image](https://github.com/user-attachments/assets/cdf1290d-f351-46b9-ac21-8ce4cccc1154)


### Grayscale Effect
![image](https://github.com/user-attachments/assets/7d052108-0981-42fc-9454-ab2628dfed81)

![image](https://github.com/user-attachments/assets/28098445-a958-4d40-b822-577e9e987311)


### Transparency Gradient
![image](https://github.com/user-attachments/assets/bea26481-d88f-4fac-87b9-720886602352)

![image](https://github.com/user-attachments/assets/5157000a-9829-4917-89a1-847cedf0374f)

![image](https://github.com/user-attachments/assets/6fc02d50-4e72-4d70-b2e8-a876ddc60466)

![image](https://github.com/user-attachments/assets/77c30311-ea4f-489b-9eea-173dadfabbd2)

### Color Segmentation
![image](https://github.com/user-attachments/assets/7c78d550-8161-4065-a552-d4fee1f3e1ae)

![image](https://github.com/user-attachments/assets/3662900d-d481-4c73-9e5b-dab99e5065cf)

![image](https://github.com/user-attachments/assets/d55a0f2c-2991-4f0e-92b2-2646c8c03dc9)

![image](https://github.com/user-attachments/assets/7eacd963-10a4-4c60-8518-f4e19d04e4a1)

![image](https://github.com/user-attachments/assets/2a389198-3c29-4363-b28c-6f9cee8e6628)

![image](https://github.com/user-attachments/assets/b6408609-d272-4e6c-a82d-5fcff5b08624)

### Rotate Clockwise
![image](https://github.com/user-attachments/assets/aee1d1fd-9c29-4802-827b-afb96672817e)

![image](https://github.com/user-attachments/assets/f0b0edb7-abf4-4973-9143-13a91ee9400c)

![image](https://github.com/user-attachments/assets/a0d08521-3101-488b-9065-59c3d8620605)

### Rotate Counter-Clockwise
![image](https://github.com/user-attachments/assets/c6acbd64-4970-4603-8c20-66ee647a1d8e)

![image](https://github.com/user-attachments/assets/80dd673a-f451-46cf-beac-2c467f953f74)

![image](https://github.com/user-attachments/assets/86a922fe-a0d5-4e1a-b413-5fd954d7e4ad)

### Flip Vertical
![image](https://github.com/user-attachments/assets/4519fcb5-a21a-410a-a051-192afb2aa64f)

![image](https://github.com/user-attachments/assets/3d5d8b0d-06b3-44d1-bec1-e245004f1c3b)

### Flip Horizontal
![image](https://github.com/user-attachments/assets/11236fca-d8d6-4a7b-9e30-268b0eb45e82)

![image](https://github.com/user-attachments/assets/d31a166b-d29a-4ff2-8f1d-487d8f10f9d6)


### Transparency with Two Images
![image](https://github.com/user-attachments/assets/5f165b8b-0586-4f73-a19d-cca63b17a006)

![image](https://github.com/user-attachments/assets/7e1e5082-d6e3-4d74-a660-c0ded1e9492a)

![image](https://github.com/user-attachments/assets/81a1df69-b2f2-4644-9c79-b29eabc5032c)

![image](https://github.com/user-attachments/assets/77da77ec-b9bd-4ae8-bb5a-1f019a7161c4)

![image](https://github.com/user-attachments/assets/f5d59d56-a319-4116-97fa-8f86f6794cbe)


## License

This project is for educational purposes and does not include a specific license. Feel free to modify and use it as needed.
