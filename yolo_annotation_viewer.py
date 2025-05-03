import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import argparse

class YOLOAnnotationViewer:
    def __init__(self, input_folder):
    
        self.images_dir = os.path.join(input_folder, "images")
        self.labels_dir = os.path.join(input_folder, "labels")

        
        # Get list of images and labels
        self.image_files = sorted([f for f in os.listdir(self.images_dir) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
        
        if not self.image_files:
            print(f"No images found in {images_dir}")
            exit(1)
            
        self.current_idx = 0
        self.zoom_factor = 1.0
        self.zoom_increment = 0.2
        self.pan_x = 0
        self.pan_y = 0
        self.last_x = 0
        self.last_y = 0
        self.dragging = False
        
        # Setup UI
        self.setup_ui()
        
        # Load first image
        self.load_current_image()
        
    def setup_ui(self):
        # Main window
        self.root = tk.Tk()
        self.root.title("YOLO Annotation Viewer")
        self.root.geometry("1200x800")
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for image display
        self.canvas_frame = ttk.Frame(main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Navigation buttons
        prev_btn = ttk.Button(control_frame, text="Previous (←)", command=self.prev_image)
        prev_btn.pack(side=tk.LEFT, padx=5)
        
        next_btn = ttk.Button(control_frame, text="Next (→)", command=self.next_image)
        next_btn.pack(side=tk.LEFT, padx=5)
        
        # Zoom buttons
        zoom_in_btn = ttk.Button(control_frame, text="Zoom In (+)", command=self.zoom_in)
        zoom_in_btn.pack(side=tk.LEFT, padx=5)
        
        zoom_out_btn = ttk.Button(control_frame, text="Zoom Out (-)", command=self.zoom_out)
        zoom_out_btn.pack(side=tk.LEFT, padx=5)
        
        reset_zoom_btn = ttk.Button(control_frame, text="Reset View (R)", command=self.reset_view)
        reset_zoom_btn.pack(side=tk.LEFT, padx=5)
        
        # Status info
        self.status_var = tk.StringVar()
        status_label = ttk.Label(control_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT, padx=5)
        
        # Key bindings
        self.root.bind("<Left>", lambda e: self.prev_image())
        self.root.bind("<Right>", lambda e: self.next_image())
        self.root.bind("<plus>", lambda e: self.zoom_in())
        self.root.bind("<minus>", lambda e: self.zoom_out())
        self.root.bind("r", lambda e: self.reset_view())
        
        # Mouse bindings for panning
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)
        self.canvas.bind("<ButtonRelease-1>", self.end_pan)
        
        # Mouse wheel for zooming
        self.canvas.bind("<MouseWheel>", self.mouse_wheel)  # Windows
        self.canvas.bind("<Button-4>", self.mouse_wheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self.mouse_wheel)    # Linux scroll down
    
    def start_pan(self, event):
        self.dragging = True
        self.last_x = event.x
        self.last_y = event.y
    
    def pan(self, event):
        if not self.dragging:
            return
            
        # Calculate the difference
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        
        # Update the pan values
        self.pan_x += dx
        self.pan_y += dy
        
        # Update last position
        self.last_x = event.x
        self.last_y = event.y
        
        # Redraw with new pan values
        self.display_current_image()
    
    def end_pan(self, event):
        self.dragging = False
    
    def mouse_wheel(self, event):
        # Zoom in/out with mouse wheel
        if event.num == 4 or event.delta > 0:
            self.zoom_in()
        elif event.num == 5 or event.delta < 0:
            self.zoom_out()
    















    def load_current_image(self):
        """Load the current image and its annotations"""
        if not self.image_files or self.current_idx >= len(self.image_files):
            return
            
        # Reset view for new image
        self.reset_view(update_display=False)
        
        # Get current image filename
        image_file = self.image_files[self.current_idx]
        base_name = os.path.splitext(image_file)[0]
        label_file = os.path.join(self.labels_dir, f"{base_name}.txt")
        
        # Load image
        image_path = os.path.join(self.images_dir, image_file)
        try:
            self.current_image = cv2.imread(image_path)
            if self.current_image is None:
                print(f"Warning: Could not load image {image_path}")
                self.next_image()
                return
                
            # Convert BGR to RGB
            self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            
            # Load annotations if available
            self.current_boxes = []
            self.current_classes = []
            
            if os.path.exists(label_file):
                height, width = self.current_image.shape[:2]
                
                with open(label_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            class_id = int(parts[0])
                            x_center = float(parts[1]) * width
                            y_center = float(parts[2]) * height
                            box_width = float(parts[3]) * width
                            box_height = float(parts[4]) * height
                            
                            # Convert to top-left, bottom-right format
                            x1 = int(x_center - box_width/2)
                            y1 = int(y_center - box_height/2)
                            x2 = int(x_center + box_width/2)
                            y2 = int(y_center + box_height/2)
                            
                            self.current_boxes.append((x1, y1, x2, y2))
                            self.current_classes.append(class_id)
            
            # Update the display
            self.display_current_image()
            
            # Update status
            self.status_var.set(f"Image {self.current_idx + 1}/{len(self.image_files)} - {image_file}")
            
        except Exception as e:
            print(f"Error loading image {image_path}: {str(e)}")
            # Skip to next image on error
            self.next_image()









    def load_current_image2(self):
        """Load the current image and its annotations"""
        if not self.image_files or self.current_idx >= len(self.image_files):
            return
            
        # Reset view for new image
        self.reset_view(update_display=False)
        
        # Get current image filename
        image_file = self.image_files[self.current_idx]
        base_name = os.path.splitext(image_file)[0]
        label_file = os.path.join(self.labels_dir, f"{base_name}.txt")
        
        # Load image
        image_path = os.path.join(self.images_dir, image_file)
        try:
            self.current_image = cv2.imread(image_path)
            if self.current_image is None:
                print(f"Warning: Could not load image {image_path}")
                self.next_image()
                return
                
            # Convert BGR to RGB
            self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            
            # Load annotations if available
            self.current_boxes = []
            self.current_classes = []
            
            if os.path.exists(label_file):
                height, width = self.current_image.shape[:2]
                
                with open(label_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            class_id = int(parts[0])
                            x_center = float(parts[1]) * width
                            y_center = float(parts[2]) * height
                            box_width = float(parts[3]) * width
                            box_height = float(parts[4]) * height
                            
                            # Convert to top-left, bottom-right format
                            x1 = int(x_center - box_width/2)
                            y1 = int(y_center - box_height/2)
                            x2 = int(x_center + box_width/2)
                            y2 = int(y_center + box_height/2)
                            
                            self.current_boxes.append((x1, y1, x2, y2))
                            self.current_classes.append(class_id)
            
            # Update the display
            self.display_current_image()
            
            # Update status
            self.status_var.set(f"Image {self.current_idx + 1}/{len(self.image_files)} - {image_file}")
            
        except Exception as e:
            print(f"Error loading image {image_path}: {str(e)}")
            self.next_image()
    





    def display_current_image(self):
        """Display current image with annotations"""
        if not hasattr(self, 'current_image') or self.current_image is None:
            return
            
        # Create a copy of the original image
        img_display = self.current_image.copy()
        
        # Draw bounding boxes
        for i, (x1, y1, x2, y2) in enumerate(self.current_boxes):
            class_id = self.current_classes[i]
            
            # Generate a unique color for each class (hue based on class_id)
            color_hue = (class_id * 30) % 180
            color = tuple(map(int, cv2.cvtColor(np.uint8([[[color_hue, 255, 255]]]), cv2.COLOR_HSV2RGB)[0][0]))
            
            # Draw rectangle
            cv2.rectangle(img_display, (x1, y1), (x2, y2), color, 2)
            
            # Add label
            label = f"Class {class_id}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(img_display, (x1, y1-th-5), (x1+tw, y1), color, -1)
            cv2.putText(img_display, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Apply zoom and pan
        h, w = img_display.shape[:2]
        
        # Calculate scaled dimensions
        new_w = int(w * self.zoom_factor)
        new_h = int(h * self.zoom_factor)
        
        # Resize image
        if self.zoom_factor != 1.0:
            img_display = cv2.resize(img_display, (new_w, new_h))
        
        # Get canvas dimensions with safety checks
        canvas_width = max(1, self.canvas.winfo_width())
        canvas_height = max(1, self.canvas.winfo_height())
        
        if canvas_width <= 1 or canvas_height <= 1:  # Canvas not yet properly initialized
            canvas_width = max(1, self.root.winfo_width() - 40)
            canvas_height = max(1, self.root.winfo_height() - 100)
        
        # Create a black canvas with minimum dimensions of 1x1
        canvas_img = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        
        # Calculate position to center the image with pan offset
        x_offset = max(0, (canvas_width - new_w) // 2 + self.pan_x)
        y_offset = max(0, (canvas_height - new_h) // 2 + self.pan_y)
        
        # Ensure offsets don't push the image completely out of view
        x_offset = min(max(0, x_offset), canvas_width - 10)
        y_offset = min(max(0, y_offset), canvas_height - 10)
            
        # Paste the image onto the canvas where it fits
        paste_width = min(new_w, canvas_width - x_offset)
        paste_height = min(new_h, canvas_height - y_offset)
        
        if paste_width > 0 and paste_height > 0:
            # Make sure we don't try to paste outside the image dimensions
            img_slice = img_display[:paste_height, :paste_width] if paste_height <= new_h and paste_width <= new_w else img_display
            
            # Get the region of the canvas where we'll paste
            canvas_region = canvas_img[y_offset:y_offset+img_slice.shape[0], 
                                    x_offset:x_offset+img_slice.shape[1]]
            
            # Make sure the shapes match before assigning
            if canvas_region.shape[:2] == img_slice.shape[:2]:
                canvas_img[y_offset:y_offset+img_slice.shape[0], 
                        x_offset:x_offset+img_slice.shape[1]] = img_slice
        
        # Convert to PhotoImage and update canvas
        pil_img = Image.fromarray(canvas_img)
        self.photo = ImageTk.PhotoImage(image=pil_img)
        
        # Clear canvas and add image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)















    def display_current_imageold(self):
        """Display current image with annotations"""
        if not hasattr(self, 'current_image') or self.current_image is None:
            return
            
        # Create a copy of the original image
        img_display = self.current_image.copy()
        
        # Draw bounding boxes
        for i, (x1, y1, x2, y2) in enumerate(self.current_boxes):
            class_id = self.current_classes[i]
            
            # Generate a unique color for each class (hue based on class_id)
            color_hue = (class_id * 30) % 180
            color = tuple(map(int, cv2.cvtColor(np.uint8([[[color_hue, 255, 255]]]), cv2.COLOR_HSV2RGB)[0][0]))
            
            # Draw rectangle
            cv2.rectangle(img_display, (x1, y1), (x2, y2), color, 2)
            
            # Add label
            label = f"Class {class_id}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(img_display, (x1, y1-th-5), (x1+tw, y1), color, -1)
            cv2.putText(img_display, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Apply zoom and pan
        h, w = img_display.shape[:2]
        
        # Calculate scaled dimensions
        new_w = int(w * self.zoom_factor)
        new_h = int(h * self.zoom_factor)
        
        # Resize image
        if self.zoom_factor != 1.0:
            img_display = cv2.resize(img_display, (new_w, new_h))
        
        # Create a black canvas the size of the display area
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:  # Canvas not yet properly initialized
            canvas_width = self.root.winfo_width() - 40
            canvas_height = self.root.winfo_height() - 100
        
        # Create a black canvas
        canvas_img = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        
        # Calculate position to center the image with pan offset
        x_offset = max(0, (canvas_width - new_w) // 2 + self.pan_x)
        y_offset = max(0, (canvas_height - new_h) // 2 + self.pan_y)
        
        # Ensure offsets don't push the image completely out of view
        if x_offset > canvas_width:
            x_offset = canvas_width - 10
        if y_offset > canvas_height:
            y_offset = canvas_height - 10
            
        # Paste the image onto the canvas where it fits
        paste_width = min(new_w, canvas_width - x_offset)
        paste_height = min(new_h, canvas_height - y_offset)
        
        if paste_width > 0 and paste_height > 0:
            # Make sure we don't try to paste outside the image dimensions
            img_slice = img_display[:paste_height, :paste_width] if paste_height <= new_h and paste_width <= new_w else img_display
            
            # Get the region of the canvas where we'll paste
            canvas_region = canvas_img[y_offset:y_offset+img_slice.shape[0], 
                                      x_offset:x_offset+img_slice.shape[1]]
            
            # Make sure the shapes match before assigning
            if canvas_region.shape[:2] == img_slice.shape[:2]:
                canvas_img[y_offset:y_offset+img_slice.shape[0], 
                          x_offset:x_offset+img_slice.shape[1]] = img_slice
        
        # Convert to PhotoImage and update canvas
        pil_img = Image.fromarray(canvas_img)
        self.photo = ImageTk.PhotoImage(image=pil_img)
        
        # Clear canvas and add image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
    
    def next_image(self):
        """Move to next image"""
        if not self.image_files:
            return
            
        self.current_idx = (self.current_idx + 1) % len(self.image_files)
        self.load_current_image()
    
    def prev_image(self):
        """Move to previous image"""
        if not self.image_files:
            return
            
        self.current_idx = (self.current_idx - 1) % len(self.image_files)
        self.load_current_image()
    
    def zoom_in(self):
        """Zoom in on image"""
        self.zoom_factor += self.zoom_increment
        self.display_current_image()
    
    def zoom_out(self):
        """Zoom out from image"""
        self.zoom_factor = max(0.2, self.zoom_factor - self.zoom_increment)
        self.display_current_image()
    
    def reset_view(self, update_display=True):
        """Reset zoom and pan to default"""
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        if update_display:
            self.display_current_image()
    
    def run(self):
        """Start the viewer"""
        # Configure canvas resize event
        self.canvas.bind("<Configure>", lambda e: self.display_current_image())
        
        # Start main loop
        self.root.mainloop()

def main():
    #python3 yolo_annotation_viewer.py --input /tmp/ram/out
    input_folder = "/tmp/ram/"
    parser = argparse.ArgumentParser(description='YOLO Annotation Viewer')
    parser.add_argument('--input', type=str, help='Directory containing YOLO folder (where the images and labels folders are)',default=input_folder)
    args = parser.parse_args()
    
    viewer = YOLOAnnotationViewer(args.input)
    viewer.run()

if __name__ == '__main__':
    main()
