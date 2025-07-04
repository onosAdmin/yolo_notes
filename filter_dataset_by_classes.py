
import os
import shutil

#in the folder data_root there is a yolo dataset, I need  to read all labels files in test ,train    │
#│    ,valid folders and then extract to a new folder only the labels files and images that contain certain classes (example 0,1,3,6)since i need to train my   │
#│    custom yolo model only on those classes    



#   1. Create a new directory for the filtered dataset.
#   2. Read all label files from the test, train, and valid directories.
#   3. For each label file, check if it contains any of the desired classes (0, 1, 3, 6).
#   4. If a label file contains the desired classes, copy both the label file and its corresponding image to the new dataset directory.
#   5. After copying, the script will also update the label files, so they only contain the desired classes.

#I want to add to the script a class conversion, I will give a list with the current class number in the labels file , i want the   │
#│    script to modify those number with the corrispective from another list i gave the script      




#  Please provide the two lists:    current_classes = [6,17,60]
#    new_classes = [0,1,2]
    
#   1. The list of current class numbers you want to convert (current_classes)
#   2. The list of new class numbers they should be converted to. (new_classes)


#  For example:
#   * Current classes: [0, 1, 3, 6]
#   * New classes: [0, 1, 2, 3]

#  This would mean that class 0 remains 0, class 1 remains 1, class 3 becomes 2, and class 6 becomes 3.



def filter_yolo_dataset(data_root, new_data_root, desired_classes, class_mapping, main_folders_list):
    if not os.path.exists(new_data_root):
        os.makedirs(new_data_root)

    for split in main_folders_list:
        new_split_dir = os.path.join(new_data_root, split)
        new_images_dir = os.path.join(new_split_dir, 'images')
        new_labels_dir = os.path.join(new_split_dir, 'labels')

        os.makedirs(new_images_dir, exist_ok=True)
        os.makedirs(new_labels_dir, exist_ok=True)

        image_dir = os.path.join(data_root, split, 'images')
        label_dir = os.path.join(data_root, split, 'labels')

        if not os.path.isdir(label_dir):
            print(f"Warning: Label directory not found, skipping: {label_dir}")
            continue

        for label_file in os.listdir(label_dir):
            if label_file.endswith('.txt'):
                label_path = os.path.join(label_dir, label_file)
                with open(label_path, 'r') as f:
                    lines = f.readlines()

                filtered_lines = []
                has_desired_class = False
                for line in lines:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    
                    class_id = int(parts[0])
                    if class_id in desired_classes:
                        has_desired_class = True
                        new_class_id = class_mapping.get(class_id)
                        
                        if new_class_id is not None:
                            new_line = f"{new_class_id} {' '.join(parts[1:])}\n"
                            filtered_lines.append(new_line)

                if has_desired_class:
                    # Copy image
                    image_file = label_file.replace('.txt', '.jpg') # Assumes image extension is .jpg
                    original_image_path = os.path.join(image_dir, image_file)
                    if os.path.exists(original_image_path):
                        shutil.copy(original_image_path, new_images_dir)
                    else:
                        print(f"Warning: Image for label {label_file} not found at {original_image_path}")
                        continue

                    # Write new label file with converted classes
                    new_label_path = os.path.join(new_labels_dir, label_file)
                    with open(new_label_path, 'w') as f:
                        f.writelines(filtered_lines)

if __name__ == '__main__':
    data_root = '/home/user/target_folder'
    new_data_root = data_root+'filtered_converted'
    current_classes = [6,17,60]
    new_classes = [0,1,2]
    
    #0 bed
    #1 chair
    #2 sofa

    
    
    
    class_mapping = dict(zip(current_classes, new_classes))
    
    desired_classes = list(class_mapping.keys())
    main_folders_list = ['train', 'valid', 'test']
    
    filter_yolo_dataset(data_root, new_data_root, desired_classes, class_mapping, main_folders_list)
    print(f"Filtered dataset with class conversion created at: {new_data_root}")
