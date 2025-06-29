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
        self.master.title("Coin & Image Processor")
        self.master.geometry("1200x800")
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
        # Add Image Processing dropdown menu
        processmenu = Menu(menubar, tearoff=0)
        processmenu.add_command(label="Grayscale", command=self.apply_grayscale)
        processmenu.add_command(label="Mean Filter", command=self.apply_mean_filter)
        processmenu.add_command(label="Median Filter", command=self.apply_median_filter)
        processmenu.add_command(
            label="Salt & Pepper Noise", command=self.apply_salt_and_pepper
        )
        processmenu.add_command(label="Roberts Edge", command=self.apply_roberts_edge)
        menubar.add_cascade(label="Image Processing", menu=processmenu)
        master.config(menu=menubar)

        # Image display
        self.img_label = Label(master)
        self.img_label.pack(pady=10)

        # Loading indicator
        self.loading_label = Label(master, text="", fg="blue", font=("Arial", 14))
        self.loading_label.pack(pady=5)

        # Remove processing buttons (now in menu)
        # self.open_btn = Button(master, text="Open Image", command=self.select_image)
        # self.open_btn.pack(side="left", padx=10, pady=10)
        # self.detect_btn = Button(master, text="Detect Coins", command=self.detect_coins)
        # self.detect_btn.pack(side="left", padx=10, pady=10)

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
        self.loading_label.config(text="")
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
        self.loading_label.config(text="Processing...")
        self.master.update_idletasks()
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

    # 3. Construir um programa que irá determinar o valor monetário em imagens de moedas de Real conforme exemplo
    # abaixo. Esta é uma imagem colorida e você precisa construir maneiras de calcular a diferença de valor das moedas.
    # Pode ser usado técnicas como segmentação de cor, análise do tamanho, etc.
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

    def apply_grayscale(self):
        if self.cv_img is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        self.loading_label.config(text="Processing...")
        self.master.update_idletasks()
        img = self.cv_img.copy()
        gray = np.zeros(img.shape[:2], dtype=np.uint8)
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                b, g, r = img[x, y]
                val = int(0.299 * r + 0.587 * g + 0.114 * b)
                gray[x, y] = val
        self.cv_img = cv.merge([gray, gray, gray])
        self.show_image(self.cv_img)

    def apply_mean_filter(self):
        if self.cv_img is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        self.loading_label.config(text="Processing...")
        self.master.update_idletasks()
        img = self.cv_img.copy()
        # Convert to grayscale if not already
        if len(img.shape) == 3:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        h, w = img.shape
        filtered = np.zeros_like(img)
        for x in range(h):
            for y in range(w):
                vals = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w:
                            vals.append(img[nx, ny])
                filtered[x, y] = int(np.mean(vals))
        self.cv_img = cv.merge([filtered, filtered, filtered])
        self.show_image(self.cv_img)

    def apply_median_filter(self):
        if self.cv_img is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        self.loading_label.config(text="Processing...")
        self.master.update_idletasks()
        img = self.cv_img.copy()
        # Convert to grayscale if not already
        if len(img.shape) == 3:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        h, w = img.shape
        filtered = np.zeros_like(img)
        for x in range(h):
            for y in range(w):
                vals = []
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w:
                            vals.append(img[nx, ny])
                filtered[x, y] = int(np.median(vals))
        self.cv_img = cv.merge([filtered, filtered, filtered])
        self.show_image(self.cv_img)

    # 1. O ruído do tipo "sal e pimenta" é um tipo de ruído impulsivo que se manifesta em imagens digitais como pontos
    # esparsos pretos e brancos.
    # Desenvolver uma função para escolher aleatoriamente 5% dos pixels, de uma imagem em escala de cinza, e definir
    # seus valores para 255 (se pixel >127) ou 0 (se pixel ≤ 127) para obter uma imagem corrompida com ruído do tipo sal e
    # pimenta. Implementar também o Filtro da Média e o Filtro da Mediana para serem aplicados em imagens em escala
    # de cinza com o ruído sal e pimenta. Não utilizar bibliotecas prontas disponíveis que realizam o processamento
    # solicitado;
    def apply_salt_and_pepper(self):
        if self.cv_img is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        self.loading_label.config(text="Processing...")
        self.master.update_idletasks()
        img = self.cv_img.copy()
        # Garantir que está em escala de cinza
        if len(img.shape) == 3:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        h, w = img.shape
        noisy = img.copy()
        num_pixels = int(0.05 * h * w)
        # Seleciona 5% dos pixels aleatoriamente
        indices = np.random.choice(h * w, num_pixels, replace=False)
        for idx in indices:
            x = idx // w
            y = idx % w
            noisy[x, y] = 255 if img[x, y] > 127 else 0
        self.cv_img = cv.merge([noisy, noisy, noisy])
        self.show_image(self.cv_img)

    # 2. Pesquisar e implementar apenas um dos seguintes algoritmos para detecção de bordas para uma imagem em
    # escala de cinza (Não utilizar bibliotecas prontas disponíveis que realizam o processamento solicitado):
    # a) Sobel
    # b) Prewitt
    # c) Roberts
    # d) Frei-Chen
    # e) Canny
    def apply_roberts_edge(self):
        if self.cv_img is None:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        self.loading_label.config(text="Processing...")
        self.master.update_idletasks()
        img = self.cv_img.copy()
        # Garantir que está em escala de cinza
        if len(img.shape) == 3:
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        h, w = img.shape
        edge = np.zeros_like(img)
        # Roberts cross operator
        for x in range(h - 1):
            for y in range(w - 1):
                gx = int(img[x, y]) - int(img[x + 1, y + 1])
                gy = int(img[x + 1, y]) - int(img[x, y + 1])
                g = min(255, int(np.sqrt(gx * gx + gy * gy)))
                edge[x, y] = g
        self.cv_img = cv.merge([edge, edge, edge])
        self.show_image(self.cv_img)


if __name__ == "__main__":
    root = Tk()
    app = CoinDetectorGUI(root)
    root.mainloop()
