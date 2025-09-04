import os
import shutil
from PIL import Image
import imagehash
import face_recognition
from sklearn.cluster import DBSCAN
import numpy as np
from tqdm import tqdm
import json
import sys

# --- CONFIG ---
INPUT_DIR = "images"    # Folder with all input images
OUTPUT_DIR = "clusters"       # Folder where clusters will be saved

# --- STEP 1: Extract face embeddings ---
embeddings = []
image_paths = []
encoding_with_image_paths = []
pil_img = ''

def get_file(dir_name):
    if not os.path.isdir(dir_name) or not os.path.exists(dir_name):
        print(f"Directory with name ['{dir_name}'] does not exist in the root directory.")
        return False

    print("Extracting face embeddings...")

    for file in tqdm(os.listdir(dir_name)) :
        path = os.path.join(dir_name, file)
        if not os.path.isfile(path):
            get_file (dir_name)
            continue
        try:
            print(f"path: {path}")
            img = face_recognition.load_image_file(path)
            face_locations = face_recognition.face_locations(img) # Get all face boxes
            faces = face_recognition.face_encodings(img, face_locations)
            for i, encoding in enumerate(faces):
                embeddings.append(encoding)
                image_paths.append(path)
                encoding_with_image_paths.append({'path': path, 'img': img, 'face_location': face_locations[i]})

        except Exception as e:
            print(f"Skipping {path}: {e}")

    return True

success = get_file(INPUT_DIR)

if (success == False):
    sys.exit()

if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
    print(f"Deleted folder: {OUTPUT_DIR}")
else:
    print(f"Folder does not exist: {OUTPUT_DIR}")

embeddings = np.array(embeddings)
print(f"Total images with faces: {len(image_paths)}")

# --- STEP 2: Cluster faces using DBSCAN ---
print("Clustering faces...")
clustering = DBSCAN(eps=0.5, min_samples=1, metric='euclidean').fit(embeddings)
labels = clustering.labels_

# --- STEP 3: Create folders and move images ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

for cluster_id in set(labels):
    cluster_folder = os.path.join(OUTPUT_DIR, f"person_{cluster_id}")
    os.makedirs(cluster_folder, exist_ok=True)

    cluster_indices = [i for i, label in enumerate(labels) if label == cluster_id]

    # print(f"{json.dumps(labels.tolist())}")
    # print(f"{json.dumps(cluster_indices)}")

    # --- Remove duplicates inside cluster using perceptual hash ---
    # hashes = {}
    copied_images = []

    for idx, img_index in enumerate(cluster_indices):
        try:
            src_path = image_paths[img_index]
            # if (src_path in copied_images):
            #     continue

            print(f"cluster_id={cluster_id}, idx = {idx}, img_index = {img_index}, src_path {src_path}")

            img = Image.open(src_path)
            h = imagehash.average_hash(img)

            # if h not in hashes:
                # hashes[h] = True
            ext = os.path.splitext(src_path)[1]
            file_name = os.path.splitext(os.path.basename(src_path))[0]
            new_name = f"{file_name}_{idx}{ext}"
            shutil.copy(src_path, os.path.join(cluster_folder, new_name))

            copied_images.append(src_path)

            if (idx == 0):
                face_record = encoding_with_image_paths[img_index]
                img_array = face_record['img']
                top, right, bottom, left = face_record['face_location']
                new_face_image = img_array[top:bottom, left:right]
                pil_img = Image.fromarray(new_face_image)
                if pil_img:
                    new_name_img = f"face_face_{file_name}_{idx}{ext}"
                    pil_img.save(os.path.join(cluster_folder, new_name_img))

        except Exception as e:
            print(f"Skipping {src_path}: {e}")

print("Done! Check the clusters folder.")
