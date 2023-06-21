import cv2
import numpy as np

def count_bottles(image_file):
    # Read the image
    image_array = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (11, 11), 0)

    # Apply Canny edge detection
    canny = cv2.Canny(blur, 30, 150)

    # Dilate the edges
    dilated = cv2.dilate(canny, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables for counting bottles and storing bounding boxes
    count = 0
    boxes = []

    # Data augmentation parameters
    rotation_angle = 30
    zoom_range = 0.2

    # Process contours and count bottles
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Adjust the threshold according to your image
            count += 1
            (x, y, w, h) = cv2.boundingRect(contour)

            # Apply data augmentation
            augmented_image = image[y:y+h, x:x+w]
            augmented_image = cv2.rotate(augmented_image, cv2.ROTATE_90_CLOCKWISE)  # Example: rotate 90 degrees clockwise
            augmented_image = cv2.resize(augmented_image, None, fx=1+zoom_range, fy=1+zoom_range)  # Example: zoom in by 20%

            # Update bounding box coordinates
            x_aug, y_aug = x, y
            w_aug, h_aug = augmented_image.shape[:2]
            boxes.append((x_aug, y_aug, x_aug + w_aug, y_aug + h_aug))

    # Draw bounding boxes on the image
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Return the bottle count
    return count

if __name__ == '__main__':
    app.run()
