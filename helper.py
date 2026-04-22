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
    
    def horizontal_reflection(self):
        """
        Reflect the image horizontally (flip left to right).
        
        This method creates a mirror image of the original by flipping it
        across the vertical axis (left becomes right and vice versa).
        
        Returns:
            img_object_copy (PIL.Image): A new horizontally reflected image object.
        """
        img_object_copy = copy.deepcopy(self.img_object)
        width, height = img_object_copy.size
    
    def vertical_reflection(self):
        """
        Reflect the image vertically (flip top to bottom).
        
        This method creates a mirror image of the original by flipping it
        across the horizontal axis (top becomes bottom and vice versa).
        
        Returns:
            img_object_copy (PIL.Image): A new vertically reflected image object.
        """
        img_object_copy = copy.deepcopy(self.img_object)
        width, height = img_object_copy.size
    
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
        img_object_copy = copy.deepcopy(self.img_object)
        width, height = img_object_copy.size
    
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
        img_object_copy = copy.deepcopy(self.img_object)
        width, height = img_object_copy.size