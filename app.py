import os
import io
import time
import base64
import cv2
import numpy as np
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "philip_face_model.pt"

# Load custom face model if available
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

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "online": True,
        "latency_ms": 14,
        "model": "YOLOv8-Nano-Philip",
        "dataset": "philipantwipuit24120002",
        "version": "2.4.0"
    })

@app.route("/figures/<path:filename>")
def serve_figure(filename):
    return send_from_directory(PROJECT_DIR / "figures", filename)

@app.route("/<path:filename>")
def serve_root_file(filename):
    file_path = PROJECT_DIR / filename
    if file_path.exists() and file_path.is_file():
        return send_from_directory(PROJECT_DIR, filename)
    return jsonify({"error": "File not found"}), 404

def annotate_and_crop(img, results):
    h, w = img.shape[:2]
    annotated = img.copy()
    face_crops = []
    total_faces = 0
    max_conf = 0.0
    philip_verified = False

    for r in results:
        for box in r.boxes:
            total_faces += 1
            conf = float(box.conf[0].item())
            cls_id = int(box.cls[0].item())
            xyxy = box.xyxy[0].tolist()
            x1, y1, x2, y2 = [int(v) for v in xyxy]
            
            x1 = max(0, min(x1, w - 1))
            y1 = max(0, min(y1, h - 1))
            x2 = max(x1 + 1, min(x2, w))
            y2 = max(y1 + 1, min(y2, h))

            conf_pct = round(conf * 100, 1)
            if conf_pct > max_conf:
                max_conf = conf_pct

            # Determine identity
            is_philip = (cls_id == 0 or "philip" in model.names.get(cls_id, "").lower())
            if is_philip and conf >= 0.25:
                philip_verified = True
                name = "Phillip Antwi"
                border_color = (191, 212, 45) # BGR teal
            else:
                name = f"Face #{total_faces}"
                border_color = (212, 182, 6) # BGR cyan

            # Draw futuristic HUD box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), border_color, 2)
            # Corner markers
            cw = min(20, (x2 - x1) // 4)
            ch = min(20, (y2 - y1) // 4)
            cv2.line(annotated, (x1, y1), (x1 + cw, y1), (255, 255, 255), 3)
            cv2.line(annotated, (x1, y1), (x1, y1 + ch), (255, 255, 255), 3)
            cv2.line(annotated, (x2, y1), (x2 - cw, y1), (255, 255, 255), 3)
            cv2.line(annotated, (x2, y1), (x2, y1 + ch), (255, 255, 255), 3)
            cv2.line(annotated, (x1, y2), (x1 + cw, y2), (255, 255, 255), 3)
            cv2.line(annotated, (x1, y2), (x1, y2 - ch), (255, 255, 255), 3)
            cv2.line(annotated, (x2, y2), (x2 - cw, y2), (255, 255, 255), 3)
            cv2.line(annotated, (x2, y2), (x2 - ch), (255, 255, 255), 3)

            # Label tag
            tag_text = f"{name} // {conf_pct}%"
            cv2.putText(annotated, tag_text, (x1, max(18, y1 - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, border_color, 2, cv2.LINE_AA)

            # Crop face thumbnail
            crop = img[y1:y2, x1:x2]
            if crop.size > 0:
                crop_thumb = cv2.resize(crop, (90, 90))
                _, crop_buf = cv2.imencode('.jpg', crop_thumb)
                crop_b64 = "data:image/jpeg;base64," + base64.b64encode(crop_buf).decode('utf-8')
                face_crops.append({
                    "name": name,
                    "confidence_pct": conf_pct,
                    "is_caleb": is_philip,
                    "is_philip": is_philip,
                    "thumbnail": crop_b64
                })

    # Encode images
    _, ann_buf = cv2.imencode('.jpg', annotated, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    ann_b64 = "data:image/jpeg;base64," + base64.b64encode(ann_buf).decode('utf-8')

    _, orig_buf = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
    orig_b64 = "data:image/jpeg;base64," + base64.b64encode(orig_buf).decode('utf-8')

    return ann_b64, orig_b64, face_crops, total_faces, max_conf, philip_verified

@app.route("/api/predict", methods=["POST"])
def predict():
    t_start = time.time()
    try:
        conf_val = float(request.form.get("conf", 0.25))
        iou_val = float(request.form.get("iou", 0.45))

        img = None
        if "file" in request.files:
            file = request.files["file"]
            img_bytes = file.read()
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif "image_b64" in request.form:
            b64_str = request.form["image_b64"]
            if "," in b64_str:
                b64_str = b64_str.split(",")[1]
            img_bytes = base64.b64decode(b64_str)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"success": False, "message": "No valid image provided"}), 400

        results = model.predict(img, conf=conf_val, iou=iou_val, imgsz=416)
        ann_b64, orig_b64, crops, total_faces, max_conf, philip_verified = annotate_and_crop(img, results)
        latency_ms = int((time.time() - t_start) * 1000)

        return jsonify({
            "success": True,
            "total_faces": total_faces,
            "caleb_verified": philip_verified,
            "philip_verified": philip_verified,
            "max_confidence": max_conf,
            "cloud_latency_ms": latency_ms,
            "annotated_image": ann_b64,
            "original_image": orig_b64,
            "face_crops": crops
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/detect", methods=["POST"])
def detect_legacy():
    return predict()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
