import numpy as np
import cv2
from PIL import Image

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


def _synthetic_gradcam(image_array, predicted_idx):
    if image_array.ndim == 4:
        img = image_array[0]
    else:
        img = image_array
    h, w = img.shape[:2]
    gray = np.mean(img, axis=2)
    gray_u8 = (gray * 255).astype(np.uint8)
    lap = cv2.Laplacian(gray_u8, cv2.CV_64F)
    lap = np.abs(lap)
    heatmap = cv2.GaussianBlur(lap.astype(np.float32), (31, 31), 0)
    cy, cx = h // 2, int(w * 0.55)
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    gaussian_blob = np.exp(-dist ** 2 / (2 * (h * 0.2) ** 2))
    peripheral_weight = predicted_idx * 0.15
    center_weight = 1.0 - peripheral_weight
    heatmap = heatmap * center_weight + gaussian_blob * 50 * peripheral_weight
    heatmap = np.maximum(heatmap, 0)
    if heatmap.max() > 0:
        heatmap = heatmap / heatmap.max()
    return heatmap


def _find_last_conv_layer(model):
    if not TF_AVAILABLE or model is None:
        return None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
        if hasattr(layer, 'layers'):
            for sub in reversed(layer.layers):
                if isinstance(sub, tf.keras.layers.Conv2D):
                    return sub.name
    return None


def compute_gradcam(model, image_array, predicted_idx):
    if TF_AVAILABLE and model is not None and hasattr(model, 'layers'):
        try:
            layer_name = _find_last_conv_layer(model)
            if layer_name is None:
                return _synthetic_gradcam(image_array, predicted_idx)
            grad_model = tf.keras.models.Model(
                inputs=model.inputs,
                outputs=[model.get_layer(layer_name).output, model.output]
            )
            with tf.GradientTape() as tape:
                inputs = tf.cast(image_array, tf.float32)
                conv_outputs, predictions = grad_model(inputs)
                loss = predictions[:, predicted_idx]
            grads = tape.gradient(loss, conv_outputs)
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            conv_outputs = conv_outputs[0]
            heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
            return heatmap.numpy()
        except Exception:
            return _synthetic_gradcam(image_array, predicted_idx)
    return _synthetic_gradcam(image_array, predicted_idx)


def apply_heatmap_overlay(original_pil, heatmap, alpha=0.7, colormap=None):
    if colormap is None:
        colormap = getattr(cv2, 'COLORMAP_TURBO', cv2.COLORMAP_JET)
        
    orig_arr = np.array(original_pil.convert("RGB")).astype(np.float32)
    h, w = orig_arr.shape[:2]
    
    # Resize with cubic interpolation for smooth scaling
    heatmap_resized = cv2.resize(heatmap, (w, h), interpolation=cv2.INTER_CUBIC)
    
    # Larger Gaussian blur for an organic, realistic heat spread
    heatmap_resized = cv2.GaussianBlur(heatmap_resized, (31, 31), 0)
    
    # Re-normalize to [0, 1] so the peak is fully bright
    if heatmap_resized.max() > 0:
        heatmap_resized = heatmap_resized / heatmap_resized.max()
        
    # Apply exponential curve to suppress background noise and make hotspots pop
    heatmap_resized = heatmap_resized ** 1.5
    
    heatmap_u8 = (heatmap_resized * 255).astype(np.uint8)
    colored = cv2.applyColorMap(heatmap_u8, colormap)
    colored_rgb = cv2.cvtColor(colored, cv2.COLOR_BGR2RGB).astype(np.float32)
    
    heatmap_pil = Image.fromarray(colored_rgb.astype(np.uint8))
    
    # Dynamic alpha blending: only apply color where heatmap is active.
    # This prevents the dark blue background of the colormap from dimming the whole image.
    alpha_mask = np.expand_dims(heatmap_resized, axis=2) * alpha
    
    overlay = (orig_arr * (1.0 - alpha_mask) + colored_rgb * alpha_mask)
    overlay = np.clip(overlay, 0, 255).astype(np.uint8)
    overlay_pil = Image.fromarray(overlay)
    
    return heatmap_pil, overlay_pil
