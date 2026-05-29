"""
RetinaGuard AI - Training Script
Run this to train the hybrid CNN+ViT model on your dataset.

Usage:
    python train.py --dataset /path/to/dataset --epochs 40 --batch-size 32

Dataset structure expected:
    dataset/
        train/
            0_No_DR/
            1_Mild/
            2_Moderate/
            3_Severe/
            4_Proliferative_DR/
        val/
            ...
        test/
            ...

Or use a CSV manifest with columns: image_path, label (0-4)
"""

import argparse
import os
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Train RetinaGuard AI model")
    parser.add_argument("--dataset",    default="./data", help="Path to dataset directory")
    parser.add_argument("--epochs",     type=int, default=40)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr",         type=float, default=1e-4)
    parser.add_argument("--output",     default="./models/weights/retinaguard_weights.h5")
    args = parser.parse_args()

    print("=" * 60)
    print("  RetinaGuard AI — Training Pipeline")
    print("=" * 60)
    print(f"  Dataset  : {args.dataset}")
    print(f"  Epochs   : {args.epochs}")
    print(f"  Batch    : {args.batch_size}")
    print(f"  LR       : {args.lr}")
    print(f"  Output   : {args.output}")
    print("=" * 60)

    try:
        import tensorflow as tf
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        from models.model import build_hybrid_model
        print(f"  TensorFlow: {tf.__version__}")
    except ImportError as e:
        print(f"  Error: {e}")
        return

    TARGET_SIZE = (224, 224)

    train_gen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1,
        brightness_range=[0.85, 1.15],
    )
    val_gen = ImageDataGenerator(rescale=1./255)

    train_ds = train_gen.flow_from_directory(
        os.path.join(args.dataset, "train"),
        target_size=TARGET_SIZE,
        batch_size=args.batch_size,
        class_mode="sparse",
    )
    val_ds = val_gen.flow_from_directory(
        os.path.join(args.dataset, "val"),
        target_size=TARGET_SIZE,
        batch_size=args.batch_size,
        class_mode="sparse",
    )

    # ── Build Model ──
    model = build_hybrid_model()
    model.summary()

    # ── Callbacks ──
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            args.output, monitor="val_accuracy",
            save_best_only=True, save_weights_only=True, verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=7, restore_best_weights=True, verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6, verbose=1
        ),
        tf.keras.callbacks.TensorBoard(log_dir="./logs"),
    ]

    # ── Train ──
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=callbacks,
    )

    print("\n✅ Training complete!")
    print(f"   Best val accuracy: {max(history.history['val_accuracy']):.4f}")
    print(f"   Weights saved to : {args.output}")
    print("\n   Restart the Streamlit app to use trained weights.")


if __name__ == "__main__":
    main()
