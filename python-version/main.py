import cv2 as cv
import numpy as np
from tkinter import filedialog, Tk


# --- Helper to select image file ---
def select_image():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an image")
    root.destroy()
    return file_path


# --- Coin color ranges (HSV) ---
colors = {
    "gold": ((15, 60, 80), (45, 255, 255)),  # Adjusted for Brazilian coins
    "silver": ((0, 0, 120), (180, 60, 255)),  # Adjusted for Brazilian coins
}

# --- Main ---
if __name__ == "__main__":
    img_path = select_image()
    if not img_path:
        print("No image selected.")
        exit()
    orig = cv.imread(img_path)
    if orig is None:
        print("Failed to load image.")
        exit()
    image = orig.copy()

    cv.namedWindow("out", cv.WINDOW_NORMAL)
    cv.resizeWindow("out", 900, 600)
    cv.namedWindow("canny", cv.WINDOW_NORMAL)
    cv.resizeWindow("canny", 500, 50)
    # Removido o trackbar e valores fixos definidos abaixo
    st = 120
    en = 60

    # Processamento de imagem (apenas uma vez)
    image = orig.copy()
    grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(grey, (5, 5), 5)
    canny = cv.Canny(blur, st, en)
    kernel = np.ones((3, 3), np.uint8)
    img_dil = cv.dilate(canny, kernel, iterations=2)
    img_morph = cv.morphologyEx(img_dil, cv.MORPH_CLOSE, kernel)
    contours, _ = cv.findContours(img_morph, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    coins = []
    for i, contour in enumerate(contours):
        area = cv.contourArea(contour)
        perimeter = cv.arcLength(contour, True)
        epsilon = perimeter * 0.02
        approx = cv.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv.boundingRect(approx)
        roi = image[y : y + h, x : x + w]
        if roi.size > 0 and area > 1000:
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.circle(image, (x + w // 2, y + h // 2), w // 2, (0, 255, 0), 2)
            hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
            coin_type = None
            for coin, (lower, upper) in colors.items():
                mask = cv.inRange(hsv_roi, np.array(lower), np.array(upper))
                if np.any(mask):
                    coin_type = coin
                    break
            if coin_type:
                coins.append((coin_type, area, x, y, w, h))
    total = 0
    for coin, area, x, y, w, h in coins:
        # Identificação baseada principalmente em área, depois cor
        print(
            f"Identified coin: {coin}, Area: {area}, Position: ({x}, {y}), Size: ({w}, {h})"
        )
        if w > 300 and h > 300:
            value = 1.0
            label = "1 real"
            color = (0, 255, 255)  # amarelo
        elif w > 280 and h > 280:
            value = 0.25
            label = "25 centavos"
            color = (0, 0, 255)  # vermelho
        elif w > 250 and h > 250:
            value = 0.5
            label = "50 centavos"
            color = (0, 255, 0)  # verde
        elif w > 220 and h > 220:
            value = 0.10
            label = "10 centavos"
            color = (255, 0, 0)  # azul
        elif w > 200 and h > 200:
            value = 0.05
            label = "5 centavos"
            color = (255, 255, 0)  # ciano
        else:
            value = 0
            label = "Desconhecida"
            color = (128, 128, 128)
        total += value
        if value > 0:
            cv.putText(
                image,
                f"{label}",
                (x + w // 2, y + h // 2),
                cv.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )
    cv.putText(
        image,
        f"Total = R${total:.2f}",
        (30, 50),
        cv.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0, 255, 255),
        3,
    )
    cv.imshow("out", image)
    cv.imshow("canny", canny)
    cv.waitKey(0)
    cv.destroyAllWindows()
