import os
import cv2
import shutil
from pathlib import Path
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.1
class_id_in_the_folder = 1
default_input_image_folder = "/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/made_myself/2x4_brick"
default_model_path = "/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/runs/detect/train5/weights/best.pt"
default_output_folder = "/tmp/ram/yolo_dataset/my_brick_2x2/"

#how to use:
#this script will process all images in the input folder using the yolo model and create YOLO format annotations
#this script works only for dataset with a single class in the image!!! and with only a obkject per image

# python 
# you should modify the following variables:
# default_input_image_folder
# default_model_path
# default_output_folder
# CONFIDENCE_THRESHOLD
# class_id_in_the_folder

# class_id_in_the_folder is the class that you have in the folder , the yolo bounding boxes will be created with this class
# you should have only one class in the input folder
# the bounding boxes will be created using a pretrained yolo model (use process_images_with_yolov10 )
# at the full image size  (use process_images_already_cropped_on_bounding_box )
# useful if you have a dataset with already cropped images but  missing bounding boxes 



def process_images_with_yolo(input_folder, model_path,class_id_in_the_folder, output_base="yolo_dataset"):
    """
    Process images in the input folder with YOLO and create YOLO format annotations.
    
    Args:
        input_folder (str): Path to the folder containing input images
        model_path (str): Path to the YOLO model weights
        output_base (str): Base name for the output folder (default: "yolo_dataset")
    """
    # Create output directories
    output_folder = f"{output_base}_{Path(input_folder).name}"
    images_dir = os.path.join(output_folder, "images")
    labels_dir = os.path.join(output_folder, "labels")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    # Load YOLO model
    model = YOLO(model_path)
    
    # Get list of image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
    image_files = [f for f in os.listdir(input_folder) 
                  if os.path.splitext(f)[1].lower() in image_extensions]
    
    print(f"Found {len(image_files)} images to process in {input_folder}")
    
    for i, img_file in enumerate(image_files, 1):
        img_path = os.path.join(input_folder, img_file)
        img_name = os.path.splitext(img_file)[0]
        
        # Read image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Warning: Could not read image {img_file}, skipping...")
            continue
        
        # Perform detection
        results = model(img)
        
        # Prepare YOLO annotation file
        classes_found_in_this_image = 0
        last_folder_name = input_folder.split("/")[-1] + "_"
        txt_path = os.path.join(labels_dir, f"{last_folder_name+img_name}.txt")

        
        for result in results:
            if len(result.boxes) > 1: #skip this image if has more than one class detected, the dataset I should pass should have only one class per image
                print("error! more than a object detected,i need a dataset with only one object per image")
                break
            for box in result.boxes:
                # Get box coordinates in YOLO format (center x, center y, width, height)
                x_center, y_center, width, height = box.xywhn[0].tolist()
                class_id = int(box.cls)
                confidence = box.conf.item()
                if confidence >= CONFIDENCE_THRESHOLD and class_id == class_id_in_the_folder :
                    #if class bounding box width is lesser than 2/3 of image width  skip it
                    # if width < (img.shape[1] * 0.8):
                    #     print("Bounding box width is lesser than 2/3 of image width, skipping...")
                    #     break

                    classes_found_in_this_image = 1
                    # Write to annotation file (class_id, x_center, y_center, width, height)
                    with open(txt_path, 'w') as f:
                        f.write(f"{class_id_in_the_folder} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
                        #f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


        
        if classes_found_in_this_image:
            # Copy original image to images directory
            shutil.copy2(img_path, os.path.join(images_dir, last_folder_name+img_file))
        
        if i % 10 == 0 or i == len(image_files):
            print(f"Processed {i}/{len(image_files)} images")
    
    print(f"\nProcessing complete! Results saved to: {output_folder}")
    print(f"- Images: {images_dir}")
    print(f"- Labels: {labels_dir}")





def process_images_already_cropped_on_bounding_box(input_folder, model_path,class_id_in_the_folder, output_base="yolo_dataset"):

    #this function will make a copy of the image with the name of the image file but with the extension .txt
    #and will write the class id, x_center, y_center, width, height in the txt file
    #the function will also copy the image to the images directory
    #the function will also copy the image with the name of the image file but with the extension .txt to the labels directory
    #the bounding box will be the size of the full image

    # Create output directories
    output_folder = f"{output_base}_{Path(input_folder).name}"
    images_dir = os.path.join(output_folder, "images")
    labels_dir = os.path.join(output_folder, "labels")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    
    # Load YOLOv10 model
    model = YOLO(model_path)
    
    # Get list of image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
    image_files = [f for f in os.listdir(input_folder) 
                  if os.path.splitext(f)[1].lower() in image_extensions]
    
    print(f"Found {len(image_files)} images to process in {input_folder}")
    
    for i, img_file in enumerate(image_files, 1):
        img_path = os.path.join(input_folder, img_file)
        img_name = os.path.splitext(img_file)[0]
        
        # Read image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Warning: Could not read image {img_file}, skipping...")
            continue
        
        
        # Prepare YOLO annotation file
        classes_found_in_this_image = 0
        last_folder_name = input_folder.split("/")[-1] + "_"
        txt_path = os.path.join(labels_dir, f"{last_folder_name+img_name}.txt")

        classes_found_in_this_image = 1
        # Write to annotation file (class_id, x_center, y_center, width, height)
        with open(txt_path, 'w') as f:
            f.write(f"{class_id_in_the_folder} 0.5 0.5 1.0 1.0\n")
            #f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


        
        if classes_found_in_this_image:
            # Copy original image to images directory
            shutil.copy2(img_path, os.path.join(images_dir, last_folder_name+img_file))
        
        if i % 10 == 0 or i == len(image_files):
            print(f"Processed {i}/{len(image_files)} images")
    
    print(f"\nProcessing complete! Results saved to: {output_folder}")
    print(f"- Images: {images_dir}")
    print(f"- Labels: {labels_dir}")




if __name__ == "__main__":
    import argparse

    # parser = argparse.ArgumentParser(description="Process images with YOLO and create YOLO format annotations.")
    # parser.add_argument("input_folder", type=str, help="Path to the folder containing input images", default=default_input_image_folder)
    # parser.add_argument("model_path", type=str, help="Path to the YOLO model weights file",default=default_model_path)
    # parser.add_argument("--output", type=str, help="Base name for the output folder (default: yolo_dataset)" , default="yolo_dataset")
    
    # args = parser.parse_args()
    
    process_images_with_yolo(default_input_image_folder, default_model_path,class_id_in_the_folder,default_output_folder)
    #process_images_already_cropped_on_bounding_box(default_input_image_folder, default_model_path,class_id_in_the_folder,default_output_folder)
