from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2

# Load the trained YOLO model
model = YOLO(r'C:\Users\jacob\OneDrive\Documents\GitHub\FashionDivaApp\fashion_detection.pt')  # Replace with your model path

# Path to the image to test
image_path = r'C:\Users\jacob\OneDrive\Documents\GitHub\FashionDivaApp\static\uploads\Stylish-jeans-pants--on-transparent-background-PNG.png'
image = cv2.imread(image_path)

# Run prediction
results = model.predict(image_path, conf=0.5)

# Load the image with OpenCV (and convert to RGB for matplotlib)
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Create a matplotlib figure
fig, ax = plt.subplots(1, figsize=(12, 8))
ax.imshow(image)

# Get results
for result in results:
    boxes = result.boxes
    for box in boxes:
        # Get coordinates and class
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        conf = float(box.conf[0])

        # Draw rectangle and label
        width, height = x2 - x1, y2 - y1
        rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='lime', facecolor='none')
        ax.add_patch(rect)
        ax.text(x1, y1 - 5, f'{class_name} ({conf:.2f})', color='lime', fontsize=12, backgroundcolor='black')

plt.axis('off')
plt.tight_layout()
plt.show()