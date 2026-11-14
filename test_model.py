from ultralytics import YOLO
from pathlib import Path

model_path = Path(r"C:\Users\User\OneDrive\Desktop\MY IA FOR ARTIFICIAL INTELLIGENCE\Philip_Face_Recognition_Project\philip_face_model.pt")
model = YOLO(str(model_path))
print("Model loaded successfully!")
print("Classes:", model.names)

# Run a quick test inference on a validation image
val_img = Path(r"C:\Users\User\OneDrive\Desktop\MY IA FOR ARTIFICIAL INTELLIGENCE\Philip_Face_Recognition_Project\dataset\images\val")
sample_img = next(val_img.glob("*.jpg"), None)
if sample_img:
    print(f"Testing prediction on: {sample_img.name}")
    results = model.predict(str(sample_img), conf=0.25)
    for r in results:
        print(f"Detected {len(r.boxes)} faces:")
        for box in r.boxes:
            cls_name = model.names[int(box.cls[0].item())]
            conf = float(box.conf[0].item()) * 100
            print(f" - {cls_name}: {conf:.2f}% confidence")
