"""
Script to parse philipantwipuit24120002.ndjson and download images + generate YOLO label txt files.
"""
import os
import json
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

PROJECT_DIR = Path(r"C:\Users\User\OneDrive\Desktop\MY IA FOR ARTIFICIAL INTELLIGENCE\Philip_Face_Recognition_Project")
NDJSON_PATH = PROJECT_DIR / "philipantwipuit24120002.ndjson"
DATASET_DIR = PROJECT_DIR / "dataset"

for split in ["train", "val"]:
    (DATASET_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
    (DATASET_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)

def process_item(item_data):
    file_name = item_data.get("file")
    url = item_data.get("url")
    split = item_data.get("split", "train")
    if split not in ["train", "val"]:
        split = "train"
    
    # Clean filename
    safe_name = Path(file_name).stem.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_") + Path(file_name).suffix
    
    img_dest = DATASET_DIR / "images" / split / safe_name
    txt_dest = DATASET_DIR / "labels" / split / (Path(safe_name).stem + ".txt")

    # Download image if not already downloaded
    if not img_dest.exists():
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp, open(img_dest, 'wb') as out_file:
                out_file.write(resp.read())
        except Exception as e:
            print(f"Error downloading {file_name}: {e}")
            return False

    # Write YOLO format label file (cls x y w h)
    boxes = item_data.get("annotations", {}).get("boxes", [])
    with open(txt_dest, "w", encoding="utf-8") as f:
        for box in boxes:
            cls_id, x, y, w, h = box
            f.write(f"{cls_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
            
    return True

def main():
    print("Reading ndjson annotations...")
    with open(NDJSON_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    header = json.loads(lines[0])
    items = [json.loads(line) for line in lines[1:]]

    print(f"Total images to process: {len(items)}")

    # Multi-threaded download (20 concurrent workers for high speed)
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(process_item, items))

    successful = sum(1 for r in results if r)
    print(f"Downloaded and processed {successful}/{len(items)} images and labels.")

    # Generate data.yaml for YOLO training
    yaml_content = f"""path: {DATASET_DIR.as_posix()}
train: images/train
val: images/val

names:
  0: Phillip
"""
    yaml_path = DATASET_DIR / "data.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    print(f"data.yaml generated at {yaml_path}")

if __name__ == "__main__":
    main()

