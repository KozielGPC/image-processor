import cv2 as cv
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Menu, messagebox
from PIL import Image, ImageTk
import os


# --- Coin color ranges (HSV) ---
colors = {
    "gold": ((15, 60, 80), (45, 255, 255)),  # Adjusted for Brazilian coins
    "silver": ((0, 0, 120), (180, 60, 255)),  # Adjusted for Brazilian coins
}


class CoinDetectorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Coin Detector")
        self.master.geometry("1000x700")
        self.image_path = None
        self.cv_img = None
        self.tk_img = None
        self.result_img = None

        # Menu
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Image", command=self.select_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        detectmenu = Menu(menubar, tearoff=0)
        detectmenu.add_command(label="Detect Coins", command=self.detect_coins)
        menubar.add_cascade(label="Detect", menu=detectmenu)
        master.config(menu=menubar)

        # Image display
        self.img_label = Label(master)
        self.img_label.pack(pady=10)

        # Buttons
        self.open_btn = Button(master, text="Open Image", command=self.select_image)
        self.open_btn.pack(side="left", padx=10, pady=10)
        self.detect_btn = Button(master, text="Detect Coins", command=self.detect_coins)
        self.detect_btn.pack(side="left", padx=10, pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")],
        )
        if file_path:
            self.image_path = file_path
            self.cv_img = cv.imread(file_path)
            if self.cv_img is None:
                messagebox.showerror("Error", "Failed to load image.")
                return
            self.show_image(self.cv_img)

    def show_image(self, img):
        # Resize for display
        img_disp = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        h, w = img_disp.shape[:2]
        scale = min(900 / w, 600 / h, 1)
        img_disp = cv.resize(img_disp, (int(w * scale), int(h * scale)))
        im_pil = Image.fromarray(img_disp)
        self.tk_img = ImageTk.PhotoImage(im_pil)
        self.img_label.config(image=self.tk_img)
        self.img_label.image = self.tk_img

    def detect_coins(self):
        if self.cv_img is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        image = self.cv_img.copy()
        orig = image.copy()
        st = 120
        en = 60
        grey = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(grey, (5, 5), 5)
        canny = cv.Canny(blur, st, en)
        kernel = np.ones((3, 3), np.uint8)
        img_dil = cv.dilate(canny, kernel, iterations=2)
        img_morph = cv.morphologyEx(img_dil, cv.MORPH_CLOSE, kernel)
        contours, _ = cv.findContours(
            img_morph, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
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
        # Draw a filled rectangle for better visibility
        text = f"Total = R${total:.2f}"
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        text_size, _ = cv.getTextSize(text, font, font_scale, thickness)
        text_w, text_h = text_size
        x, y = 30, 50
        # Draw filled rectangle (black background)
        cv.rectangle(
            image,
            (x - 10, y - text_h - 10),
            (x + text_w + 10, y + 10),
            (0, 0, 0),
            -1,
        )
        # Draw white border
        cv.rectangle(
            image,
            (x - 10, y - text_h - 10),
            (x + text_w + 10, y + 10),
            (255, 255, 255),
            2,
        )
        # Draw the text (white)
        cv.putText(
            image,
            text,
            (x, y),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
        )
        self.show_image(image)


if __name__ == "__main__":
    root = Tk()
    app = CoinDetectorGUI(root)
    root.mainloop()
