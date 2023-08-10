import argparse
import cv2
import pandas as pd

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
        self.img = cv2.imread(image_path)
        self.clicked = False
        self.current_red = self.current_green = self.current_blue = self.xpos = self.ypos = 0
        self.csv = pd.read_csv(csv_path, names=["color", "color_name", "hex", "R", "G", "B"], header=None)
        self.setup_window()

    def setup_window(self):
        """
        Set up the OpenCV window and mouse callback.
        """
        cv2.namedWindow('image')
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
        color_diffs = [(abs(r - int(row['R'])) + abs(g - int(row['G'])) + abs(b - int(row['B'])), row['color_name'])
                       for index, row in self.csv.iterrows()]
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
            self.clicked = True
            self.xpos = x
            self.ypos = y
            self.current_blue, self.current_green, self.current_red = self.img[y, x]
            self.current_blue = int(self.current_blue)
            self.current_green = int(self.current_green)
            self.current_red = int(self.current_red)

    def draw_rectangle(self):
        """
        Draw a rectangle on the image with the color of the clicked pixel.
        """
        cv2.rectangle(self.img, (20, 20), (750, 60), (self.current_blue, self.current_green, self.current_red), -1)

    def get_color_text(self):
        """
        Get the color name and RGB values text.

        Returns:
            str: Text containing color name and RGB values.
        """
        text = f"{self.get_color_name(self.current_red, self.current_green, self.current_blue)} R={self.current_red} G={self.current_green} B={self.current_blue}"
        return text

    def draw_text(self, text):
        """
        Draw the color name and RGB values text on the image.

        Args:
            text (str): Text to be drawn.
        """
        color = (255, 255, 255) if self.current_red + self.current_green + self.current_blue < 600 else (0, 0, 0)
        cv2.putText(self.img, text, (50, 50), 2, 0.8, color, 2, cv2.LINE_AA)

    def update_image_display(self):
        """
        Update the displayed image.
        """
        cv2.imshow("image", self.img)

    def handle_key_press(self):
        """
        Handle key press events.
        """
        key = cv2.waitKey(20) & 0xFF
        if key == 27:  # Check for 'esc' key
            self.close_windows()

    def close_windows(self):
        """
        Close all OpenCV windows.
        """
        cv2.destroyAllWindows()

    def run(self):
        """
        Run the color detection application loop.
        """
        while True:
            self.update_image_display()
            if self.clicked:
                self.draw_rectangle()
                text = self.get_color_text()
                self.draw_text(text)
                self.clicked = False

            self.handle_key_press()  # Moved inside the loop

            # Break the loop when user hits 'esc' key
            if cv2.waitKey(20) & 0xFF == 27:
                break

        self.close_windows()    

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help="Image Path")
    args = vars(ap.parse_args())
    img_path = args['image']
    colors_csv_path = 'colors.csv'

    detector = ColorDetector(img_path, colors_csv_path)
    detector.run()






