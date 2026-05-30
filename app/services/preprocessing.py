from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def preprocess_image(path: Path) -> bytes:
    image = cv2.imread(str(path))
    if image is None:
        return path.read_bytes()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, h=9)
    gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    scaled = upscale(gray)
    binary = cv2.adaptiveThreshold(
        scaled,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )
    ok, encoded = cv2.imencode(".jpg", binary)
    return encoded.tobytes() if ok else path.read_bytes()


def upscale(image: np.ndarray, target_width: int = 1800) -> np.ndarray:
    height, width = image.shape[:2]
    if width >= target_width:
        return image
    scale = target_width / width
    return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
