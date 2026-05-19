import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageOps, ImageTk

from helper import GeometryAlgorithm, ImageLoader


PREVIEW_SIZE = (260, 260)
DEFAULT_IMAGE_PATH = os.path.join("image", "image.png")


class GeometryPreviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometry Transformation Viewer")
        self.root.geometry("1120x860")
        self.root.minsize(980, 720)

        self.image_loader = ImageLoader()
        self.current_image_path = None
        self.original_image = None
        self.algorithm_manager = None
        self.preview_refs = {}

        self.offset_x_var = tk.StringVar(value="100")
        self.offset_y_var = tk.StringVar(value="100")
        self.scale_x_var = tk.StringVar(value="2.0")
        self.scale_y_var = tk.StringVar(value="2.0")
        self.angle_var = tk.StringVar(value="45")
        self.expand_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Choose an image to begin.")

        self.preview_widgets = {}

        self._build_layout()
        self._load_default_image()

    def _build_layout(self):
        main_frame = ttk.Frame(self.root, padding=16)
        main_frame.pack(fill="both", expand=True)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x")

        ttk.Label(
            header_frame,
            text="Geometry Transformation Viewer",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            header_frame,
            text="Preview the base image and every geometry algorithm in one window.",
        ).pack(anchor="w", pady=(4, 0))

        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding=12)
        controls_frame.pack(fill="x", pady=(16, 12))

        ttk.Button(controls_frame, text="Open Image", command=self.choose_image).grid(
            row=0, column=0, padx=(0, 12), pady=6, sticky="w"
        )
        ttk.Button(controls_frame, text="Refresh Preview", command=self.refresh_previews).grid(
            row=0, column=1, padx=(0, 18), pady=6, sticky="w"
        )

        self.path_label = ttk.Label(controls_frame, text="No image selected.")
        self.path_label.grid(row=0, column=2, columnspan=6, pady=6, sticky="w")

        ttk.Label(controls_frame, text="Offset X").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(controls_frame, textvariable=self.offset_x_var, width=10).grid(
            row=1, column=1, sticky="w", padx=(0, 16), pady=6
        )

        ttk.Label(controls_frame, text="Offset Y").grid(row=1, column=2, sticky="w", pady=6)
        ttk.Entry(controls_frame, textvariable=self.offset_y_var, width=10).grid(
            row=1, column=3, sticky="w", padx=(0, 16), pady=6
        )

        ttk.Label(controls_frame, text="Scale X").grid(row=1, column=4, sticky="w", pady=6)
        ttk.Entry(controls_frame, textvariable=self.scale_x_var, width=10).grid(
            row=1, column=5, sticky="w", padx=(0, 16), pady=6
        )

        ttk.Label(controls_frame, text="Scale Y").grid(row=1, column=6, sticky="w", pady=6)
        ttk.Entry(controls_frame, textvariable=self.scale_y_var, width=10).grid(
            row=1, column=7, sticky="w", pady=6
        )

        ttk.Label(controls_frame, text="Angle").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(controls_frame, textvariable=self.angle_var, width=10).grid(
            row=2, column=1, sticky="w", padx=(0, 16), pady=6
        )

        ttk.Checkbutton(
            controls_frame,
            text="Expand rotation canvas",
            variable=self.expand_var,
            command=self.refresh_previews,
        ).grid(row=2, column=2, columnspan=3, sticky="w", pady=6)

        ttk.Label(main_frame, textvariable=self.status_var).pack(anchor="w", pady=(0, 12))

        gallery_frame = ttk.Frame(main_frame)
        gallery_frame.pack(fill="both", expand=True)

        previews = [
            ("Original Image", "Base image"),
            ("Horizontal Reflection", "Flip top to bottom"),
            ("Vertical Reflection", "Flip left to right"),
            ("Translation", "Shift image position"),
            ("Scaling", "Resize using scale factors"),
            ("Rotation", "Rotate around image center"),
        ]

        for index, (title, default_caption) in enumerate(previews):
            card = ttk.LabelFrame(gallery_frame, text=title, padding=12)
            row = index // 3
            column = index % 3
            card.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")

            image_label = ttk.Label(card, anchor="center")
            image_label.pack(fill="both", expand=True)

            caption_label = ttk.Label(card, text=default_caption, wraplength=260, justify="center")
            caption_label.pack(fill="x", pady=(10, 0))

            self.preview_widgets[title] = (image_label, caption_label)

        for column in range(3):
            gallery_frame.columnconfigure(column, weight=1)
        for row in range(2):
            gallery_frame.rowconfigure(row, weight=1)

        self.root.bind("<Return>", lambda _event: self.refresh_previews())

    def _load_default_image(self):
        if os.path.exists(DEFAULT_IMAGE_PATH):
            self.load_image(DEFAULT_IMAGE_PATH)

    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff"),
                ("All files", "*.*"),
            ],
        )
        if file_path:
            self.load_image(file_path)

    def load_image(self, image_path):
        try:
            self.original_image = self.image_loader.load_image(image_path)
            self.algorithm_manager = GeometryAlgorithm(self.original_image)
            self.current_image_path = image_path
            self.path_label.config(text=os.path.abspath(image_path))
            self.status_var.set(
                f"Loaded '{os.path.basename(image_path)}' ({self.original_image.width}x{self.original_image.height})."
            )
            self.refresh_previews()
        except Exception as exc:
            messagebox.showerror("Image Load Error", f"Could not load image:\n{exc}")
            self.status_var.set("Failed to load the selected image.")

    def _read_parameters(self):
        try:
            return {
                "offset_x": int(self.offset_x_var.get()),
                "offset_y": int(self.offset_y_var.get()),
                "scale_x": float(self.scale_x_var.get()),
                "scale_y": float(self.scale_y_var.get()),
                "angle": float(self.angle_var.get()),
                "expand": self.expand_var.get(),
            }
        except ValueError as exc:
            raise ValueError("Please enter valid numeric values for the transformation settings.") from exc

    def refresh_previews(self):
        if not self.algorithm_manager:
            return

        try:
            params = self._read_parameters()
            previews = {
                "Original Image": (
                    self.original_image,
                    f"Base image\n{self.original_image.width}x{self.original_image.height}",
                ),
                "Horizontal Reflection": (
                    self.algorithm_manager.horizontal_reflection(),
                    "Flip top to bottom",
                ),
                "Vertical Reflection": (
                    self.algorithm_manager.vertical_reflection(),
                    "Flip left to right",
                ),
                "Translation": (
                    self.algorithm_manager.translation(params["offset_x"], params["offset_y"]),
                    f"Offset X = {params['offset_x']}, Offset Y = {params['offset_y']}",
                ),
                "Scaling": (
                    self.algorithm_manager.scaling(params["scale_x"], params["scale_y"]),
                    f"Scale X = {params['scale_x']}, Scale Y = {params['scale_y']}",
                ),
                "Rotation": (
                    self.algorithm_manager.rotation(params["angle"], expand=params["expand"]),
                    f"Angle = {params['angle']}°, Expand = {'Yes' if params['expand'] else 'No'}",
                ),
            }

            for title, (image, caption) in previews.items():
                self._update_preview(title, image, caption)

            self.status_var.set("Preview updated successfully.")
        except Exception as exc:
            self.status_var.set(f"Preview update failed: {exc}")
            messagebox.showerror("Preview Error", str(exc))

    def _update_preview(self, title, image, caption):
        preview_image = self._build_preview_image(image)
        photo = ImageTk.PhotoImage(preview_image)

        image_label, caption_label = self.preview_widgets[title]
        image_label.config(image=photo)
        caption_label.config(text=caption)

        self.preview_refs[title] = photo

    def _build_preview_image(self, image):
        display_image = image.convert("RGBA")
        fitted_image = ImageOps.contain(display_image, PREVIEW_SIZE, Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", PREVIEW_SIZE, (245, 245, 245, 255))
        x_offset = (PREVIEW_SIZE[0] - fitted_image.width) // 2
        y_offset = (PREVIEW_SIZE[1] - fitted_image.height) // 2
        canvas.paste(fitted_image, (x_offset, y_offset), fitted_image)

        return canvas


def main():
    root = tk.Tk()
    GeometryPreviewApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
