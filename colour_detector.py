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

- Dislike having to double click to get image information 

- Need to hit esc to leave the program. Maybe put the prompt in the corner or in the ReadME file. 

- Variable names are awkward. Need to change those 

- Program doesn't show the hexcode!? 

- Not enough OOP, but can easily change that :) 
'''

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

# Reading the image with opencv
img = cv2.imread(img_path)

# declaring global variables (are used later on)
hovered = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        distance = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if (distance <= minimum):
            minimum = distance
            color_name = csv.loc[i, "color_name"]
    return color_name


# function to get x,y coordinates of mouse hover
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        global b, g, r, xpos, ypos, hovered
        hovered = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while (cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) >= 1):

    cv2.imshow("image", img)
    if hovered:

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        hovered = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
