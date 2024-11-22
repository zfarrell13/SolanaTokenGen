import cv2
import numpy as np

class ImageResizer:
    def __init__(self, image_path, output_path):
        """
        Initialize the resizer with the input and output paths.
        """
        self.image_path = image_path
        self.output_path = output_path

    def load_image(self):
        """
        Load the image from the provided path using OpenCV.
        """
        img = cv2.imread(self.image_path)
        if img is None:
            raise ValueError(f"Error: Unable to load image at {self.image_path}")
        return img

    def resize_to_canvas(self, img, canvas_size=512):
        """
        Resize the image to fit within a square canvas while maintaining aspect ratio.
        Adds white padding to make the final image exactly the canvas size.
        """
        # Get the original dimensions
        original_height, original_width = img.shape[:2]

        # Determine the scaling factor to fit within the canvas size
        scale = min(canvas_size / original_width, canvas_size / original_height)

        # Calculate the new dimensions
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        # Resize the image
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

        # Create a canvas_size x canvas_size white background
        final_img = np.full((canvas_size, canvas_size, 3), 255, dtype=np.uint8)

        # Center the resized image on the white background
        x_offset = (canvas_size - new_width) // 2
        y_offset = (canvas_size - new_height) // 2
        final_img[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_img

        return final_img

    def save_image(self, img):
        """
        Save the processed image to the output path.
        """
        cv2.imwrite(self.output_path, img)

    def process(self):
        """
        Main method to load, resize, and save the image.
        """
        img = self.load_image()
        resized_img = self.resize_to_canvas(img)
        self.save_image(resized_img)
        print(f"Image successfully resized and saved to {self.output_path}")


if __name__ == "__main__":
    image_path = "path_to_input_image.jpeg"
    output_path = "path_to_output_image.jpeg"
    
    resizer = ImageResizer(image_path, output_path)
    resizer.process()