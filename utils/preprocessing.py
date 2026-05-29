"""
Image preprocessing utilities: resize, normalize, CLAHE, quality check
"""

import cv2
import numpy as np
from PIL import Image


TARGET_SIZE = (456, 456)

DR_CLASSES = [
    "No DR",
    "Mild DR",
    "Moderate DR",
    "Severe DR",
    "Proliferative DR"
]


def pil_to_cv2(pil_img):
    """Convert PIL image to BGR OpenCV array."""
    arr = np.array(pil_img.convert("RGB"))
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv_img):
    """Convert BGR OpenCV array to RGB PIL image."""
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def apply_clahe(cv_img):
    """Apply CLAHE to LAB lightness channel."""
    lab = cv2.cvtColor(cv_img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced = cv2.merge([cl, a, b])
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)


def preprocess_image(pil_img):
    """
    Full preprocessing pipeline:
    1. Resize to TARGET_SIZE
    2. Apply CLAHE
    3. Normalize to [0, 1]
    Returns: (preprocessed_pil, preprocessed_array)
    """
    cv_img = pil_to_cv2(pil_img)

    # Resize
    resized = cv2.resize(cv_img, TARGET_SIZE, interpolation=cv2.INTER_LANCZOS4)

    # CLAHE enhancement
    enhanced = apply_clahe(resized)

    # Normalize
    normalized = enhanced.astype(np.float32) / 255.0
    model_input = np.expand_dims(normalized, axis=0)

    # For display (back to uint8)
    display_arr = (normalized * 255).astype(np.uint8)
    display_pil = cv2_to_pil(display_arr)

    return display_pil, model_input


def check_image_quality(pil_img):
    """
    Assess fundus image quality: blur, brightness, contrast.
    Returns a dict with scores and a quality label.
    """
    cv_img = pil_to_cv2(pil_img)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # Blur detection (Laplacian variance)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Brightness (mean of grayscale)
    brightness = float(np.mean(gray))

    # Contrast (std of grayscale)
    contrast = float(np.std(gray))

    # Quality assessment
    issues = []
    if blur_score < 80:
        issues.append("blurry")
    if brightness < 40:
        issues.append("too dark")
    elif brightness > 210:
        issues.append("overexposed")
    if contrast < 20:
        issues.append("low contrast")

    if len(issues) == 0:
        quality_score = "Excellent"
        quality_color = "#22C55E"
    elif len(issues) == 1:
        quality_score = "Acceptable"
        quality_color = "#EAB308"
    else:
        quality_score = "Poor"
        quality_color = "#EF4444"

    return {
        "blur_score": round(blur_score, 1),
        "brightness": round(brightness, 1),
        "contrast": round(contrast, 1),
        "issues": issues,
        "quality_score": quality_score,
        "quality_color": quality_color,
    }


def get_image_stats(pil_img):
    """Return width, height, mode, file-size estimate."""
    w, h = pil_img.size
    return {"width": w, "height": h, "mode": pil_img.mode}
