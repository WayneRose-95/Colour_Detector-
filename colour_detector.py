import argparse  # Module for parsing command-line arguments
import cv2  # OpenCV library for image processing
import pandas as pd  # Library for data manipulation

class ColorDetector:
    """
    A class for detecting colors in an image using mouse clicks.
    """

    def __init__(self, image_path, csv_path='colors.csv'):
        """
        Initialize the ColorDetector instance.

        Args:
            image_path (str): Path to the input image.
            csv_path (str, optional): Path to the CSV file containing color data. Defaults to 'colors.csv'.
        """
        # Read the input image
        self.img = cv2.imread(image_path)
        # Flag to indicate if mouse was clicked  
        self.clicked = False 
        # Initialize color values and mouse position
        self.current_red = self.current_green = self.current_blue = self.xpos = self.ypos = 0 
        # Read color data from CSV 
        self.csv = pd.read_csv(csv_path, names=["color", "color_name", "hex", "R", "G", "B"], header=None)  
        self.setup_window()  # Set up the OpenCV window and mouse callback

    def setup_window(self):
        """
        Set up the OpenCV window and mouse callback.
        """
        # Create a window named 'image'
        cv2.namedWindow('image')
        # Set mouse callback to 'draw_function'  
        cv2.setMouseCallback('image', self.draw_function)  

    def get_color_name(self, r, g, b):
        """
        Get the closest color name based on RGB values.

        Args:
            r (int): Red component value.
            g (int): Green component value.
            b (int): Blue component value.

        Returns:
            str: Closest color name.
        """
         # Calculate color differences and names
        color_diffs = [(abs(r - int(row['R'])) + abs(g - int(row['G'])) + abs(b - int(row['B'])), row['color_name'])
                       for index, row in self.csv.iterrows()] 
        # Return the color name with the minimum difference
        return min(color_diffs, key=lambda x: x[0])[1]  

    def draw_function(self, event, x, y, flags, param):
        """
        Mouse event handler to track pixel coordinates and RGB values.

        Args:
            event: Mouse event type.
            x (int): X-coordinate of the mouse cursor.
            y (int): Y-coordinate of the mouse cursor.
            flags: Additional flags.
            param: Additional parameters.
        """
        if event == cv2.EVENT_MOUSEMOVE:
            # Mouse movement detected
            self.clicked = True  
            # Store mouse X-coordinate
            self.xpos = x  
            # Store mouse Y-coordinate
            self.ypos = y  
            # Get RGB values of the pixel
            self.current_blue, self.current_green, self.current_red = self.img[y, x]  
            self.current_blue = int(self.current_blue)
            self.current_green = int(self.current_green)
            self.current_red = int(self.current_red)

    def draw_rectangle(self):
        """
        Draw a rectangle on the image with the color of the clicked pixel.
        """
        # Draw a colored rectangle
        cv2.rectangle(self.img, (20, 20), (750, 60), (self.current_blue, self.current_green, self.current_red), -1)  

    def get_color_text(self):
        """
        Get the color name and RGB values text.

        Returns:
            str: Text containing color name and RGB values.
        """
        # Compose color name and RGB text
        text = f"{self.get_color_name(self.current_red, self.current_green, self.current_blue)} R={self.current_red} G={self.current_green} B={self.current_blue}"  
        return text

    def draw_text(self, text):
        """
        Draw the color name and RGB values text on the image.

        Args:
            text (str): Text to be drawn.
        """
        # Determine text color based on background brightness
        color = (255, 255, 255) if self.current_red + self.current_green + self.current_blue < 600 else (0, 0, 0)  
        # Draw the text on the image
        cv2.putText(self.img, text, (50, 50), 2, 0.8, color, 2, cv2.LINE_AA)  

    def update_image_display(self):
        """
        Update the displayed image.
        """
        # Display the updated image
        cv2.imshow("image", self.img)  

    def handle_key_press(self):
        """
        Handle key press events.
        """
        # Wait for a key press event (limited to lower 8 bits)
        key = cv2.waitKey(20) & 0xFF  
        # Check for 'esc' key (27 is ASCII code for 'esc')
        if key == 27: 
            # Call method to close OpenCV windows 
            self.close_windows()  

    def close_windows(self):
        """
        Close all OpenCV windows.
        """
        # Close all OpenCV windows
        cv2.destroyAllWindows()  

    def run(self):
        """
        Run the color detection application loop.
        """
        while True:
            # Update the displayed image
            self.update_image_display()  
            if self.clicked:
                # Draw the rectangle with clicked color
                self.draw_rectangle() 
                # Get color name and RGB values text 
                text = self.get_color_text()
                # Draw the text on the image  
                self.draw_text(text)  
                # Reset the clicked flag
                self.clicked = False  

            # Call method to handle key press events
            self.handle_key_press()  

            # Break the loop when user hits 'esc' key
            if cv2.waitKey(20) & 0xFF == 27:
                break

        self.close_windows()  # Call method to close OpenCV windows

if __name__ == "__main__":
    # Create ArgumentParser object for parsing command-line arguments
    ap = argparse.ArgumentParser() 
    # Add argument for input image path 
    ap.add_argument('-i', '--image', required=True, help="Image Path")  
    # Parse the command-line arguments and store in a dictionary
    args = vars(ap.parse_args()) 
    # Get the image path from the dictionary 
    img_path = args['image']
    # Set the default path for the color data CSV file  
    colors_csv_path = 'colors.csv'  

    # Create an instance of ColorDetector
    detector = ColorDetector(img_path, colors_csv_path)
    # Call the run method to start the color detection loop  
    detector.run()  







