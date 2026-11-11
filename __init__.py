import math
import os

import numpy as np
import torch
from PIL import Image, ImageOps
import folder_paths


class OptionalLoadLastFrame:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = []
        if os.path.isdir(input_dir):
            files = sorted(
                f for f in os.listdir(input_dir)
                if os.path.isfile(os.path.join(input_dir, f))
                and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"))
            )
        return {
            "required": {
                "image": (["None"] + files, {"image_upload": True}),
                "auto_resize": ("BOOLEAN", {"default": True}),
                "max_megapixels": ("FLOAT", {
                    "default": 4.0, "min": 0.1, "max": 20.0, "step": 0.5,
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("last_frame",)
    FUNCTION = "load_image"
    CATEGORY = "image"

    def load_image(self, image="None", auto_resize=True, max_megapixels=4.0):
        if not image or image == "None":
            return (None,)

        path = folder_paths.get_annotated_filepath(image)
        with Image.open(path) as source:
            img = ImageOps.exif_transpose(source).convert("RGB")

        width, height = img.size
        pixels = width * height
        max_pixels = int(max_megapixels * 1_000_000)
        if auto_resize and pixels > max_pixels:
            scale = math.sqrt(max_pixels / pixels)
            new_width = max(1, int(width * scale))
            new_height = max(1, int(height * scale))
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(
                f"[OptionalLoadLastFrame] Resized {image}: "
                f"{width}x{height} -> {new_width}x{new_height}"
            )

        arr = np.asarray(img, dtype=np.float32) / 255.0
        return (torch.from_numpy(arr)[None, ...],)


NODE_CLASS_MAPPINGS = {"OptionalLoadLastFrame": OptionalLoadLastFrame}
NODE_DISPLAY_NAME_MAPPINGS = {
    "OptionalLoadLastFrame": "Optional Image Loader (Auto Resize)"
}
