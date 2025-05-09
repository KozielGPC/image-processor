// Import necessary libraries
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;

public class NewJFrame extends javax.swing.JFrame {

    // Instance variables
    private BufferedImage currentImage; // Stores the currently loaded image
    private boolean isImageDisplayed = false; // Flag to check if an image is displayed
    private JSlider transparencySlider; // Slider for transparency level

    public NewJFrame() {
        initializeComponents();
    }

    // Initialize UI components
    @SuppressWarnings("unchecked")
    private void initializeComponents() {

        imageLabel = new javax.swing.JLabel();
        menuBar = new javax.swing.JMenuBar();
        fileMenu = new javax.swing.JMenu();
        openMenuItem = new javax.swing.JMenuItem();
        saveMenuItem = new javax.swing.JMenuItem();
        exitMenuItem = new javax.swing.JMenuItem();
        imageMenu = new javax.swing.JMenu();
        negativeMenuItem = new javax.swing.JMenuItem();
        grayscaleMenuItem = new javax.swing.JMenuItem();
        transparencyMenuItem = new javax.swing.JMenuItem();
        colorSegmentationMenuItem = new javax.swing.JMenuItem();
        rotateImageClockwiseMenuItem = new javax.swing.JMenuItem();
        rotateImageCounterClockwiseMenuItem = new javax.swing.JMenuItem();
        flipImageVerticalMenuItem = new javax.swing.JMenuItem();
        flipImageHorizontalMenuItem = new javax.swing.JMenuItem();
        transparencyWithTwoImagesMenuItem = new javax.swing.JMenuItem();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        // File menu setup
        fileMenu.setText("File");

        openMenuItem.setText("Open...");
        openMenuItem.addActionListener(evt -> openImage(evt));
        fileMenu.add(openMenuItem);

        saveMenuItem.setText("Save...");
        saveMenuItem.addActionListener(evt -> saveImage(evt));
        fileMenu.add(saveMenuItem);

        exitMenuItem.setText("Exit");
        exitMenuItem.addActionListener(evt -> exitApplication(evt));
        fileMenu.add(exitMenuItem);

        menuBar.add(fileMenu);

        // Image menu setup
        imageMenu.setText("Image");

        negativeMenuItem.setText("Negative");
        negativeMenuItem.addActionListener(evt -> applyNegativeEffect(evt));
        imageMenu.add(negativeMenuItem);

        grayscaleMenuItem.setText("Grayscale");
        grayscaleMenuItem.addActionListener(evt -> applyGrayscaleEffect(evt));
        imageMenu.add(grayscaleMenuItem);

        transparencyMenuItem.setText("Transparency Gradient");
        transparencyMenuItem.addActionListener(evt -> {
            if (transparencySlider == null) {
                transparencySlider = new JSlider(0, 100, 0);
                transparencySlider.setMajorTickSpacing(20);
                transparencySlider.setPaintTicks(true);
                transparencySlider.setPaintLabels(true);
                transparencySlider.addChangeListener(e -> applyTransparencyEffect(transparencySlider.getValue()));
                
                // Add the slider to the frame
                getContentPane().add(transparencySlider, BorderLayout.SOUTH);
                pack();
            }
            transparencySlider.setVisible(true);
        });
        imageMenu.add(transparencyMenuItem);

        colorSegmentationMenuItem.setText("Color Segmentation");
        colorSegmentationMenuItem.addActionListener(evt -> {
            JColorChooser colorChooser = new JColorChooser();
            JDialog colorDialog = JColorChooser.createDialog(this, "Select Target Color", true, colorChooser, e -> {
                Color selectedColor = colorChooser.getColor();
                if (selectedColor != null) {
                    applyColorSegmentation(selectedColor.getRed(), selectedColor.getGreen(), selectedColor.getBlue());
                }
            }, null);

            if (transparencySlider != null) {
                transparencySlider.setVisible(false);
            }

            colorDialog.setVisible(true);
        });
        imageMenu.add(colorSegmentationMenuItem);

        rotateImageClockwiseMenuItem.setText("Rotate Clockwise");
        rotateImageClockwiseMenuItem.addActionListener(evt -> rotateImage90Degrees(true));
        imageMenu.add(rotateImageClockwiseMenuItem);

        rotateImageCounterClockwiseMenuItem.setText("Rotate Counter-Clockwise");
        rotateImageCounterClockwiseMenuItem.addActionListener(evt -> rotateImage90Degrees(false));
        imageMenu.add(rotateImageCounterClockwiseMenuItem);

        flipImageVerticalMenuItem.setText("Flip Vertical");
        flipImageVerticalMenuItem.addActionListener(evt -> flipImage(false, true));
        imageMenu.add(flipImageVerticalMenuItem);

        flipImageHorizontalMenuItem.setText("Flip Horizontal");
        flipImageHorizontalMenuItem.addActionListener(evt -> flipImage(true, false));
        imageMenu.add(flipImageHorizontalMenuItem);

        transparencyWithTwoImagesMenuItem.setText("Transparency with Two Images");
        transparencyWithTwoImagesMenuItem.addActionListener(evt -> {
            JFileChooser fileChooser = new JFileChooser(new File("images"));
            FileNameExtensionFilter filter = new FileNameExtensionFilter("BMP, JPG, PNG & GIF Images", "bmp", "jpg", "png", "gif");
            fileChooser.setFileFilter(filter);
            fileChooser.setDialogTitle("Open Second Image");
            int option = fileChooser.showOpenDialog(this);

            if (option == JFileChooser.APPROVE_OPTION) {
                File selectedFile = fileChooser.getSelectedFile();
                try {
                    BufferedImage secondImage = ImageIO.read(selectedFile);
                    if (currentImage.getWidth() == secondImage.getWidth() && currentImage.getHeight() == secondImage.getHeight()) {
                        applyTransparencyEffectWithTwoImages(currentImage, secondImage);
                    } else {
                        JOptionPane.showMessageDialog(this, "Images must have the same dimensions.", "Error", JOptionPane.ERROR_MESSAGE);
                    }
                } catch (IOException e) {
                    JOptionPane.showMessageDialog(this, "Error loading the second image.", "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        });
        imageMenu.add(transparencyWithTwoImagesMenuItem);

        menuBar.add(imageMenu);

        setJMenuBar(menuBar);

        // Layout setup
        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(imageLabel)
                .addGap(0, 400, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(imageLabel)
                .addGap(0, 279, Short.MAX_VALUE))
        );

        pack();
    }

    // Open image file
    private void openImage(java.awt.event.ActionEvent evt) {
        JFileChooser fileChooser = new JFileChooser(new File("images")); 
        FileNameExtensionFilter filter = new FileNameExtensionFilter("BMP, JPG, PNG & GIF Images", "bmp", "jpg", "png", "gif");
        fileChooser.setFileFilter(filter);
        fileChooser.setDialogTitle("Open Image");
        int option = fileChooser.showOpenDialog(this);

        if (option == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            try {
                currentImage = ImageIO.read(selectedFile);
                displayImage(currentImage, true);
                System.out.println("Image opened successfully!");
            } catch (IOException e) {
                System.out.println("Error: Unable to open the image file.");
            }
        }
    }

    // Save image file
    private void saveImage(java.awt.event.ActionEvent evt) {
        JFileChooser fileChooser = new JFileChooser(new File("images"));	
        FileNameExtensionFilter filter = new FileNameExtensionFilter("JPG Images", "jpg");
        fileChooser.setFileFilter(filter);
        fileChooser.setDialogTitle("Save Image");
        int option = fileChooser.showSaveDialog(this);

        if (option == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            try {
                ImageIO.write(currentImage, "jpg", selectedFile);
                System.out.println("Image saved successfully!");
            } catch (IOException e) {
                System.out.println("Error: Unable to save the image file.");
            }
        }
    }

    // Exit application
    private void exitApplication(java.awt.event.ActionEvent evt) {
        System.exit(0);
    }

    // Apply negative effect to the image
    private void applyNegativeEffect(java.awt.event.ActionEvent evt) {
        int width = currentImage.getWidth();
        int height = currentImage.getHeight();

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                Color originalColor = new Color(currentImage.getRGB(x, y));
                int red = 255 - originalColor.getRed();
                int green = 255 - originalColor.getGreen();
                int blue = 255 - originalColor.getBlue();
                Color negativeColor = new Color(red, green, blue);
                currentImage.setRGB(x, y, negativeColor.getRGB());
            }
        }
        displayImage(currentImage, true);
    }

    // Apply grayscale effect to the image
    private void applyGrayscaleEffect(java.awt.event.ActionEvent evt) {
        int width = currentImage.getWidth();
        int height = currentImage.getHeight();

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                Color originalColor = new Color(currentImage.getRGB(x, y));
                int grayValue = (int) (0.299 * originalColor.getRed() + 0.587 * originalColor.getGreen() + 0.114 * originalColor.getBlue());
                Color grayColor = new Color(grayValue, grayValue, grayValue);
                currentImage.setRGB(x, y, grayColor.getRGB());
            }
        }
        displayImage(currentImage, true);
    }

