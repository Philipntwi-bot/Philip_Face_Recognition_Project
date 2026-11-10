import os
import sys
from pathlib import Path
from ultralytics import YOLO

PROJECT_DIR = Path(__file__).resolve().parent

def train_face_model(data_yaml_path):
    """
    Trains a YOLOv8 nano model on Philip's face dataset.
    """
    print(f"Loading YOLOv8n base model...")
    model = YOLO("yolov8n.pt")  # automatically downloads pretrained YOLOv8n weights

    print(f"Starting training on dataset: {data_yaml_path}")
    results = model.train(
        data=data_yaml_path,
        epochs=30,
        imgsz=640,
        batch=8,
        project=str(PROJECT_DIR / "runs"),
        name="philip_face_detection",
        exist_ok=True,
        verbose=True
    )
    
    # Save best model to project root for the web app
    best_weights = PROJECT_DIR / "runs" / "philip_face_detection" / "weights" / "best.pt"
    if best_weights.exists():
        import shutil
        target = PROJECT_DIR / "philip_face_model.pt"
        shutil.copy2(best_weights, target)
        print(f"✔ Best model exported to: {target}")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        train_face_model(sys.argv[1])
    else:
        print("Usage: python train_model.py path/to/data.yaml")

