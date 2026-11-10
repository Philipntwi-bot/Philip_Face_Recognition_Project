# Philip Face Recognition AI (Ultralytics YOLOv8)

**Student:** Philip Antwi  
**Programme:** BSc Information Technology  
**Institution:** Pentecost University  

---

## Project Overview

A custom facial detection and recognition model trained on Philip's biometric dataset using **Ultralytics YOLOv8**. The application enables real-time edge facial identification with bounding box localization and confidence calibration.

---

## Features
- Custom face dataset annotated via **Ultralytics HUB** (`kwabena/mypersonaldataset`).
- State-of-the-art **YOLOv8** object detection backbone.
- Real-time webcam and static image inference interface.
- Cybernetic dark-mode web application.

---

## Setup & Running

```bash
# 1. Install dependencies
pip install ultralytics torch opencv-python

# 2. Train the model (once dataset is downloaded)
python train_model.py data.yaml

# 3. Test inference
python -c "from ultralytics import YOLO; model = YOLO('philip_face_model.pt'); model.predict('test.jpg', show=True)"
```
