# Necklace Detection & Keypoint Refinement

## 📌 Overview
This project focuses on detecting and refining necklace keypoints using a hybrid approach that combines:

- **Deep Learning (YOLO Keypoints)**
- **Segmentation (MediaPipe)**
- **Classical Computer Vision (OpenCV Contours)**

The goal is to obtain **accurate and robust necklace anchor points** around the neck area.


## 📁 Project Structure

```
.
├── assets (Assets Directory)
├── datasets (Dataset Directory)
├── models (Models Directory)
├── src (Code Directory)
├── Dockerfile
├── README.md
└── result.json

```

---
## ⚙️ Pipeline
The project consists of three main stages:
- Dataset Annotation  
- Model Training (Necklace Keypoint Detection)  
- Necklace Detection & Keypoint Refinement

---

## Dataset Annotation
### 1. Download Dataset
The dataset used in this project can be downloaded from Kaggle:
https://www.kaggle.com/datasets/osmankagankurnaz/human-profile-photos-dataset

### 2. Open CVAT
For image annotation, this project uses **CVAT (Computer Vision Annotation Tool)**.
https://app.cvat.ai/


### 3. Login to CVAT
To start using CVAT, log in to your account.
- If you don’t have an account yet, you can sign up using:
  - Google  
  - GitHub  

![Login CVAT](assets/cvat/logincvat.gif)


### 4. Upload Images
To upload images:
1. Go to the **Tasks** tab  
2. Click the **“+”** button → **Create New Task**  
3. Fill in:
   - Project (optional)  
   - Task name  
4. Upload images by:
   - Clicking **“Click or drag files”**, or  
   - Dragging and dropping your images  
5. Select all desired images and click **Open**

Uploaded images will appear in the preview section below.
![Upload Images](assets/cvat/createnewtask.gif)


### 5. Assign Skeleton
To create a skeleton for keypoint annotation:
1. In the **Create New Task** page, go to the **Constructor** tab  
2. Click **Setup Skeleton**  
3. Upload a sample image  
4. Define keypoints by clicking on the image  
5. To connect keypoints:
   - Press `\` (backslash)  
   - Click the points you want to connect  
6. Enter a name for the skeleton  
7. Click:
   - **Submit & Open**, or  
   - **Submit & Continue**
You can view your created task in the **Tasks** tab.
![Setup Skeleton](assets/cvat/setupskeleton.gif)


### 6. Annotating Images
To annotate images:
1. Open your task  
2. Go to the **Jobs** section and select a job  
3. In the annotation interface:
   - Use the left toolbar (neuron-like icon)  
   - Select **Shape** (or skeleton tool if configured)  
4. Place and adjust keypoints according to the image  
5. Don’t forget to click **Save**
![Annotating](assets/cvat/annotating.gif)


### 7. Export Dataset
After completing all annotations:
1. Open the menu  
2. Click **Export job as a dataset**  
3. Choose the desired format  
4. Wait for the export process to complete  
5. Click **Download** (via the three-dot menu)

The dataset will be downloaded as a `.zip` file.
![Export Data](assets/cvat/exportdata.gif)

---

## Training Model: Necklace Keypoint Detection

### Data Preprocessing (YOLO Format)
### 1. Extract Dataset
Extract the downloaded dataset and move it to your desired project directory.


### 2. Create Folder Structure
Create the following folder structure:
```dataset/
├── train/
│ ├── images/
│ └── labels/
├── val/
│ ├── images/
│ └── labels/
```


### 3. Split Dataset (Train & Validation)
Split the dataset into training and validation sets by running:

```bash
python split.py
```
Make sure to adjust the directory paths inside the script to match your local setup (especially for `train/labels` and `val/labels`).


### 4. Move Images to Corresponding Folders
After splitting labels, move the images into their corresponding folders:

- `train/images` → for training data  
- `val/images` → for validation data  

You can use the provided script:
```bash
python moving_image.py
```
Ensure all directory paths inside the script are correctly configured.


### 5. Configure Dataset (data.yaml)
Open the `data.yaml` file and adjust it as follows:

```yaml
path: path_to_your_dataset
train: train/images
val: val/images

kpt_shape: [number_of_keypoints, 3]

names:
  0: necklace

Notes:
- path → root directory of your dataset
- kpt_shape → format is [num_keypoints, 3]
    - (x, y, visibility) for each keypoint
```


### 6. Train the Model
Run the training script:
```bash
python model.py
```
Before training, make sure to:
- Set the correct dataset YAML path
- Adjust hyperparameters (epochs, batch size, etc.)
- Define the output folder name

---

## Necklace Detection & Keypoint Refinement

### 1. Download MediaPipe Model
Download the required MediaPipe segmentation model in this link : 
https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite

Stored it in models folder


### 2. Load Input Image
Read the input image using OpenCV or another image processing library.


### 3. Crop Upper Body Region
Crop the image to focus on the face area to reduce noise and irrelevant regions using haar cascade.


### 4. Resize to 640×640
Resize or crop the image to **640×640**, match the input size of the model.


### 5. Person Segmentation
Perform segmentation using MediaPipe and extract:
- Face
- Skin
- Clothing

This helps isolate the human region from the background.


### 6. Neck Area Detection
Run YOLO keypoint model to detect keypoints:
- Right neck–shoulder
- Left neck–shoulder
- Neck center


### 7. Keypoint Refinement
Each keypoint is refined using a two-stage contour-based approach.

**1. Define ROI**
Create bounding boxes around:
- Left neck–shoulder point
- Right neck–shoulder point


**2. Contour Detection**
Within each ROI:
Initial Contour Snapping (adjusment_point)
- Find largest contour
- Snap keypoint to contour horizontally
- Snap keypoint to contour boundary:
    - Search contour points within horizontal band (same y ± tolerance)
    - Select:
      Rightmost point (right side)
      Leftmost point (left side)


**3. Contour-Based Refinement (refining_point)**
a. Contour Detection
   Extract largest contour from skin_roi

b. Polygon approximation (cv2.approxPolyDP)
   Simplifies contour into key vertices

c. Candidate Generation
   Compute distance from each vertex to original keypoint

d. Directional Filtering
   - Right side → keep points with x ≥ keypoint
   - Left side → keep points with x ≤ keypoint
   - Fallback if empty

e. Best Candidate Selection
   - Sort by distance
   - Select closest vertex

f. Final Adjustment (Snap to Contour)
   - Apply adjusment_point again
   - Align point precisely to contour edge


**4. Validation**
- Use refined point if close enough
- Else fallback


## 8. Neck Center Handling
- Directly from YOLO
- No refinement


## 9. Visualization (Optional)
- Green: YOLO keypoints
- Red: refined points
- Blue: original coordinates


## 10. Coordinate Mapping
1. Resized → Cropped  
2. Cropped → Original  


## 11. Export Output
```json
{
    "right_neck_shoulder_point": [x, y],
    "left_neck_shoulder_point": [x, y],
    "neck_point": [x, y],
    "coordinate_resize": {
        "rns_resize": [x, y],
        "lns_resize": [x, y],
        "neck": [x, y]
    }
}
```


## ▶️ How to Use

### 1. Install Dependencies

Install all required libraries:
```bash
pip install -r requirements.txt
```
### 2. Run as API (Web-Based)
If you want to use the system as a web service:
```bash
uvicorn api:app --reload
```

### 3. Run as Script (Program-Based)
If you want to run the pipeline directly:
```bash
python main.py "path image.jpg"
```

# 🎥 DEMO
**API:**
[demo](assets/demo.gif)


**SCRIPT:**
[demo](assets/demomain.gif)
