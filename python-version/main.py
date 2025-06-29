import cv2 as cv
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Menu, messagebox
from PIL import Image, ImageTk

COIN_CLASSES = [
    {
        "min_size": 300,
        "value": 1.0,
        "label": "1 real",
        "color": (0, 255, 255),
    },  # yellow
    {
        "min_size": 280,
        "value": 0.25,
        "label": "25 centavos",
        "color": (0, 0, 255),
    },  # red
    {
        "min_size": 250,
        "value": 0.5,
        "label": "50 centavos",
        "color": (0, 255, 0),
    },  # green
    {
        "min_size": 220,
        "value": 0.10,
        "label": "10 centavos",
        "color": (255, 255, 255),
    },  # white
    {
        "min_size": 200,
        "value": 0.05,
        "label": "5 centavos",
        "color": (255, 255, 0),
    },  # cyan
]
COIN_UNKNOWN = {"value": 0, "label": "Desconhecida", "color": (128, 128, 128)}


class CoinDetectorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Coin Detector")
        self.master.geometry("1000x700")
        self.image_path = None
        self.cv_img = None
        self.tk_img = None

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
        processed_img, coin_info, total_value = self.process_image(self.cv_img)
        self.annotate_and_show(processed_img, coin_info, total_value)

    def process_image(self, img):
        """Process the image and return annotated image, coin info list, and total value."""
        img_copy = img.copy()
        canny_img = self.preprocess_image(img_copy)
        contours = self.find_coin_contours(canny_img)
        coin_info = self.extract_coin_info(img_copy, contours)
        total_value = sum([info["value"] for info in coin_info])
        return img_copy, coin_info, total_value

    def preprocess_image(self, img):
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        blurred_img = cv.GaussianBlur(gray_img, (5, 5), 5)
        canny_img = cv.Canny(blurred_img, 120, 60)
        kernel = np.ones((3, 3), np.uint8)
        dilated_img = cv.dilate(canny_img, kernel, iterations=2)
        morph_img = cv.morphologyEx(dilated_img, cv.MORPH_CLOSE, kernel)
        return morph_img

    def find_coin_contours(self, morph_img):
        contours, _ = cv.findContours(
            morph_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        return contours

    def extract_coin_info(self, img, contours):
        coin_info = []
        for contour in contours:
            area = cv.contourArea(contour)
            perimeter = cv.arcLength(contour, True)
            epsilon = perimeter * 0.02
            approx = cv.approxPolyDP(contour, epsilon, True)
            x, y, w, h = cv.boundingRect(approx)
            if (
                w > COIN_CLASSES[-1]["min_size"] and h > COIN_CLASSES[-1]["min_size"]
            ):  # Check if width is above minimum size
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv.circle(img, (x + w // 2, y + h // 2), w // 2, (0, 255, 0), 2)
                value, label, color = self.classify_coin_by_size(w, h)
                coin_info.append(
                    {
                        "area": area,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                        "value": value,
                        "label": label,
                        "color": color,
                    }
                )
        return coin_info

    def classify_coin_by_size(self, width, height):
        for coin in COIN_CLASSES:
            if width > coin["min_size"] and height > coin["min_size"]:
                return coin["value"], coin["label"], coin["color"]
        return COIN_UNKNOWN["value"], COIN_UNKNOWN["label"], COIN_UNKNOWN["color"]

    def annotate_and_show(self, img, coin_info, total_value):
        for info in coin_info:
            if info["value"] > 0:
                # Draw filled rectangle behind label for better readability
                label = f"{info['label']}"
                font = cv.FONT_HERSHEY_SIMPLEX
                font_scale = 0.8
                thickness = 2
                text_size, _ = cv.getTextSize(label, font, font_scale, thickness)
                text_w, text_h = text_size
                center_x = info["x"] + info["w"] // 2
                center_y = info["y"] + info["h"] // 2
                rect_x1 = center_x - text_w // 2 - 6
                rect_y1 = center_y - text_h // 2 - 6
                rect_x2 = center_x + text_w // 2 + 6
                rect_y2 = center_y + text_h // 2 + 6
                cv.rectangle(
                    img,
                    (rect_x1, rect_y1),
                    (rect_x2, rect_y2),
                    (0, 0, 0),
                    -1,
                )
                cv.putText(
                    img,
                    label,
                    (center_x - text_w // 2, center_y + text_h // 2 - 4),
                    font,
                    font_scale,
                    info["color"],
                    thickness,
                )
        # Draw a filled rectangle for better visibility of total
        text = f"Total = R${total_value:.2f}"
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        text_size, _ = cv.getTextSize(text, font, font_scale, thickness)
        text_w, text_h = text_size
        x, y = 30, 50
        cv.rectangle(
            img,
            (x - 10, y - text_h - 10),
            (x + text_w + 10, y + 10),
            (0, 0, 0),
            -1,
        )
        cv.rectangle(
            img,
            (x - 10, y - text_h - 10),
            (x + text_w + 10, y + 10),
            (255, 255, 255),
            2,
        )
        cv.putText(
            img,
            text,
            (x, y),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
        )
        self.show_image(img)


if __name__ == "__main__":
    root = Tk()
    app = CoinDetectorGUI(root)
    root.mainloop()
