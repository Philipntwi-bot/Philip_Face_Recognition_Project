import os
import sys
import shutil
from pathlib import Path
from ultralytics import YOLO

PROJECT_DIR = Path(r"C:\Users\User\OneDrive\Desktop\MY IA FOR ARTIFICIAL INTELLIGENCE\Philip_Face_Recognition_Project")
DATA_YAML = PROJECT_DIR / "dataset" / "data.yaml"

def main():
    print("=" * 60)
    print("  TRAINING YOLOV8 MODEL: PHILIP FACE RECOGNITION")
    print("=" * 60)

    # Load YOLOv8 Nano base model
    model = YOLO("yolov8n.pt")

    # Train model
    print("Starting training on local dataset...")
    results = model.train(
        data=str(DATA_YAML),
        epochs=15,             # 15 epochs provides solid convergence without over-exhausting CPU
        imgsz=416,             # 416x416 optimized for swift training and real-time webcam inference
        batch=16,
        workers=2,
        project=str(PROJECT_DIR / "runs"),
        name="philip_face_detect",
        exist_ok=True,
        verbose=True
    )

    # Copy best weights to root for web app
    best_weights = PROJECT_DIR / "runs" / "philip_face_detect" / "weights" / "best.pt"
    if best_weights.exists():
        target = PROJECT_DIR / "philip_face_model.pt"
        shutil.copy2(best_weights, target)
        print(f"\n✔ BEST MODEL EXPORTED SUCCESSFULLY: {target}")
    else:
        print("\nNotice: best.pt was not found at standard path.")

    print("\nTraining completed successfully!")

if __name__ == "__main__":
    main()