    // 1. Desenvolver os métodos abaixo:
    // a) Carregar uma imagem no formato RGB e aplicar transparência com a cor preta RGB=(0, 0, 0),
    // alterando gradativamente o valor do (alpha) de 1 até 0. Iniciar com o preto opaco até ficar
    // totalmente transparente permitindo visualizar a imagem carregada.
    private void applyTransparencyEffect(int alphaValue) {
        int width = currentImage.getWidth();
        int height = currentImage.getHeight();
        BufferedImage transparentImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                Color originalColor = new Color(currentImage.getRGB(x, y));
                int alpha = (int) ((1.0 - (double) alphaValue / 100) * 255);
                Color transparentColor = new Color(originalColor.getRed(), originalColor.getGreen(), originalColor.getBlue(), alpha);
                transparentImage.setRGB(x, y, transparentColor.getRGB());
            }
        }

        currentImage = transparentImage;
        displayImage(currentImage, false);
    }

    // 1. b)  Carregar duas imagens no formato RGB, de mesmo tamanho, e sobrepor as imagens alterando
    // gradativamente o valor do (alpha) de 1 até 0. 
    //  Fórmula para mistura:
    //  R’ = R1*(1-α) + R2*α
    //  G’ = G1*(1-α) + G2*α
    //  B’ = B1*(1-α) + B2*α
    // A alteração do valor do α pode ser feita utilizando a opção do menu, ou uma tecla de atalho ou uma
    // função sleep(). 
    private void applyTransparencyEffectWithTwoImages(BufferedImage image1, BufferedImage image2) {
        int width = image1.getWidth();
        int height = image1.getHeight();

        // Create a new frame to display the two images side by side
        JFrame sideBySideFrame = new JFrame("Images Side by Side");
        sideBySideFrame.setLayout(new GridLayout(1, 2));

        JLabel image1Label = new JLabel(new ImageIcon(image1));
        JLabel image2Label = new JLabel(new ImageIcon(image2));

        sideBySideFrame.add(new JScrollPane(image1Label));
        sideBySideFrame.add(new JScrollPane(image2Label));

        sideBySideFrame.pack();
        sideBySideFrame.setVisible(true);

        // Create another frame to display the blended image with a slider
        JFrame blendedFrame = new JFrame("Blended Image");
        blendedFrame.setLayout(new BorderLayout());

        JLabel blendedImageLabel = new JLabel();
        blendedFrame.add(new JScrollPane(blendedImageLabel), BorderLayout.CENTER);

        JSlider alphaSlider = new JSlider(0, 100, 50);
        alphaSlider.setMajorTickSpacing(20);
        alphaSlider.setPaintTicks(true);
        alphaSlider.setPaintLabels(true);

        alphaSlider.addChangeListener(e -> {
            int alphaValue = alphaSlider.getValue();
            BufferedImage blendedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);

            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    Color color1 = new Color(image1.getRGB(x, y));
                    Color color2 = new Color(image2.getRGB(x, y));

                    double alpha = alphaValue / 100.0;
                    int red = (int) (color1.getRed() * (1 - alpha) + color2.getRed() * alpha);
                    int green = (int) (color1.getGreen() * (1 - alpha) + color2.getGreen() * alpha);
                    int blue = (int) (color1.getBlue() * (1 - alpha) + color2.getBlue() * alpha);

                    Color blendedColor = new Color(red, green, blue);
                    blendedImage.setRGB(x, y, blendedColor.getRGB());
                }
            }

            blendedImageLabel.setIcon(new ImageIcon(blendedImage));
        });

        blendedFrame.add(alphaSlider, BorderLayout.SOUTH);
        blendedFrame.pack();
        blendedFrame.setVisible(true);

        // Trigger the initial blending
        alphaSlider.setValue(50);
    }

    // 3. Desenvolver um método para segmentar uma imagem no formato RGB mantendo na imagem os
    // objetos de uma determinada cor e o restante da imagem na cor preta. O usuário deverá entrar com o
    // RGB da cor desejada. 
    private void applyColorSegmentation(int targetRed, int targetGreen, int targetBlue) {
        int width = currentImage.getWidth();
        int height = currentImage.getHeight();
        BufferedImage segmentedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                Color originalColor = new Color(currentImage.getRGB(x, y));
                
                
                int maxValueRed = targetRed + 50;
                int minValueRed = targetRed - 50;
                boolean isCloseToRedColor = originalColor.getRed() >= minValueRed && originalColor.getRed() <= maxValueRed;

                int maxValueGreen = targetGreen + 50;
                int minValueGreen = targetGreen - 50;
                boolean isCloseToGreenColor = originalColor.getGreen() >= minValueGreen && originalColor.getGreen() <= maxValueGreen;

                int maxValueBlue = targetBlue + 50;
                int minValueBlue = targetBlue - 50;
                boolean isCloseToBlueColor = originalColor.getBlue() >= minValueBlue && originalColor.getBlue() <= maxValueBlue;

                boolean isCloseToTargetColor = isCloseToRedColor && isCloseToGreenColor && isCloseToBlueColor;
                if (isCloseToTargetColor) {
                    segmentedImage.setRGB(x, y, originalColor.getRGB());
                } else {
                    segmentedImage.setRGB(x, y, Color.BLACK.getRGB());
                }
            }
        }

        currentImage = segmentedImage;
        displayImage(currentImage, true);
    }

    // 4. 1) Rotação da imagem no sentido horário e anti-horário (com ângulos de 90º);
    private void rotateImage90Degrees(boolean clockwise) {
        int width = currentImage.getWidth();
        int height = currentImage.getHeight();

        // Necessário para quando imagem não for quadrada
        BufferedImage rotatedImage = new BufferedImage(height, width, BufferedImage.TYPE_INT_RGB);

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if (clockwise) {
                    rotatedImage.setRGB(height - y - 1, x, currentImage.getRGB(x, y)); // Rotate 90 degrees clockwise
                } else {
                    rotatedImage.setRGB(y, width - x - 1, currentImage.getRGB(x, y)); // Rotate 90 degrees counter-clockwise
                }
            }
        }

        currentImage = rotatedImage;
        displayImage(currentImage, true);
    }

    // 4. 3. Espelhamento vertical e horizontal; 
    private void flipImage(boolean horizontal, boolean vertical) {
        int width = currentImage.getWidth();
        int height = currentImage.getHeight();

        BufferedImage segmentedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if(horizontal) {
                    segmentedImage.setRGB(width - x - 1, y, currentImage.getRGB(x, y)); // Horizontal flip
                }
                if(vertical) {
                    segmentedImage.setRGB(x, height - y - 1, currentImage.getRGB(x, y)); // Vertical flip
                }
            }
        }

        currentImage = segmentedImage;
        displayImage(currentImage, true);
    }

    // Display the image on the JLabel
    private void displayImage(BufferedImage image, boolean resize) {
        ImageIcon icon = new ImageIcon(image);
        if (!isImageDisplayed) {
            imageLabel.setIcon(icon);
            Container contentPane = getContentPane();
            contentPane.setLayout(new GridLayout());
            contentPane.add(new JScrollPane(imageLabel));
            isImageDisplayed = true;
        } else {
            imageLabel.setIcon(icon);
        }
        if (resize) {
            setSize(image.getWidth() + 25, image.getHeight() + 70);
        }
    }

    // Main method to run the application
    public static void main(String[] args) {
        java.awt.EventQueue.invokeLater(() -> new NewJFrame().setVisible(true));
    }

    // Variables declaration
    private javax.swing.JLabel imageLabel;
    private javax.swing.JMenuBar menuBar;
    private javax.swing.JMenu fileMenu;
    private javax.swing.JMenu imageMenu;
    private javax.swing.JMenuItem openMenuItem;
    private javax.swing.JMenuItem saveMenuItem;
    private javax.swing.JMenuItem exitMenuItem;
    private javax.swing.JMenuItem negativeMenuItem;
    private javax.swing.JMenuItem grayscaleMenuItem;
    private javax.swing.JMenuItem transparencyMenuItem;
    private javax.swing.JMenuItem colorSegmentationMenuItem;
    private javax.swing.JMenuItem rotateImageClockwiseMenuItem;
    private javax.swing.JMenuItem rotateImageCounterClockwiseMenuItem;
    private javax.swing.JMenuItem flipImageVerticalMenuItem;
    private javax.swing.JMenuItem flipImageHorizontalMenuItem;
    private javax.swing.JMenuItem transparencyWithTwoImagesMenuItem;
}
