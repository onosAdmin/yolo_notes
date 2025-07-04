
import os
import shutil

#given the folder /home/marco/gemini-cli/appliance.v2i.yolov8filtered_converted/train   search for all the labelling files in trhe folder   │
#│    labels and if the file has one only line and has a weight of more than 850 bytes move it to a tmp folder , move to that folder also the    │
#│    relative image      



def move_large_single_line_labels(train_dir):
    labels_dir = os.path.join(train_dir, 'labels')
    images_dir = os.path.join(train_dir, 'images')
    tmp_dir = os.path.join(train_dir, 'to_modify')

    os.makedirs(tmp_dir, exist_ok=True)

    for label_file in os.listdir(labels_dir):
        if label_file.endswith('.txt'):
            label_path = os.path.join(labels_dir, label_file)
            
            # Check file size
            if os.path.getsize(label_path) > 170:
                with open(label_path, 'r') as f:
                    lines = f.readlines()
                
                # Check if there is only one line
                if len(lines) == 1:
                    # Move label file
                    shutil.move(label_path, tmp_dir)

                    # Move corresponding image
                    image_file = label_file.replace('.txt', '.jpg')
                    image_path = os.path.join(images_dir, image_file)
                    if os.path.exists(image_path):
                        shutil.move(image_path, tmp_dir)
                    else:
                        print(f"Warning: Image for label {label_file} not found at {image_path}")


                
                # Check if there is only one line
                elif len(lines) == 2 and os.path.getsize(label_path) > 340:
                    # Move label file
                    shutil.move(label_path, tmp_dir)

                    # Move corresponding image
                    image_file = label_file.replace('.txt', '.jpg')
                    image_path = os.path.join(images_dir, image_file)
                    if os.path.exists(image_path):
                        shutil.move(image_path, tmp_dir)
                    else:
                        print(f"Warning: Image for label {label_file} not found at {image_path}")





if __name__ == '__main__':
    train_dir = '/home/marco/gemini-cli/appliance.v2i.yolov8filtered_converted/valid'
    move_large_single_line_labels(train_dir)
    print("Finished moving files.")
