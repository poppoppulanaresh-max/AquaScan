import os
import glob
import sys

def inspect_yolo_labels(labels_dir):
    """Scans YOLO label text files in a directory and generates a diagnostic report.
    
    YOLO format: <class_id> <x_center> <y_center> <width> <height>
    Coordinates are normalized between 0.0 and 1.0.
    """
    if not os.path.exists(labels_dir):
        print(f"❌ Error: Directory '{labels_dir}' does not exist.")
        return

    txt_files = glob.glob(os.path.join(labels_dir, "*.txt"))
    if not txt_files:
        print(f"❌ Error: No .txt label files found in '{labels_dir}'.")
        return

    total_files = len(txt_files)
    total_boxes = 0
    box_widths = []
    box_heights = []
    oversized_boxes = [] # List of (filename, line_idx, w, h)
    empty_label_files = 0

    print(f"🔍 Starting scan of {total_files} label files in '{labels_dir}'...\n")

    for file_path in txt_files:
        filename = os.path.basename(file_path)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        if not lines or len(lines) == 0:
            empty_label_files += 1
            continue
            
        for idx, line in enumerate(lines):
            parts = line.strip().split()
            if len(parts) != 5:
                continue
                
            try:
                cls_id = int(parts[0])
                x, y, w, h = map(float, parts[1:])
                total_boxes += 1
                box_widths.append(w)
                box_heights.append(h)
                
                # Check if box covers more than 50% of the image area or is wider/taller than 80%
                if (w * h > 0.5) or (w > 0.8) or (h > 0.8):
                    oversized_boxes.append((filename, idx + 1, w, h))
            except ValueError:
                continue

    # Generate stats
    avg_boxes = total_boxes / total_files if total_files > 0 else 0
    avg_width = sum(box_widths) / len(box_widths) if box_widths else 0
    avg_height = sum(box_heights) / len(box_heights) if box_heights else 0

    print("=" * 60)
    print("📊 YOLO LABELS DIAGNOSTIC REPORT")
    print("=" * 60)
    print(f"• Total label files scanned:       {total_files}")
    print(f"• Empty label files (background):  {empty_label_files} ({empty_label_files/total_files*100:.1f}%)")
    print(f"• Total bounding boxes found:      {total_boxes}")
    print(f"• Avg boxes per image:             {avg_boxes:.2f}")
    if total_boxes > 0:
        print(f"• Avg bounding box width:          {avg_width:.3f} ({avg_width*100:.1f}% of image width)")
        print(f"• Avg bounding box height:         {avg_height:.3f} ({avg_height*100:.1f}% of image height)")
        print(f"• Oversized bounding boxes (>50% area or >80% size): {len(oversized_boxes)}")
    print("=" * 60)

    if oversized_boxes:
        print("\n🚨 WARNING: Oversized bounding boxes detected! This makes the model guess one big box.")
        print("Here are the first 10 flagged files:")
        for idx, (fname, line_num, w, h) in enumerate(oversized_boxes[:10]):
            print(f"  [{idx+1}] {fname} (line {line_num}): width={w:.2f}, height={h:.2f} (Area={w*h:.2f})")
        if len(oversized_boxes) > 10:
            print(f"  ... and {len(oversized_boxes) - 10} more files.")
        print("\n💡 SOLUTION: Re-annotate these images with tight boxes around individual particles.")
    else:
        print("\n✅ Success: No oversized bounding boxes found. Bounding boxes are tight and correctly sized.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_yolo_labels(sys.argv[1])
    else:
        # Ask for path
        path = input("Enter path to your dataset labels directory (e.g., 'datasets/train/labels'): ").strip()
        inspect_yolo_labels(path)
