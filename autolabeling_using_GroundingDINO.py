import os
from autodistill_grounding_dino import GroundingDINO
from autodistill.detection import CaptionOntology
import cv2
import supervision as sv # <-- Import supervision

DATASET_NAME = "lego_dataset"

base_model = GroundingDINO(ontology=CaptionOntology({"lego": "lego"}))

# IMAGE_NAME = "/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/made_myself/2x2_brick/2025-05-03-133029_1.jpg"
# image = os.path.join(DATASET_NAME, IMAGE_NAME)
# predictions = base_model.predict(image)
# image = cv2.imread(image)
# annotator = sv.BoxAnnotator()
# annotated_image = annotator.annotate(scene=image, detections=predictions)
# sv.plot_image(annotated_image)


base_model.label(input_folder="/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/made_myself/2x4_brick/", output_folder="/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/made_myself/autolabel_2x4_brick")
