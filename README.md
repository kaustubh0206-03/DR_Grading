# 🩺 Attention-Enhanced Hybrid CNN and Vision Transformer for Explainable Diabetic Retinopathy Grading

<p align="center">
  <img src="assets/banner.png" alt="Project Banner" width="100%">
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Keras](https://img.shields.io/badge/Keras-DeepLearning-red)
![OpenCV](https://img.shields.io/badge/OpenCV-ComputerVision-green)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

</p>

---

# 📖 Table of Contents

* Overview
* Why This Project Matters
* Understanding Diabetic Retinopathy
* Problem Statement
* Project Objectives
* Proposed Architecture
* Complete Workflow
* Dataset Information
* Image Preprocessing
* Data Augmentation
* EfficientNetB5 CNN Branch
* Vision Transformer Branch
* Feature Fusion
* CBAM Attention Module
* Classification Head
* Grad-CAM Explainability
* Training Strategy
* Loss Functions
* Optimizer
* Evaluation Metrics
* Technology Stack
* Project Structure
* Expected Outputs
* Research Contributions
* Future Scope
* Team Information
* Conclusion

---

# 📌 Overview

Diabetic Retinopathy (DR) is one of the leading causes of preventable blindness among diabetic patients worldwide.

The disease damages retinal blood vessels and gradually affects vision. Early diagnosis is critical because timely treatment can significantly reduce the risk of permanent vision loss.

Unfortunately, traditional screening requires expert ophthalmologists and large amounts of time. In many regions, especially rural areas, access to specialists is limited.

This project introduces an **Attention-Enhanced Hybrid Deep Learning Framework** capable of automatically grading diabetic retinopathy severity using retinal fundus images.

The proposed architecture combines:

* EfficientNetB5
* Vision Transformer (ViT)
* Feature Fusion
* CBAM Attention Mechanism
* Grad-CAM Explainability

to create an accurate, robust, and clinically interpretable diagnostic framework.

Unlike traditional black-box AI systems, this model provides visual explanations highlighting the retinal regions responsible for every prediction.

---

# 🌍 Why This Project Matters

Globally, millions of diabetic patients require routine retinal screening every year.

Challenges include:

* Limited ophthalmologists
* Increasing patient population
* Manual screening workload
* Subjective interpretation
* Delayed diagnosis

Artificial Intelligence can help by:

✅ Reducing screening workload

✅ Improving accessibility

✅ Supporting ophthalmologists

✅ Enabling faster diagnosis

✅ Improving healthcare scalability

This project is designed to serve as an AI-assisted diagnostic support system rather than replacing healthcare professionals.

---

# 👁 Understanding Diabetic Retinopathy

## What is the Retina?

The retina is a thin layer of tissue located at the back of the eye.

Its primary function is to:

* Capture light
* Convert light into neural signals
* Send information to the brain

```text
Light
 ↓
 Retina
 ↓
 Brain
 ↓
 Vision
```

---

## What Causes Diabetic Retinopathy?

Persistent high blood sugar damages retinal blood vessels.

Damaged vessels may:

* Leak blood
* Leak fluid
* Become blocked
* Swell abnormally
* Grow new abnormal vessels

These abnormalities gradually impair vision.

---

# 📊 Diabetic Retinopathy Severity Levels

The system predicts one of five severity classes.

| Label | Class            | Description                      |
| ----- | ---------------- | -------------------------------- |
| 0     | No_DR            | No signs of diabetic retinopathy |
| 1     | Mild             | Presence of microaneurysms       |
| 2     | Moderate         | Increased retinal abnormalities  |
| 3     | Severe           | Significant retinal damage       |
| 4     | Proliferative_DR | Advanced abnormal vessel growth  |

---

# 🚨 Problem Statement

Traditional diabetic retinopathy diagnosis relies heavily on manual examination of retinal fundus images.

Major challenges include:

## Clinical Challenges

* Limited specialists
* Time-consuming diagnosis
* Human fatigue
* Subjective grading

## Technical Challenges

* Tiny lesion detection
* High class imbalance
* Inter-class similarity
* Poor explainability
* Model generalization

The objective is to develop a robust AI system capable of accurately grading diabetic retinopathy severity while providing transparent visual explanations.

---

# 🎯 Project Objectives

## Primary Objective

Develop an explainable Attention-Enhanced Hybrid CNN-Vision Transformer framework for diabetic retinopathy grading.

---

## Specific Objectives

* Improve retinal image quality.
* Extract lesion-level features.
* Capture global retinal context.
* Improve classification accuracy.
* Handle class imbalance.
* Focus on clinically relevant regions.
* Generate visual explanations.
* Support ophthalmologists in diagnosis.

---

# 🏗 Proposed Architecture

```text
Input Retinal Fundus Image
              │
              ▼
     Image Preprocessing
              │
              ▼
      Data Augmentation
              │
              ▼

 ┌────────────────────────────┐
 │                            │
 ▼                            ▼

EfficientNetB5          Vision Transformer
 CNN Branch                 ViT Branch

(Local Features)       (Global Features)

 │                            │
 └───────────┬────────────────┘
             ▼

       Feature Fusion

             ▼

       CBAM Attention

             ▼

      Dense Layers

             ▼

      Softmax Layer

             ▼

      DR Prediction

             ▼

     Grad-CAM Heatmap
```

---

# 🔄 Complete Workflow

When a retinal image is uploaded:

### Step 1

Image quality enhancement and preprocessing.

### Step 2

Data augmentation improves dataset diversity.

### Step 3

EfficientNetB5 extracts local retinal lesions.

### Step 4

Vision Transformer captures global retinal structure.

### Step 5

Features from both branches are fused.

### Step 6

CBAM attention refines important information.

### Step 7

Dense layers perform classification.

### Step 8

Softmax predicts diabetic retinopathy severity.

### Step 9

Grad-CAM generates visual explanations.

---

# 📂 Dataset Information

## Dataset Used

### APTOS 2019 Blindness Detection Dataset

The dataset contains retinal fundus images collected from diabetic patients.

---

## Classes

```text
0 → No_DR
1 → Mild
2 → Moderate
3 → Severe
4 → Proliferative_DR
```

---

## Dataset Characteristics

* Multi-Class Classification
* Real Clinical Data
* Medical Imaging Dataset
* Class Imbalance Present
* Five Severity Categories

---

# 🖼 Image Preprocessing

Retinal images often suffer from:

* Uneven illumination
* Noise
* Contrast variations
* Resolution inconsistencies

Preprocessing improves image quality before training.

---

## Image Resizing

All images are resized to:

```text
224 × 224 × 3
```

Benefits:

* Consistent input dimensions
* Faster training
* Lower memory requirements

---

## CLAHE

### Contrast Limited Adaptive Histogram Equalization

Purpose:

* Improve local contrast
* Enhance lesions
* Highlight blood vessels

Benefits:

* Better lesion visibility
* Improved feature extraction

---

## Ben Graham Preprocessing

Popular retinal image enhancement technique.

Benefits:

* Illumination normalization
* Vessel enhancement
* Improved lesion visibility

---

## Normalization

Pixel values are scaled between:

```text
0 → 1
```

Benefits:

* Stable optimization
* Faster convergence
* Better gradient flow

---

# 🔄 Data Augmentation

Medical datasets are generally limited in size.

To improve generalization, augmentation is applied.

Techniques include:

* Rotation
* Horizontal Flip
* Vertical Flip
* Zoom
* Brightness Adjustment
* Width Shift
* Height Shift
* Shear Transformation
* Gaussian Noise

Benefits:

* Reduces overfitting
* Improves robustness
* Simulates real-world variability

---

# 🧠 EfficientNetB5 CNN Branch

## What is EfficientNetB5?

EfficientNetB5 is a state-of-the-art Convolutional Neural Network architecture that uses compound scaling.

Unlike traditional CNNs, it scales:

```text
Depth
Width
Resolution
```

simultaneously.

---

## Why EfficientNetB5?

Advantages:

* High accuracy
* Efficient architecture
* Strong transfer learning performance
* Excellent medical image representation

---

## What Does It Learn?

EfficientNetB5 focuses on:

* Microaneurysms
* Exudates
* Hemorrhages
* Vessel abnormalities
* Cotton wool spots

Think of it as a specialist examining tiny retinal lesions.

---

# 🌐 Vision Transformer (ViT) Branch

## What is a Vision Transformer?

A Vision Transformer applies Transformer architecture to image data.

Unlike CNNs, ViT analyzes the entire image globally.

---

## How ViT Works

### Step 1

Image is divided into patches.

### Step 2

Patches become embeddings.

### Step 3

Self-attention learns patch relationships.

### Step 4

Global image representation is created.

---

## Why Use ViT?

Advantages:

* Global context understanding
* Long-range dependency learning
* Better structural awareness

Think of it as a specialist examining the retina as a whole.

---

# 🔗 Feature Fusion

The model now possesses:

```text
CNN Features
```

and

```text
Transformer Features
```

These representations are combined.

```text
CNN Features
       +
ViT Features
       ↓
Fused Features
```

Benefits:

* Local + Global understanding
* Rich feature representation
* Improved classification performance

---

# 🎯 CBAM Attention Module

CBAM stands for:

```text
Convolutional Block Attention Module
```

---

## Why Attention?

Not every retinal region is important.

Attention helps the model focus on critical regions.

---

## Channel Attention

Answers:

```text
What is important?
```

---

## Spatial Attention

Answers:

```text
Where is it important?
```

---

## Benefits

CBAM guides the model toward:

* Hemorrhages
* Exudates
* Microaneurysms
* Vessel abnormalities

while suppressing irrelevant information.

---

# 🧮 Classification Head

The refined feature representation passes through:

```text
Dense Layer
      ↓
Batch Normalization
      ↓
Dropout
      ↓
Softmax Layer
```

Final Output:

```text
No_DR
Mild
Moderate
Severe
Proliferative_DR
```

---

# 🔥 Grad-CAM Explainability

## Why Explainability?

Healthcare professionals need to know:

```text
Why did the model make this prediction?
```

Deep learning models often behave like black boxes.

Grad-CAM provides transparency.

---

## What is Grad-CAM?

Gradient-weighted Class Activation Mapping.

Grad-CAM generates heatmaps highlighting retinal regions responsible for predictions.

---

## Example

```text
Input Image
      ↓

Prediction:
Moderate DR

      ↓

Grad-CAM

Highlights:
• Hemorrhages
• Exudates
• Retinal Lesions
```

---

## Benefits

* Transparency
* Trustworthiness
* Clinical interpretability
* Better decision support

---

# 🚀 Training Strategy

## Stage 1

Train classification layers.

```text
Freeze Backbone
Train Head
```

---

## Stage 2

Fine-tuning.

```text
Unfreeze Layers
Train End-to-End
```

---

# 📉 Loss Functions

## Focal Loss

Used to address:

```text
Class Imbalance
```

by giving greater emphasis to difficult samples.

---

## Categorical Cross Entropy

Used for:

```text
Multi-Class Classification
```

---

# ⚙ Optimizer

## Adam Optimizer

Advantages:

* Adaptive learning rates
* Fast convergence
* Stable optimization

---

# 📈 Evaluation Metrics

The model is evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix
* Classification Report

---

# 🛠 Technology Stack

## Programming Language

* Python

## Deep Learning Frameworks

* TensorFlow
* Keras

## Computer Vision

* OpenCV

## Data Processing

* NumPy
* Pandas

## Machine Learning

* Scikit-Learn

## Visualization

* Matplotlib
* Seaborn

---

# 📁 Recommended Project Structure

```text
project/
│
├── dataset/
│
├── notebooks/
│
├── models/
│   ├── efficientnetb5.py
│   ├── vit.py
│   ├── cbam.py
│   ├── fusion.py
│
├── training/
│
├── inference/
│
├── explainability/
│   └── gradcam.py
│
├── outputs/
│
├── requirements.txt
│
└── README.md
```

---

# 🎯 Expected Outputs

For every uploaded retinal image:

The system generates:

✅ Predicted Class

✅ Confidence Score

✅ Probability Distribution

✅ Grad-CAM Heatmap

✅ Explainable Visualization

---

# 🏆 Research Contributions

### Hybrid Deep Learning Framework

Combines CNN and Vision Transformer architectures.

### Attention-Based Learning

CBAM integration improves feature refinement.

### Explainable Artificial Intelligence

Grad-CAM provides transparent visual explanations.

### Clinical Decision Support

Designed to assist ophthalmologists.

### Scalable Screening Framework

Suitable for large-scale deployment.

---

# 🔮 Future Scope

Potential future improvements include:

* Swin Transformer Integration
* OCT + Fundus Fusion
* Multi-Modal Learning
* Self-Supervised Learning
* Real-Time Screening Systems
* Mobile Deployment
* Cloud-Based Diagnosis
* Federated Learning

---

# 👨‍💻 Project Team

### Final Year Research Project

Department of Computer Science and Engineering

Institute of Technical Education and Research (ITER)

Siksha 'O' Anusandhan (Deemed to be University)

---

## Team Members

* Balvindar Das
* Kaustubh Kumar
* Samiksha Mund
* Kumari Shreya

---

## Supervisor

Dr. Sushil Kumar Maurya

---

# 🏁 Conclusion

This project presents an Explainable Artificial Intelligence framework for diabetic retinopathy grading using retinal fundus images.

By combining:

* EfficientNetB5
* Vision Transformer
* Feature Fusion
* CBAM Attention
* Grad-CAM

the system leverages both local lesion information and global retinal context while maintaining transparency through visual explanations.

The final objective is to create a reliable, interpretable, and clinically useful AI-assisted screening framework capable of supporting ophthalmologists in the early detection and grading of diabetic retinopathy.

---

## ⭐ If you found this project useful, consider giving it a star.

```
"Early Detection Saves Vision."
```
