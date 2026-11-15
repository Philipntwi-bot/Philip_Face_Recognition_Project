import os
import io
import cv2
import torch
import numpy as np
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "philip_face_model.pt"

# Fallback to base model if custom not yet trained
if MODEL_PATH.exists():
    model = YOLO(str(MODEL_PATH))
    print(f"Loaded custom face model: {MODEL_PATH}")
else:
    model = YOLO("yolov8n.pt")
    print("Custom model not found, using base yolov8n.pt")

@app.route("/")
def index():
    html_file = PROJECT_DIR / "index.html"
    return render_template_string(html_file.read_text(encoding="utf-8"))

@app.route("/figures/<path:filename>")
def serve_figure(filename):
    return send_from_directory(PROJECT_DIR / "figures", filename)

@app.route("/api/detect", methods=["POST"])
def detect():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
        
        file = request.files["image"]
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = model.predict(img, conf=0.35, imgsz=416)
        detections = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                xyxy = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                class_name = model.names.get(cls_id, "Philip")

                detections.append({
                    "class": class_name,
                    "confidence": round(conf * 100, 2),
                    "box": {
                        "x1": round(xyxy[0], 1),
                        "y1": round(xyxy[1], 1),
                        "x2": round(xyxy[2], 1),
                        "y2": round(xyxy[3], 1)
                    }
                })

        return jsonify({
            "detections": detections,
            "total": len(detections)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

