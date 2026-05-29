# 👁️ RetinaGuard AI

**Advanced Diabetic Retinopathy Screening Platform**

A production-quality Streamlit app for AI-powered DR grading using a hybrid CNN + Vision Transformer architecture.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
RetinaGuard-AI/
├── app.py                    # Main Streamlit entry point
├── train.py                  # Model training script
├── requirements.txt
├── .streamlit/
│   └── config.toml           # Theme & server config
│
├── pages/
│   ├── home.py               # Landing page
│   ├── predict.py            # Upload & Predict
│   ├── explainability.py     # Grad-CAM visualization
│   ├── analytics.py          # Performance dashboard
│   └── history.py            # Prediction history
│
├── models/
│   ├── model.py              # Hybrid CNN+ViT model + demo stub
│   └── weights/              # Place trained .h5 weights here
│
├── utils/
│   ├── styles.py             # Global CSS injection
│   ├── preprocessing.py      # CLAHE, resize, quality check
│   ├── gradcam.py            # Grad-CAM computation
│   ├── database.py           # SQLite CRUD
│   └── 
            └── GlobalAveragePooling1D → 64-dim
                        │
               Adaptive Fusion (320→256→128)
                        │
               Output: 5 Classes (Softmax)
                   No DR | Mild | Moderate | Severe | Proliferative
```

**~2.1M parameters** — lightweight and deployable on CPU.

---

## 🎓 Demo Mode

If no trained weights are found in `models/weights/retinaguard_weights.h5`, the app runs in **Demo Mode**:
- Predictions are **deterministic** (same image → same result)
- Grad-CAM heatmaps are **synthetic** but visually realistic
- Analytics metrics are **clearly labeled as preliminary**

This allows full end-to-end app exploration without training.

---

## 🏋️ Training

```bash
python train.py \
    --dataset /path/to/your/dataset \
    --epochs 40 \
    --batch-size 32
```

Dataset should follow ImageDataGenerator directory structure or be adapted in `train.py`.

Recommended dataset: [Kaggle DR Detection](https://www.kaggle.com/c/diabetic-retinopathy-detection)

---

## ⚕️ Disclaimer

> RetinaGuard AI is a research/demonstration platform.
> It is **NOT** a certified medical device and must **NOT** be used for clinical diagnosis
> without proper validation and regulatory approval.
> All results must be reviewed by a qualified ophthalmologist.

---

## 🛠️ Tech Stack

- **Streamlit** — UI framework
- **TensorFlow / Keras** — Model architecture
- **OpenCV** — Image processing & CLAHE
- **NumPy / Pandas** — Data handling
- **Plotly** — Interactive charts
- **SQLite** — Prediction history
- **FPDF2** — PDF report generation
- **Pillow** — Image I/O
