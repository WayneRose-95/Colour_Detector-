import cv2
import numpy as np
import pandas as pd
import argparse

'''
Positives: 

+ Use of flags allow user input 

+ Uses pandas in intricate way to calculate colour distances 

+ UI when using program is clear for test image. 


Negatives 

- Variable names are awkward. Need to change those 

- Program doesn't show the hexcode!? 

- Not enough OOP, but can easily change that :) 

'''



# Upon intialisation of the class, the csv_file and the image_path will be read. 

class ColourDetector:
    
    r = g = b = xpos = ypos = 0 

    def __init__(self, image_path, csv_file_name):
        # Reading the image with opencv
        self.image = cv2.imread(image_path)
        self.hovered = bool
        index = ["color", "color_name", "hex", "R", "G", "B"]
        # Reading csv file with pandas and giving names to each column
        self.csv = pd.read_csv(csv_file_name, names=index, header=None)
        # Creating argument parser to take image path from command line
        ap = argparse.ArgumentParser()
        ap.add_argument('-i', '--image', required=True, help="Image Path")
        args = vars(ap.parse_args())
        print(args)
        image_path = args['image']


    # function to calculate minimum distance from all colors and get the most matching color
    def getColorName(self, R, G, B):
        minimum = 10000
        for i in range(len(self.csv)):
            distance = abs(R - int(self.csv.loc[i, "R"])) + abs(G - int(self.csv.loc[i, "G"])) + abs(B - int(self.csv.loc[i, "B"]))
            if (distance <= minimum):
                minimum = distance
                color_name = self.csv.loc[i, "color_name"]
                print(color_name)
        return color_name


    # function to get x,y coordinates of mouse hover
    def draw_function(self, event, x, y, flags=None, param=None):
        if event == cv2.EVENT_MOUSEMOVE:
            global b, g, r, xpos, ypos, hovered
            hovered = True
            xpos = x
            ypos = y
            b, g, r = self.image[y, x]
            b = int(b)
            g = int(g)
            r = int(r)
            print(b, g, r, xpos, ypos)
    
    #     cv2.setMouseCallback('image', self.draw_function(cv2.EVENT_MOUSEMOVE, x, y))
    #     TypeError: on_mouse must be callable

    def open_window(self, x, y, flags=None, param=None):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_function)

        while (cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) >= 1):

            cv2.imshow("image", self.image)
            hovered = False 
            if hovered:
                # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
                cv2.rectangle(self.image, (20, 20), (750, 60), (b, g, r), -1)

                # Creating text string to display( Color name and RGB values )
                text = self.getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

                # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
                cv2.putText(self.image, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

                # For very light colours we will display text in black colour
                if (r + g + b >= 600):
                    cv2.putText(self.image, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

                hovered = True

            # Break the loop when user hits 'esc' key
            if cv2.waitKey(20) & 0xFF == 27:
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    picture = ColourDetector("colorpic.jpg", "colors.csv")
    picture.getColorName(100, 150, 200)
    picture.draw_function(cv2.EVENT_MOUSEMOVE, 10, 20)
    picture.open_window(50, 50)