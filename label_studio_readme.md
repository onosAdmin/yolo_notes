




Install label studio

```
pip install label-studio
```


Before running label-studio execute this command replace the path with your dataset path (for example where the images and labels folders are )
```

export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/

label-studio start
```




Now setup the input and output folders:

go to
http://localhost:8080/projects/2/settings/storage
add the source storage and the target storage
check the config "Treat every bucket object as a source file"   or the images will not showup!
press the sync storage button

Create a new project
on the tab  labelling setup select the Object detection with bounding boxes
Now on the Add label names  form  put each of your object classes followed by a new line (press enter to  go to the new line)
Press the button add , remove car and airplane classes if present
Press save














## IMPORT PREANNOTATED YOLO DATASETS
https://labelstud.io/blog/tutorial-importing-local-yolo-pre-annotated-images-to-label-studio/


Before running label-studio execute this command replace the path with your dataset path (for example where the images and labels folders are )

```

export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/

label-studio start
```



Check this:
http://localhost:8080/data/local-files/?d=made_myself/autolabel_2x4_brick/train/images/2025-05-03-131352_3.jpg

It should work



given the images are here:
 /media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/made_myself/autolabel_2x4_brick/train/images






add the classes.txt file to the train/ folder


the file should contain every class and there should be a new line separating each
for example:

```
brick_1x6
brick_2x2
brick_2x4
plate_1x2
plate_2x2
plate_2x4
```



Replace autolabel_2x4_brick/images/  with your path

Run the converter to convert the yolo annotations to json

```
label-studio-converter import yolo -i /media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/made_myself/autolabel_2x4_brick/train/ -o output.json --image-root-url "/data/local-files/?d=made_myself/autolabel_2x4_brick/train/images/"
```



If the import is not working correctly you could try to modify the json 

replace all occurence of "d=one/images/" in the file with your path 
in my case the absolute path is:
label-studio-converter import yolo -i /media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/made_myself/autolabel_2x4_brick/train/images
so I have to replace this:
"d=one/images/"   with: "d=made_myself/autolabel_2x4_brick/train/images/"  



  1. Create a new project in Label Studio
  2. Use Labeling Config from "/media/data/progetti/prog_miei/computer_vision/yolo_video/output.label_config.xml"
  3. Import "/media/data/progetti/prog_miei/computer_vision/yolo_video/output.json" to the project
  
  
  
Warning:
If you want to import a prelabeled dataset you should not import the local storage, you should just import the json and labelstudio will handle the rest  

