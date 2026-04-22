import os
from helper import ImageLoader, GeometryAlgorithm

def get_input(prompt, default=None):
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def main():
    image_loader = ImageLoader()
    print("=== Geometry Transformation CLI ===")
    
    while True:
        image_path = get_input("\nEnter the path to your image (or 'exit' to quit)")
        
        if image_path.lower() == 'exit':
            print("Goodbye!")
            break
            
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found.")
            continue
            
        try:
            img_object = image_loader.load_image(image_path)
            print(f"Successfully loaded '{image_path}' ({img_object.width}x{img_object.height})")
        except Exception as e:
            print(f"Error loading image: {e}")
            continue

        algorithm_manager = GeometryAlgorithm(img_object)
        
        while True:
            print("\nSelect a transformation:")
            print("1. Horizontal Reflection (Flip Left-Right)")
            print("2. Vertical Reflection (Flip Top-Bottom)")
            print("3. Translation (Shift)")
            print("4. Scaling (Resize)")
            print("5. Rotation")
            print("7. Change Image Path")
            print("8. Exit")
            
            choice = get_input("Choice")
            
            if choice == '7':
                break
            if choice == '8':
                print("Goodbye!")
                return
                
            processed_img = None
            try:
                if choice == '1':
                    processed_img = algorithm_manager.horizontal_reflection()
                elif choice == '2':
                    processed_img = algorithm_manager.vertical_reflection()
                elif choice == '3':
                    offset_x = int(get_input("Horizontal offset (pixels)", "0"))
                    offset_y = int(get_input("Vertical offset (pixels)", "0"))
                    processed_img = algorithm_manager.translation(offset_x, offset_y)
                elif choice == '4':
                    scale_x = float(get_input("Horizontal scale factor", "1.0"))
                    scale_y = float(get_input("Vertical scale factor", "1.0"))
                    processed_img = algorithm_manager.scaling(scale_x, scale_y)
                elif choice == '5':
                    angle = float(get_input("Rotation angle (degrees)", "45"))
                    expand = get_input("Expand canvas? (y/n)", "y").lower() == 'y'
                    processed_img = algorithm_manager.rotation(angle, expand=expand)
                else:
                    print("Invalid choice. Please try again.")
                    continue
                
                if processed_img:
                    # Suggest a default save path
                    base, ext = os.path.splitext(image_path)
                    default_save = f"{base}_transformed{ext}"
                    save_path = get_input("Enter save path", default_save)
                    
                    # Ensure directory exists
                    save_dir = os.path.dirname(save_path)
                    if save_dir and not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                        
                    image_loader.save_image(processed_img, save_path)
                    print(f"Successfully saved transformed image to '{save_path}'")
                    
            except ValueError as e:
                print(f"Error executing transformation: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
