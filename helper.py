from PIL import Image
import copy

class ImageLoader:
    def __init__(self):
        pass
      
    def load_image(self, image_path):
        """
        Load an image from the specified file path.
        
        Args:
            image_path (str): The file path to the image file.
        
        Returns:
            img_object (PIL.Image): The PIL Image object.
        """
        
        img_object = Image.open(image_path)
        
        return img_object

    def save_image(self, img_object, image_save_path) -> None:
        """
        Save an image to the specified file path.
        
        Args:
            img_object (PIL.Image): The PIL Image object to save.
            image_save_path (str): The file path where the image will be saved.
        
        Returns:
            None
        """
        
        img_object.save(image_save_path)
        

class GeometryAlgorithm:
    def __init__(self, img_object):
        """
        Initialize the GeometryAlgorithm with an image object.
        
        Args:
            img_object (PIL.Image): The PIL Image object to convert.
        """
        self.img_object = img_object
        self.pixels = self.img_object.load()

    def _background_pixel(self):
        """
        Return a zero-valued background pixel compatible with the image mode.
        """
        bands = len(self.img_object.getbands())
        if bands == 1:
            return 0
        return tuple(0 for _ in range(bands))
    
    def horizontal_reflection(self):
        """
        Reflect the image horizontally (flip top to bottom).
        
        This method creates a mirror image of the original by flipping it
        across the horizontal axis (top becomes bottom and vice versa).
        
        Returns:
            img_object_copy (PIL.Image): A new horizontally reflected image object.
        """
        img_object_copy = copy.deepcopy(self.img_object)
        width, height = img_object_copy.size
        pixels = img_object_copy.load()
        
        for i in range(height):
            for j in range(width):
                pixels[j, i] = self.pixels[j, height - i - 1]
        
        return img_object_copy
    
    def vertical_reflection(self):
        """
        Reflect the image vertically (flip left to right).
        
        This method creates a mirror image of the original by flipping it
        across the vertical axis (left becomes right and vice versa).
        
        Returns:
            img_object_copy (PIL.Image): A new vertically reflected image object.
        """
        img_object_copy = copy.deepcopy(self.img_object)
        width, height = img_object_copy.size
        pixels = img_object_copy.load()
        
        for i in range(height):
            for j in range(width):
                pixels[j, i] = self.pixels[width - j - 1, i]

        return img_object_copy
                
    
    def translation(self, offset_x, offset_y):
        """
        Translate (shift) the image by a specified offset.
        
        This method moves the image by the given number of pixels in the
        x and y directions. Pixels that move outside the image bounds are
        discarded, and empty areas are filled based on the translation mode.
        
        Args:
            offset_x (int): The horizontal offset in pixels (positive = right, negative = left).
            offset_y (int): The vertical offset in pixels (positive = down, negative = up).
        
        Returns:
            img_object_copy (PIL.Image): A new translated image object.
        """
        img_object_copy = copy.deepcopy(self.img_object)
        width, height = img_object_copy.size
        pixels = img_object_copy.load()
        background = self._background_pixel()
        
        for i in range(height):
            for j in range(width):
                source_x = j - offset_x
                source_y = i - offset_y

                if 0 <= source_x < width and 0 <= source_y < height:
                    pixels[j, i] = self.pixels[source_x, source_y]
                else:
                    pixels[j, i] = background
        
        return img_object_copy
    
    def scaling(self, scale_x, scale_y):
        """
        Scale the image by specified factors in x and y directions.
        
        This method resizes the image by multiplying its dimensions by the
        given scale factors. Values greater than 1 enlarge the image, while
        values between 0 and 1 shrink it.
        
        Args:
            scale_x (float): The horizontal scale factor (> 0).
            scale_y (float): The vertical scale factor (> 0).
        
        Returns:
            img_object_copy (PIL.Image): A new scaled image object.
            
        Raises:
            ValueError: If scale factors are not positive values.
        """
        if scale_x <= 0 or scale_y <= 0:
            raise ValueError("scale_x and scale_y must be positive values")
        
        width, height = self.img_object.size
        
        scaled_width = int(width * scale_x)
        scaled_height = int(height * scale_y)
        
        scaled_img = Image.new(self.img_object.mode, (scaled_width, scaled_height))
        scaled_pixels = scaled_img.load()
        
        for i in range(scaled_height):
            for j in range(scaled_width):
                original_pixel_i = min(int(i / scale_y), height - 1)
                original_pixel_j = min(int(j / scale_x), width - 1)
                
                scaled_pixels[j, i] = self.pixels[original_pixel_j, original_pixel_i]

        # Keep the original canvas size by cropping the scaled result.
        cropped_img = scaled_img.crop((0, 0, width, height))

        return cropped_img
    
    def rotation(self, angle, expand=True):
        """
        Rotate the image by a specified angle (in degrees).
        
        This method rotates the image counter-clockwise around its center.
        Positive angles rotate counter-clockwise, negative angles rotate clockwise.
        
        Args:
            angle (float): The rotation angle in degrees.
            expand (bool): If True, the output image will be large enough to hold
                          the entire rotated image. If False, the output image will
                          have the same size as the input. Default: True.
        
        Returns:
            img_object_copy (PIL.Image): A new rotated image object.
        """
        import math
        
        img_object_copy = copy.deepcopy(self.img_object)
        width, height = img_object_copy.size
        pixels = img_object_copy.load()
        background = self._background_pixel()
        
        # Convert angle to radians
        angle_rad = math.radians(angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        # Calculate center
        center_x = (width - 1) / 2
        center_y = (height - 1) / 2
        
        if expand:
            # Calculate new dimensions
            corners = [
                (0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)
            ]
            rotated_corners = []
            for x, y in corners:
                # Translate to center
                tx = x - center_x
                ty = y - center_y
                # Rotate
                rx = tx * cos_angle - ty * sin_angle
                ry = tx * sin_angle + ty * cos_angle
                rotated_corners.append((rx, ry))
            
            # Find bounding box
            xs = [c[0] for c in rotated_corners]
            ys = [c[1] for c in rotated_corners]
            new_width = math.ceil(max(xs) - min(xs)) + 1
            new_height = math.ceil(max(ys) - min(ys)) + 1
            
            rotated_img = Image.new(img_object_copy.mode, (new_width, new_height))
            rotated_pixels = rotated_img.load()
            
            # New center
            new_center_x = new_width / 2
            new_center_y = new_height / 2
            
            for i in range(new_height):
                for j in range(new_width):
                    # Translate to center
                    tx = j - new_center_x
                    ty = i - new_center_y
                    
                    # Inverse rotation
                    orig_x = tx * cos_angle + ty * sin_angle + center_x
                    orig_y = -tx * sin_angle + ty * cos_angle + center_y
                    
                    # Round to nearest pixel
                    orig_x = int(round(orig_x))
                    orig_y = int(round(orig_y))
                    
                    # Check bounds
                    if 0 <= orig_x < width and 0 <= orig_y < height:
                        rotated_pixels[j, i] = pixels[orig_x, orig_y]
                    else:
                        rotated_pixels[j, i] = background
            
            return rotated_img
        else:
            # Keep original dimensions
            rotated_img = Image.new(img_object_copy.mode, (width, height))
            rotated_pixels = rotated_img.load()
            
            for i in range(height):
                for j in range(width):
                    # Translate to center
                    tx = j - center_x
                    ty = i - center_y
                    
                    # Inverse rotation
                    orig_x = tx * cos_angle + ty * sin_angle + center_x
                    orig_y = -tx * sin_angle + ty * cos_angle + center_y
                    
                    # Round to nearest pixel
                    orig_x = int(round(orig_x))
                    orig_y = int(round(orig_y))
                    
                    # Check bounds
                    if 0 <= orig_x < width and 0 <= orig_y < height:
                        rotated_pixels[j, i] = pixels[orig_x, orig_y]
                    else:
                        rotated_pixels[j, i] = background
            
            return rotated_img
