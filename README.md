# Philip Face Recognition AI (Ultralytics YOLOv8)

**Student Name:** Philip Antwi  
**Student ID / Index No:** PUIT24120002  
**Programme:** BSc Information Technology  
**Institution:** Pentecost University  
**Faculty:** Faculty of Information Technology and Computing  
**Course:** Artificial Intelligence & Machine Learning  

---

## 🚀 Project Overview

A custom deep learning biometric facial detection and recognition system engineered and trained using **Ultralytics YOLOv8 Nano**. The system performs real-time edge facial identification, bounding-box localization, and target class verification (`Phillip`) with ultra-low latency (~180 ms).

Accompanying this repository is the complete academic project report:
- 📄 **[Philip_Face_Recognition_Report.docx](Philip_Face_Recognition_Report.docx)** (Microsoft Word Document)
- 📑 **[Philip_Face_Recognition_Report.pdf](Philip_Face_Recognition_Report.pdf)** (Official Formatted PDF)

---

## 📊 Model Evaluation & Empirical Benchmarks

The model was trained on 772 primary high-resolution images annotated with 775 ground-truth bounding boxes via the **Ultralytics Hub** cloud platform (`philipantwipuit24120002.ndjson`).

| Metric | Score / Benchmark |
|---|---|
| **mAP @ IoU 0.50** | **92.11%** |
| **Precision** | **90.38%** |
| **Recall** | **88.89%** |
| **mAP @ IoU 0.50:0.95** | **58.75%** |
| **CPU Inference Latency** | **~180 ms** |
| **Neural Network Backbone** | **YOLOv8 Nano (YOLOv8n - 3.2M parameters)** |

---

## 🏛️ System Architecture

```
[Webcam Stream / Image Upload]
             │
             ▼
[Web Frontend (HTML5, Canvas, TailwindCSS)]
             │
             ▼ (POST /detect)
[Flask REST API Microservice (app.py)]
             │
             ▼ (Inference Tensor)
[Ultralytics YOLOv8 (philip_face_model.pt)]
             │
             ▼
[JSON: Bounding Box Coordinates, Confidence %, Class: 'Phillip']
```

---

## 🛠️ Installation & Local Execution

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/Philipntwi-bot/Philip_Face_Recognition_Project.git
cd Philip_Face_Recognition_Project
pip install -r requirements.txt
# or:
pip install ultralytics torch torchvision flask flask-cors opencv-python
```

### 2. Start the Backend API
```bash
python app.py
```
*The Flask REST API will start on `http://127.0.0.1:5000`.*

### 3. Open the Web Application
Simply launch `index.html` in any modern web browser or use a live server:
- Toggle between **Webcam Live Stream** and **Image Upload**.
- Instant HUD bounding-box overlay with live confidence score and millisecond latency tracking.

---

## 📁 Repository Structure

```
├── Philip_Face_Recognition_Report.docx # Official Academic Report (.docx)
├── Philip_Face_Recognition_Report.pdf  # Official Academic Report (.pdf)
├── app.py                              # Flask RESTful API service
├── index.html                          # Cybernetic web application UI
├── philip_face_model.pt                # Trained YOLOv8 Nano model weights
├── train_model.py                      # Training pipeline script
├── test_model.py                       # Validation & inference test script
├── prepare_dataset.py                  # Dataset parsing & YOLO format conversion
├── generate_report.py                  # Automated academic report generator
├── generate_plots.py                   # Plotting script for loss and mAP curves
├── figures/                            # High-resolution academic charts & diagrams
└── README.md                           # Documentation
```

---

## 🎓 Academic Submission Notice
Submitted in partial fulfilment of the requirements for the BSc Information Technology programme at **Pentecost University**, Ghana.
