import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import shutil

fig_dir = Path(r"C:\Users\User\OneDrive\Desktop\MY IA FOR ARTIFICIAL INTELLIGENCE\Philip_Face_Recognition_Project\figures")
runs_dir = Path(r"C:\Users\User\OneDrive\Desktop\MY IA FOR ARTIFICIAL INTELLIGENCE\Philip_Face_Recognition_Project\runs\philip_face_detect")
csv_path = runs_dir / "results.csv"

# 1. Read results
df = pd.read_csv(csv_path)
df.columns = [c.strip() for c in df.columns]

# 2. Plot Loss Curves
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
ax.plot(df['epoch'], df['train/box_loss'], 'o-', label='Train Box Loss', color='#2563eb', lw=2)
ax.plot(df['epoch'], df['val/box_loss'], 's--', label='Val Box Loss', color='#60a5fa', lw=2)
ax.plot(df['epoch'], df['train/cls_loss'], 'o-', label='Train Cls Loss', color='#dc2626', lw=2)
ax.plot(df['epoch'], df['val/cls_loss'], 's--', label='Val Cls Loss', color='#f87171', lw=2)
ax.plot(df['epoch'], df['train/dfl_loss'], 'o-', label='Train DFL Loss', color='#16a34a', lw=2)
ax.plot(df['epoch'], df['val/dfl_loss'], 's--', label='Val DFL Loss', color='#4ade80', lw=2)

ax.set_title('YOLOv8 Training and Validation Loss Curves (10 Epochs)', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('Epoch', fontsize=11)
ax.set_ylabel('Loss', fontsize=11)
ax.set_xticks(df['epoch'])
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, fontsize=9, loc='upper right')
plt.tight_layout()
plt.savefig(fig_dir / 'loss_curves.png')
plt.close()

# 3. Plot Metrics Progression
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
ax.plot(df['epoch'], df['metrics/mAP50(B)'], 'D-', label='mAP@0.50 (Peak: 92.11%)', color='#0284c7', lw=2.5)
ax.plot(df['epoch'], df['metrics/precision(B)'], 'o--', label='Precision (Peak: 90.38%)', color='#10b981', lw=2)
ax.plot(df['epoch'], df['metrics/recall(B)'], '^-', label='Recall (Peak: 88.89%)', color='#8b5cf6', lw=2)
ax.plot(df['epoch'], df['metrics/mAP50-95(B)'], 's--', label='mAP@0.50:0.95 (Final: 58.75%)', color='#f59e0b', lw=2)

ax.set_title('Validation Detection Metrics Progression Across Training', fontsize=13, fontweight='bold', pad=10)
ax.set_xlabel('Epoch', fontsize=11)
ax.set_ylabel('Score (0.0 to 1.0)', fontsize=11)
ax.set_ylim(0.0, 1.05)
ax.set_xticks(df['epoch'])
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, fontsize=9, loc='lower right')
plt.tight_layout()
plt.savefig(fig_dir / 'metrics_curves.png')
plt.close()

# 4. Copy existing YOLO visual artifacts
if (runs_dir / 'labels.jpg').exists():
    shutil.copy(runs_dir / 'labels.jpg', fig_dir / 'dataset_labels.jpg')
if (runs_dir / 'train_batch0.jpg').exists():
    shutil.copy(runs_dir / 'train_batch0.jpg', fig_dir / 'train_batch0.jpg')

# 5. System Architecture Diagram
fig, ax = plt.subplots(figsize=(10, 3.8), dpi=300)
ax.axis('off')

boxes = [
    ("User Input\n(Webcam Stream /\nImage Upload)", 0.10, 0.5),
    ("Web Frontend\n(HTML5, Canvas,\nTailwindCSS)", 0.32, 0.5),
    ("Flask Backend API\n(POST /detect\nOpenCV Decode)", 0.55, 0.5),
    ("Ultralytics YOLOv8\nInference Model\n(philip_face_model.pt)", 0.77, 0.5),
    ("Response JSON\n(Bounding Box,\nScore, 'Phillip')", 0.94, 0.5),
]

for label, x, y in boxes:
    ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#f1f5f9', edgecolor='#0284c7', lw=1.5))

arrows = [(0.17, 0.5, 0.24, 0.5), (0.40, 0.5, 0.46, 0.5), (0.64, 0.5, 0.69, 0.5), (0.85, 0.5, 0.88, 0.5)]
for x1, y1, x2, y2 in arrows:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=2, color='#334155'))

ax.set_title('Figure: High-Level End-to-End Face Detection System Architecture', fontsize=12, fontweight='bold', y=0.92)
ax.set_xlim(0, 1.02)
ax.set_ylim(0.2, 0.8)
plt.tight_layout()
plt.savefig(fig_dir / 'system_architecture.png')
plt.close()

print("ALL_PLOTS_GENERATED_SUCCESSFULLY")
